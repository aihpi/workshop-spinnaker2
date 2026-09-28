<div style="background-color: #ffffff; color: #000000; padding: 10px;">
<img src="00_aisc/img/logo_aisc_bmftr.jpg">
<h1> Workshop: Neuromorphic Computing on SpiNNaker2
</div>

Material for a 3-hour hands-on workshop on the SpiNNaker2 neuromorphic chip, aimed at ML researchers and software developers. Participants learn why neuromorphic hardware can save energy, the basics of spiking neurons and networks, and how to run their own spiking networks on SpiNNaker2 chips with [py-spinnaker2](https://spinnaker2.gitlab.io/py-spinnaker2/).

> **Status:** planning. The workshop is planned for early November 2026.

## Repository structure

| Folder | Content |
|---|---|
| `00_aisc/` | AISC logos and images |
| `01_knowledge_base/` | Notes and sources (local only, not tracked in git) |
| `02_workshop_design/` | Brief, outline and demo plans |

## Setup

TODO: running on the chips via the HPI cluster, and the Brian2 fallback.

## Workshop outline

TODO, see `02_workshop_design/brief.md` for the current draft.

## Author

- [David Goll](https://hpi.de/kisz)

## Issues and the project board

`.github/workflows/add-issue-to-project.yml` adds every new issue to the [AIHPI project board](https://github.com/orgs/aihpi/projects/3). It needs a token in the secret `ADD_ISSUE_TO_PROJECT`, because the workflow's own `GITHUB_TOKEN` cannot write to organisation projects.

- **Public repository**: nothing to do, the organisation-level secret is inherited.
- **Private repository**: organisation secrets are not available to private repositories on the organisation's GitHub plan, so set the secret once after creating the repository. Ask an organisation admin for the token file, then run `gh secret set ADD_ISSUE_TO_PROJECT -R aihpi/<repository> < path/to/token-file`.

Until the secret exists, the workflow fails on every new issue with `Input required and not supplied: github-token`. Nothing else is affected.

## License

[MIT](LICENSE)

---

## Acknowledgements
<img src="00_aisc/img/logo_bmftr_de.png" alt="drawing" style="width:170px;"/>

The [AI Service Centre Berlin Brandenburg](http://hpi.de/kisz) is funded by the [Federal Ministry of Research, Technology and Space](https://www.bmbf.de/) under the funding code 16IS22092.
