// Exercise the renderer and its controls without a browser or network dependency.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const docs = path.join(__dirname, '../docs');
const renderer = fs.readFileSync(path.join(docs, 'scholar_visualization.js'), 'utf8');

function load(award, dataScript) {
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
      classList: { add(key) { node(id).classes[key] = true; } },
    });
    return nodes.get(id);
  }
  const context = vm.createContext({
    window: {},
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
  const script = fs.readFileSync(path.join(docs, filename), 'utf8');
  const {node, properties, data} = load(award, script);
  const rowCount = () => (node('#table').markup.match(/class="row"/g) || []).length;
  assert.equal(rowCount(), data.metadata.joinedRows);
  assert.equal(properties['--year-count'], data.metadata.yearMax - data.metadata.yearMin + 1);
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
  console.log(`${award}: default rows, missing rows, search, empty state, year range, and wrong-dataset guard passed`);
}
assert.equal(load('turing').node('#empty').classes.visible, true);
