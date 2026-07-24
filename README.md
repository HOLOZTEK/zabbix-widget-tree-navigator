# zabbix-widget-tree-navigator

[English](README.md) | [日本語](README.ja.md)

Tree Navigator is a Zabbix dashboard widget that displays host groups and hosts as a collapsible directory tree. Selecting a group or host broadcasts the selected IDs to other dashboard widgets.

## Preview

<img src="screenshots/tree-navigator-view.png" width="750" alt="Tree Navigator widget showing host groups and hosts in a collapsible tree" />

<img src="screenshots/tree-navigator-settings.png" width="520" alt="Tree Navigator widget configuration form" />

## Features

- Displays host groups and hosts in a collapsible tree
- Broadcasts selected host group IDs and host IDs to other widgets
- Supports host-group-only and host-group-plus-host display modes
- Configurable root label, initial expansion depth, and target host groups
- Optional recursive sub-group inclusion
- Optional host-count tooltip on hover
- Search box for finding and jumping to matching hosts
- Single-select and multi-select modes. In multi-select mode, checkboxes appear beside host and host group icons, and checked IDs are broadcast immediately.
- Japanese and English UI support

## Settings

| Setting | Description |
| ------- | ----------- |
| Root name | Label shown at the top of the tree |
| Display mode | Host groups only, or host groups and hosts |
| Host groups | Limit the tree to selected groups; empty means all groups |
| Initial depth | Initial expansion depth, from 0 to 10; default is 1 |
| Include sub-groups | Recursively include sub-groups |
| Show host count in tooltip | Show host counts while hovering over groups |

## Broadcast Outputs

- Selected host group ID
- Selected host group IDs
- Selected host ID
- Selected host IDs

In single-select mode, selecting a group broadcasts the selected group ID and all descendant group IDs from the full group hierarchy, regardless of the `Include sub-groups` display setting.

In multi-select mode, checked groups broadcast only their own group IDs. Host and group checkboxes can be mixed, and every checkbox change broadcasts the current selection immediately.

For compatibility with the standard Host navigator widget and related widgets, host selections are sent to both single and multiple host ID outputs.

## Requirements

- Zabbix 7.0 or later
- PHP 8.0 or later

## Installation

### Install from RPM

1. Download the RPM package and install it on the Zabbix server.
   ```bash
   rpm -Uvh zabbix-widget-tree-navigator-*.rpm
   ```
2. In the Zabbix UI, enable the module from Administration -> Modules.
3. Add the widget to a dashboard.

### Install from Source

1. Place this repository under the Zabbix frontend modules directory.
   ```text
   /usr/share/zabbix/modules/tree-navigator
   ```
2. Set ownership and permissions so the Zabbix frontend can read the files.
3. In the Zabbix UI, enable the module from Administration -> Modules.

## Documentation

- [CHANGELOG](docs/CHANGELOG.md)
- [CONTRIBUTING](docs/CONTRIBUTING.md)
- [SECURITY](docs/SECURITY.md)
- [Screenshot Guide](docs/screenshot-guide.md)
- [LICENSE](LICENSE)

## Repository Layout

Files loaded as a Zabbix module are kept in the repository root and the `actions/`, `assets/`, `includes/`, and `views/` directories. Publication and maintenance documents are kept under `docs/`.

## Version

Latest version: **v1.3.1**

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
