%define _rpmfilename %%{NAME}-%%{VERSION}.%%{ARCH}.rpm
Name:           zabbix-widget-tree-navigator
Version:        1.4.12
Release:        0
Summary:        Tree Navigator widget for Zabbix dashboard
License:        MIT
BuildArch:      noarch

%description
Zabbix dashboard widget that displays host groups and hosts as a collapsible
directory tree.

Features:
- Configurable root node name displayed at the top of the tree
- Directory-tree style display: host groups as folders, hosts as files
- Two display modes: host groups only / host groups and hosts
- Configurable host group filter (multiple groups supported)
- Single group selection broadcasts the selected group and all descendant group IDs
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
- "Reset to initial view" toolbar button: restores the tree's expand/collapse
  state to the configured Initial depth, discarding the remembered per-user
  state without explicitly resetting the search bar, search query, selection,
  or scroll position
- Japanese and English locale support

%prep
# nothing

%install
SRCDIR=%{_sourcedir}/zabbix-widget-tree-navigator
STAGEDIR=%{buildroot}/usr/share/zabbix-widget-tree-navigator
LICENSEDIR=%{buildroot}%{_licensedir}/%{name}

install -d ${LICENSEDIR}
install -m 644 ${SRCDIR}/LICENSE                                                ${LICENSEDIR}/

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
install -m 644 ${SRCDIR}/locale/ja_JP/LC_MESSAGES/holoztek-tree-navigator.po   ${STAGEDIR}/locale/ja_JP/LC_MESSAGES/
install -m 644 ${SRCDIR}/locale/ja_JP/LC_MESSAGES/holoztek-tree-navigator.mo   ${STAGEDIR}/locale/ja_JP/LC_MESSAGES/
install -m 644 ${SRCDIR}/locale/en_US/LC_MESSAGES/holoztek-tree-navigator.po   ${STAGEDIR}/locale/en_US/LC_MESSAGES/
install -m 644 ${SRCDIR}/locale/en_US/LC_MESSAGES/holoztek-tree-navigator.mo   ${STAGEDIR}/locale/en_US/LC_MESSAGES/
install -m 644 ${SRCDIR}/views/widget.edit.js.php                               ${STAGEDIR}/views/
install -m 644 ${SRCDIR}/views/widget.edit.php                                  ${STAGEDIR}/views/
install -m 644 ${SRCDIR}/views/widget.view.php                                  ${STAGEDIR}/views/

%files
%license %{_licensedir}/%{name}/LICENSE
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
MODDIR=${ZBXMODDIR}/holoztek_tree_navigator
OLDMODDIR=${ZBXMODDIR}/tree-navigator

# 自パッケージ専有のディレクトリなので無条件で置き換える
rm -rf "${MODDIR}"
mkdir -p "${MODDIR}"
cp -rp "${SRCSTAGE}/." "${MODDIR}/"

# v1.4.8以前は modules/tree-navigator という汎用的すぎる名前を使っていたため、
# 別ベンダーのモジュールが同名ディレクトリを先に使っている可能性がある。
# 自動削除は「author が HOLOZTEK と明記されている」または「id が既に
# holoztek_tree_navigator（新形式、当パッケージ以外が書く可能性は実質無い）」
# の場合のみに限定する。旧形式id(tree-navigator)かつauthor欄なしのケース
# （v1.4.0のHOLOZTEK製と、authorを書いていない別ベンダー製が区別不能）は
# 自動削除せず警告のみとし、手動確認・削除を促す。
if [ -f "${OLDMODDIR}/manifest.json" ]; then
    ID_VAL=$(grep -Eo '"id"[[:space:]]*:[[:space:]]*"[^"]*"' "${OLDMODDIR}/manifest.json" | head -1 | sed -E 's/.*:[[:space:]]*"([^"]*)"/\1/')
    AUTHOR_VAL=$(grep -Eo '"author"[[:space:]]*:[[:space:]]*"[^"]*"' "${OLDMODDIR}/manifest.json" | head -1 | sed -E 's/.*:[[:space:]]*"([^"]*)"/\1/')
    AUTO_OK=0
    if [ "${AUTHOR_VAL}" = "HOLOZTEK" ] || [ "${ID_VAL}" = "holoztek_tree_navigator" ]; then
        AUTO_OK=1
    fi
    if [ "${AUTO_OK}" -eq 1 ]; then
        rm -rf "${OLDMODDIR}"
    else
        echo "Warning: ${OLDMODDIR} exists (id=${ID_VAL:-unknown}, author=${AUTHOR_VAL:-unset}) but could not be confirmed as a HOLOZTEK tree-navigator install. Leaving it in place; please verify manually and remove it yourself if appropriate. It may instead belong to a different vendor's module." >&2
    fi
fi

%preun
if [ $1 -eq 0 ]; then
    rm -rf /usr/share/zabbix/ui/modules/holoztek_tree_navigator 2>/dev/null || true
    rm -rf /usr/share/zabbix/modules/holoztek_tree_navigator 2>/dev/null || true
fi

%changelog
* Sat Aug 22 2026 HOLOZTEK <ttake-55@users.noreply.github.com> - 1.4.12-0
- コードレビュー指摘対応（issue #9、2点）: 「初期表示に戻す」ボタンが
  リセット後の状態をlocalStorageへ再保存していたため、ウィジェット設定の
  Initial depthを変更しても次回描画時に反映されない不具合を修正。
  内部処理では resetToInitialView() で saveOpenState() を呼ばず、
  localStorageの対象キーをremoveItem()で削除するよう変更
- v1.4.8エントリの見出し表記を「コードレビュー指摘対応（5点）」から
  実際の項目数に合わせ「コードレビュー指摘対応（6点）」へ修正

* Sat Aug 22 2026 HOLOZTEK <ttake-55@users.noreply.github.com> - 1.4.11-0
- 機能追加: ツールバーに「初期表示に戻す」ボタンを追加。クリックすると
  ツリーの開閉状態を Initial depth 設定に基づく初期状態にリセットし、
  リセット後の状態を通常の開閉操作と同様にlocalStorageへ即時保存する
  （#restoreOpenState()の初期展開ロジックを#applyInitialDepth()として
  共通化し、新規リセット処理と共有）
- リセット対象はツリーの開閉状態のみ。検索バーの表示・検索語・選択状態・
  スクロール位置の明示的なリセットは行わない
- パッケージメタデータ修正: debian/copyrightのSourceを公開GitHub
  リポジトリURLへ変更、manifest.jsonにurlフィールドを追加、
  メンテナー表記をHOLOZTEK <ttake-55@users.noreply.github.com>へ変更

* Tue Aug 11 2026 HOLOZTEK <ttake-55@users.noreply.github.com> - 1.4.10-0
- 【高】v1.4.9で追加した旧ディレクトリ自動削除の安全確認ロジックが
  不十分だった不具合を修正。旧ロジックは author欄が空の場合も
  無条件でHOLOZTEK由来と判定していたため、authorを書いていない
  別ベンダーのtree-navigatorモジュール（旧id: tree-navigator）を
  誤って削除しうる状態だった。修正後は「author=="HOLOZTEK"」または
  「id=="holoztek_tree_navigator"（新形式、自パッケージ以外が書く
  可能性は実質無い）」の場合のみ自動削除し、旧id・author空欄の
  ケース（v1.4.0のHOLOZTEK製自身と区別不能）は自動削除せず警告のみ
  として手動確認・削除を促す方式に変更（%post）。

* Mon Aug 10 2026 HOLOZTEK <ttake-55@users.noreply.github.com> - 1.4.9-0
- コードレビュー指摘対応（3点）:
  1. 【高】実体のモジュール配置ディレクトリ (modules/tree-navigator) が
     依然として汎用的すぎる名前のままで、他ベンダーのモジュールとの
     ファイルシステム上の衝突リスクが残っていた不具合を修正。配置先を
     modules/holoztek_tree_navigator へ変更（manifest.idは既に
     holoztek_tree_navigatorのため、dashboard widget typeの再変更は不要）。
     %post/%preunのMODDIRを新パスへ変更し、旧ディレクトリ
     (modules/tree-navigator) は無条件rm -rfせず、manifest.jsonのid
     （tree-navigatorまたはholoztek_tree_navigator）とauthor（未設定または
     "HOLOZTEK"）を確認した上でHOLOZTEK由来と判定できた場合のみ削除する
     安全確認ロジックを%postへ追加。DEB側はpostinstに旧ディレクトリの
     安全判定を追加し、prermは新しいholoztek_tree_navigator配置先へ追従
  2. %descriptionの「Sub-group recursive mode: selecting a parent
     broadcasts all descendant group IDs」という説明が、Include
     sub-groups設定（表示上の自動展開のみを制御）とシングル選択時の
     子孫ID配信（設定に関わらず常時実行）を結び付けて読めてしまう
     曖昧さがあった不具合を修正。READMEの正確な説明に合わせ「Single
     group selection broadcasts the selected group and all descendant
     group IDs」へ簡略化
  3. バージョン番号がmanifest.json/README/RPM spec/debian/changelogなど
     複数箇所へ手作業で埋め込まれており、過去にREADMEのバージョン表記
     修正漏れが発生した実績があったため、scripts/check-version-consistency.sh
     を追加しリリース前に各ファイルのバージョン一致を検査できるようにした。
     また、Gitea側のリリース一覧と重複するREADME末尾の「## バージョン」
     セクションを削除

* Mon Aug 10 2026 HOLOZTEK <ttake-55@users.noreply.github.com> - 1.4.8-0
- コードレビュー指摘対応（6点）:
  1. READMEのバージョン表記がv1.4.6のままだったのをv1.4.7へ修正漏れがあった
     不具合を修正（本リリースのバージョンに追随する形でv1.4.8表記に更新）
  2. 旧ID（tree-navigator）からのアップグレード手順をREADMEに追加。モジュール
     再スキャン・再有効化、既存/テンプレートダッシュボードのウィジェットtype
     更新方法（widgetid/fields/referenceは変更不要）を明記
  3. グローバル関数 _tn() を _holoztek_tn() へ変更し、他モジュールとの再宣言
     衝突リスクを解消。Widget.php/includes/WidgetForm.php/views/widget.edit.php/
     views/widget.view.php の呼び出し元も追随
  4. gettextドメインを tree-navigator から holoztek-tree-navigator へ変更
     （bindtextdomain/bind_textdomain_codeset/dgettextを統一）。.po/.moファイル名
     もholoztek-tree-navigator.po/.moへリネームし、RPM/DEBの配置定義も追随
  5. 設定画面のJSグローバル window.widget_tree_navigator_form を
     window.holoztek_tree_navigator_form へ変更し、widget.edit.phpの初期化
     呼び出しも追随
  6. ツールチップのグローバルCSSクラス .tree-navigator-tooltip を
     .holoztek-tree-navigator-tooltip へ変更し、class.widget.jsの生成側も追随
- RPM/DEBパッケージ名・Giteaリポジトリ名・モジュール配置ディレクトリ
  (tree-navigator) は互換性維持のため据え置き。manifest.id・PHP名前空間・
  アクション名・JSウィジェットクラス・CSSのウィジェットスコープは既に新IDで
  統一済みのため対象外（コード全体への機械的一括置換は行っていない）

* Mon Aug 10 2026 HOLOZTEK <ttake-55@users.noreply.github.com> - 1.4.7-0
- コードレビュー指摘対応（2点）:
  1. RPMにMITライセンス文書が同梱されていなかった不具合を修正。LICENSEを
     %%{_licensedir}/%%{name}/LICENSE へインストールし、%%files に %%license
     ディレクティブで登録（DEB側は元々debian/copyrightで同梱済みだった）
  2. READMEがv1.4.0時点の内容のまま更新されていなかった不具合を修正。
     最新バージョン表記をv1.4.7に更新、v1.3.2で追加したフォルダ/ホスト文字色
     設定項目を設定項目一覧に追加、DEBインストール手順を追加

* Mon Aug 10 2026 HOLOZTEK <ttake-55@users.noreply.github.com> - 1.4.6-0
- 不具合修正: v1.4.5でトグルボタンへの突き刺さりを解消した際、開閉トグルの
  無いグループ（子要素を持たない葉ノード）で今度は接続線がフォルダアイコン
  まで届かず途切れて見えるようになった。トグルの有無でアイコンまでの距離
  が異なる（トグルは実体のあるボーダー付きボックス、非トグル時はプレース
  ホルダーのみで見た目上の障害物が無い）ことを考慮していなかった
- assets/css/widget.css に :has() セレクタを追加し、実際にトグルボタン
  （.tn-toggle）を持つグループ行のみ width: 15px（トグル手前で停止）、
  トグルの無い葉グループは width: 26px（フォルダアイコン手前まで到達）と
  ケースごとに接続線の長さを分岐

* Mon Aug 10 2026 HOLOZTEK <ttake-55@users.noreply.github.com> - 1.4.5-0
- 不具合修正: v1.4.4の修正でホストグループ行の接続線が伸びすぎ、開閉トグル
  （+/-）ボタンの枠に線が突き刺さって見える不具合を修正。実測の結果、
  トグルボタンの左端手前で線が止まるべきところ、線幅26pxはトグルの箱
  （幅14px、開始位置22px）の内側まで入り込んでいた
- assets/css/widget.css の .tn-children > .tn-group::after の width を
  26pxから15pxに修正（トグル左端の1px手前で止まり、ホスト行の接続線と
  同様に自然に接続して見えるよう調整。ヘッドレスブラウザでの実測値に基づく）

* Mon Aug 10 2026 HOLOZTEK <ttake-55@users.noreply.github.com> - 1.4.4-0
- 不具合修正: ホストグループ（フォルダ）行のツリー接続線がアイコン手前で途切れて
  見える不具合を修正。グループ行には開閉トグルボタン（+/-、幅14px）が常に付くが、
  接続線の長さはトグルが無いホスト行と同じ想定で計算されており、トグル分の幅を
  考慮していなかったため、根元の縦線からアイコンまでの横線が大きく短すぎた
- assets/css/widget.css に .tn-children > .tn-group::after のグループ専用ルール
  （width: 26px）を追加し、ホスト用ルール（23px）と同様にトグル幅を考慮した長さに調整

* Mon Aug 10 2026 HOLOZTEK <ttake-55@users.noreply.github.com> - 1.4.3-0
- 不具合修正: v1.4.1のモジュール識別子リネーム（id: tree-navigator →
  holoztek_tree_navigator）により、Zabbixコアが付与するウィジェットコンテナの
  CSSクラスが dashboard-widget-tree-navigator から
  dashboard-widget-holoztek_tree_navigator に変わったが、widget.css側の
  スコープセレクタを追随させていなかったため、170/171でフォルダ・ホストタイプ
  アイコン等ウィジェット内の装飾が一切表示されなくなっていた
- assets/css/widget.css内の .dashboard-widget-tree-navigator スコープ
  セレクタ（67箇所）を .dashboard-widget-holoztek_tree_navigator に一括修正

* Mon Aug 10 2026 HOLOZTEK <ttake-55@users.noreply.github.com> - 1.4.2-0
- manifest.jsonに author（HOLOZTEK）・description（英語1行説明）を追加。
  Zabbixモジュールマニフェストの任意メタデータ欠落を指摘され対応

* Mon Aug 10 2026 HOLOZTEK <ttake-55@users.noreply.github.com> - 1.4.1-0
- Giteaコードレビュー指摘対応: モジュール識別子（id/namespace/action/js_class）が
  一般的すぎて他ベンダーのモジュールと将来衝突しうるとの指摘を受け、HOLOZTEK
  プレフィックスを付与
  1. manifest.jsonの id を tree-navigator から holoztek_tree_navigator へ変更
  2. namespace を TreeNavigator から HoloztekTreeNavigator へ変更（Widget.php・
     includes/WidgetForm.php・actions/WidgetView.phpのnamespace宣言も追随）
  3. action を widget.tree-navigator.view から widget.holoztek_tree_navigator.view
     へ変更
  4. JSクラス名を CWidgetTreeNavigator から CWidgetHoloztekTreeNavigator へ変更
     （同一ダッシュボード内でJS実行コンテキストを共有するため、js_classの衝突が
     最も実害が出やすいと判断し対象に含めた）
- モジュールディレクトリ名(tree-navigator)・gettextドメイン・RPM/DEBパッケージ名・
  Giteaリポジトリ名は変更なし（Zabbixのモジュールレジストリ内部の識別子のみが
  対象のため）
- 既存の配置済みウィジェット（170/171/174、計23件）はZabbix API(dashboard.update)
  でtypeフィールドのみ新IDへ書き換え、表示設定はそのまま引き継ぎ

* Sun Aug 09 2026 HOLOZTEK <ttake-55@users.noreply.github.com> - 1.4.0-0
- 機能変更なし。リリース工程の変更のみ反映：
  1. RPMをel9/el10個別ビルドから単一noarchファイルに統一（_rpmfilenameから
     %%{dist}を除去）。BuildArch: noarchでコンパイル済みバイナリを含まない
     ため、170/171どちらでビルドしても同一内容
  2. Debianパッケージング(.deb)をdebian/配下に追加（v1.3.3で試験導入済み）

* Sat Aug 08 2026 HOLOZTEK <ttake-55@users.noreply.github.com> - 1.3.3-0
- コードレビュー issue #4 対応: RPMの%%installに views/widget.edit.js.php の配置が
  抜けており、v1.3.2のel9/el10 RPMいずれにも同ファイルが含まれていなかった不具合を
  修正。設定画面でwidget_tree_navigator_formが未定義となりカラーピッカー初期化
  （フォルダ文字色・ホスト文字色）が動作しない可能性があった

* Sat Aug 08 2026 HOLOZTEK <ttake-55@users.noreply.github.com> - 1.3.2-0
- フォルダ文字色（folder_font_color）・ホスト文字色（host_font_color）を設定画面から
  個別に指定できるように追加。CWidgetFieldColorで2フィールドを新設し、CSSカスタム
  プロパティ（--tn-folder-color / --tn-host-color）としてサーバー側でウィジェット
  ラッパーに注入。ルートの「Server」ラベルにもフォルダ文字色を適用
- 設定画面のカラーピッカーUI初期化用にwidget.edit.js.phpを新規追加
- manifest.jsonのバージョン表記ずれ（デプロイ済み1.3.0 vs 実体1.3.1相当）を本リリースで解消

* Sat Jul 18 2026 HOLOZTEK <ttake-55@users.noreply.github.com> - 1.3.1-0
- v1.3.0コードレビュー対応（Issue #3）2点
  1. 同一ホストが複数グループに属する場合、片方のチェックボックスを操作しても
     同じhostidを持つ他のチェックボックス表示が同期しない不具合を修正。
     #onCheckboxToggle()で状態更新後に#applyMultiSelection()を呼び、
     同一id・複数箇所のチェックボックス表示を内部Set・broadcast内容と一致させる
  2. manifest.jsonのwidget.outに_hostidsを追加し、_hostid/_hostidsを常に同じ
     内容（シングル選択時は[選択ホストID]、マルチ選択時はチェック済み全ホストID、
     未選択・モード切替時は空配列）で配信するよう修正。標準の複数ホスト入力
     _hostidsを参照するウィジェットとも連携可能に

* Fri Jul 17 2026 HOLOZTEK <ttake-55@users.noreply.github.com> - 1.3.0-0
- ホスト・ホストグループのマルチセレクトに対応。ツールバーにシングル/マルチ選択切替
  ボタンを追加し、マルチ選択時はホスト・ホストグループのアイコン左側にチェックボック
  スを表示。チェックしたホスト/グループのID（グループはそのグループ自身のIDのみ、子孫
  展開なし）を変更の都度即時ブロードキャスト。ホスト・グループのチェックは混在可能
  で親子の連動はなし（独立）。モード切替時は選択をクリアし空配列を配信
- シングル選択時の動作（recursive設定に基づく子孫ノード展開・全階層ベースの
  _hostgroupids配信等）は従来どおり変更なし

* Mon Jul 13 2026 HOLOZTEK <ttake-55@users.noreply.github.com> - 1.2.4-0
- Issue #1 対応：検索バー開時にウィジェット再描画（データ更新）してもドロップダウン候補が
  正しく復元されるよう#syncSearchUI()から#renderDropdown()を呼ぶよう修正
- グループ選択時のブロードキャストを recursive 設定から分離：_hostgroupid は常に選択した
  単一グループのみ、_hostgroupids は recursive の ON/OFF に関わらずZabbix全体の階層に対する
  実際の子孫グループ全てを配信するよう修正（表示フィルターで隠れているグループも含む）。
  recursive設定は子孫ノードの自動展開（表示上の利便性）のみを制御する
- README：検索機能の説明を「候補表示と該当ホストへのジャンプ」に修正（実装と不一致だった
  「フィルタリング」表現を訂正）

* Mon Jul 13 2026 HOLOZTEK <ttake-55@users.noreply.github.com> - 1.2.3-0
- ホスト選択時に親グループID（_hostgroupid）を配信しないよう修正（空配列で明示的に
  クリア）。groupids/hostidsをOR（合算）で扱う受信側ウィジェット（radar-chart等）で、
  ホストを1件選択したはずが親グループ全体が表示されてしまう不具合を修正
- 未使用となったdata-parent-groupid属性を削除

* Thu Jun 11 2026 HOLOZTEK <ttake-55@users.noreply.github.com> - 1.2.2-0
- RPM %postのmkdir -p個別サブディレクトリ作成を削除し、rm -rf → mkdir -p "${MODDIR}" → cp -rp の順序に整理
- #onDropdownClick()のindex上限チェックを追加（idx < this.#search_results.length）

* Thu Jun 11 2026 HOLOZTEK <ttake-55@users.noreply.github.com> - 1.2.1-0
- ドロップダウン選択をhostid依存からresult index依存に変更（同一hostidの複数候補が正しくジャンプするよう修正）
- 検索バーを閉じたときにinput.valueもクリアするよう修正
- 検索UI・ツールチップ文言をローカライズ（_tn()使用、JS用ラベルはdata-*属性経由）
- show_mode=0（ホストグループのみ）のとき検索UIを非表示に変更
- fields_values['groupids']の参照を??演算子で防御的に変更
- RPM %postで旧モジュールディレクトリをrm -rfしてから再インストールするよう変更

* Thu Jun 11 2026 HOLOZTEK <ttake-55@users.noreply.github.com> - 1.2.0-0
- ホスト名部分一致検索ボックスを追加（ツリー上部の虫眼鏡ボタンで表示・非表示切替）
- 入力中にドロップダウン候補リストを表示（最大15件）
- 複数一致時は Next / Prev ボタンおよびEnterキーで順番にジャンプ
- 一致ホストへのジャンプ時に祖先グループを自動展開・選択してブロードキャスト

* Sat Jun 06 2026 HOLOZTEK <ttake-55@users.noreply.github.com> - 1.1.0-0
- initial_depthの説明文を「展開状態の保存がない場合の初期展開階層」に変更

* Sat Jun 06 2026 HOLOZTEK <ttake-55@users.noreply.github.com> - 1.0.2-0
- show_host_count=false時にフォルダのdata属性を付与せずツールチップを非表示に
- スクロール位置保存・復元を専用メソッドに分離（onClearContents/setContentsでも実施）
- イベントリスナーの二重登録対策を強化（null判定ガード・解除後にnullリセット）
- specファイルをpackaging/rpm配下に一本化（ルート直下のspec削除）
- specのLicenseをProprietaryに修正
- initial_depthにsetFieldHintで説明文を追加
- ツールチップCSSクラスをtree-navigator-tooltipに変更

* Fri Jun 05 2026 HOLOZTEK <ttake-55@users.noreply.github.com> - 1.0.1-0
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

* Mon Apr 27 2026 HOLOZTEK <ttake-55@users.noreply.github.com> - 1.0.0-1
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
