# Publication Checklist

Use this checklist before publishing `zabbix-widget-tree-navigator` from staging to GitHub.

## Source

- Confirm staged source is based on the approved release tag.
- Confirm `manifest.json` version matches the approved release version.
- Confirm package metadata versions match the approved release version.
- Confirm README release links, package filenames, install commands, and source archive commands match the approved release version.
- Run `scripts/check-version-consistency.sh` before publishing.
- Run `scripts/check-release-version.sh <approved-version>` before publishing.
- Confirm `manifest.json` contains public `author`, `description`, and `url` metadata.
- Confirm no private URLs, credentials, internal hostnames, or environment-specific files are included.
- Confirm README installation instructions match the distributed artifact format.
- Confirm source installation instructions copy only runtime module files, not the full Git repository.

## Repository

- Confirm target GitHub owner is exactly `HOLOZTEK`.
- Confirm target GitHub repository name is exactly `zabbix-widget-tree-navigator`.
- Confirm target GitHub repository visibility is `public`.
- Confirm Repository Topics are set to `zabbix`, `zabbix-widget`, `monitoring`, `dashboard`, and `php`.
- Confirm the publication approval record specifies owner `HOLOZTEK`.
- Confirm the publication approval record specifies repository `zabbix-widget-tree-navigator`.
- Confirm the publication approval record specifies the approved release version.
- Confirm the publication approval record specifies the full current staging commit SHA.
- Confirm the publication approval record specifies target `GitHub`.
- Confirm the publication approval record specifies visibility `public`.

## Documentation

- Confirm README and LICENSE are present in the repository root.
- Confirm `README.md` is the English default README and `README.ja.md` is the Japanese README.
- Confirm both README files contain working language switch links.
- Confirm CHANGELOG, CONTRIBUTING, SECURITY, screenshot guide, and the publication checklist are under `docs/`.
- Confirm SECURITY describes a private vulnerability reporting path and does not rely on a version table that can drift.
- Confirm RPM and DEB package metadata are present and use MIT-compatible public release metadata.
- Confirm the required README preview and dashboard example images are present under `screenshots/`.
- Confirm the required screenshots cover single-select group mode, single-select group-and-host mode, host search, multi-select group-and-host mode, and the settings form.
- Confirm the Japanese README uses the Japanese settings screenshot.
- Confirm the dashboard integration example image is shown outside the Preview section.
- Confirm screenshots contain no hostnames, IP addresses, organization names, alerts, metrics, credentials, or internal URLs.
- Confirm the license is MIT License for free public widget distribution.
- Confirm LICENSE keeps the standard MIT License text without inserting brand-specific lines into the license body.
- Confirm GitHub recognizes the repository license as MIT License.
- Confirm the copyright holder name is `ttake-55` for this public release.

## Release

- Push the reviewed staging content to GitHub only after publication approval.
- Push the approved release tag only after staged content and approved version match exactly.
- Create a GitHub release only from the approved tag and version.

## Maintenance Notes

- Consider consolidating `scripts/check-version-consistency.sh` and `scripts/check-release-version.sh` into one release validation script with portable dependencies.
- Include the first release entry in `docs/CHANGELOG.md` in automated release validation to prevent changelog version drift.
