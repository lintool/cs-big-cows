// Exercise the renderer and its controls without a browser or network dependency.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.join(__dirname, '..');
const renderer = fs.readFileSync(path.join(root, 'scholar_visualization.js'), 'utf8');

function load(award, dataScript, currentYear = 2026) {
  const nodes = new Map();
  const properties = {};
  function node(id) {
    if (!nodes.has(id)) nodes.set(id, {
      events: {}, classes: {}, style: {}, textContent: '', innerHTML: '', measurements: 0,
      get styles() { return this.style; },
      get markup() { return this.innerHTML; },
      addEventListener(event, handler) { this.events[event] = handler; },
      getBoundingClientRect() { this.measurements++; return {width: 200, height: 30}; },
      focus() { this.focused = true; },
      classList: {
        add(key) { node(id).classes[key] = true; },
        toggle(key, value) { node(id).classes[key] = value; },
      },
    });
    return nodes.get(id);
  }
  const window = Object.assign(node('#window'), {innerWidth: 1024, innerHeight: 768});
  const document = Object.assign(node('#document'), {
    body: { dataset: { award } },
    getElementById: id => node(`#${id}`),
    documentElement: { style: { setProperty: (key, value) => { properties[key] = value; } } },
  });
  const context = vm.createContext({
    window,
    Date: class extends Date { getUTCFullYear() { return currentYear; } },
    document,
  });
  if (dataScript) vm.runInContext(dataScript, context);
  vm.runInContext(renderer, context);
  const names = () => [...node('#table').markup.matchAll(/class="author" role="cell" title="([^"]+)"/g)].map(match => match[1]);
  function sort(key) {
    node('#table').events.click({target: {closest: () => ({dataset: {sort: key}})}});
    assert.equal(node(`#sort-${key}`).focused, true);
  }
  return {node, properties, names, sort, data: context.window.SCHOLAR_DATA, window: context.window, document: context.document};
}

function loadRows(award, rows) {
  const script = `window.SCHOLAR_DATA = ${JSON.stringify({schemaVersion: 1, metadata: {award}, rows})};`;
  return load(award, script);
}

for (const [award, filename] of [['fellows', 'scholar_data.js'], ['turing', 'turing_scholar_data.js']]) {
  const script = fs.readFileSync(path.join(root, filename), 'utf8');
  const {node, properties, data, window, document} = load(award, script);
  const rowCount = () => (node('#table').markup.match(/class="row"/g) || []).length;
  assert.equal(rowCount(), data.metadata.joinedRows);
  assert.equal(properties['--year-count'], 41);
  assert.equal(node('#citation-source').textContent, 'All citation statistics from Google Scholar, as of 2026-09-17.');
  assert.equal(node('#summary').textContent, 'Cites are Google Scholar’s reported all-time total; the per-year histogram displays 1986–2026.');
  assert.ok(node('#table').markup.includes('data-tooltip="1986:'));
  assert.ok(!node('#table').markup.includes('data-tooltip="1985:'));
  assert.ok(node('#table').markup.includes('data-tooltip="2026:'));
  const hover = () => node('#table').events.pointermove({clientX: 1010, clientY: 760,
    target: {closest: () => ({dataset: {tooltip: '2023: 1,234 cites'}})}});
  hover();
  assert.equal(node('#citation-tooltip').textContent, '2023: 1,234 cites');
  assert.equal(node('#citation-tooltip').styles.display, 'block');
  assert.equal(node('#citation-tooltip').styles.left, '816px');
  assert.equal(node('#citation-tooltip').styles.top, '718px');
  const stationaryBar = {dataset: {tooltip: '2024: 0 cites'}};
  const measurements = node('#citation-tooltip').measurements;
  for (const clientX of [10, 20]) {
    node('#table').events.pointermove({clientX, clientY: 20, target: {closest: () => stationaryBar}});
  }
  assert.equal(node('#citation-tooltip').measurements, measurements + 1, 'Moving within one bar should reuse tooltip dimensions');
  assert.equal(node('#citation-tooltip').textContent, '2024: 0 cites');
  assert.equal(node('#citation-tooltip').styles.left, '32px');
  assert.equal(node('#citation-tooltip').styles.top, '32px');
  for (const hide of [
    () => node('#table').events.pointerleave(),
    () => window.events.scroll(),
    () => window.events.resize(),
    () => document.events.keydown({key: 'Escape'}),
    () => node('#table').events.pointermove({target: {closest: () => null}}),
    () => node('#search').events.input({target: {value: ''}}),
  ]) {
    hover();
    hide();
    assert.equal(node('#citation-tooltip').styles.display, 'none');
  }
  assert.equal((node('#table').markup.match(/class="bar(?: zero)?(?: before-induction)?"/g) || []).length,
    data.metadata.joinedRows * properties['--year-count']);
  assert.equal((node('#table').markup.match(/class="chart quality-low"/g) || []).length,
    data.rows.filter(row => row.hasScholar && row.scholarQuality === 'N').length);
  node('#showMissing').events.change({target: {checked: true}});
  assert.equal(rowCount(), data.metadata.totalRows);
  for (const [service, field] of [['ACM', 'acmProfile'], ['Google Scholar', 'scholarProfile'], ['DBLP', 'dblpProfile']]) {
    assert.equal(node('#table').markup.split(`title="${service} profile"`).length - 1,
      data.rows.filter(row => row[field]).length, `${award}: ${service} icons include links without metrics`);
  }
  assert.equal((node('#table').markup.match(/<span class="author-name">/g) || []).length, data.rows.length);
  assert.ok(!/<a[^>]*>[^<]+<\/a>/.test(node('#table').markup), 'Names must not be links');
  const missing = data.rows.find(row => !row.hasScholar);
  node('#search').events.input({target: {value: missing.name.toUpperCase()}});
  assert.ok(node('#table').markup.includes('No Google Scholar data'));
  node('#showMissing').events.change({target: {checked: false}});
  assert.equal(rowCount(), 0);
  assert.equal(node('#empty').classes.visible, true);
  node('#search').events.input({target: {value: 'no-such-recipient-12345'}});
  assert.equal(rowCount(), 0);
  node('#search').events.input({target: {value: ''}});
  assert.equal(rowCount(), data.metadata.joinedRows);
  const mismatch = load(award === 'fellows' ? 'turing' : 'fellows', script);
  assert.equal(mismatch.node('#table').hidden, true);
  assert.equal(mismatch.node('#empty').classes.visible, true);
  const nextYear = load(award, script, 2027);
  assert.equal(nextYear.properties['--year-count'], 42);
  assert.equal(nextYear.node('#summary').textContent, 'Cites are Google Scholar’s reported all-time total; the per-year histogram displays 1986–2027.');
  console.log(`${award}: default rows, missing rows, search, empty state, year range, and wrong-dataset guard passed`);
}
assert.equal(load('turing').node('#empty').classes.visible, true);

for (const award of ['fellows', 'turing']) {
  const fields = ['acmProfile', 'scholarProfile', 'dblpProfile'];
  const services = ['ACM profile', 'Google Scholar profile', 'DBLP profile'];
  const rows = Array.from({length: 8}, (_, mask) => ({name: `Recipient ${mask}`, year: 2025,
    hasScholar: false, citationByYear: {},
    ...Object.fromEntries(fields.map((field, index) => [field, mask & (1 << index) ? `https://example.org/${field}` : ''])),
  }));
  const {node} = loadRows(award, rows);
  node('#showMissing').events.change({target: {checked: true}});
  const iconGroups = [...node('#table').markup.matchAll(/class="profile-links">([\s\S]*?)<\/span><\/div>/g)];
  assert.equal(iconGroups.length, 8);
  iconGroups.forEach(([, markup], mask) => {
    const slots = [...markup.matchAll(/<a class="profile-link"[^>]*title="([^"]+)"|<span class="profile-slot"/g)].map(match => match[1] || null);
    assert.deepEqual(slots, services.map((service, index) => mask & (1 << index) ? service : null));
  });
  const page = fs.readFileSync(path.join(root, award === 'fellows' ? 'acm_fellows.html' : 'turing_award_winners.html'), 'utf8');
  for (const [, src] of page.matchAll(/<script src="([^"]+)"/g)) {
    assert.ok(src.startsWith('./'), 'Visualization scripts must load locally');
    assert.ok(fs.existsSync(path.join(root, src)));
  }
  for (const [, src] of node('#table').markup.matchAll(/<img[^>]*src="([^"]+)"/g)) {
    assert.ok(src.startsWith('./assets/'), 'Profile icons must load locally');
    assert.ok(fs.existsSync(path.join(root, src)));
  }
  console.log(`${award}: fixed profile slots for all eight link combinations and local scripts passed`);
}

for (const award of ['fellows', 'turing']) {
  const rows = [
    {name: 'Old', year: 1985, approximate_citations_at_induction: 9999, hasScholar: true},
    {name: 'Boundary', year: 1986, approximate_citations_at_induction: 0, hasScholar: true},
    {name: 'Later', year: 1987, approximate_citations_at_induction: 5, hasScholar: true},
    {name: 'Missing', year: 1984, approximate_citations_at_induction: null, hasScholar: false},
  ].map(row => ({...row, citationByYear: {'2026': 1}}));
  const {node, names, sort} = loadRows(award, rows);
  node('#showMissing').events.change({target: {checked: true}});
  assert.equal((node('#table').markup.match(/role="cell">-<\/div>/g) || []).length, award === 'turing' ? 2 : 0);
  sort('approximate_citations_at_induction');
  assert.deepEqual(names(), award === 'turing' ? ['Later', 'Boundary', 'Old', 'Missing'] : ['Old', 'Later', 'Boundary', 'Missing']);
  sort('approximate_citations_at_induction');
  assert.deepEqual(names(), ['Boundary', 'Later', 'Old', 'Missing']);
}

for (const award of ['fellows', 'turing']) {
  for (const scholarQuality of ['Y', 'N']) {
    const rows = [{name: 'Test Recipient', year: 2023, scholarQuality, hasScholar: true,
      citationByYear: {'2021': 0, '2022': 10, '2023': 20, '2024': 30}}];
    const {node} = loadRows(award, rows);
    const markup = node('#table').markup;
    assert.ok(markup.includes('class="bar before-induction" style="height:33%" data-tooltip="2022: 10 cites"'));
    assert.ok(markup.includes('class="bar" style="height:67%" data-tooltip="2023: 20 cites"'));
    assert.ok(markup.includes('class="bar" style="height:100%" data-tooltip="2024: 30 cites"'));
    assert.ok(markup.includes('data-tooltip="2021: 0 cites"'));
    assert.ok(markup.includes('data-tooltip="2020: no captured data"'));
    assert.equal(markup.includes('class="chart quality-low"'), scholarQuality === 'N');
  }
}

for (const award of ['fellows', 'turing']) {
  const rows = ['Orso, Alessandro', 'De Micheli, Giovanni', 'Bob Beta, Jr.', 'Arvind', 'Ada Lovelace']
    .map(name => ({name, year: 2025, hasScholar: true, citationByYear: {'2026': 1}}));
  const {node, names} = loadRows(award, rows);
  for (const [query, expected] of [
    ['Alessandro Orso', ['Orso, Alessandro']],
    ['ORSO,   ALESSANDRO', ['Orso, Alessandro']],
    ['Orso Alessandro', ['Orso, Alessandro']],
    ['Giovanni De Micheli', ['De Micheli, Giovanni']],
    ['Bob Beta Jr.', ['Bob Beta, Jr.']],
    ['Arvind', ['Arvind']],
    ['Ada Lovelace', ['Ada Lovelace']],
    ['Alessandro Lovelace', []],
  ]) {
    node('#search').events.input({target: {value: query}});
    assert.deepEqual(names(), expected, `${award}: search ${query}`);
  }
  console.log(`${award}: directory and given-name-first search, spaces, commas, suffixes, and single names passed`);
}

{
  const rows = ['Zulu, Amy', 'Alpha, Zoe', 'De Micheli, Giovanni', 'Bob Beta, Jr.']
    .map(name => ({name, year: 2025, hasScholar: true, citationByYear: {'2026': 1}}));
  const {names, sort} = loadRows('fellows', rows);
  assert.deepEqual(names(), ['Alpha, Zoe', 'Bob Beta, Jr.', 'De Micheli, Giovanni', 'Zulu, Amy']);
  sort('name');
  assert.deepEqual(names(), ['Alpha, Zoe', 'Bob Beta, Jr.', 'De Micheli, Giovanni', 'Zulu, Amy']);
}

for (const award of ['fellows', 'turing']) {
  const rows = [
    {name: 'Amy Zulu', year: 2024, citations: 0, approximate_citations_at_induction: 0, hIndex: 0},
    {name: 'Zoe Alpha', year: 2024, citations: 10, approximate_citations_at_induction: 6, hIndex: 5},
    {name: 'Bob Alpha Jr.', year: 2024, citations: 10, approximate_citations_at_induction: 4, hIndex: 3},
    {name: 'Carl Young', year: 2025, citations: 9, approximate_citations_at_induction: 8, hIndex: 2},
    {name: 'Mina Missing', year: 2023, citations: null, approximate_citations_at_induction: null, hIndex: null},
  ].map(row => ({...row, hasScholar: row.citations !== null, citationByYear: {'2026': 1}}));
  const {node, data, names, sort} = loadRows(award, rows);
  assert.deepEqual(names(), ['Carl Young', 'Bob Alpha Jr.', 'Zoe Alpha', 'Amy Zulu']);
  assert.match(node('#table').markup, /role="cell">9<\/div>\s*<div class="metric" role="cell">8<\/div>\s*<div class="metric" role="cell">2<\/div>/);
  sort('name');
  assert.deepEqual(names(), ['Bob Alpha Jr.', 'Zoe Alpha', 'Carl Young', 'Amy Zulu']);
  assert.ok(node('#table').markup.includes('aria-sort="ascending"'));
  sort('name');
  assert.deepEqual(names(), ['Amy Zulu', 'Carl Young', 'Zoe Alpha', 'Bob Alpha Jr.']);
  node('#showMissing').events.change({target: {checked: true}});
  sort('approximate_citations_at_induction');
  assert.deepEqual(names(), ['Carl Young', 'Zoe Alpha', 'Bob Alpha Jr.', 'Amy Zulu', 'Mina Missing']);
  sort('approximate_citations_at_induction');
  assert.deepEqual(names(), ['Amy Zulu', 'Bob Alpha Jr.', 'Zoe Alpha', 'Carl Young', 'Mina Missing']);
  sort('citations');
  assert.deepEqual(names(), ['Bob Alpha Jr.', 'Zoe Alpha', 'Carl Young', 'Amy Zulu', 'Mina Missing']);
  sort('citations');
  assert.deepEqual(names(), ['Amy Zulu', 'Carl Young', 'Bob Alpha Jr.', 'Zoe Alpha', 'Mina Missing']);
  sort('hIndex');
  assert.deepEqual(names(), ['Zoe Alpha', 'Bob Alpha Jr.', 'Carl Young', 'Amy Zulu', 'Mina Missing']);
  node('#search').events.input({target: {value: 'alpha'}});
  assert.deepEqual(names(), ['Zoe Alpha', 'Bob Alpha Jr.']);
  sort('hIndex');
  assert.deepEqual(names(), ['Bob Alpha Jr.', 'Zoe Alpha']);
  node('#search').events.input({target: {value: ''}});
  sort('year');
  assert.deepEqual(names(), ['Carl Young', 'Bob Alpha Jr.', 'Zoe Alpha', 'Amy Zulu', 'Mina Missing']);
  sort('year');
  assert.deepEqual(names(), ['Mina Missing', 'Bob Alpha Jr.', 'Zoe Alpha', 'Amy Zulu', 'Carl Young']);
  assert.equal(JSON.stringify(data.rows), JSON.stringify(rows), 'Sorting must not mutate the dataset');
  console.log(`${award}: year/last-name default, header toggles, ties, suffixes, zero/missing metrics, filtering, and source order passed`);
}
