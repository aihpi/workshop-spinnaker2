"""Render a clipboard-copy button as HTML/JS.

Provides two entry points:

- :func:`copy_button` -- unchanged from the original standalone version:
  builds a button and immediately displays it, positioned via `align` in
  its own full-width wrapper.
- :func:`render_copy_button_html` -- the underlying builder, returning the
  button's HTML/JS as a string instead of displaying it. Used internally
  by :func:`copy_button`, and also imported by ``csnippets.py`` to embed
  the button inline inside a layout it already controls (e.g. next to a
  filename in a header row), via ``standalone=False``.

The button's appearance, animation, and clipboard behavior are unchanged
from the original version; only the display-vs-return split is new.
"""

from IPython.display import HTML, display
import html
import json
import uuid

# ---- Global defaults (edit these to change behavior everywhere) ----------
# COPY_BUTTON_MODE: "icon"      -> clipboard icon only
#                   "text"      -> label text only
#                   "icon+text" -> icon on the left, label to its right
COPY_BUTTON_MODE = "icon+text"

# COPY_BUTTON_ALIGN: "left" or "right" -- horizontal placement of the button
# (only used in standalone mode; see `standalone` on render_copy_button_html)
COPY_BUTTON_ALIGN = "left"
# ----------------------------------------------------------------------------

_CLIPBOARD_ICON = """
<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24"
     fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect>
  <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path>
</svg>
"""

_CHECK_ICON = """
<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24"
     fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <polyline points="20 6 9 17 4 12"></polyline>
</svg>
"""


#: Default button colors -- the original, dark-only appearance. Passed
#: explicitly as a set by ``csnippets.py`` for its light variant; left as
#: plain defaults here so standalone `copy_button()`/`render_copy_button_html()`
#: calls look exactly as before if colors aren't specified.
DEFAULT_BUTTON_COLORS = {
    "background_color": "#2d2d2d",
    "text_color": "#cccccc",
    "border_color": "#3c3c3c",
    "hover_background_color": "#3c3c3c",
    "hover_border_color": "#565656",
    "success_border_color": "#0e639c",
    "success_text_color": "#4fc1ff",
}


def render_copy_button_html(
    text: str,
    label: str = "Copy to clipboard",
    mode: str | None = None,
    align: str | None = None,
    standalone: bool = True,
    background_color: str = DEFAULT_BUTTON_COLORS["background_color"],
    text_color: str = DEFAULT_BUTTON_COLORS["text_color"],
    border_color: str = DEFAULT_BUTTON_COLORS["border_color"],
    hover_background_color: str = DEFAULT_BUTTON_COLORS["hover_background_color"],
    hover_border_color: str = DEFAULT_BUTTON_COLORS["hover_border_color"],
    success_border_color: str = DEFAULT_BUTTON_COLORS["success_border_color"],
    success_text_color: str = DEFAULT_BUTTON_COLORS["success_text_color"],
) -> str:
    """Builds the HTML/JS for a clipboard-copy button, without displaying it.

    Args:
        text: The text copied to the clipboard when the button is clicked.
        label: The label shown next to (or instead of) the icon, and
            restored after the "Copied!" confirmation fades.
        mode: "icon", "text", or "icon+text". Defaults to
            :data:`COPY_BUTTON_MODE`.
        align: "left" or "right". Only used when `standalone` is True, to
            position the button within its own full-width wrapper.
            Defaults to :data:`COPY_BUTTON_ALIGN`.
        standalone: If True (default), wraps the button in a full-width
            flex container that positions it left/right on its own -- this
            is what :func:`copy_button` uses for a plain, self-contained
            display. If False, returns just the bare button and its
            script, with no positioning wrapper, for embedding inside a
            layout the caller already controls (e.g. a header row that
            also has other content next to it).
        background_color: Button background at rest.
        text_color: Label/icon color at rest.
        border_color: Border color at rest.
        hover_background_color: Background color while hovered.
        hover_border_color: Border color while hovered.
        success_border_color: Border color during the "Copied!" confirmation.
        success_text_color: Label/icon color during the "Copied!" confirmation.

    Returns:
        An HTML string containing the button and its supporting script.
    """
    mode = mode or COPY_BUTTON_MODE
    align = align or COPY_BUTTON_ALIGN

    show_icon = mode in ("icon", "icon+text")
    show_label = mode in ("text", "icon+text")

    btn_id = f"copybtn-{uuid.uuid4().hex}"

    icon_span = f'<span class="cb-icon" style="display:flex;">{_CLIPBOARD_ICON}</span>' if show_icon else ""
    label_span = f'<span class="cb-label">{html.escape(label)}</span>' if show_label else ""

    button_html = f"""<button id="{btn_id}"
        data-text="{html.escape(text, quote=True)}"
        data-label="{html.escape(label, quote=True)}"
        data-mode="{mode}"
        style="
          display: flex;
          align-items: center;
          gap: 6px;
          background-color: {background_color};
          color: {text_color};
          border: 1px solid {border_color};
          border-radius: 6px;
          padding: 6px 14px;
          font-family: -apple-system, 'Segoe UI', sans-serif;
          font-size: 13px;
          cursor: pointer;
          transition: background-color 0.15s ease, border-color 0.15s ease, color 0.15s ease;
        "
        onmouseover="this.style.backgroundColor='{hover_background_color}'; this.style.borderColor='{hover_border_color}';"
        onmouseout="this.style.backgroundColor='{background_color}'; this.style.borderColor='{border_color}';"
      >{icon_span}{label_span}</button>"""

    script = f"""
    <script>
    (function() {{
      const btn = document.getElementById("{btn_id}");
      const checkIcon = {json.dumps(_CHECK_ICON)};
      const clipboardIcon = {json.dumps(_CLIPBOARD_ICON)};
      const iconEl = btn.querySelector(".cb-icon");
      const labelEl = btn.querySelector(".cb-label");

      btn.addEventListener("click", function() {{
        navigator.clipboard.writeText(btn.dataset.text).then(() => {{
          btn.style.borderColor = "{success_border_color}";
          btn.style.color = "{success_text_color}";
          if (iconEl) iconEl.innerHTML = checkIcon;
          if (labelEl) labelEl.innerText = "Copied!";
          setTimeout(() => {{
            btn.style.borderColor = "{border_color}";
            btn.style.color = "{text_color}";
            if (iconEl) iconEl.innerHTML = clipboardIcon;
            if (labelEl) labelEl.innerText = btn.dataset.label;
          }}, 1200);
        }});
      }});
    }})();
    </script>
    """

    if standalone:
        justify = "flex-start" if align == "left" else "flex-end"
        return f'<div style="display:flex; justify-content:{justify}; width:100%;">{button_html}</div>{script}'
    return button_html + script


def copy_button(
    text: str,
    label: str = "Copy to clipboard",
    mode: str | None = None,
    align: str | None = None,
) -> None:
    """Render a button that copies `text` to the clipboard when clicked.

    Works with remote Jupyter kernels (e.g. VS Code + SSH remote) because
    the HTML/JS output renders in the local webview, not on the kernel host.

    mode:  "icon", "text", or "icon+text" (defaults to COPY_BUTTON_MODE)
    align: "left" or "right" (defaults to COPY_BUTTON_ALIGN)
    """
    display(HTML(render_copy_button_html(text, label=label, mode=mode, align=align, standalone=True)))


# example
# copy_button("hello world")
# copy_button("hello world", mode="icon", align="right")
