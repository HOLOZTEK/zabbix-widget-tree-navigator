# Screenshot Guide

Use sanitized screenshots from a demo Zabbix environment. Do not use production dashboards or real monitoring data.

## Required Images

| File | Purpose | Suggested Size |
| ---- | ------- | -------------- |
| `screenshots/tree-navigator-view.png` | Main dashboard widget view with host groups and hosts expanded | 1200 x 700 or similar |
| `screenshots/tree-navigator-settings.png` | Widget configuration form showing the key options | 900 x 650 or similar |

## Optional Images

| File | Purpose |
| ---- | ------- |
| `screenshots/tree-navigator-search.png` | Search box with a sanitized host match |
| `screenshots/tree-navigator-multiselect.png` | Multi-select mode with checked demo groups or hosts |
| `screenshots/tree-navigator-broadcast.png` | Dashboard example showing another widget reacting to selection |

## Sanitizing Checklist

- Use demo host groups such as `Datacenter A`, `Linux Servers`, `Network Devices`, and `Applications`.
- Use demo host names such as `web-01`, `db-01`, `router-01`, and `app-01`.
- Remove or crop out browser address bars, usernames, internal URLs, IP addresses, alerts, and real metric values.
- Avoid showing customer names, organization names, environment names, inventory values, or production dashboard titles.
- Keep the screenshots readable at README width: 750 px for the main view and 520 px for the settings form.

## README Behavior

The README already references the two required image files. After the PNG files are added to `screenshots/`, GitHub and Gitea will render them automatically.
