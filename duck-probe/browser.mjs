// duck.ai UI-driven 1-turn viability (anonymous, no secrets). Playwright v3.
// Method per community guides (hirotomasato/duckapi root-cause + pavnxet headless pass):
// real Chrome (channel="chrome", NOT bundled Chromium) + drive the app's OWN send so the
// page mints x-fe-signals / x-vqd-hash-1 itself; tee SSE via fetch hook; model via body rewrite.
import { chromium } from 'playwright';
const MODEL = "tinfoil/gemma4-31b";
const REAL_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36";
const PROMPT = "Reply with exactly: DUCK-OK. Then on a new line, state your model name as you know it in under 10 words.";
const t0 = Date.now();
const out = { model: MODEL, chrome: null, sent: false, rewriteApplied: false };
const HOOK = "Object.defineProperty(navigator,'webdriver',{get:()=>undefined});"
+ "window.__duckai={chunks:[],done:false,err:null,rewrite:null,rewriteApplied:false};"
+ "(function(){const O=window.fetch;window.fetch=async function(u,o){o=o||{};"
+ "if(typeof u==='string'&&u.indexOf('/duckchat/v1/chat')!==-1){"
+ "const D=window.__duckai;D.chunks=[];D.done=false;D.err=null;"
+ "const rw=D.rewrite;D.rewrite=null;"
+ "if(rw&&typeof o.body==='string'){try{const j=JSON.parse(o.body);"
+ "if(rw.model)j.model=rw.model;"
+ "o=Object.assign({},o,{body:JSON.stringify(j)});D.rewriteApplied=true;}catch(e){}}"
+ "const r=await O.call(this,u,o);"
+ "try{const rd=r.clone().body.getReader();const dec=new TextDecoder();"
+ "(async function pump(){try{while(true){const x=await rd.read();"
+ "if(x.done){D.chunks.push(dec.decode());D.done=true;break;}"
+ "const s=dec.decode(x.value,{stream:true});D.chunks.push(s);"
+ "if(s.indexOf('\"action\":\"error\"')!==-1)D.err=s;}"
+ "}catch(e){D.err=String(e);D.done=true;}})();"
+ "}catch(e){D.err=String(e);D.done=true;}"
+ "return r;}return O.apply(this,arguments);};})();";
let browser = null;
try {
  const launch = { headless: true, channel: "chrome", args: ["--disable-blink-features=AutomationControlled", "--no-sandbox"] };
  try { browser = await chromium.launch(launch); out.chrome = "channel-chrome"; }
  catch (e1) {
    try { browser = await chromium.launch({ headless: true, executablePath: "/usr/bin/google-chrome", args: launch.args }); out.chrome = "usr-bin-google-chrome"; }
    catch (e2) { browser = await chromium.launch({ headless: true, args: launch.args }); out.chrome = "bundled-chromium-fallback"; }
  }
  const ctx = await browser.newContext({ userAgent: REAL_UA, viewport: { width: 1280, height: 720 }, locale: "en-US" });
  await ctx.addInitScript(HOOK);
  const page = await ctx.newPage();
  page.on("response", async (r) => {
    try {
      if (r.url().indexOf("/duckchat/v1/chat") !== -1) {
        out.chatHttp = r.status();
        const h = await r.allResponseHeaders();
        for (const k of ["x-ratelimit-limit", "x-ratelimit-remaining", "x-ratelimit-reset", "retry-after", "x-vqd-4"])
          if (h[k]) { out.rateLimit = out.rateLimit || {}; out.rateLimit[k] = (k === "x-vqd-4") ? true : h[k]; }
      }
    } catch {}
  });
  const g = await page.goto("https://duck.ai/", { waitUntil: "domcontentloaded", timeout: 60000 }).catch((e) => ({ gotoErr: String(e).slice(0, 160) }));
  out.goto = g && g.status ? { http: g.status(), url: page.url() } : { err: (g && g.gotoErr) || "goto-failed", url: page.url() };
  const openedAt = Date.now();
  let ta = null;
  for (let i = 0; i < 35; i++) {
    try { ta = await page.$("textarea"); } catch {}
    if (ta && Date.now() - openedAt >= 2000) break;
    await page.waitForTimeout(200);
  }
  out.textareaFound = !!ta;
  if (!ta) { out.fatal = "no-textarea"; out.totalMs = Date.now() - t0; console.log(JSON.stringify(out)); await browser.close(); process.exit(0); }
  await page.evaluate((rw) => { window.__duckai = { chunks: [], done: false, err: null, rewrite: rw, rewriteApplied: false }; }, { model: MODEL });
  await ta.click().catch(() => {});
  await ta.fill(PROMPT).catch(() => {});
  await page.waitForTimeout(300);
  let sent = false;
  try {
    for (const btn of await page.$$("button")) {
      let t = "", a = "";
      try { t = ((await btn.innerText()) || "").trim(); a = (await btn.getAttribute("aria-label")) || ""; } catch {}
      if (t === "Ask" || t === "Send" || a === "Ask" || a === "Send") { await btn.click({ force: true }).catch(() => {}); sent = true; break; }
    }
  } catch {}
  if (!sent) { try { await ta.press("Enter"); sent = true; out.sentVia = "enter"; } catch {} } else { out.sentVia = "button"; }
  out.sent = sent;
  if (!sent) { out.fatal = "send-failed"; out.totalMs = Date.now() - t0; console.log(JSON.stringify(out)); await browser.close(); process.exit(0); }
  const t1 = Date.now();
  let idx = 0, buf = "", sawData = false, hookErr = null, rewriteApplied = false;
  const deadline = Date.now() + 120000;
  while (Date.now() < deadline) {
    let st = null;
    try {
      st = await page.evaluate((n) => {
        const D = window.__duckai || { chunks: [], done: false, err: null };
        return { n: D.chunks.length, text: D.chunks.slice(n).join(""), done: D.done, err: D.err, rw: !!D.rewriteApplied };
      }, idx);
    } catch (e) { hookErr = String(e).slice(0, 160); break; }
    idx = st.n;
    if (st.rw) rewriteApplied = true;
    if (st.err) { hookErr = st.err.slice(0, 500); break; }
    if (st.text) { sawData = true; buf += st.text; }
    if (st.done) break;
    await page.waitForTimeout(sawData ? 250 : 500);
  }
  out.rewriteApplied = rewriteApplied;
  out.latencyMs = Date.now() - t1;
  const chunks = [];
  let errType = null;
  for (const line of buf.split("\n")) {
    const t = line.trim();
    if (t.indexOf("data:") === 0) {
      const p = t.slice(5).trim();
      if (p === "[DONE]") continue;
      try {
        const j = JSON.parse(p);
        if (j && j.action === "error") { errType = JSON.stringify(j).slice(0, 200); continue; }
        if (j && typeof j.message === "string") chunks.push(j.message);
        else if (j && typeof j.content === "string") chunks.push(j.content);
      } catch (e) {}
    }
  }
  const answer = chunks.join("");
  out.answerChars = answer.length;
  out.answerHead200 = answer.slice(0, 200);
  if (hookErr) out.hookErr = hookErr.slice(0, 300);
  if (errType) out.errType = errType;
  if (!hookErr && !errType && !answer) out.fatal = "empty-stream";
  out.rawWireChars = buf.length;
  out.totalMs = Date.now() - t0;
  console.log(JSON.stringify(out));
  await browser.close();
} catch (e) {
  out.err = String(e).slice(0, 300);
  out.totalMs = Date.now() - t0;
  console.log(JSON.stringify(out));
  try { if (browser) await browser.close(); } catch {}
}
