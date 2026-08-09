# zabbix-widget-tree-navigator

[English](README.md) | [日本語](README.ja.md)

## Overview

Tree Navigator is a Zabbix dashboard widget that displays host groups and hosts as a collapsible directory tree. It works as a dashboard navigation control: selecting a host group or host broadcasts dynamic parameters to linked widgets, so operators can move from a tree selection to related maps, status summaries, graphs, or other dashboard panels.

<img src="screenshots/tree-navigator-dashboard-example.png" width="750" alt="Tree Navigator driving other Zabbix dashboard widgets" />

## Features

| Function | What it does |
| -------- | ------------ |
| Host group tree navigation | Browse nested Zabbix host groups as a compact, collapsible tree. |
| Host group selection | Select a host group branch and broadcast the selected group IDs to linked widgets. |
| Host selection | Drill down from groups to hosts and broadcast either host group IDs or host IDs. |
| Host search | Search for a host by keyword and jump directly to the matching tree node. |
| Multi-select | Check multiple hosts or groups and broadcast the combined selection immediately. |
| Widget integration | Use Zabbix dynamic parameters to drive maps, summaries, graphs, and other panels. |

<table>
  <tr>
    <td align="center" valign="top" width="25%">
      <strong>Host Group Selection</strong><br>
      <img src="screenshots/tree-navigator-single-group.png" width="180" alt="Tree Navigator widget in single-select host group mode">
    </td>
    <td align="center" valign="top" width="25%">
      <strong>Host Selection</strong><br>
      <img src="screenshots/tree-navigator-single-group-host.png" width="180" alt="Tree Navigator widget in single-select host group and host mode">
    </td>
    <td align="center" valign="top" width="25%">
      <strong>Host Search</strong><br>
      <img src="screenshots/tree-navigator-search.png" width="180" alt="Tree Navigator widget search box showing host matches">
    </td>
    <td align="center" valign="top" width="25%">
      <strong>Multi-Select</strong><br>
      <img src="screenshots/tree-navigator-multi-group-host.png" width="180" alt="Tree Navigator widget in multi-select host group and host mode">
    </td>
  </tr>
</table>

## Settings

| Setting | Description |
| ------- | ----------- |
| Root name | Label shown at the top of the tree |
| Display mode | Host groups only, or host groups and hosts |
| Host groups | Limit the tree to selected groups; empty means all groups |
| Initial depth | Initial expansion depth, from 0 to 10; default is 1 |
| Include sub-groups | Recursively include sub-groups |
| Show host count in tooltip | Show host counts while hovering over groups |
| Folder text color | Text color for host group and root labels |
| Host text color | Text color for host labels |

<img src="screenshots/tree-navigator-settings.png" width="520" alt="Tree Navigator widget configuration form" />

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

Latest version: **v1.3.3**

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
