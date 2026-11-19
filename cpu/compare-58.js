// cpu/compare-58.js — stdlib only. Reads results-58.csv, prints L1/L3 by
// ds11 flag + Fisher exact (two-sided) + Wilson 95% CI. No deps.
'use strict';
const fs = require('fs');
const p = process.argv[2] || 'cpu/results-58.csv';
const txt = fs.readFileSync(p, 'utf8').trim().split('\n');
const h = txt[0].split(',');
const ci = n => h.indexOf(n);
const rows = txt.slice(1).map(l => {
  const c = l.split(',');
  const g = i => (c[i] || '').trim();
  return { task: g(ci('task')), is11: g(ci('is_ds11')) === '1', L1: +g(ci('L1')), L3: +g(ci('L3')) };
});
function wilson(x, n, z = 1.96) {
  if (!n) return [0, 0];
  const ph = x / n, d = 1 + z * z / n, c = ph + z * z / (2 * n);
  const m = z * Math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n));
  return [Math.max(0, (c - m) / d), Math.min(1, (c + m) / d)];
}
function fisher(a, b, c, d) {
  // two-sided via enumeration on a (11 vs 47 margins fixed)
  const logC = (n, k) => {
    if (k < 0 || k > n) return -Infinity;
    k = Math.min(k, n - k); let s = 0;
    for (let i = 1; i <= k; i++) s += Math.log(n - k + i) - Math.log(i);
    return s;
  };
  const n1 = a + b, n2 = c + d, m1 = a + c;
  const obs = logC(n1, a) + logC(n2, c) - logC(n1 + n2, m1);
  let p = 0;
  for (let x = Math.max(0, m1 - n2); x <= Math.min(n1, m1); x++) {
    const lp = logC(n1, x) + logC(n2, m1 - x) - logC(n1 + n2, m1);
    if (lp <= obs + 1e-9) p += Math.exp(lp);
  }
  return Math.min(1, p);
}
for (const k of ['L1', 'L3']) {
  const g11 = rows.filter(r => r.is11), g47 = rows.filter(r => !r.is11);
  const a = g11.filter(r => r[k]).length, b = g11.length - a;
  const cc = g47.filter(r => r[k]).length, dd = g47.length - cc;
  const [l1, u1] = wilson(a, g11.length), [l2, u2] = wilson(cc, g47.length);
  console.log(`${k}: DS11 ${a}/${g11.length} [${l1.toFixed(2)},${u1.toFixed(2)}] vs rest ${cc}/${g47.length} [${l2.toFixed(2)},${u2.toFixed(2)}] Fisher-p=${fisher(a, b, cc, dd).toFixed(4)}`);
}
console.log(`cells=${rows.length} ds11=${rows.filter(r => r.is11).length}`);
