"""Extract tagged code snippets from C/C++ source and display them in Jupyter.

This module scans C/C++ source files for landmark comments of the form::

    // #tag-1
    // #tag-1 original_file.c
    // #tag-1 original_file.c 42
    // #tag-1 original_file.c 3-24

Everything between one landmark and the next (or the end of the file) is
captured as a :class:`Snippet`, keyed by its tag. Snippets can then be
rendered as syntax-highlighted, selectable HTML in a single call, instead of
relying on Jupyter's native Markdown-cell code fences (which, at least in
VS Code, can suffer from missing syntax highlighting and a text-selection /
cell-drag conflict).

The two optional words after the tag are positional: a filename may be given
on its own to record where the snippet originated, and a line number or line
range (e.g. ``3-24``) is only recognized when it follows a filename. This
origin information is never inferred from the landmark's actual position in
the file -- if it isn't given explicitly, :attr:`Snippet.line_start` and
:attr:`Snippet.line_end` are both ``None`` and nothing is displayed for it,
regardless of the ``show_linenumber`` setting.

Every snippet is rendered in both a dark and a light variant, with only the
one matching the current theme visible (see :data:`DARK_THEME`,
:data:`LIGHT_THEME`, and :data:`_THEME_TOGGLE_CSS`), so it switches
automatically with no need to re-run the cell. This works in JupyterLab
and classic Jupyter Notebook, and also when a notebook is published as a
static site page with Material for MkDocs (e.g. via mkdocs-jupyter) -- the
snippet reacts to that theme's light/dark toggle in the browser too.

Note on reopening a saved notebook: Jupyter only renders a cell's *stored*
HTML output as-is (``<style>`` included) if the notebook is "trusted" for
the current user/session -- normally true right after you run the cell
yourself, but not guaranteed when reopening a previously-saved ``.ipynb``
later or as a different user. If it loads untrusted, the front end may
sanitize stored outputs and strip the theme-switching ``<style>`` block
entirely. Each variant therefore also carries its own fallback ``display``
value as an inline style (see :attr:`_Theme.default_display`), so an
untrusted reload still shows a single, correct-looking snippet (the dark
variant, by default) instead of both variants stacked on top of each other;
re-running the cell restores full automatic switching.

Requires:
    pygments, and ``copy_button.py`` (renders the header's copy-to-clipboard
    button) importable alongside this module -- e.g. in the same directory.

    Install pygments with ``pip install pygments`` (add
    ``--break-system-packages`` if running in an externally managed
    environment such as a sandbox).

Typical usage example:

    from csnippets import CSnippets

    csnippets = CSnippets(show_filename=True, show_linenumber=True,
                           show_copy_button=True, copy_button_mode="icon")
    csnippets.load("path/to/c/project")  # a single file or a directory

    csnippets.display("tag-1")
    csnippets.display("tag-1", show_gutter_linenumbers=True)  # IDE-style gutter
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple

from IPython.display import HTML, display
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import CLexer, CppLexer

try:
    # Works when csnippets is imported as part of a package, e.g.
    # `from helpers.csnippets import CSnippets`, with copy_button.py sitting
    # next to it in that same package/folder.
    from .copy_button import render_copy_button_html, DEFAULT_BUTTON_COLORS
except ImportError:
    # Falls back to a plain top-level import, for cases where csnippets.py
    # is run/imported standalone (its own directory directly on sys.path)
    # rather than as a submodule of a package.
    from copy_button import render_copy_button_html, DEFAULT_BUTTON_COLORS

#: Matches a whole line containing only a landmark comment, e.g.::
#:
#:     // #tag-1
#:     // #tag-1 neuron_model_impl.c
#:     // #tag-1 neuron_model_impl.c 42
#:     // #tag-1 neuron_model_impl.c 3-24
#:
#: Group 1 is the tag (including the leading ``#``), with no spaces allowed.
#: Group 2 is an optional second word: the origin filename to record. Groups
#: 3 and 4 are an optional third word: either a single line number (group 3
#: only) or a line range such as ``3-24`` (group 3 is the start, group 4 is
#: the end). Groups 3/4 are only recognized when group 2 (the filename) is
#: also present.
TAG_PATTERN = re.compile(r"^\s*//\s*(#\S+)(?:\s+(\S+)(?:\s+(\d+)(?:-(\d+))?)?)?\s*$")

#: File extensions scanned by default when :meth:`CSnippets.load` is given a
#: directory.
DEFAULT_EXTENSIONS = {".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".hh"}

#: Extensions rendered with a C++ lexer; everything else falls back to C.
CPP_EXTENSIONS = {".cpp", ".hpp", ".cc", ".cxx", ".hh"}

#: Shared font metrics applied to the header, gutter, and code, so all three
#: read at a consistent size and (for the gutter/code) line up row for row.
FONT_STYLE = (
    "font-family:SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace; font-size:13px; line-height:1.4;"
)

#: Zeroes out the browser's default ``<pre>`` margin/padding. Left alone,
#: that default margin pushes the code down and creates a visible gap and
#: misalignment against the gutter.
PRE_RESET = "margin:0; padding:0;"

#: Muted divider color used both for the horizontal rule under the header
#: and the vertical rule between the gutter and the code.
DIVIDER_COLOR = "rgba(128, 128, 128, 0.35)"


@dataclass(frozen=True)
class _Theme:
    """One visual theme for a rendered snippet: the colors that go with it.

    The Pygments *style* is deliberately not part of this -- it stays a
    per-instance setting (:attr:`CSnippets.style` / :attr:`CSnippets.light_style`),
    so it remains as configurable as it always was; only the fixed colors
    live here.

    Attributes:
        css_class: CSS class used to show/hide this variant; see
            :data:`_THEME_TOGGLE_CSS`.
        background: Background color forced onto the cell and the code.
        header_color: Text color used for the filename/line-number header.
        button_colors: Color set passed through to
            :func:`copy_button.render_copy_button_html` for the copy button
            rendered in this variant's header (background/text/border for
            its rest, hover, and "Copied!" states).
        border_color: Border color for this variant's outer box.
        default_display: CSS ``display`` value baked into this variant's
            wrapper element as an inline style -- the fallback shown
            whenever :data:`_THEME_TOGGLE_CSS` doesn't take effect at all
            (see the module docstring's note on untrusted notebook
            reloads). ``"block"`` for the variant shown by default,
            ``"none"`` for the other one.
    """

    css_class: str
    background: str
    header_color: str
    button_colors: dict[str, str]
    border_color: str
    default_display: str


#: The dark variant: close to VS Code's default dark editor background. Its
#: button colors match copy_button.py's own original defaults exactly, so
#: the dark variant's appearance is unchanged from before theming existed.
#: It's also the fallback shown whenever the toggle stylesheet can't apply
#: (see :attr:`_Theme.default_display`), matching prior default behavior.
DARK_THEME = _Theme(
    css_class="csnippet-theme-dark",
    background="#2A2E3A",
    header_color="#aaaaaa",
    button_colors=dict(DEFAULT_BUTTON_COLORS),
    border_color="#444",
    default_display="block",
)

#: The light variant: a typical light Jupyter/editor layout -- plain, pale
#: grey. Pair this with a light-appropriate Pygments style (see
#: :attr:`CSnippets.light_style`, default ``"vs"``) rather than just reusing
#: the dark palette on a light background. Its button colors are likewise a
#: light-appropriate set, distinct from the dark defaults.
LIGHT_THEME = _Theme(
    css_class="csnippet-theme-light",
    background="#f5f5f5",
    header_color="#555555",
    border_color="#AAAAAA",
    button_colors={
        "background_color": "#f3f3f3",
        "text_color": "#333333",
        "border_color": "#d0d0d0",
        "hover_background_color": "#e8e8e8",
        "hover_border_color": "#b0b0b0",
        "success_border_color": "#0969da",
        "success_text_color": "#0969da",
    },
    default_display="none",
)

#: CSS that shows only the theme variant matching the page's current theme.
#: Both variants are always rendered (Pygments bakes its token colors into
#: the HTML at render time in Python, so which one to show has to be
#: decided in the browser via CSS, not by re-running Pygments) -- this just
#: picks which one is visible.
#:
#: Every rule below uses ``!important``, specifically so it can override
#: each variant's own inline ``display`` fallback (see
#: :attr:`_Theme.default_display`), which otherwise always wins since an
#: inline style outranks a plain class/attribute selector. That fallback
#: matters because this stylesheet doesn't always survive: Jupyter only
#: renders a cell's *stored* HTML output as-is (``<style>`` included) when
#: the notebook is trusted for the current user/session -- see the module
#: docstring's note on untrusted reloads, where this whole ``<style>``
#: block can get stripped out from under a previously-executed output.
#:
#: Signals are checked in increasing order of precedence (later rules in
#: the stylesheet win ties, since all selectors below resolve to the same
#: specificity within their group):
#:
#: 1. Fallback: the OS/browser's ``prefers-color-scheme``, for renderers
#:    where none of the more specific signals below apply.
#: 2. JupyterLab sets ``data-jp-theme-light="true"/"false"`` on ``<body>``
#:    to reflect the notebook's actual theme choice (browser-hosted Jupyter
#:    Notebook/JupyterLab).
#: 3. Material for MkDocs (e.g. notebooks rendered as static site pages via
#:    mkdocs-jupyter) sets ``data-md-color-scheme`` on ``<body>``, set to
#:    ``"slate"`` for its dark scheme and ``"default"`` for its light
#:    scheme in a stock install -- these are the built-in scheme names; a
#:    site using custom-named color schemes would need matching selectors
#:    added here.
#:
#: If none of these signals are present (or this stylesheet didn't survive
#: at all), each variant's own :attr:`_Theme.default_display` decides what
#: shows -- the dark variant, matching prior behavior.
_THEME_TOGGLE_CSS = f"""<style>
@media (prefers-color-scheme: light) {{
  .{DARK_THEME.css_class} {{ display: none !important; }}
  .{LIGHT_THEME.css_class} {{ display: block !important; }}
}}
body[data-jp-theme-light="true"] .{DARK_THEME.css_class} {{ display: none !important; }}
body[data-jp-theme-light="true"] .{LIGHT_THEME.css_class} {{ display: block !important; }}
body[data-jp-theme-light="false"] .{DARK_THEME.css_class} {{ display: block !important; }}
body[data-jp-theme-light="false"] .{LIGHT_THEME.css_class} {{ display: none !important; }}
body[data-md-color-scheme="default"] .{DARK_THEME.css_class} {{ display: none !important; }}
body[data-md-color-scheme="default"] .{LIGHT_THEME.css_class} {{ display: block !important; }}
body[data-md-color-scheme="slate"] .{DARK_THEME.css_class} {{ display: block !important; }}
body[data-md-color-scheme="slate"] .{LIGHT_THEME.css_class} {{ display: none !important; }}
</style>"""


class Landmark(NamedTuple):
    """A single parsed landmark comment, before its snippet body is sliced out.

    Attributes:
        line_index: Zero-based index of the landmark line within the file.
        tag: The tag with its leading ``#`` stripped.
        filename: The explicit origin filename, or ``None`` if not given.
        line_start: The explicit origin line number (or the start of an
            origin line range), or ``None`` if not given.
        line_end: The end of the origin line range, or ``None`` if only a
            single origin line number was given (or none at all).
    """

    line_index: int
    tag: str
    filename: str | None
    line_start: int | None
    line_end: int | None


@dataclass
class Snippet:
    """A single tagged code snippet extracted from a source file.

    Attributes:
        tag: The tag identifying this snippet (without the leading ``#``).
        code: The snippet's source code, with leading/trailing blank lines
            stripped.
        filename: The name to display as this snippet's origin. This is the
            explicit filename given on the landmark line, if any, otherwise
            the actual name of the file it was parsed from.
        source_path: The real path on disk that this snippet was read from.
        line_start: The explicit origin line number (or the start of an
            origin line range) given on the landmark line, or ``None`` if
            none was given. This is independent of where the landmark
            actually sits in ``source_path``.
        line_end: The end of the origin line range given on the landmark
            line, or ``None`` if only a single origin line number was given
            (or none at all).
    """

    tag: str
    code: str
    filename: str
    source_path: str
    line_start: int | None
    line_end: int | None

    def __repr__(self) -> str:
        """Returns a short, human-readable summary of this snippet.

        Returns:
            A string of the form ``Snippet(tag=..., filename=..., lines=...)``.
        """
        n_lines = self.code.count("\n") + 1 if self.code else 0
        return f"Snippet(tag={self.tag!r}, filename={self.filename!r}, lines={n_lines})"


class CSnippets:
    """Parses C/C++ files for tagged landmarks and displays them as HTML.

    Attributes:
        snippets: Mapping of tag to the :class:`Snippet` last loaded for it.
        style: Name of the Pygments style used for the dark theme variant.
        light_style: Name of the Pygments style used for the light theme
            variant.
        show_filename: Default setting for whether :meth:`display` shows the
            small filename header above a snippet.
        show_linenumber: Default setting for whether :meth:`display` shows a
            snippet's origin line number/range in that header (only applies
            when the snippet actually has one).
        show_gutter_linenumbers: Default setting for whether :meth:`display`
            adds an IDE-style line-number gutter down the left side of the
            highlighted code itself.
        show_copy_button: Default setting for whether :meth:`display` shows
            a copy-to-clipboard button on the right side of the header,
            copying the snippet's code.
        copy_button_mode: Default appearance passed to
            :func:`copy_button.render_copy_button_html`: ``"icon"``,
            ``"text"``, or ``"icon+text"``.
    """

    def __init__(
        self,
        style: str = "monokai",
        light_style: str = "vs",
        show_filename: bool = True,
        show_linenumber: bool = True,
        show_gutter_linenumbers: bool = False,
        show_copy_button: bool = True,
        copy_button_mode: str = "icon",
    ):
        """Initializes an empty snippet collection.

        Args:
            style: Name of the Pygments style used when the notebook is in
                its dark theme (e.g. ``"monokai"``, ``"dracula"``,
                ``"native"``).
            light_style: Name of the Pygments style used when the notebook
                is in its light theme (e.g. ``"vs"``, ``"default"``,
                ``"friendly"``) -- pick one designed for a light background,
                since the dark-theme palette generally reads poorly on one.
            show_filename: Default value for ``show_filename`` in
                :meth:`display`, when not overridden per call.
            show_linenumber: Default value for ``show_linenumber`` in
                :meth:`display`, when not overridden per call.
            show_gutter_linenumbers: Default value for
                ``show_gutter_linenumbers`` in :meth:`display`, when not
                overridden per call. Off by default.
            show_copy_button: Default value for ``show_copy_button`` in
                :meth:`display`, when not overridden per call.
            copy_button_mode: Default value for ``copy_button_mode`` in
                :meth:`display`, when not overridden per call. One of
                ``"icon"``, ``"text"``, or ``"icon+text"``.
        """
        self.snippets: dict[str, Snippet] = {}
        self.style = style
        self.light_style = light_style
        self.show_filename = show_filename
        self.show_linenumber = show_linenumber
        self.show_gutter_linenumbers = show_gutter_linenumbers
        self.show_copy_button = show_copy_button
        self.copy_button_mode = copy_button_mode

    # ------------------------------------------------------------------ #
    # Loading
    # ------------------------------------------------------------------ #

    def load(self, path: str | Path, extensions: set[str] | None = None, recursive: bool = True) -> "CSnippets":
        """Loads snippets from a single file or every matching file in a directory.

        Args:
            path: Path to a single source file, or a directory to scan.
            extensions: File extensions to include when ``path`` is a
                directory (case-insensitive, each including the leading
                dot). Defaults to :data:`DEFAULT_EXTENSIONS`.
            recursive: Whether to scan subdirectories when ``path`` is a
                directory.

        Returns:
            This :class:`CSnippets` instance, so calls can be chained, e.g.
            ``CSnippets().load("src")``.

        Raises:
            FileNotFoundError: If ``path`` does not exist.
        """
        path = Path(path)
        extensions = {e.lower() for e in (extensions or DEFAULT_EXTENSIONS)}

        if path.is_file():
            self._parse_file(path)
        elif path.is_dir():
            pattern = "**/*" if recursive else "*"
            for file_path in sorted(path.glob(pattern)):
                if file_path.is_file() and file_path.suffix.lower() in extensions:
                    self._parse_file(file_path)
        else:
            raise FileNotFoundError(f"No such file or directory: {path}")

        return self

    def _parse_file(self, file_path: Path) -> None:
        """Parses a single file and stores every snippet it contains.

        Existing entries for the same tag are overwritten, with a warning
        printed to note the collision.

        Args:
            file_path: Path of the file to read and parse.
        """
        text = file_path.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
        landmarks = self._find_landmarks(lines)

        for i, landmark in enumerate(landmarks):
            start = landmark.line_index + 1  # snippet starts right after the landmark line
            end = landmarks[i + 1].line_index if i + 1 < len(landmarks) else len(lines)
            code = self._strip_blank_edges(lines[start:end])
            filename = landmark.filename or file_path.name

            if landmark.tag in self.snippets:
                print(
                    f"Warning: duplicate tag '{landmark.tag}' in {file_path} "
                    f"(line {landmark.line_index + 1}); overwriting previous entry "
                    f"from {self.snippets[landmark.tag].source_path}"
                )

            self.snippets[landmark.tag] = Snippet(
                tag=landmark.tag,
                code=code,
                filename=filename,
                source_path=str(file_path),
                line_start=landmark.line_start,
                line_end=landmark.line_end,
            )

    @staticmethod
    def _find_landmarks(lines: list[str]) -> list[Landmark]:
        """Finds every landmark comment in a file's lines.

        Args:
            lines: The file's content, split into individual lines.

        Returns:
            A list of :class:`Landmark` instances, one per matching line, in
            the order they appear in ``lines``.
        """
        landmarks = []
        for idx, line in enumerate(lines):
            match = TAG_PATTERN.match(line)
            if match:
                tag = match.group(1).lstrip("#")
                filename = match.group(2)
                start_str, end_str = match.group(3), match.group(4)
                line_start = int(start_str) if start_str is not None else None
                line_end = int(end_str) if end_str is not None else None
                landmarks.append(Landmark(idx, tag, filename, line_start, line_end))
        return landmarks

    @staticmethod
    def _strip_blank_edges(lines: list[str]) -> str:
        """Removes leading and trailing blank lines and joins the rest.

        Args:
            lines: The candidate snippet's lines, taken verbatim from the
                source file.

        Returns:
            The lines rejoined with newlines, with any leading and trailing
            blank lines removed. Blank lines in the middle of the snippet
            are left untouched.
        """
        start, end = 0, len(lines)
        while start < end and lines[start].strip() == "":
            start += 1
        while end > start and lines[end - 1].strip() == "":
            end -= 1
        return "\n".join(lines[start:end])

    # ------------------------------------------------------------------ #
    # Lookup / display
    # ------------------------------------------------------------------ #

    def get(self, tag: str) -> Snippet:
        """Looks up the snippet stored for a tag.

        Args:
            tag: The tag to look up (without the leading ``#``).

        Returns:
            The :class:`Snippet` stored for ``tag``.

        Raises:
            KeyError: If no snippet has been loaded for ``tag``.
        """
        try:
            return self.snippets[tag]
        except KeyError:
            raise KeyError(f"No snippet for tag '{tag}'. Known tags: {self.tags()}") from None

    def tags(self) -> list[str]:
        """Lists every tag currently loaded.

        Returns:
            A sorted list of all tags with a loaded snippet.
        """
        return sorted(self.snippets.keys())

    @staticmethod
    def _lexer_for(filename: str):
        """Picks a Pygments lexer based on a filename's extension.

        Args:
            filename: The filename to inspect (only its extension is used).

        Returns:
            A :class:`~pygments.lexers.CppLexer` instance if the extension
            is one of :data:`CPP_EXTENSIONS`, otherwise a
            :class:`~pygments.lexers.CLexer` instance.
        """
        ext = Path(filename).suffix.lower()
        return CppLexer() if ext in CPP_EXTENSIONS else CLexer()

    def _render_header(
        self,
        snippet: Snippet,
        show_filename: bool,
        show_linenumber: bool,
        show_copy_button: bool,
        copy_button_mode: str,
        header_color: str,
        button_colors: dict[str, str],
    ) -> str:
        """Builds the header row and its divider rule.

        The filename/line info (if shown) sits on the left; the
        copy-to-clipboard button (if shown) sits on the right, via a
        ``justify-content: space-between`` row. Either side may be empty
        depending on ``show_filename``/``show_copy_button``; if both are
        disabled, nothing is rendered at all -- not even the divider. The
        header text uses :data:`FONT_STYLE`, the same font metrics used for
        the code and gutter, so it reads at a consistent size.

        Args:
            snippet: The snippet being displayed.
            show_filename: Whether to render the filename/line info on the
                left side of the header.
            show_linenumber: Whether to append the origin line number (or
                range) next to the filename, if the snippet has one.
            show_copy_button: Whether to render a copy-to-clipboard button
                on the right side of the header, copying the snippet's
                code.
            copy_button_mode: Passed straight through to
                :func:`copy_button.render_copy_button_html` ("icon",
                "text", or "icon+text").
            header_color: Text color for the filename/line info, from the
                active :class:`_Theme` (dark/light need different shades to
                stay readable against their respective backgrounds).
            button_colors: Color set for the copy button, from the active
                :class:`_Theme` (see :attr:`_Theme.button_colors`), passed
                straight through to
                :func:`copy_button.render_copy_button_html` as keyword
                arguments.

        Returns:
            An HTML string for the header and its divider, or an empty
            string if both ``show_filename`` and ``show_copy_button`` are
            ``False``.
        """
        left = ""
        if show_filename:
            line_part = ""
            if show_linenumber and snippet.line_start is not None:
                if snippet.line_end is not None and snippet.line_end != snippet.line_start:
                    line_part = f" (lines {snippet.line_start}-{snippet.line_end})"
                else:
                    line_part = f" (line {snippet.line_start})"
            left = f"{snippet.filename}{line_part}"

        right = ""
        if show_copy_button:
            right = render_copy_button_html(
                snippet.code,
                mode=copy_button_mode,
                standalone=False,
                **button_colors,
            )

        if not left and not right:
            return ""

        return (
            '<div style="display:flex; justify-content:space-between; '
            f'align-items:center; {FONT_STYLE} color:{header_color};">'
            f"<div>{left}</div><div>{right}</div>"
            "</div>"
            f'<div style="height:1px; margin:6px 0; background-color:{DIVIDER_COLOR};"></div>'
        )

    @staticmethod
    def _render_gutter(start_line: int, n_lines: int) -> str:
        """Builds a plain-text line-number gutter to sit beside a snippet.

        Rendered as its own ``<pre>`` block (not a table), so it lines up
        with the code's ``<pre>`` block via matching font metrics rather
        than relying on table-cell layout -- avoiding notebook front ends
        (e.g. VS Code's Jupyter renderer) that apply their own default
        styling (such as right-aligned table cells) to bare
        ``<table>``/``<td>`` elements in HTML output. Uses :data:`PRE_RESET`
        and :data:`FONT_STYLE`, the same values forced onto the code's own
        ``<pre>`` block in :meth:`display`, so the two align.

        Args:
            start_line: The first line number to display.
            n_lines: How many consecutive line numbers to render.

        Returns:
            An HTML string for the gutter pane.
        """
        numbers = "\n".join(str(start_line + i) for i in range(n_lines))
        return (
            f'<pre style="{PRE_RESET} {FONT_STYLE} text-align:right; '
            "color:#8a8a8a; background:transparent !important; "
            'user-select:none; -webkit-user-select:none;">'
            f"{numbers}</pre>"
        )

    def _render_variant(
        self,
        snippet: Snippet,
        theme: _Theme,
        pygments_style: str,
        show_filename: bool,
        show_linenumber: bool,
        show_gutter_linenumbers: bool,
        show_copy_button: bool,
        copy_button_mode: str,
    ) -> str:
        """Renders one full theme variant (dark or light) of a snippet.

        Args:
            snippet: The snippet being displayed.
            theme: The colors (background, header text) for this variant.
            pygments_style: The Pygments style to highlight with -- pass a
                style suited to `theme` (e.g. a dark style with
                :data:`DARK_THEME`, a light one with :data:`LIGHT_THEME`),
                since the two aren't cross-checked here.
            show_filename: See :meth:`display`.
            show_linenumber: See :meth:`display`.
            show_gutter_linenumbers: See :meth:`display`.
            show_copy_button: See :meth:`display`.
            copy_button_mode: See :meth:`display`.

        Returns:
            An HTML string for this variant, tagged with ``theme.css_class``
            so :data:`_THEME_TOGGLE_CSS` can show/hide it appropriately, and
            carrying ``theme.default_display`` as its inline fallback
            visibility for whenever that stylesheet doesn't apply.
        """
        formatter = HtmlFormatter(style=pygments_style, noclasses=True)
        html_code = highlight(snippet.code, self._lexer_for(snippet.filename), formatter)

        # Always force the shared margin/padding/font metrics onto
        # Pygments' own <pre> block, appended after its existing style so
        # ours wins -- this keeps it consistent with the header and gutter
        # regardless of show_gutter_linenumbers, and keeps it aligned with
        # the gutter's <pre> when the gutter is shown. Also force an
        # explicit background-color directly on this <pre> (not just the
        # wrapping <div> below): JupyterLab ships a rule targeting every
        # `pre` element in rendered HTML output --
        #   .jp-ThemedContainer .jp-RenderedHTMLCommon pre {
        #     background-color: var(--jp-layout-color0); ... }
        # -- which resolves to black or white depending on the notebook's
        # theme. Pygments never puts a background on the <pre> itself (only
        # on the wrapping <div>), so with nothing of ours on the <pre> to
        # compete, that rule was winning outright and visually covering the
        # div's background underneath it. `!important` here isn't strictly
        # required (JupyterLab's rule doesn't use it), but keeps this robust
        # against theme variations that might.
        html_code = re.sub(
            r'(<pre style="[^"]*)(")',
            rf"\1 {PRE_RESET} {FONT_STYLE} background-color:{theme.background} !important;\2",
            html_code,
            count=1,
        )
        # Force Pygments' own wrapping <div> background to match too, so
        # there's no visible seam in renderers (e.g. VS Code) that don't
        # override the <pre> background the way JupyterLab does.
        html_code = re.sub(
            r"background: #[0-9a-fA-F]{6}",
            f"background: {theme.background} !important",
            html_code,
            count=1,
        )

        header = self._render_header(
            snippet,
            show_filename,
            show_linenumber,
            show_copy_button,
            copy_button_mode,
            theme.header_color,
            theme.button_colors,
        )

        if show_gutter_linenumbers:
            n_lines = snippet.code.count("\n") + 1 if snippet.code else 1
            gutter = self._render_gutter(snippet.line_start or 1, n_lines)
            body = (
                '<div style="display:flex; align-items:stretch;">'
                f'<div style="flex:0 0 auto;">{gutter}</div>'
                '<div style="flex:0 0 auto; width:1px; margin:0 8px; '
                f'background-color:{DIVIDER_COLOR};"></div>'
                f'<div style="flex:1 1 auto; min-width:0; overflow-x:auto;">{html_code}</div>'
                "</div>"
            )
        else:
            body = html_code

        return (
            f'<div class="{theme.css_class}" style="border:1px solid {theme.border_color}; '
            f"border-radius:6px; padding:8px; background-color:{theme.background} !important; "
            f'display:{theme.default_display};">'
            f"{header}{body}</div>"
        )

    def display(
        self,
        tag: str,
        show_filename: bool | None = None,
        show_linenumber: bool | None = None,
        show_gutter_linenumbers: bool | None = None,
        show_copy_button: bool | None = None,
        copy_button_mode: str | None = None,
    ) -> None:
        """Renders a snippet as syntax-highlighted, selectable HTML.

        Renders both a dark and a light variant (see :data:`DARK_THEME`,
        :data:`LIGHT_THEME`, :attr:`style`, :attr:`light_style`) and embeds
        CSS (:data:`_THEME_TOGGLE_CSS`) that shows only the one matching the
        notebook's current theme, switching automatically if the theme
        changes later without needing to re-run the cell. If that CSS ever
        fails to apply at all (see the module docstring's note on untrusted
        notebook reloads), each variant's own inline fallback keeps exactly
        one of the two visible rather than showing both.

        Args:
            tag: The tag of the snippet to display.
            show_filename: Whether to show the filename info on the left
                side of the header. Defaults to :attr:`show_filename` when
                not given.
            show_linenumber: Whether to include the origin line number (or
                range) next to the filename, if the snippet has one.
                Defaults to :attr:`show_linenumber` when not given.
                Regardless of this setting, nothing is shown for a snippet
                whose :attr:`Snippet.line_start` is ``None``.
            show_gutter_linenumbers: Whether to show an IDE-style
                line-number gutter down the left side of the highlighted
                code, in its own pane separated by a thin vertical divider.
                Defaults to :attr:`show_gutter_linenumbers` when not given
                (off by default). If the snippet has a known origin
                line/range, the gutter starts counting from that line
                instead of from 1.
            show_copy_button: Whether to show a copy-to-clipboard button on
                the right side of the header, copying the snippet's code.
                Defaults to :attr:`show_copy_button` when not given. If
                both this and ``show_filename`` are ``False``, no header
                (and no divider) is rendered at all.
            copy_button_mode: Appearance of the copy button -- "icon",
                "text", or "icon+text". Defaults to
                :attr:`copy_button_mode` when not given.

        Raises:
            KeyError: If no snippet has been loaded for ``tag``.
        """
        snippet = self.get(tag)

        if show_filename is None:
            show_filename = self.show_filename
        if show_linenumber is None:
            show_linenumber = self.show_linenumber
        if show_gutter_linenumbers is None:
            show_gutter_linenumbers = self.show_gutter_linenumbers
        if show_copy_button is None:
            show_copy_button = self.show_copy_button
        if copy_button_mode is None:
            copy_button_mode = self.copy_button_mode

        dark_html = self._render_variant(
            snippet,
            DARK_THEME,
            self.style,
            show_filename,
            show_linenumber,
            show_gutter_linenumbers,
            show_copy_button,
            copy_button_mode,
        )
        light_html = self._render_variant(
            snippet,
            LIGHT_THEME,
            self.light_style,
            show_filename,
            show_linenumber,
            show_gutter_linenumbers,
            show_copy_button,
            copy_button_mode,
        )

        display(HTML(_THEME_TOGGLE_CSS + dark_html + light_html))

    def __repr__(self) -> str:
        """Returns a short summary of how many snippets are loaded.

        Returns:
            A string of the form ``CSnippets(N snippet(s) loaded)``.
        """
        return f"CSnippets({len(self.snippets)} snippet(s) loaded)"


if __name__ == "__main__":
    # Quick sanity check outside of Jupyter: parse a path given on the
    # command line and list the tags that were found.
    import sys

    if len(sys.argv) != 2:
        print("Usage: python csnippets.py <file_or_directory>")
        raise SystemExit(1)

    manager = CSnippets().load(sys.argv[1])
    print(manager)
    for found_tag in manager.tags():
        print(" -", manager.get(found_tag))
