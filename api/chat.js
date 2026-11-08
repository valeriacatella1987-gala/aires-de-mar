// Chat web -> agente de Vale (n8n). La clave compartida vive solo acá (variable de Vercel),
// nunca en el navegador. El "teléfono" del chat es 999 + 10 dígitos derivados de la sesión:
// así el agente y el CRM lo tratan como una conversación más, marcada como web.
const crypto = require("crypto");

const N8N = process.env.AIRES_N8N_URL; // https://<n8n>/webhook
const SECRET = process.env.AIRES_WEB_SECRET;
const MAX_TEXT = 600;
const LIMITE = 20; // mensajes por sesión cada 10 min (por instancia; freno básico al abuso)
const uso = new Map();

const phoneDe = (sid) => {
  const h = crypto.createHash("sha256").update(sid).digest("hex").slice(0, 15);
  return "999" + (BigInt("0x" + h) % 10000000000n).toString().padStart(10, "0");
};

const mismoOrigen = (req) => {
  const origin = req.headers.origin;
  if (!origin) return true; // GET same-origin no siempre manda Origin
  try { return new URL(origin).host === req.headers.host; } catch { return false; }
};

module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  if (!N8N || !SECRET) return res.status(503).json({ ok: false });
  if (!mismoOrigen(req)) return res.status(403).json({ ok: false });

  const src = req.method === "GET" ? req.query : req.body || {};
  const sid = String(src.sid || "");
  if (!/^[A-Za-z0-9-]{16,64}$/.test(sid)) return res.status(400).json({ ok: false });
  const phone = phoneDe(sid);
  const headers = { "x-aires-web": SECRET, "Content-Type": "application/json" };

  try {
    if (req.method === "POST") {
      const text = String(src.text || "").replace(/\s+/g, " ").trim().slice(0, MAX_TEXT);
      if (!text) return res.status(400).json({ ok: false });
      const ahora = Date.now();
      const u = (uso.get(sid) || []).filter((t) => ahora - t < 600000);
      if (u.length >= LIMITE) return res.status(429).json({ ok: false });
      uso.set(sid, [...u, ahora]);
      const r = await fetch(`${N8N}/aires/web`, {
        method: "POST", headers, body: JSON.stringify({ phone, text }),
        signal: AbortSignal.timeout(8000),
      });
      return res.status(r.ok ? 200 : 502).json({ ok: r.ok });
    }
    if (req.method === "GET") {
      const since = String(src.since || "");
      if (Number.isNaN(Date.parse(since))) return res.status(400).json({ ok: false });
      const q = new URLSearchParams({ phone, since });
      const r = await fetch(`${N8N}/aires/web/poll?${q}`, { headers, signal: AbortSignal.timeout(8000) });
      if (!r.ok) return res.status(502).json({ ok: false });
      const j = await r.json();
      const messages = (j.messages || []).map((m) => ({ id: m.id, text: m.message, at: m.created_at }));
      return res.status(200).json({ ok: true, messages });
    }
    return res.status(405).json({ ok: false });
  } catch {
    return res.status(502).json({ ok: false });
  }
};
