# Screenshot Guide

Use sanitized screenshots from a demo Zabbix environment. Do not use production dashboards or real monitoring data.

## Required Images

| File | Purpose | Suggested Size |
| ---- | ------- | -------------- |
| `screenshots/tree-navigator-single-group.png` | Single-select host group mode | 1200 x 700 or similar |
| `screenshots/tree-navigator-single-group-host.png` | Single-select host group and host mode | 1200 x 700 or similar |
| `screenshots/tree-navigator-search.png` | Host search with sanitized match candidates | 1200 x 700 or similar |
| `screenshots/tree-navigator-multi-group-host.png` | Multi-select host group and host mode | 1200 x 700 or similar |
| `screenshots/tree-navigator-settings.png` | English widget configuration form showing the key options | 900 x 650 or similar |
| `screenshots/tree-navigator-settings-ja.png` | Japanese widget configuration form showing the key options | 900 x 650 or similar |
| `screenshots/tree-navigator-dashboard-example.png` | Dashboard integration example with linked widgets | 1600 x 980 or similar |

## Optional Images

| File | Purpose |
| ---- | ------- |
| `screenshots/tree-navigator-broadcast.png` | Dashboard example showing another widget reacting to selection |
| `screenshots/tree-navigator-colors.png` | Settings or widget view showing separate folder and host text colors |

## Suggested Captions

Use these captions as README text or release notes when the matching screenshots are added.

| File | English Caption | Japanese Caption |
| ---- | --------------- | ---------------- |
| `tree-navigator-single-group.png` | Navigate host groups in single-select mode and broadcast the selected group branch to linked widgets. | シングル選択のグループモードで、選択したグループ階層を連携先ウィジェットへブロードキャストできます。 |
| `tree-navigator-single-group-host.png` | Drill from host groups down to individual hosts and broadcast either group IDs or host IDs. | グループから個別ホストまでたどり、グループ ID またはホスト ID をブロードキャストできます。 |
| `tree-navigator-multi-group-host.png` | Select multiple hosts or groups and broadcast the combined selection to linked widgets immediately. | 複数のホストやグループを選択し、連携先ウィジェットへまとめて即時ブロードキャストできます。 |
| `tree-navigator-settings.png` | Tune the root label, display mode, group filter, expansion depth, tooltips, and text colors from the widget settings. | ルート名、表示モード、対象グループ、初期展開深さ、ツールチップ、文字色を設定画面から調整できます。 |
| `tree-navigator-settings-ja.png` | Tune the same settings in the Japanese Zabbix UI. | 日本語UIで、同じ設定項目を確認・調整できます。 |
| `tree-navigator-dashboard-example.png` | Use Tree Navigator as a dashboard navigation control that drives linked widgets. | Tree Navigator をダッシュボードのナビゲーションとして使い、連携先ウィジェットを切り替えられます。 |
| `tree-navigator-search.png` | Search for a host and jump directly to the matching node in the tree. | ホスト名を検索し、該当するツリーノードへ素早く移動できます。 |
| `tree-navigator-broadcast.png` | Use host and host group broadcasts to drive other dashboard widgets. | ホストやホストグループのブロードキャストで、他のダッシュボードウィジェットを連動できます。 |
| `tree-navigator-colors.png` | Use separate folder and host text colors to match the tree to your dashboard theme. | フォルダとホストの文字色を個別に設定し、ダッシュボードの見た目に合わせられます。 |

## Sanitizing Checklist

- Use demo host groups such as `Datacenter A`, `Linux Servers`, `Network Devices`, and `Applications`.
- Use demo host names such as `web-01`, `db-01`, `router-01`, and `app-01`.
- Capture the three widget mode screenshots from the same demo dashboard and with similar crop boundaries.
- In the search screenshot, show the search box with sanitized host candidates and one highlighted or selected match.
- In the multi-select screenshot, check at least two demo entries so the checkbox behavior is visible.
- Keep the preview screenshots focused on the Tree Navigator widget itself.
- Use the dashboard example screenshot only for the integration example section.
- Remove or crop out browser address bars, usernames, internal URLs, IP addresses, alerts, and real metric values.
- Avoid showing customer names, organization names, environment names, inventory values, or production dashboard titles.
- Keep the preview screenshots readable at README width: 220 px for widget views and 300 px for the settings form.
- Keep the dashboard integration example readable at README width: 750 px.
- If color settings are shown, use neutral demo colors that remain readable on the Zabbix dashboard background.

## README Behavior

The README files already reference the required image files. After the PNG files are added to `screenshots/`, GitHub and Gitea will render them automatically.
