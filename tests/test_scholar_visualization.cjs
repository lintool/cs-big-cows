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
      events: {}, classes: {}, styles: {}, textContent: '', markup: '',
      on(event, handler) { this.events[event] = handler; return this; },
      text(value) { this.textContent = value; return this; },
      classed(key, value) { this.classes[key] = value; return this; },
      style(key, value) { this.styles[key] = value; return this; },
      html(value) { this.markup = value; return this; },
      focus() { this.focused = true; },
      classList: { add(key) { node(id).classes[key] = true; } },
    });
    return nodes.get(id);
  }
  const context = vm.createContext({
    window: {},
    Date: class extends Date { getUTCFullYear() { return currentYear; } },
    document: {
      body: { dataset: { award } },
      getElementById: id => node(`#${id}`),
      documentElement: { style: { setProperty: (key, value) => { properties[key] = value; } } },
    },
    d3: {
      range: (start, end) => Array.from({length: end - start}, (_, i) => start + i),
      max: values => Math.max(...values),
      format: () => value => new Intl.NumberFormat('en-US').format(value),
      select: node,
    },
  });
  if (dataScript) vm.runInContext(dataScript, context);
  vm.runInContext(renderer, context);
  return {node, properties, data: context.window.SCHOLAR_DATA};
}

for (const [award, filename] of [['fellows', 'scholar_data.js'], ['turing', 'turing_scholar_data.js']]) {
  const script = fs.readFileSync(path.join(root, filename), 'utf8');
  const {node, properties, data} = load(award, script);
  const rowCount = () => (node('#table').markup.match(/class="row"/g) || []).length;
  assert.equal(rowCount(), data.metadata.joinedRows);
  assert.equal(properties['--year-count'], 45);
  assert.ok(node('#summary').textContent.endsWith('1982–2026'));
  assert.ok(node('#table').markup.includes('title="1982: 0 citations"'));
  assert.ok(node('#table').markup.includes('title="2026:'));
  assert.equal((node('#table').markup.match(/class="bar(?: zero)?"/g) || []).length,
    data.metadata.joinedRows * properties['--year-count']);
  node('#showMissing').events.change({target: {checked: true}});
  assert.equal(rowCount(), data.metadata.totalRows);
  const missing = data.rows.find(row => !row.hasScholar);
  node('#search').events.input({target: {value: missing.name.toUpperCase()}});
  assert.ok(node('#table').markup.includes('No Scholar data'));
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
  assert.equal(nextYear.properties['--year-count'], 45);
  assert.ok(nextYear.node('#summary').textContent.endsWith('1983–2027'));
  console.log(`${award}: default rows, missing rows, search, empty state, year range, and wrong-dataset guard passed`);
}
assert.equal(load('turing').node('#empty').classes.visible, true);

for (const award of ['fellows', 'turing']) {
  const rows = [
    {name: 'Amy Zulu', year: 2024, citations: 0, hIndex: 0},
    {name: 'Zoe Alpha', year: 2024, citations: 10, hIndex: 5},
    {name: 'Bob Alpha Jr.', year: 2024, citations: 10, hIndex: 3},
    {name: 'Carl Young', year: 2025, citations: 9, hIndex: 2},
    {name: 'Mina Missing', year: 2023, citations: null, hIndex: null},
  ].map(row => ({...row, hasScholar: row.citations !== null, citationByYear: {'2026': 1}}));
  const script = `window.SCHOLAR_DATA = ${JSON.stringify({schemaVersion: 1, metadata: {award}, rows})};`;
  const {node, data} = load(award, script);
  const names = () => [...node('#table').markup.matchAll(/class="author" role="cell" title="([^"]+)"/g)].map(match => match[1]);
  function sort(key) {
    node('#table').events.click({target: {closest: () => ({dataset: {sort: key}})}});
    assert.equal(node(`#sort-${key}`).focused, true);
  }
  assert.deepEqual(names(), ['Carl Young', 'Bob Alpha Jr.', 'Zoe Alpha', 'Amy Zulu']);
  sort('name');
  assert.deepEqual(names(), ['Bob Alpha Jr.', 'Zoe Alpha', 'Carl Young', 'Amy Zulu']);
  assert.ok(node('#table').markup.includes('aria-sort="ascending"'));
  sort('name');
  assert.deepEqual(names(), ['Amy Zulu', 'Carl Young', 'Zoe Alpha', 'Bob Alpha Jr.']);
  node('#showMissing').events.change({target: {checked: true}});
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
