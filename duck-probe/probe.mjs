// duck.ai 1-turn viability probe (anonymous, no secrets). Node 18+.
const MODEL = "tinfoil/gemma4-31b";
const t0 = Date.now();
const st = await fetch("https://duckduckgo.com/duckchat/v1/status", {headers: {"x-vqd-accept": "1"}});
const vqd = st.headers.get("x-vqd-4");
const out = {model: MODEL, statusEndpoint: st.status, vqdIssued: !!vqd};
if (!vqd) { out.fatal = "no-vqd-token"; console.log(JSON.stringify(out)); process.exit(0); }
const body = JSON.stringify({model: MODEL, messages: [{role: "user", content: "Reply with exactly: DUCK-OK. Then on a new line, state your model name as you know it in under 10 words."}]});
const t1 = Date.now();
const chat = await fetch("https://duckduckgo.com/duckchat/v1/chat", {
  method: "POST", headers: {"Content-Type": "application/json", "x-vqd-4": vqd}, body,
  signal: AbortSignal.timeout(120000)
}).catch(e => ({ok: false, err: String(e).slice(0, 200)}));
out.chatHttp = chat.status !== undefined ? chat.status : "fetch-failed";
out.vqdRotated = !!(chat.headers && chat.headers.get("x-vqd-4"));
out.rateLimit = {};
if (chat.headers) for (const k of ["x-ratelimit-limit", "x-ratelimit-remaining", "x-ratelimit-reset", "retry-after"])
  if (chat.headers.get(k)) out.rateLimit[k] = chat.headers.get(k);
if (chat.ok !== false && chat.text) {
  const raw = await chat.text();
  out.latencyMs = Date.now() - t1;
  out.rawChars = raw.length;
  const chunks = [];
  for (const line of raw.split("\n")) {
    const t = line.trim();
    if (!t.startsWith("data:")) continue;
    const p = t.slice(5).trim();
    if (p === "[DONE]") break;
    try { const j = JSON.parse(p); if (typeof j.message === "string") chunks.push(j.message); else if (typeof j.content === "string") chunks.push(j.content); else chunks.push(p.slice(0, 200)); }
    catch (e) { chunks.push(p.slice(0, 200)); }
  }
  const answer = chunks.join("");
  out.answerChars = answer.length;
  out.answerHead200 = answer.slice(0, 200);
  out.rawHead300 = raw.slice(0, 300);
} else { out.err = chat.err || ("http-" + chat.status); }
out.totalMs = Date.now() - t0;
console.log(JSON.stringify(out));
