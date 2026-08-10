/*
 * Tree Navigator Widget
 *
 * Displays host groups and hosts as a collapsible directory tree.
 *
 * Single-select mode (default): clicking a group name broadcasts _hostgroupid
 * (the group alone) and _hostgroupids (the group plus all real descendant
 * groups across the full Zabbix-wide hierarchy, regardless of the "recursive"
 * display-filter setting). Clicking a host name broadcasts _hostid and
 * _hostids as [hostid] (clears any previously broadcast _hostgroupid, so a
 * single-host selection is not widened back out to its parent group by
 * widgets that OR groupids/hostids together).
 *
 * Multi-select mode: toggled via the checkbox-icon button in the widget
 * toolbar. Checkboxes appear next to every host/group icon; hosts and groups
 * can be checked in any combination. A host that belongs to multiple groups
 * gets one checkbox per occurrence in the tree; all of them are kept in sync
 * with the underlying Set on every toggle. _hostgroupid/_hostgroupids both
 * carry the set of checked groups' own IDs (no descendant expansion), and
 * _hostid/_hostids both carry the set of checked hosts. Every checkbox
 * change re-broadcasts immediately. Switching between single/multi mode
 * clears the current selection and broadcasts empty.
 *
 * Clicking a host icon shows the Zabbix host menu (data-menu-popup).
 * The search box filters hosts by partial name match with Next/Prev
 * navigation; in multi-select mode a match is only expanded to and scrolled
 * into view (it does not check its checkbox or broadcast).
 */

class CWidgetHoloztekTreeNavigator extends CWidget {

	/**
	 * Path of the currently selected group node, or null.
	 * @type {string|null}
	 */
	#selected_path = null;

	/**
	 * hostid of the currently selected host, or null.
	 * @type {string|null}
	 */
	#selected_hostid = null;

	/**
	 * Scroll position, preserved across refreshes.
	 * @type {number}
	 */
	#scroll_top = 0;

	/**
	 * Floating tooltip element for folder icon hover (appended to body).
	 * @type {HTMLElement|null}
	 */
	#tooltip = null;

	/** Bound event handler references for removeEventListener. */
	#_clickHandler      = null;
	#_mouseOverHandler  = null;
	#_mouseOutHandler   = null;
	#_searchInputHandler   = null;
	#_searchKeydownHandler = null;

	/** Whether the search bar is currently visible. */
	#search_open = false;

	/** Current search query string. */
	#search_query = '';

	/** All host label elements matching the current query (tree document order). */
	#search_results = [];

	/** Index of the currently highlighted match (-1 = none). */
	#search_index = -1;

	/** Whether multi-select mode is currently active. */
	#is_multi = false;

	/** groupids currently checked in multi-select mode. @type {Set<string>} */
	#checked_groupids = new Set();

	/** hostids currently checked in multi-select mode. @type {Set<string>} */
	#checked_hostids = new Set();

	/** localStorage key for persisting expanded node paths. */
	get #storageKey() {
		return 'tn_open_' + this._widgetid;
	}

	// ── Lifecycle ──────────────────────────────────────────────────────────────

	onActivate() {
		this.#restoreScrollPosition();

		if (this.#_clickHandler === null) {
			this.#_clickHandler        = this.#onClick.bind(this);
			this.#_mouseOverHandler    = this.#onMouseOver.bind(this);
			this.#_mouseOutHandler     = this.#onMouseOut.bind(this);
			this.#_searchInputHandler  = this.#onSearchInput.bind(this);
			this.#_searchKeydownHandler = this.#onSearchKeydown.bind(this);

			this._body.addEventListener('click',     this.#_clickHandler);
			this._body.addEventListener('mouseover', this.#_mouseOverHandler);
			this._body.addEventListener('mouseout',  this.#_mouseOutHandler);
			this._body.addEventListener('input',     this.#_searchInputHandler);
			this._body.addEventListener('keydown',   this.#_searchKeydownHandler);
		}
	}

	onDeactivate() {
		this.#saveScrollPosition();

		if (this.#_clickHandler !== null) {
			this._body.removeEventListener('click',     this.#_clickHandler);
			this._body.removeEventListener('mouseover', this.#_mouseOverHandler);
			this._body.removeEventListener('mouseout',  this.#_mouseOutHandler);
			this._body.removeEventListener('input',     this.#_searchInputHandler);
			this._body.removeEventListener('keydown',   this.#_searchKeydownHandler);

			this.#_clickHandler        = null;
			this.#_mouseOverHandler    = null;
			this.#_mouseOutHandler     = null;
			this.#_searchInputHandler  = null;
			this.#_searchKeydownHandler = null;
		}

		this.#hideTooltip();
	}

	onClearContents() {
		this.#saveScrollPosition();
		this.#hideTooltip();
	}

	setContents(response) {
		super.setContents(response);

		this.#restoreOpenState();
		this.#applyModeUI();
		this.#applyMultiSelection();
		this.#applySelection();
		this.#syncSearchUI();

		if (!this.#search_open || this.#search_index < 0) {
			this.#restoreScrollPosition();
		}

		// Auto-select first group when this widget's output is being referred to.
		if (!this.#is_multi && this.isReferred() && !this.hasEverUpdated()
				&& this.#selected_path === null && this.#selected_hostid === null) {
			this.#selectFirstGroup();
		}
	}

	onReferredUpdate() {
		if (!this.#is_multi && this.#selected_path === null && this.#selected_hostid === null) {
			this.#selectFirstGroup();
		}
	}

	hasPadding() {
		return false;
	}

	// ── Event handlers ─────────────────────────────────────────────────────────

	#onClick(e) {
		// Multi-select mode toggle button
		if (e.target.closest('.js-tn-mode-toggle')) {
			this.#onModeToggle();
			return;
		}

		// Multi-select checkbox
		const checkbox = e.target.closest('.js-tn-checkbox');

		if (checkbox) {
			this.#onCheckboxToggle(checkbox);
			return;
		}

		// Search toggle button
		if (e.target.closest('.js-tn-search-toggle')) {
			this.#onSearchToggle();
			return;
		}

		// Search clear button
		if (e.target.closest('.js-tn-search-clear')) {
			this.#onSearchClear();
			return;
		}

		// Search prev/next navigation buttons
		if (e.target.closest('.js-tn-search-prev')) {
			this.#onSearchPrev();
			return;
		}

		if (e.target.closest('.js-tn-search-next')) {
			this.#onSearchNext();
			return;
		}

		// Dropdown item click
		const dropdown = e.target.closest('.js-tn-search-dropdown');
		if (dropdown) {
			const item = e.target.closest('li');
			if (item && !item.classList.contains('tn-search-dropdown-more')) {
				this.#onDropdownClick(item);
			}
			return;
		}

		// Toggle expand/collapse
		const toggle = e.target.closest('.js-tn-toggle');

		if (toggle) {
			const li = toggle.closest('.tn-node.tn-group');

			if (li) {
				this.#toggleNode(li);
			}

			return;
		}

		// Host icon click → Zabbix data-menu-popup handler takes care of it
		if (e.target.closest('.js-tn-host-icon')) {
			return;
		}

		// Group label click (single-select mode only; multi-select uses checkboxes)
		const group_label = e.target.closest('.js-tn-group-label');

		if (group_label?.dataset.groupid) {
			if (!this.#is_multi) {
				this.#selectGroup(group_label);
			}
			return;
		}

		// Host label click (single-select mode only; multi-select uses checkboxes)
		const host_label = e.target.closest('.js-tn-host-label');

		if (host_label?.dataset.hostid) {
			if (!this.#is_multi) {
				this.#selectHost(host_label);
			}
		}
	}

	#onMouseOver(e) {
		const folder = e.target.closest('.js-tn-folder[data-recursive-host-count]');

		if (folder) {
			const count    = folder.dataset.recursiveHostCount;
			const template = this.#label('labelHostCount') || 'Hosts: {0}';
			this.#showTooltip(template.replace('{0}', count), folder);
		}
	}

	#onMouseOut(e) {
		if (!e.relatedTarget?.closest('.js-tn-folder')) {
			this.#hideTooltip();
		}
	}

	// ── Search ─────────────────────────────────────────────────────────────────

	#onSearchToggle() {
		this.#search_open = !this.#search_open;

		const bar = this._body.querySelector('.js-tn-search-bar');

		if (bar) {
			bar.style.display = this.#search_open ? 'block' : 'none';
		}

		if (this.#search_open) {
			this._body.querySelector('.js-tn-search-input')?.focus();
		}
		else {
			const input = this._body.querySelector('.js-tn-search-input');
			if (input) input.value = '';

			this.#search_query   = '';
			this.#search_results = [];
			this.#search_index   = -1;
			this.#clearDropdown();
			this.#updateSearchNav();
			this.#updateClearButton();
		}
	}

	#onSearchInput(e) {
		if (!e.target.closest('.js-tn-search-input')) return;

		this.#search_query   = e.target.value.trim();
		this.#search_index   = -1;
		this.#search_results = this.#buildSearchResults(this.#search_query);
		this.#renderDropdown();
		this.#updateSearchNav();
		this.#updateClearButton();
	}

	#onSearchClear() {
		const input = this._body.querySelector('.js-tn-search-input');
		if (input) input.value = '';

		this.#search_query   = '';
		this.#search_results = [];
		this.#search_index   = -1;
		this.#clearDropdown();
		this.#updateSearchNav();
		this.#updateClearButton();

		input?.focus();
	}

	#onSearchKeydown(e) {
		if (!e.target.closest('.js-tn-search-input')) return;

		if (e.key === 'Enter') {
			e.preventDefault();

			if (this.#search_results.length > 0) {
				const next = this.#search_index < 0
					? 0
					: (this.#search_index + 1) % this.#search_results.length;
				this.#jumpToMatch(next);
			}
		}
		else if (e.key === 'Escape') {
			e.preventDefault();
			this.#onSearchToggle();
		}
	}

	#onSearchPrev() {
		if (this.#search_results.length === 0) return;

		const prev = this.#search_index <= 0
			? this.#search_results.length - 1
			: this.#search_index - 1;
		this.#jumpToMatch(prev);
	}

	#onSearchNext() {
		if (this.#search_results.length === 0) return;

		const next = this.#search_index < 0
			? 0
			: (this.#search_index + 1) % this.#search_results.length;
		this.#jumpToMatch(next);
	}

	#onDropdownClick(item_el) {
		const idx = Number(item_el.dataset.resultIndex);

		if (Number.isInteger(idx) && idx >= 0 && idx < this.#search_results.length) {
			this.#jumpToMatch(idx);
		}

		this.#clearDropdown();
	}

	#buildSearchResults(query) {
		if (!query) return [];

		const lower = query.toLowerCase();

		return Array.from(
			this._body.querySelectorAll('.js-tn-host-label[data-hostid]')
		).filter(el => el.textContent.toLowerCase().includes(lower));
	}

	#renderDropdown() {
		const dropdown = this._body.querySelector('.js-tn-search-dropdown');
		if (!dropdown) return;

		dropdown.innerHTML = '';

		if (this.#search_results.length === 0) {
			dropdown.style.display = 'none';
			return;
		}

		const max = Math.min(this.#search_results.length, 15);

		for (let i = 0; i < max; i++) {
			const el = this.#search_results[i];
			const li = document.createElement('li');
			li.dataset.resultIndex = String(i);
			li.textContent         = el.textContent;

			if (i === this.#search_index) {
				li.classList.add('tn-search-dropdown-active');
			}

			dropdown.appendChild(li);
		}

		if (this.#search_results.length > max) {
			const more     = document.createElement('li');
			const template = this.#label('labelMoreResults') || 'and {0} more';
			more.className   = 'tn-search-dropdown-more';
			more.textContent = '… ' + template.replace('{0}', String(this.#search_results.length - max));
			dropdown.appendChild(more);
		}

		dropdown.style.display = '';
	}

	#clearDropdown() {
		const dropdown = this._body.querySelector('.js-tn-search-dropdown');

		if (dropdown) {
			dropdown.innerHTML    = '';
			dropdown.style.display = 'none';
		}
	}

	#updateClearButton() {
		const clear_btn = this._body.querySelector('.js-tn-search-clear');

		if (clear_btn) {
			clear_btn.style.display = this.#search_query ? 'flex' : 'none';
		}
	}

	#updateSearchNav() {
		const count_el = this._body.querySelector('.js-tn-search-count');
		const prev_btn = this._body.querySelector('.js-tn-search-prev');
		const next_btn = this._body.querySelector('.js-tn-search-next');
		const total    = this.#search_results.length;

		if (count_el) {
			if (total === 0) {
				count_el.textContent = this.#search_query ? '0 / 0' : '';
			}
			else {
				const pos = this.#search_index >= 0 ? this.#search_index + 1 : '-';
				count_el.textContent = `${pos} / ${total}`;
			}
		}

		const has_multi = total > 1;
		if (prev_btn) prev_btn.disabled = !has_multi;
		if (next_btn) next_btn.disabled = !has_multi;
	}

	#jumpToMatch(index) {
		if (index < 0 || index >= this.#search_results.length) return;

		this.#search_index = index;
		const label = this.#search_results[index];

		this.#expandAncestors(label);

		if (!this.#is_multi) {
			this.#selectHost(label);
		}

		label.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
		this.#updateSearchNav();
	}

	#expandAncestors(label_el) {
		let node = label_el.parentElement;

		while (node) {
			const group = node.closest('.tn-node.tn-group');
			if (!group) break;
			group.classList.add('tn-open');
			node = group.parentElement;
		}

		this.#saveOpenState();
	}

	#syncSearchUI() {
		const bar = this._body.querySelector('.js-tn-search-bar');

		if (bar) {
			bar.style.display = this.#search_open ? 'block' : 'none';
		}

		if (!this.#search_open || !this.#search_query) return;

		const input = this._body.querySelector('.js-tn-search-input');
		if (input) input.value = this.#search_query;

		this.#search_results = this.#buildSearchResults(this.#search_query);

		if (this.#search_index >= this.#search_results.length) {
			this.#search_index = this.#search_results.length - 1;
		}

		if (this.#search_index >= 0) {
			this.#expandAncestors(this.#search_results[this.#search_index]);
		}

		this.#renderDropdown();
		this.#updateSearchNav();
		this.#updateClearButton();
	}

	// ── Tree interaction ───────────────────────────────────────────────────────

	#toggleNode(li) {
		li.classList.toggle('tn-open');
		this.#saveOpenState();
	}

	#selectGroup(label) {
		const groupid       = label.dataset.groupid;
		const is_recursive   = this.#isRecursive();

		// _hostgroupids always carries the selected group plus every real descendant
		// group across the full Zabbix-wide hierarchy (data-child-groupids), regardless
		// of the "recursive" display filter setting. "recursive" only controls whether
		// the tree auto-expands descendant nodes below, a display-only convenience.
		const broadcast_groupids = (label.dataset.childGroupids || groupid).split(',').filter(Boolean);

		if (is_recursive) {
			// Expand the selected node and all its descendants
			const li = label.closest('.tn-node.tn-group');

			if (li) {
				li.classList.add('tn-open');

				for (const desc of li.querySelectorAll('.tn-node.tn-group')) {
					desc.classList.add('tn-open');
				}

				this.#saveOpenState();
			}
		}

		this.#selected_hostid = null;
		this.#selected_path   = label.closest('.tn-node')?.dataset.path ?? null;

		this.#applySelection();

		this.broadcast({
			[CWidgetsData.DATA_TYPE_HOST_GROUP_ID]:  [groupid],
			[CWidgetsData.DATA_TYPE_HOST_GROUP_IDS]: broadcast_groupids,
			[CWidgetsData.DATA_TYPE_HOST_ID]:        [],
			[CWidgetsData.DATA_TYPE_HOST_IDS]:       []
		});
	}

	#selectHost(label) {
		const hostid          = label.dataset.hostid;

		this.#selected_path   = null;
		this.#selected_hostid = hostid;

		this.#applySelection();

		// 親groupidは配信しない。groupids/hostidsをOR（合算）で扱う受信側ウィジェット
		// （radar-chart等）で、単一ホスト選択のはずが親グループ全体が表示されてしまう
		// 不具合を防ぐため、_hostgroupidは空配列で明示的にクリアする。
		this.broadcast({
			[CWidgetsData.DATA_TYPE_HOST_GROUP_ID]:  [],
			[CWidgetsData.DATA_TYPE_HOST_GROUP_IDS]: [],
			[CWidgetsData.DATA_TYPE_HOST_ID]:        [hostid],
			[CWidgetsData.DATA_TYPE_HOST_IDS]:       [hostid]
		});
	}

	#selectFirstGroup() {
		const first = this._body.querySelector('.js-tn-group-label[data-groupid]');

		if (first) {
			this.#selectGroup(first);
		}
	}

	// ── Multi-select mode ──────────────────────────────────────────────────────

	#onModeToggle() {
		this.#is_multi = !this.#is_multi;

		this.#checked_groupids.clear();
		this.#checked_hostids.clear();
		this.#selected_path   = null;
		this.#selected_hostid = null;

		this.#applyModeUI();
		this.#applyMultiSelection();
		this.#applySelection();

		this.broadcast({
			[CWidgetsData.DATA_TYPE_HOST_GROUP_ID]:  [],
			[CWidgetsData.DATA_TYPE_HOST_GROUP_IDS]: [],
			[CWidgetsData.DATA_TYPE_HOST_ID]:        [],
			[CWidgetsData.DATA_TYPE_HOST_IDS]:       []
		});
	}

	#onCheckboxToggle(checkbox) {
		if (checkbox.classList.contains('js-tn-group-checkbox')) {
			const groupid = checkbox.dataset.groupid;

			if (checkbox.checked) {
				this.#checked_groupids.add(groupid);
			}
			else {
				this.#checked_groupids.delete(groupid);
			}
		}
		else if (checkbox.classList.contains('js-tn-host-checkbox')) {
			const hostid = checkbox.dataset.hostid;

			if (checkbox.checked) {
				this.#checked_hostids.add(hostid);
			}
			else {
				this.#checked_hostids.delete(hostid);
			}
		}

		// A host can appear under multiple groups, so the same hostid may have more
		// than one checkbox in the tree; re-sync all of them against the Set state
		// to keep display and broadcast content consistent.
		this.#applyMultiSelection();

		this.#broadcastMultiSelection();
	}

	#broadcastMultiSelection() {
		const groupids = Array.from(this.#checked_groupids);
		const hostids   = Array.from(this.#checked_hostids);

		this.broadcast({
			[CWidgetsData.DATA_TYPE_HOST_GROUP_ID]:  groupids,
			[CWidgetsData.DATA_TYPE_HOST_GROUP_IDS]: groupids,
			[CWidgetsData.DATA_TYPE_HOST_ID]:        hostids,
			[CWidgetsData.DATA_TYPE_HOST_IDS]:       hostids
		});
	}

	#applyModeUI() {
		const container = this._body.querySelector('.tn-container');

		if (container) {
			container.classList.toggle('tn-multi-mode', this.#is_multi);
		}

		const toggle_btn = this._body.querySelector('.js-tn-mode-toggle');

		if (toggle_btn) {
			toggle_btn.classList.toggle('tn-active', this.#is_multi);
			toggle_btn.title = this.#is_multi
				? (this.#label('labelMultiOn')  || 'Switch to single-select')
				: (this.#label('labelMultiOff') || 'Switch to multi-select');
		}
	}

	#applyMultiSelection() {
		for (const cb of this._body.querySelectorAll('.js-tn-group-checkbox')) {
			cb.checked = this.#checked_groupids.has(cb.dataset.groupid);
		}

		for (const cb of this._body.querySelectorAll('.js-tn-host-checkbox')) {
			cb.checked = this.#checked_hostids.has(cb.dataset.hostid);
		}
	}

	// ── Selection display ──────────────────────────────────────────────────────

	#applySelection() {
		for (const el of this._body.querySelectorAll('.tn-selected')) {
			el.classList.remove('tn-selected');
		}

		if (this.#selected_path !== null) {
			const li = this._body.querySelector(
				`.tn-node[data-path="${CSS.escape(this.#selected_path)}"]`
			);
			li?.querySelector('.tn-group-label')?.classList.add('tn-selected');
		}

		if (this.#selected_hostid !== null) {
			const labels = this._body.querySelectorAll(
				`.tn-host-label[data-hostid="${this.#selected_hostid}"]`
			);

			for (const lbl of labels) {
				lbl.classList.add('tn-selected');
			}
		}
	}

	// ── Open state persistence ─────────────────────────────────────────────────

	#restoreOpenState() {
		// Close all group nodes first
		for (const li of this._body.querySelectorAll('.tn-node.tn-group')) {
			li.classList.remove('tn-open');
		}

		let open_paths = null;

		try {
			const stored = localStorage.getItem(this.#storageKey);

			if (stored !== null) {
				open_paths = new Set(JSON.parse(stored));
			}
		}
		catch (_) {}

		if (open_paths === null) {
			// Default: open nodes up to initial_depth levels
			const depth = parseInt(
				this._body.querySelector('.tn-container')?.dataset.initialDepth ?? '1'
			);
			const openLevel = (ul, remaining) => {
				if (remaining <= 0) return;
				for (const li of ul.querySelectorAll(':scope > li.tn-node.tn-group')) {
					li.classList.add('tn-open');
					const children = li.querySelector(':scope > .tn-children');
					if (children) openLevel(children, remaining - 1);
				}
			};
			const tree = this._body.querySelector('.tn-tree');
			if (tree) openLevel(tree, depth);
		}
		else {
			for (const li of this._body.querySelectorAll('.tn-node.tn-group')) {
				if (li.dataset.path && open_paths.has(li.dataset.path)) {
					li.classList.add('tn-open');
				}
			}
		}
	}

	#saveOpenState() {
		const open_paths = [];

		for (const li of this._body.querySelectorAll('.tn-node.tn-group.tn-open')) {
			if (li.dataset.path) {
				open_paths.push(li.dataset.path);
			}
		}

		try {
			localStorage.setItem(this.#storageKey, JSON.stringify(open_paths));
		}
		catch (_) {}
	}

	// ── Scroll position ────────────────────────────────────────────────────────

	#saveScrollPosition() {
		const container = this._body.querySelector('.tn-container');

		if (container) {
			this.#scroll_top = container.scrollTop;
		}
	}

	#restoreScrollPosition() {
		const container = this._body.querySelector('.tn-container');

		if (container) {
			container.scrollTop = this.#scroll_top;
		}
	}

	// ── Helpers ────────────────────────────────────────────────────────────────

	#label(dataKey) {
		return this._body.querySelector('.tn-wrapper')?.dataset[dataKey] ?? '';
	}

	#isRecursive() {
		return this._body.querySelector('.tn-container')?.dataset.recursive === '1';
	}

	// ── Folder icon tooltip ────────────────────────────────────────────────────

	#showTooltip(text, anchor) {
		if (!this.#tooltip) {
			this.#tooltip = document.createElement('div');
			this.#tooltip.className = 'holoztek-tree-navigator-tooltip';
			document.body.appendChild(this.#tooltip);
		}

		this.#tooltip.textContent  = text;
		this.#tooltip.style.display = 'block';

		const rect = anchor.getBoundingClientRect();
		const tw   = this.#tooltip.offsetWidth;
		const th   = this.#tooltip.offsetHeight;
		const vw   = window.innerWidth;
		const vh   = window.innerHeight;

		let x = rect.right + 6;
		let y = rect.top;

		if (x + tw > vw) x = rect.left - tw - 6;
		if (y + th > vh) y = vh - th - 6;

		this.#tooltip.style.left = x + 'px';
		this.#tooltip.style.top  = y + 'px';
	}

	#hideTooltip() {
		if (this.#tooltip) {
			this.#tooltip.style.display = 'none';
		}
	}
}
