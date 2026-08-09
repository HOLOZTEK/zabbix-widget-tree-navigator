%define _rpmfilename %%{NAME}-%%{VERSION}.%%{ARCH}.rpm
Name:           zabbix-widget-tree-navigator
Version:        1.4.0
Release:        0
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
- Clicking a host name broadcasts _hostid + _hostids as [hostid] (clears any
  previously broadcast _hostgroupid)
- Clicking a host icon shows the Zabbix host context menu
- Single/multi-select toggle in the widget toolbar: multi-select mode shows
  checkboxes next to host and host group icons, broadcasting the checked
  hostids/groupids (_hostid + _hostids, _hostgroupid + _hostgroupids)
  immediately on every change; checkboxes for the same host/group id stay in
  sync even when the id appears more than once in the tree
- Japanese and English locale support

%prep
# nothing

%install
SRCDIR=%{_sourcedir}/zabbix-widget-tree-navigator
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
install -m 644 ${SRCDIR}/views/widget.edit.js.php                               ${STAGEDIR}/views/
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

rm -rf "${MODDIR}"
mkdir -p "${MODDIR}"
cp -rp "${SRCSTAGE}/." "${MODDIR}/"

%preun
if [ $1 -eq 0 ]; then
    rm -rf /usr/share/zabbix/ui/modules/tree-navigator 2>/dev/null || true
    rm -rf /usr/share/zabbix/modules/tree-navigator 2>/dev/null || true
fi

%changelog
* Sun Aug 09 2026 claude <noreply> - 1.4.0-0
- 機能変更なし。リリース工程の変更のみ反映：
  1. RPMをel9/el10個別ビルドから単一noarchファイルに統一（_rpmfilenameから
     %%{dist}を除去）。BuildArch: noarchでコンパイル済みバイナリを含まない
     ため、170/171どちらでビルドしても同一内容
  2. Debianパッケージング(.deb)をdebian/配下に追加（v1.3.3で試験導入済み）

* Sat Aug 08 2026 claude <noreply> - 1.3.3-0
- コードレビュー issue #4 対応: RPMの%%installに views/widget.edit.js.php の配置が
  抜けており、v1.3.2のel9/el10 RPMいずれにも同ファイルが含まれていなかった不具合を
  修正。設定画面でwidget_tree_navigator_formが未定義となりカラーピッカー初期化
  （フォルダ文字色・ホスト文字色）が動作しない可能性があった

* Sat Aug 08 2026 claude <noreply> - 1.3.2-0
- フォルダ文字色（folder_font_color）・ホスト文字色（host_font_color）を設定画面から
  個別に指定できるように追加。CWidgetFieldColorで2フィールドを新設し、CSSカスタム
  プロパティ（--tn-folder-color / --tn-host-color）としてサーバー側でウィジェット
  ラッパーに注入。ルートの「Server」ラベルにもフォルダ文字色を適用
- 設定画面のカラーピッカーUI初期化用にwidget.edit.js.phpを新規追加
- manifest.jsonのバージョン表記ずれ（デプロイ済み1.3.0 vs 実体1.3.1相当）を本リリースで解消

* Sat Jul 18 2026 claude <noreply> - 1.3.1-0
- v1.3.0コードレビュー対応（Issue #3）2点
  1. 同一ホストが複数グループに属する場合、片方のチェックボックスを操作しても
     同じhostidを持つ他のチェックボックス表示が同期しない不具合を修正。
     #onCheckboxToggle()で状態更新後に#applyMultiSelection()を呼び、
     同一id・複数箇所のチェックボックス表示を内部Set・broadcast内容と一致させる
  2. manifest.jsonのwidget.outに_hostidsを追加し、_hostid/_hostidsを常に同じ
     内容（シングル選択時は[選択ホストID]、マルチ選択時はチェック済み全ホストID、
     未選択・モード切替時は空配列）で配信するよう修正。標準の複数ホスト入力
     _hostidsを参照するウィジェットとも連携可能に

* Fri Jul 17 2026 claude <noreply> - 1.3.0-0
- ホスト・ホストグループのマルチセレクトに対応。ツールバーにシングル/マルチ選択切替
  ボタンを追加し、マルチ選択時はホスト・ホストグループのアイコン左側にチェックボック
  スを表示。チェックしたホスト/グループのID（グループはそのグループ自身のIDのみ、子孫
  展開なし）を変更の都度即時ブロードキャスト。ホスト・グループのチェックは混在可能
  で親子の連動はなし（独立）。モード切替時は選択をクリアし空配列を配信
- シングル選択時の動作（recursive設定に基づく子孫ノード展開・全階層ベースの
  _hostgroupids配信等）は従来どおり変更なし

* Mon Jul 13 2026 claude <noreply> - 1.2.4-0
- Issue #1 対応：検索バー開時にウィジェット再描画（データ更新）してもドロップダウン候補が
  正しく復元されるよう#syncSearchUI()から#renderDropdown()を呼ぶよう修正
- グループ選択時のブロードキャストを recursive 設定から分離：_hostgroupid は常に選択した
  単一グループのみ、_hostgroupids は recursive の ON/OFF に関わらずZabbix全体の階層に対する
  実際の子孫グループ全てを配信するよう修正（表示フィルターで隠れているグループも含む）。
  recursive設定は子孫ノードの自動展開（表示上の利便性）のみを制御する
- README：検索機能の説明を「候補表示と該当ホストへのジャンプ」に修正（実装と不一致だった
  「フィルタリング」表現を訂正）

* Mon Jul 13 2026 claude <noreply> - 1.2.3-0
- ホスト選択時に親グループID（_hostgroupid）を配信しないよう修正（空配列で明示的に
  クリア）。groupids/hostidsをOR（合算）で扱う受信側ウィジェット（radar-chart等）で、
  ホストを1件選択したはずが親グループ全体が表示されてしまう不具合を修正
- 未使用となったdata-parent-groupid属性を削除

* Wed Jun 11 2026 claude <noreply> - 1.2.2-0
- RPM %postのmkdir -p個別サブディレクトリ作成を削除し、rm -rf → mkdir -p "${MODDIR}" → cp -rp の順序に整理
- #onDropdownClick()のindex上限チェックを追加（idx < this.#search_results.length）

* Wed Jun 11 2026 claude <noreply> - 1.2.1-0
- ドロップダウン選択をhostid依存からresult index依存に変更（同一hostidの複数候補が正しくジャンプするよう修正）
- 検索バーを閉じたときにinput.valueもクリアするよう修正
- 検索UI・ツールチップ文言をローカライズ（_tn()使用、JS用ラベルはdata-*属性経由）
- show_mode=0（ホストグループのみ）のとき検索UIを非表示に変更
- fields_values['groupids']の参照を??演算子で防御的に変更
- RPM %postで旧モジュールディレクトリをrm -rfしてから再インストールするよう変更

* Wed Jun 11 2026 claude <noreply> - 1.2.0-0
- ホスト名部分一致検索ボックスを追加（ツリー上部の虫眼鏡ボタンで表示・非表示切替）
- 入力中にドロップダウン候補リストを表示（最大15件）
- 複数一致時は Next / Prev ボタンおよびEnterキーで順番にジャンプ
- 一致ホストへのジャンプ時に祖先グループを自動展開・選択してブロードキャスト

* Fri Jun 06 2026 claude <noreply> - 1.1.0-0
- initial_depthの説明文を「展開状態の保存がない場合の初期展開階層」に変更

* Fri Jun 06 2026 claude <noreply> - 1.0.2-0
- show_host_count=false時にフォルダのdata属性を付与せずツールチップを非表示に
- スクロール位置保存・復元を専用メソッドに分離（onClearContents/setContentsでも実施）
- イベントリスナーの二重登録対策を強化（null判定ガード・解除後にnullリセット）
- specファイルをpackaging/rpm配下に一本化（ルート直下のspec削除）
- specのLicenseをProprietaryに修正
- initial_depthにsetFieldHintで説明文を追加
- ツールチップCSSクラスをtree-navigator-tooltipに変更

* Thu Jun 05 2026 claude <noreply> - 1.0.1-0
- JSイベントリスナーの重複登録対策（バインド済みハンドラをフィールドに保持しonDeactivateで解除）
- スクロール位置保存・復元の対象を.tn-containerに修正
- Sub-groups有効時に選択グループの子孫グループも表示・ブロードキャスト対象に含めるよう修正
- CSSスコープをdiv.dashboard-widget-tree-navigator配下に変更
- .hm-iconなど汎用クラス名を.tn-host-type-iconに変更
- CSpanの自動エスケープに合わせhtmlspecialchars()の手動適用を削除
- recursive_host_countをhostidのユニーク数で計算（重複カウント解消）
- groupids_filterをstrvalで文字列正規化
- show_host_countフィールド追加（無効時はAPI::Host()->get()を省略）
- detectDeviceType()のinventory未定義時の警告対策（?? null）
- RPM spec の SRCDIR を zabbix-widget-tree-navigator に修正
- manifest.json / spec のバージョンを 1.0.1 に統一

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
