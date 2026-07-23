# Publication Checklist

Use this checklist before publishing `zabbix-widget-tree-navigator` from staging to GitHub.

## Source

- Confirm staged source is based on tag `v1.3.1`.
- Confirm `manifest.json` contains version `1.3.1`.
- Confirm no private URLs, credentials, internal hostnames, or environment-specific files are included.
- Confirm README installation instructions match the distributed artifact format.

## Repository

- Confirm target GitHub repository name is exactly `zabbix-widget-tree-navigator`.
- Confirm the publication approval record specifies repository `zabbix-widget-tree-navigator`.
- Confirm the publication approval record specifies version `v1.3.1`.
- Confirm the publication approval target is `GitHub`.

## Documentation

- Confirm README and LICENSE are present in the repository root.
- Confirm CHANGELOG, CONTRIBUTING, SECURITY, screenshot guide, and the publication checklist are under `docs/`.
- Confirm README preview images are present under `screenshots/`.
- Confirm screenshots contain no hostnames, IP addresses, organization names, alerts, metrics, credentials, or internal URLs.
- Confirm the license is MIT License for free public widget distribution.
- Confirm the copyright holder name is appropriate for public release.

## Release

- Push the reviewed staging content to GitHub only after publication approval.
- Push tag `v1.3.1` only after staged content and approved version match exactly.
- Create a GitHub release only from the approved tag and version.
