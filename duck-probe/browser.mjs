// duck.ai 1-turn Chromium viability (anonymous, no secrets). Playwright.
import { chromium } from 'playwright';
const MODEL = "tinfoil/gemma4-31b";
const t0 = Date.now();
const out = { model: MODEL, browserLaunched: false, cfChallenge: false, statusSeen: false, vqdIssued: false };
let browser = null;
try {
  browser = await chromium.launch({ headless: true, args: ["--disable-blink-features=AutomationControlled", "--no-sandbox"] });
  out.browserLaunched = true;
  const ctx = await browser.newContext({
    userAgent: "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    viewport: { width: 1280, height: 720 }, locale: "en-US"
  });
  const page = await ctx.newPage();
  let vqd = null, vqdRotated = false, chatHttp = null;
  const rateLimit = {};
  page.on("response", async (r) => {
    try {
      const u = r.url();
      if (u.includes("/duckchat/v1/status")) {
        out.statusSeen = true;
        const h = await r.allResponseHeaders();
        const v = h["x-vqd-4"];
        if (v) { vqd = v; out.vqdIssued = true; }
      }
      if (u.includes("/duckchat/v1/chat")) {
        chatHttp = r.status();
        const h = await r.allResponseHeaders();
        if (h["x-vqd-4"]) vqdRotated = true;
        for (const k of ["x-ratelimit-limit", "x-ratelimit-remaining", "x-ratelimit-reset", "retry-after"])
          if (h[k]) rateLimit[k] = h[k];
      }
    } catch {}
  });
  await page.goto("https://duck.ai/", { waitUntil: "domcontentloaded", timeout: 60000 }).catch(() => {});
  await page.waitForTimeout(12000);
  try {
    const title = await page.title();
    const bodyTxt = (await page.content()).slice(0, 4000);
    out.cfChallenge = /just a moment|verifying|challenge/i.test(title + " " + bodyTxt);
    out.pageTitle = title.slice(0, 120);
  } catch {}
  if (!vqd) {
    const st = await page.evaluate(async () => {
      try {
        const r = await fetch("https://duckduckgo.com/duckchat/v1/status", { headers: { "x-vqd-accept": "1" } });
        return { http: r.status, issued: false };
      } catch (e) { return { err: String(e).slice(0, 150) }; }
    });
    out.evalStatus = st;
    await page.waitForTimeout(4000);
  }
  if (!vqd) { out.fatal = "no-vqd-token-browser"; out.totalMs = Date.now() - t0; console.log(JSON.stringify(out)); await browser.close(); process.exit(0); }
  const t1 = Date.now();
  const ans = await page.evaluate(async (args) => {
    try {
      const r = await fetch("https://duckduckgo.com/duckchat/v1/chat", {
        method: "POST", headers: { "Content-Type": "application/json", "x-vqd-4": args.vqd },
        body: JSON.stringify({ model: args.model, messages: [{ role: "user", content: "Reply with exactly: DUCK-OK. Then on a new line, state your model name as you know it in under 10 words." }] })
      });
      const raw = await r.text();
      const chunks = [];
      for (const line of raw.split("\n")) {
        const t = line.trim();
        if (!t.startsWith("data:")) continue;
        const p = t.slice(5).trim();
        if (p === "[DONE]") break;
        try {
          const j = JSON.parse(p);
          if (typeof j.message === "string") chunks.push(j.message);
          else if (typeof j.content === "string") chunks.push(j.content);
          else chunks.push(p.slice(0, 200));
        } catch (e) { chunks.push(p.slice(0, 200)); }
      }
      const answer = chunks.join("");
      return { http: r.status, rawChars: raw.length, answerChars: answer.length, answerHead200: answer.slice(0, 200), rawHead300: raw.slice(0, 300) };
    } catch (e) { return { err: String(e).slice(0, 200) }; }
  }, { vqd, model: MODEL });
  out.chatHttp = ans.http !== undefined ? ans.http : (chatHttp || ans.err || "eval-failed");
  out.answerChars = ans.answerChars; out.answerHead200 = ans.answerHead200; out.rawHead300 = ans.rawHead300;
  out.rawChars = ans.rawChars; if (ans.err && out.answerChars === undefined) out.err = ans.err;
  out.latencyMs = Date.now() - t1;
  out.vqdRotated = vqdRotated; out.rateLimit = rateLimit;
  out.totalMs = Date.now() - t0;
  console.log(JSON.stringify(out));
  await browser.close();
} catch (e) {
  out.err = String(e).slice(0, 300);
  out.totalMs = Date.now() - t0;
  console.log(JSON.stringify(out));
  try { if (browser) await browser.close(); } catch {}
}
