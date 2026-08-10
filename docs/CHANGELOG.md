# Changelog

All notable changes to this project are documented in this file.

## v1.4.0 - 2026-08-09

- First public release on GitHub under HOLOZTEK.
- Updated the public release assets to version `1.4.0`.
- Changed RPM distribution to a single `noarch` package without an OS-specific distribution suffix.
- Added Debian package metadata for `.deb` distribution.
- Updated installation instructions for RPM, DEB, and source-based installation.

## v1.3.3 - 2026-08-08

- Fixed the RPM packaging rule so `views/widget.edit.js.php` is included.
- Ensured the color picker initializer required by the widget settings form is shipped in RPM packages.

## v1.3.2 - 2026-08-08

- Added separate folder and host text color settings.
- Added `folder_font_color` and `host_font_color` widget fields.
- Applied configured colors through CSS custom properties.
- Added the widget settings JavaScript initializer for color picker fields.
- Updated `manifest.json` version metadata.

## v1.3.1 - 2026-07-18

- Fixed multi-select checkbox synchronization.
- Added `_hostids` broadcast output for selected hosts.

## Previous Releases

Earlier release history is available from Git tags:

- v1.3.0
- v1.2.4
- v1.2.3
- v1.2.2
- v1.2.1
- v1.2.0
- v1.1.0
- v1.0.2
- v1.0.1
- v1.0.0
