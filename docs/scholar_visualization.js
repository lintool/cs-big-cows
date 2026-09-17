(() => {
  const DATA = window.SCHOLAR_DATA;
  if (!DATA || DATA.schemaVersion !== 1 || !Array.isArray(DATA.rows) || !DATA.metadata) {
    document.getElementById('table').hidden = true;
    const message = document.getElementById('empty');
    message.textContent = 'Citation data could not be loaded. Keep scholar_data.js alongside this page and reload.';
    message.classList.add('visible');
    return;
  }
    const YEAR_MIN = DATA.metadata.yearMin;
    const YEAR_MAX = DATA.metadata.yearMax;
    const YEARS = d3.range(YEAR_MIN, YEAR_MAX + 1).map(String);
    const state = { query: '', showMissing: false };

    const table = d3.select('#table');
    const summary = d3.select('#summary');
    const empty = d3.select('#empty');

    d3.select('#search').on('input', event => { state.query = event.target.value.trim().toLowerCase(); render(); });
    d3.select('#showMissing').on('change', event => { state.showMissing = event.target.checked; render(); });
    function fmt(value) {
      return value == null ? '' : d3.format(',')(value);
    }

    function filteredRows() {
      return DATA.rows.filter(row => {
        if (!state.showMissing && !row.hasScholar) return false;
        if (!state.query) return true;
        return row.name.toLowerCase().includes(state.query);
      });
    }

    function chart(row) {
      if (!row.hasScholar) return '<div class="chart-cell missing">No Scholar data</div>';
      const values = YEARS.map(year => row.citationByYear[year] || 0);
      const max = d3.max(values) || 1;
      const bars = YEARS.map((year, index) => {
        const value = values[index];
        const height = value ? Math.max(2, Math.round((value / max) * 100)) : 1;
        const cls = value ? 'bar' : 'bar zero';
        return `<div class="${cls}" style="height:${height}%" title="${year}: ${fmt(value)} citations"></div>`;
      }).join('');
      return `<div class="chart-cell"><div class="chart" aria-label="Citation history for ${escapeHtml(row.name)}">${bars}</div></div>`;
    }

    function escapeHtml(value) {
      return String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
    }

    function authorCell(row) {
      const name = escapeHtml(row.name);
      const acm = row.acmProfile ? `<a href="${row.acmProfile}">${name}</a>` : name;
      const scholar = row.hasScholar ? `<a class="subtle-link" href="${row.scholarProfile}">Scholar</a>` : '';
      return `${acm}${scholar}`;
    }

    function citationsCell(row) {
      return row.hasScholar ? fmt(row.citations) : '';
    }

    function hIndexCell(row) {
      return row.hasScholar ? fmt(row.hIndex) : '';
    }

    function axisHtml() {
      return `<div></div><div>Author</div><div>Citations</div><div>h-index</div><div></div>`;
    }

    function render() {
      const rows = filteredRows();
      const visibleWithData = rows.filter(row => row.hasScholar).length;
      summary.text(`${fmt(rows.length)} shown · ${fmt(visibleWithData)} with Scholar data · ${YEAR_MIN}–${YEAR_MAX}`);
      empty.classed('visible', rows.length === 0);
      table.style('display', rows.length ? null : 'none');

      const html = [`<div class="row head">${axisHtml()}</div>`].concat(rows.map(row => `
        <div class="row">
          <div class="year">${row.year || ''}</div>
          <div class="author" title="${escapeHtml(row.name)}">${authorCell(row)}</div>
          <div class="metric">${citationsCell(row)}</div>
          <div class="metric">${hIndexCell(row)}</div>
          ${chart(row)}
        </div>`)).join('');
      table.html(html);
    }

    render();
})();
