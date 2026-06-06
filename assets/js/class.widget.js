/*
 * Tree Navigator Widget
 *
 * Displays host groups and hosts as a collapsible directory tree.
 * Clicking a group name broadcasts _hostgroupid (+ child groupids if recursive).
 * Clicking a host name broadcasts _hostid + direct parent _hostgroupid.
 * Clicking a host icon shows the Zabbix host menu (data-menu-popup).
 */

class CWidgetTreeNavigator extends CWidget {

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
	#_clickHandler     = null;
	#_mouseOverHandler = null;
	#_mouseOutHandler  = null;

	/** localStorage key for persisting expanded node paths. */
	get #storageKey() {
		return 'tn_open_' + this._widgetid;
	}

	// ── Lifecycle ──────────────────────────────────────────────────────────────

	onActivate() {
		this.#restoreScrollPosition();

		if (this.#_clickHandler === null) {
			this.#_clickHandler     = this.#onClick.bind(this);
			this.#_mouseOverHandler = this.#onMouseOver.bind(this);
			this.#_mouseOutHandler  = this.#onMouseOut.bind(this);

			this._body.addEventListener('click',     this.#_clickHandler);
			this._body.addEventListener('mouseover', this.#_mouseOverHandler);
			this._body.addEventListener('mouseout',  this.#_mouseOutHandler);
		}
	}

	onDeactivate() {
		this.#saveScrollPosition();

		if (this.#_clickHandler !== null) {
			this._body.removeEventListener('click',     this.#_clickHandler);
			this._body.removeEventListener('mouseover', this.#_mouseOverHandler);
			this._body.removeEventListener('mouseout',  this.#_mouseOutHandler);

			this.#_clickHandler     = null;
			this.#_mouseOverHandler = null;
			this.#_mouseOutHandler  = null;
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
		this.#applySelection();
		this.#restoreScrollPosition();

		// Auto-select first group when this widget's output is being referred to.
		if (this.isReferred() && !this.hasEverUpdated()
				&& this.#selected_path === null && this.#selected_hostid === null) {
			this.#selectFirstGroup();
		}
	}

	onReferredUpdate() {
		if (this.#selected_path === null && this.#selected_hostid === null) {
			this.#selectFirstGroup();
		}
	}

	hasPadding() {
		return false;
	}

	// ── Event handlers ─────────────────────────────────────────────────────────

	#onClick(e) {
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

		// Group label click
		const group_label = e.target.closest('.js-tn-group-label');

		if (group_label?.dataset.groupid) {
			this.#selectGroup(group_label);
			return;
		}

		// Host label click
		const host_label = e.target.closest('.js-tn-host-label');

		if (host_label?.dataset.hostid) {
			this.#selectHost(host_label);
		}
	}

	#onMouseOver(e) {
		const folder = e.target.closest('.js-tn-folder[data-recursive-host-count]');

		if (folder) {
			const count = folder.dataset.recursiveHostCount;
			this.#showTooltip(`所属ホスト：${count}台`, folder);
		}
	}

	#onMouseOut(e) {
		if (!e.relatedTarget?.closest('.js-tn-folder')) {
			this.#hideTooltip();
		}
	}

	// ── Tree interaction ───────────────────────────────────────────────────────

	#toggleNode(li) {
		const is_open = li.classList.toggle('tn-open');
		this.#saveOpenState();
	}

	#selectGroup(label) {
		const groupid    = label.dataset.groupid;
		const is_recursive = this.#isRecursive();

		let groupids;

		if (is_recursive) {
			const raw = label.dataset.childGroupids || groupid;
			groupids  = raw.split(',').filter(Boolean);

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
		else {
			groupids = [groupid];
		}

		this.#selected_hostid = null;
		this.#selected_path   = label.closest('.tn-node')?.dataset.path ?? null;

		this.#applySelection();

		this.broadcast({
			[CWidgetsData.DATA_TYPE_HOST_GROUP_ID]:  groupids,
			[CWidgetsData.DATA_TYPE_HOST_GROUP_IDS]: groupids,
			[CWidgetsData.DATA_TYPE_HOST_ID]:        []
		});
	}

	#selectHost(label) {
		const hostid          = label.dataset.hostid;
		const parent_groupid  = label.dataset.parentGroupid;

		this.#selected_path   = null;
		this.#selected_hostid = hostid;

		this.#applySelection();

		this.broadcast({
			[CWidgetsData.DATA_TYPE_HOST_GROUP_ID]:  parent_groupid ? [parent_groupid] : [],
			[CWidgetsData.DATA_TYPE_HOST_GROUP_IDS]: parent_groupid ? [parent_groupid] : [],
			[CWidgetsData.DATA_TYPE_HOST_ID]:        [hostid]
		});
	}

	#selectFirstGroup() {
		const first = this._body.querySelector('.js-tn-group-label[data-groupid]');

		if (first) {
			this.#selectGroup(first);
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

	#isRecursive() {
		return this._body.querySelector('.tn-container')?.dataset.recursive === '1';
	}

	// ── Folder icon tooltip ────────────────────────────────────────────────────

	#showTooltip(text, anchor) {
		if (!this.#tooltip) {
			this.#tooltip = document.createElement('div');
			this.#tooltip.className = 'tree-navigator-tooltip';
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
