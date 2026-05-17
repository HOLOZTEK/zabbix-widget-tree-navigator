Name:           zabbix-widget-tree-navigator
Version:        1.0.0
Release:        1%{?dist}
Summary:        Tree Navigator widget for Zabbix dashboard
License:        Proprietary
BuildArch:      noarch

%description
Zabbix dashboard widget that displays host groups and hosts as a collapsible
directory tree.

Features:
- Configurable root node name displayed at the top of the tree
- Directory-tree style display: host groups as folders, hosts as files
- Two display modes: host groups only / host groups and hosts
- Configurable host group filter (multiple groups supported)
- Sub-group recursive mode: selecting a parent broadcasts all descendant group IDs
- Collapsible tree nodes with +/- toggle; expanded state persisted per widget
- CSS guide-line connectors for clean tree visualization
- Hosts displayed one indent level deeper than host groups
- Folder icon hover shows recursive host count (including sub-groups)
- OS-type host icons (server / linux / windows / network / virtual)
- Clicking a group name broadcasts _hostgroupid + _hostgroupids
- Clicking a host name broadcasts _hostid + direct parent _hostgroupid
- Clicking a host icon shows the Zabbix host context menu
- Japanese and English locale support

%prep
# nothing

%install
SRCDIR=%{_sourcedir}/tree-navigator
STAGEDIR=%{buildroot}/usr/share/zabbix-widget-tree-navigator

install -d ${STAGEDIR}/actions
install -d ${STAGEDIR}/assets/css
install -d ${STAGEDIR}/assets/js
install -d ${STAGEDIR}/includes
install -d ${STAGEDIR}/locale/ja_JP/LC_MESSAGES
install -d ${STAGEDIR}/locale/en_US/LC_MESSAGES
install -d ${STAGEDIR}/views

install -m 644 ${SRCDIR}/manifest.json                                          ${STAGEDIR}/
install -m 644 ${SRCDIR}/Widget.php                                             ${STAGEDIR}/
install -m 644 ${SRCDIR}/actions/WidgetView.php                                 ${STAGEDIR}/actions/
install -m 644 ${SRCDIR}/assets/css/widget.css                                  ${STAGEDIR}/assets/css/
install -m 644 ${SRCDIR}/assets/js/class.widget.js                              ${STAGEDIR}/assets/js/
install -m 644 ${SRCDIR}/includes/WidgetForm.php                                ${STAGEDIR}/includes/
install -m 644 ${SRCDIR}/includes/helpers.php                                   ${STAGEDIR}/includes/
install -m 644 ${SRCDIR}/locale/ja_JP/LC_MESSAGES/tree-navigator.po            ${STAGEDIR}/locale/ja_JP/LC_MESSAGES/
install -m 644 ${SRCDIR}/locale/ja_JP/LC_MESSAGES/tree-navigator.mo            ${STAGEDIR}/locale/ja_JP/LC_MESSAGES/
install -m 644 ${SRCDIR}/locale/en_US/LC_MESSAGES/tree-navigator.po            ${STAGEDIR}/locale/en_US/LC_MESSAGES/
install -m 644 ${SRCDIR}/locale/en_US/LC_MESSAGES/tree-navigator.mo            ${STAGEDIR}/locale/en_US/LC_MESSAGES/
install -m 644 ${SRCDIR}/views/widget.edit.php                                  ${STAGEDIR}/views/
install -m 644 ${SRCDIR}/views/widget.view.php                                  ${STAGEDIR}/views/

%files
/usr/share/zabbix-widget-tree-navigator/

%post
if [ -d /usr/share/zabbix/ui/modules ]; then
    ZBXMODDIR=/usr/share/zabbix/ui/modules
elif [ -d /usr/share/zabbix/modules ]; then
    ZBXMODDIR=/usr/share/zabbix/modules
else
    echo "Warning: Zabbix modules directory not found. Skipping module installation." >&2
    exit 0
fi

SRCSTAGE=/usr/share/zabbix-widget-tree-navigator
MODDIR=${ZBXMODDIR}/tree-navigator

mkdir -p "${MODDIR}/actions" "${MODDIR}/assets/css" "${MODDIR}/assets/js" \
         "${MODDIR}/includes" \
         "${MODDIR}/locale/ja_JP/LC_MESSAGES" \
         "${MODDIR}/locale/en_US/LC_MESSAGES" \
         "${MODDIR}/views"

cp -rp "${SRCSTAGE}/." "${MODDIR}/"

%preun
if [ $1 -eq 0 ]; then
    rm -rf /usr/share/zabbix/ui/modules/tree-navigator 2>/dev/null || true
    rm -rf /usr/share/zabbix/modules/tree-navigator 2>/dev/null || true
fi

%changelog
* Mon Apr 27 2026 claude <noreply> - 1.0.0-1
- 初回リリース
- 設定可能なルート名を先頭に表示（デフォルト: Zabbix）
- ディレクトリツリー形式でホストグループ・ホストを表示
- ホストグループのみ / ホストグループ＋ホスト の2表示モード
- ホストグループフィルター（複数指定可、未指定時は全グループ表示）
- サブグループ再帰モード（親選択時に子グループIDも一括ブロードキャスト）
- ＋/－ボタンでツリー折りたたみ、展開状態をlocalStorageで保持
- CSSガイドラインによるツリー接続線表示（途切れなし）
- ホストはホストグループより一段右に表示
- フォルダアイコンホバーで下位グループを含む合計ホスト数をツールチップ表示
- ホストアイコンクリックでZabbixホストコンテキストメニュー表示
- OS種別アイコン（server / linux / windows / network / virtual）
- 日本語・英語ロケール対応
