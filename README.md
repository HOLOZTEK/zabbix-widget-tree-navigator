# zabbix-widget-tree-navigator

[English](README.md) | [日本語](README.ja.md)

## Overview

Tree Navigator is a Zabbix dashboard widget that displays host groups and hosts as a collapsible directory tree.

It works as a dashboard navigation control: selecting a host group or host broadcasts dynamic parameters to linked widgets.

Operators can move from a tree selection to related maps, status summaries, graphs, or other dashboard panels.

<img src="screenshots/tree-navigator-dashboard-example.png" width="750" alt="Tree Navigator driving other Zabbix dashboard widgets" />

[Latest release](https://github.com/HOLOZTEK/zabbix-widget-tree-navigator/releases/tag/v1.4.8) | [RPM](https://github.com/HOLOZTEK/zabbix-widget-tree-navigator/releases/download/v1.4.8/zabbix-widget-tree-navigator-1.4.8.noarch.rpm) | [DEB](https://github.com/HOLOZTEK/zabbix-widget-tree-navigator/releases/download/v1.4.8/zabbix-widget-tree-navigator_1.4.8_all.deb) | [Source](https://github.com/HOLOZTEK/zabbix-widget-tree-navigator/releases/download/v1.4.8/zabbix-widget-tree-navigator-1.4.8.tar.gz)

## Why Tree Navigator?

Tree Navigator is not a replacement for the standard Host navigator widget.

It is intended for dashboards where the host group hierarchy itself is the navigation model.

Use it when linked widgets need host group IDs as well as host IDs, or when operators need to select multiple hosts and groups from the same tree.

## Features

<table>
  <tr>
    <th align="left" nowrap style="white-space: nowrap;">Function</th>
    <th align="left">What it does</th>
  </tr>
  <tr>
    <td nowrap style="white-space: nowrap;">Tree view</td>
    <td>Browse nested Zabbix host groups as a compact, collapsible tree.</td>
  </tr>
  <tr>
    <td nowrap style="white-space: nowrap;">Host group selection</td>
    <td>Select a host group branch and broadcast the selected group IDs to linked widgets.</td>
  </tr>
  <tr>
    <td nowrap style="white-space: nowrap;">Host selection</td>
    <td>Drill down from groups to hosts and broadcast either host group IDs or host IDs.</td>
  </tr>
  <tr>
    <td nowrap style="white-space: nowrap;">Host menu access</td>
    <td>Click a host icon to open the standard Zabbix host menu shown for host clicks.</td>
  </tr>
  <tr>
    <td nowrap style="white-space: nowrap;">Multi-select</td>
    <td>Check multiple hosts or groups and broadcast the combined selection immediately.</td>
  </tr>
  <tr>
    <td nowrap style="white-space: nowrap;">Host search feature</td>
    <td>Search for a host by keyword and jump directly to the matching tree node.</td>
  </tr>
  <tr>
    <td nowrap style="white-space: nowrap;">Widget integration</td>
    <td>Use Zabbix dynamic parameters to drive maps, summaries, graphs, and other panels.</td>
  </tr>
</table>

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
      <strong>Multi-Select</strong><br>
      <img src="screenshots/tree-navigator-multi-group-host.png" width="180" alt="Tree Navigator widget in multi-select host group and host mode">
    </td>
    <td align="center" valign="top" width="25%">
      <strong>Host Search Feature</strong><br>
      <img src="screenshots/tree-navigator-search.png" width="180" alt="Tree Navigator widget search box showing host matches">
    </td>
  </tr>
</table>

## Settings

<table>
  <tr bgcolor="#f0f3f5" style="background-color: #f0f3f5;">
    <th align="left">Setting</th>
    <th align="left">Description</th>
  </tr>
  <tr>
    <td>Root name</td>
    <td>Label shown at the top of the tree</td>
  </tr>
  <tr>
    <td>Display mode</td>
    <td>Chooses whether the tree shows host groups only, or host groups and hosts.</td>
  </tr>
  <tr>
    <td>Host groups</td>
    <td>Specifies the host groups displayed by the navigator. Multiple groups can be selected. If empty, all host groups are included.</td>
  </tr>
  <tr>
    <td>Initial depth</td>
    <td>Initial expansion depth, from 0 to 10; default is 1</td>
  </tr>
  <tr>
    <td>Include sub-groups</td>
    <td>Includes descendant group nodes under the host groups selected in the Host groups setting.</td>
  </tr>
  <tr>
    <td>Show host count in tooltip</td>
    <td>Enables host-count tooltips when hovering over host group icons.</td>
  </tr>
  <tr>
    <td>Folder text color</td>
    <td>Text color for host group and root labels</td>
  </tr>
  <tr>
    <td>Host text color</td>
    <td>Text color for host labels</td>
  </tr>
</table>

<img src="screenshots/tree-navigator-settings.png" width="520" alt="Tree Navigator widget configuration form" />

## Selection Behavior

<table>
  <tr bgcolor="#f0f3f5" style="background-color: #f0f3f5;">
    <th align="left">Mode</th>
    <th align="left">Visible items</th>
    <th align="left">Selection</th>
    <th align="left">Broadcast behavior</th>
  </tr>
  <tr>
    <td>Host groups only</td>
    <td>Host group tree</td>
    <td>Single host group</td>
    <td>Broadcasts the selected group ID and all descendant group IDs from the full group hierarchy.</td>
  </tr>
  <tr>
    <td>Host groups and hosts</td>
    <td>Host group tree and hosts</td>
    <td>Single host group or host</td>
    <td>Broadcasts group IDs for group selection, or host IDs for host selection.</td>
  </tr>
  <tr>
    <td>Multi-select</td>
    <td>Host group tree and hosts with checkboxes</td>
    <td>Multiple host groups and hosts</td>
    <td>Broadcasts checked group IDs only for checked groups, and checked host IDs for checked hosts.</td>
  </tr>
</table>

`Include sub-groups` controls which descendant group nodes are shown under the configured Host groups filter. It does not change the multi-select rule that only checked groups are broadcast.

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
   rpm -Uvh zabbix-widget-tree-navigator-1.4.8.noarch.rpm
   ```
2. The package places the widget files under the active Zabbix frontend module directory automatically.
3. In the Zabbix UI, enable the module from Administration -> Modules.
4. Add the widget to a dashboard.

### Install from DEB

1. Download the DEB package and install it on the Zabbix server.
   ```bash
   apt install ./zabbix-widget-tree-navigator_1.4.8_all.deb
   ```
2. The package places the widget files under the active Zabbix frontend module directory automatically.
3. In the Zabbix UI, enable the module from Administration -> Modules.
4. Add the widget to a dashboard.

### Install from Source

RPM or DEB installation is recommended for normal use. For source-based installation, use the release archive and copy only the files required by the Zabbix module.

1. Download and extract the release source archive.
   ```bash
   curl -L -o zabbix-widget-tree-navigator-1.4.8.tar.gz https://github.com/HOLOZTEK/zabbix-widget-tree-navigator/releases/download/v1.4.8/zabbix-widget-tree-navigator-1.4.8.tar.gz
   tar -xzf zabbix-widget-tree-navigator-1.4.8.tar.gz
   ```
2. Copy the runtime module files to the Zabbix frontend modules directory as `tree-navigator`.
   ```bash
   install -d /usr/share/zabbix/ui/modules/tree-navigator
   cd zabbix-widget-tree-navigator-1.4.8
   cp -a manifest.json Widget.php actions assets includes locale views /usr/share/zabbix/ui/modules/tree-navigator/
   ```
   Use `/usr/share/zabbix/modules/tree-navigator` instead if your Zabbix installation uses the legacy module path.
3. Set ownership and permissions so the Zabbix frontend can read the files.
4. In the Zabbix UI, enable the module from Administration -> Modules.
5. Add the widget to a dashboard.

## Upgrading from the Old Module ID

In v1.4.1, the Zabbix module identifier changed from `tree-navigator` to `holoztek_tree_navigator` to reduce the risk of name collisions with modules from other vendors.

The RPM/DEB package name and the frontend module directory remain `zabbix-widget-tree-navigator` and `tree-navigator` for compatibility, but Zabbix treats the new manifest ID as a different widget type.

If you are upgrading from v1.4.0 or earlier:

1. Install the new RPM/DEB package, or replace the source files with the v1.4.8 runtime files.
2. In the Zabbix UI, open Administration -> Modules, run the module scan, and enable the module with ID `holoztek_tree_navigator`.
3. Disable or remove the old `tree-navigator` module entry if it remains listed.
4. Export or back up the dashboard before making API changes.
5. Retrieve the complete existing dashboard structure, including all pages and widgets, with `dashboard.get`.
6. Change only widgets whose `type` is `tree-navigator` to `holoztek_tree_navigator`. Keep `widgetid`, `fields`, and `reference` unchanged.
7. Call `dashboard.update` with the complete `pages` structure. The `pages` parameter replaces the existing dashboard pages; pages omitted from the request can be removed.
8. Apply the same type change to template dashboards if you use template dashboard widgets.

Example migration logic after retrieving the complete dashboard and before calling `dashboard.update`:

```php
foreach ($dashboard['pages'] as &$page) {
    foreach ($page['widgets'] as &$widget) {
        if ($widget['type'] === 'tree-navigator') {
            $widget['type'] = 'holoztek_tree_navigator';
        }
    }
}
```

## Documentation

- [CHANGELOG](docs/CHANGELOG.md)
- [CONTRIBUTING](docs/CONTRIBUTING.md)
- [SECURITY](docs/SECURITY.md)
- [Screenshot Guide](docs/screenshot-guide.md)
- [LICENSE](LICENSE)

## Repository Layout

Files loaded as a Zabbix module are kept in the repository root and the `actions/`, `assets/`, `includes/`, and `views/` directories. Publication and maintenance documents are kept under `docs/`.

## Maintainer

Developed and maintained by [HOLOZTEK](https://github.com/HOLOZTEK).

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
