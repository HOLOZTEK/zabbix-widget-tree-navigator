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
| `screenshots/tree-navigator-colors.png` | Settings or widget view showing separate folder and host text colors |

## Suggested Captions

Use these captions as README text or release notes when the matching screenshots are added.

| File | English Caption | Japanese Caption |
| ---- | --------------- | ---------------- |
| `tree-navigator-view.png` | Browse host groups and hosts in a collapsible tree without leaving the dashboard. | ダッシュボード上で、ホストグループとホストを折りたたみ可能なツリーとして確認できます。 |
| `tree-navigator-settings.png` | Tune the root label, display mode, group filter, expansion depth, tooltips, and text colors from the widget settings. | ルート名、表示モード、対象グループ、初期展開深さ、ツールチップ、文字色を設定画面から調整できます。 |
| `tree-navigator-search.png` | Search for a host and jump directly to the matching node in the tree. | ホスト名を検索し、該当するツリーノードへ素早く移動できます。 |
| `tree-navigator-multiselect.png` | Select multiple hosts or groups and broadcast the combined selection to linked widgets immediately. | 複数のホストやグループを選択し、連携先ウィジェットへまとめて即時ブロードキャストできます。 |
| `tree-navigator-broadcast.png` | Use host and host group broadcasts to drive other dashboard widgets. | ホストやホストグループのブロードキャストで、他のダッシュボードウィジェットを連動できます。 |
| `tree-navigator-colors.png` | Use separate folder and host text colors to match the tree to your dashboard theme. | フォルダとホストの文字色を個別に設定し、ダッシュボードの見た目に合わせられます。 |

## Sanitizing Checklist

- Use demo host groups such as `Datacenter A`, `Linux Servers`, `Network Devices`, and `Applications`.
- Use demo host names such as `web-01`, `db-01`, `router-01`, and `app-01`.
- Remove or crop out browser address bars, usernames, internal URLs, IP addresses, alerts, and real metric values.
- Avoid showing customer names, organization names, environment names, inventory values, or production dashboard titles.
- Keep the screenshots readable at README width: 750 px for the main view and 520 px for the settings form.
- If color settings are shown, use neutral demo colors that remain readable on the Zabbix dashboard background.

## README Behavior

The README already references the two required image files. After the PNG files are added to `screenshots/`, GitHub and Gitea will render them automatically.
