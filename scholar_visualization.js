(() => {
  const DATA = window.SCHOLAR_DATA;
  if (!DATA || DATA.schemaVersion !== 1 || !Array.isArray(DATA.rows) || !DATA.metadata ||
      DATA.metadata.award !== document.body.dataset.award) {
    document.getElementById('table').hidden = true;
    const message = document.getElementById('empty');
    message.textContent = 'Citation data could not be loaded for this award. Keep the matching data script alongside this page and reload.';
    message.classList.add('visible');
    return;
  }
    // Use one display window for both awards, regardless of dataset coverage.
    const YEAR_COUNT = 45;
    const YEAR_MAX = new Date().getUTCFullYear();
    const YEAR_MIN = YEAR_MAX - YEAR_COUNT + 1;
    const YEARS = d3.range(YEAR_MIN, YEAR_MAX + 1).map(String);
    document.documentElement.style.setProperty('--year-count', YEARS.length);
    const state = { query: '', showMissing: false, sortKey: 'year', sortDirection: -1 };
    const nameCollator = new Intl.Collator('en', { sensitivity: 'base' });
    const sortLabels = { year: 'Year', name: 'Name', citations: 'Citations', hIndex: 'h-index' };

    const table = d3.select('#table');
    const summary = d3.select('#summary');
    const empty = d3.select('#empty');
    const withData = DATA.rows.filter(row => row.hasScholar).length;
    d3.select('#coverage').html([
      ['Total recipients', DATA.rows.length],
      ['With citation data', withData],
      ['Without citation data', DATA.rows.length - withData],
    ].map(([label, count]) => `<div><dt>${label}</dt><dd>${fmt(count)}</dd></div>`).join(''));

    d3.select('#search').on('input', event => { state.query = event.target.value.trim().toLowerCase(); render(); });
    d3.select('#showMissing').on('change', event => { state.showMissing = event.target.checked; render(); });
    table.on('click', event => {
      const button = event.target.closest('button[data-sort]');
      if (!button) return;
      const key = button.dataset.sort;
      if (!Object.hasOwn(sortLabels, key)) return;
      state.sortDirection = state.sortKey === key ? -state.sortDirection : (key === 'name' ? 1 : -1);
      state.sortKey = key;
      render();
      document.getElementById(`sort-${key}`).focus();
    });
    function fmt(value) {
      return value == null ? '' : d3.format(',')(value);
    }

    function lastName(name) {
      const parts = name.trim().replace(/,?\s+(?:Jr\.?|Sr\.?|II|III|IV)$/i, '').split(/\s+/);
      return parts[parts.length - 1];
    }

    function compareNames(a, b) {
      return nameCollator.compare(lastName(a.name), lastName(b.name)) || nameCollator.compare(a.name, b.name);
    }

    function compareRows(a, b) {
      if (state.sortKey === 'name') {
        return state.sortDirection * compareNames(a, b) || (b.year || 0) - (a.year || 0);
      }
      const value = row => state.sortKey === 'year' ? row.year : (row.hasScholar ? row[state.sortKey] : null);
      const av = value(a), bv = value(b);
      // Keep unavailable metrics last in either direction; zero is a valid value.
      if ((av == null) !== (bv == null)) return av == null ? 1 : -1;
      return state.sortDirection * ((av ?? 0) - (bv ?? 0)) ||
        (b.year || 0) - (a.year || 0) || compareNames(a, b);
    }

    function filteredRows() {
      return DATA.rows.filter(row => {
        if (!state.showMissing && !row.hasScholar) return false;
        if (!state.query) return true;
        return row.name.toLowerCase().includes(state.query);
      }).sort(compareRows);
    }

    function chart(row) {
      if (!row.hasScholar) return '<div class="chart-cell missing" role="cell">No Scholar data</div>';
      const values = YEARS.map(year => row.citationByYear[year] || 0);
      const max = d3.max(values) || 1;
      const bars = YEARS.map((year, index) => {
        const value = values[index];
        const height = value ? Math.max(2, Math.round((value / max) * 100)) : 1;
        const cls = value ? 'bar' : 'bar zero';
        return `<div class="${cls}" style="height:${height}%" title="${year}: ${fmt(value)} citations"></div>`;
      }).join('');
      return `<div class="chart-cell" role="cell"><div class="chart" aria-label="Citation history for ${escapeHtml(row.name)}">${bars}</div></div>`;
    }

    function escapeHtml(value) {
      return String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
    }

    function authorCell(row) {
      const name = escapeHtml(row.name);
      return row.scholarProfile ? `<a href="${escapeHtml(row.scholarProfile)}">${name}</a>` : name;
    }

    function citationsCell(row) {
      return row.hasScholar ? fmt(row.citations) : '';
    }

    function hIndexCell(row) {
      return row.hasScholar ? fmt(row.hIndex) : '';
    }

    function axisHtml() {
      const ticks = YEARS.map(year => {
        const labeled = +year % 5 === 0;
        return `<span class="axis-year${labeled ? ' tick' : ''}" title="${year}">${labeled ? `<span class="axis-label">${year}</span>` : ''}</span>`;
      }).join('');
      const headers = Object.entries(sortLabels).map(([key, label]) => {
        const active = state.sortKey === key;
        const direction = state.sortDirection === 1 ? 'ascending' : 'descending';
        const arrow = active ? (state.sortDirection === 1 ? '↑' : '↓') : '↕';
        return `<div role="columnheader"${active ? ` aria-sort="${direction}"` : ''}><button type="button" id="sort-${key}" class="sort-button" data-sort="${key}" aria-label="Sort by ${key === 'name' ? 'last name' : label}">${label} <span aria-hidden="true">${arrow}</span></button></div>`;
      }).join('');
      return `${headers}<div role="columnheader" class="axis" aria-label="Citation year">${ticks}</div>`;
    }

    function render() {
      const rows = filteredRows();
      summary.text(`${fmt(rows.length)} shown · Citation years ${YEAR_MIN}–${YEAR_MAX}`);
      empty.classed('visible', rows.length === 0);
      table.style('display', rows.length ? null : 'none');

      const html = [`<div class="row head" role="row">${axisHtml()}</div>`].concat(rows.map(row => `
        <div class="row" role="row">
          <div class="year" role="cell">${row.year || ''}</div>
          <div class="author" role="cell" title="${escapeHtml(row.name)}">${authorCell(row)}</div>
          <div class="metric" role="cell">${citationsCell(row)}</div>
          <div class="metric" role="cell">${hIndexCell(row)}</div>
          ${chart(row)}
        </div>`)).join('');
      table.html(html);
    }

    render();
})();
