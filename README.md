# zabbix-widget-tree-navigator

[English](README.md) | [日本語](README.ja.md)

Tree Navigator is a Zabbix dashboard widget that displays host groups and hosts as a collapsible directory tree. Selecting a group or host broadcasts the selected IDs to other dashboard widgets.

## Preview

| Function | What it does |
| -------- | ------------ |
| Single-select host group navigation | Select a host group branch and broadcast the selected group IDs to linked widgets. |
| Single-select host navigation | Drill down from groups to hosts and broadcast either host group IDs or host IDs. |
| Host search | Search for a host by keyword and jump directly to the matching tree node. |
| Multi-select navigation | Check multiple hosts or groups and broadcast the combined selection immediately. |
| Widget settings | Configure display mode, target groups, expansion depth, tooltips, and text colors. |

<table>
  <tr>
    <td align="center" width="33%">
      <strong>Single-Select: Host Groups</strong><br>
      <img src="screenshots/tree-navigator-single-group.png" width="220" alt="Tree Navigator widget in single-select host group mode">
    </td>
    <td align="center" width="33%">
      <strong>Single-Select: Groups and Hosts</strong><br>
      <img src="screenshots/tree-navigator-single-group-host.png" width="220" alt="Tree Navigator widget in single-select host group and host mode">
    </td>
    <td align="center" width="33%">
      <strong>Host Search</strong><br>
      <img src="screenshots/tree-navigator-search.png" width="220" alt="Tree Navigator widget search box showing host matches">
    </td>
  </tr>
  <tr>
    <td align="center" width="33%">
      <strong>Multi-Select: Groups and Hosts</strong><br>
      <img src="screenshots/tree-navigator-multi-group-host.png" width="220" alt="Tree Navigator widget in multi-select host group and host mode">
    </td>
    <td align="center" width="33%">
      <strong>Settings</strong><br>
      <img src="screenshots/tree-navigator-settings.png" width="300" alt="Tree Navigator widget configuration form">
    </td>
    <td width="33%"></td>
  </tr>
</table>

## Dashboard Integration Example

<img src="screenshots/tree-navigator-dashboard-example.png" width="750" alt="Tree Navigator driving other Zabbix dashboard widgets" />

Tree Navigator can be used as a dashboard navigation control. Selecting a group or host updates linked widgets through Zabbix dashboard dynamic parameters, so operators can move from a tree selection to related maps, status summaries, graphs, or other dashboard panels.

## Feature Highlights

### Navigate Host Groups as a Tree

Tree Navigator turns Zabbix host groups into a compact, collapsible tree. Operators can browse nested host groups, expand only the areas they need, and keep the dashboard focused even when the monitored environment has many groups.

### Drill Down to Hosts

The widget can show hosts under each host group, with host icons and optional host-count tooltips. The search box helps jump to a matching host without manually expanding every branch.

### Drive Other Dashboard Widgets

Selecting a host group or host broadcasts dynamic parameters to other widgets. Single-select mode is useful for quick filtering, while multi-select mode lets operators check several hosts or groups and broadcast the combined selection immediately.

### Customize the View

The configuration form controls the root label, display mode, target host groups, initial expansion depth, recursive sub-group behavior, host-count tooltips, and separate folder/host text colors.

## Features

- Displays host groups and hosts in a collapsible tree
- Broadcasts selected host group IDs and host IDs to other widgets
- Supports host-group-only and host-group-plus-host display modes
- Configurable root label, initial expansion depth, and target host groups
- Optional recursive sub-group inclusion
- Optional host-count tooltip on hover
- Separate folder and host text color settings
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
| Folder text color | Text color for host group and root labels |
| Host text color | Text color for host labels |

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
