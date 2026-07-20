# Contributing

Thank you for your interest in improving zabbix-widget-tree-navigator.

## Scope

This repository is prepared for public distribution of the Tree Navigator widget for Zabbix.
Before submitting changes, please confirm that the change is compatible with the supported
Zabbix and PHP versions listed in the README.

## Development Notes

- Keep widget behavior compatible with Zabbix 7.0 or later.
- Do not commit generated packages, local configuration, credentials, or environment-specific files.
- Update `manifest.json` and `README.md` when user-visible behavior or compatibility changes.
- Add an entry to `CHANGELOG.md` for release-facing changes.

## Reporting Issues

When reporting an issue, include:

- Zabbix version
- PHP version
- Widget version
- Browser and version
- Steps to reproduce
- Expected and actual behavior

## Pull Requests

Pull requests should describe the purpose of the change, affected behavior, and verification performed.
Security-sensitive reports should follow `SECURITY.md` instead of being submitted publicly.
