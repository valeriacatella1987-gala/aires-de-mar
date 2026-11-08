/* ============================================================
   Aires de Mar — interacciones (todo en archivo externo: la CSP no permite JS inline)
   ============================================================ */

/* 👉 ÚNICO lugar para cambiar el número de WhatsApp. */
const WA_NUMBER = "5492255625427";
document.querySelectorAll("[data-wa]").forEach((el) => {
  const msg = encodeURIComponent(el.getAttribute("data-wa") || "");
  el.setAttribute("href", `https://wa.me/${WA_NUMBER}?text=${msg}`);
  el.setAttribute("target", "_blank");
  el.setAttribute("rel", "noopener noreferrer");
});

/* Mail armado en JS: no queda como texto plano para los bots que rastrean mailto:. */
const EMAIL_USER = "airesdemarpampas";
const EMAIL_DOMAIN = "gmail.com";
const EMAIL = `${EMAIL_USER}@${EMAIL_DOMAIN}`;
document.querySelectorAll("[data-mail]").forEach((el) => {
  const subject = encodeURIComponent(el.getAttribute("data-mail") || "Consulta - Aires de Mar");
  el.setAttribute("href", `mailto:${EMAIL}?subject=${subject}`);
});

/* Los botones "Consultá" abrían solo mailto:, que no hace nada si la persona no tiene
   una app de correo configurada (la mayoría en el celu). Ahora abren una ventanita
   para elegir WhatsApp o Gmail; mailto queda como opción secundaria. */
const contact = document.getElementById("contact");
const gmailLink = document.getElementById("gmailLink");
const copyBtn = contact.querySelector(".contact__copy");
document.querySelectorAll("[data-mail]:not(.contact__alt)").forEach((el) => {
  el.addEventListener("click", (e) => {
    e.preventDefault();
    const subject = encodeURIComponent(el.getAttribute("data-mail") || "Consulta - Aires de Mar");
    gmailLink.href = `https://mail.google.com/mail/?view=cm&fs=1&to=${EMAIL}&su=${subject}`;
    contact.querySelector(".contact__alt").href = `mailto:${EMAIL}?subject=${subject}`;
    copyBtn.textContent = "Copiar el mail";
    contact.showModal();
  });
});
contact.querySelector(".contact__close").addEventListener("click", () => contact.close());
contact.addEventListener("click", (e) => { if (e.target === contact) contact.close(); });
contact.querySelectorAll("a").forEach((a) => a.addEventListener("click", () => contact.close()));
copyBtn.addEventListener("click", async () => {
  try { await navigator.clipboard.writeText(EMAIL); copyBtn.textContent = "¡Copiado!"; }
  catch { copyBtn.textContent = EMAIL; }
});

const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const root = document.documentElement;
const nav = document.getElementById("nav");
const heroBg = document.querySelector(".hero__bg");

/* Scroll: fondo del nav + barra de progreso + parallax del hero (un solo rAF por frame) */
let ticking = false;
const onScroll = () => {
  const y = window.scrollY;
  nav.classList.toggle("scrolled", y > 40);
  const max = root.scrollHeight - window.innerHeight;
  root.style.setProperty("--p", max > 0 ? (y / max).toFixed(4) : "0");
  if (!reduceMotion && y < window.innerHeight) heroBg.style.setProperty("--py", `${(y * 0.3).toFixed(1)}px`);
  ticking = false;
};
onScroll();
window.addEventListener("scroll", () => {
  if (!ticking) { ticking = true; requestAnimationFrame(onScroll); }
}, { passive: true });

/* Menú móvil */
const toggle = document.getElementById("navToggle");
const links = document.getElementById("navLinks");
const setMenu = (open) => {
  links.classList.toggle("open", open);
  toggle.setAttribute("aria-expanded", String(open));
  toggle.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
};
toggle.addEventListener("click", () => setMenu(!links.classList.contains("open")));
links.querySelectorAll("a").forEach((a) => a.addEventListener("click", () => setMenu(false)));
document.addEventListener("keydown", (e) => { if (e.key === "Escape") setMenu(false); });

/* Contadores animados (4 → 4,8 → 60) */
const animateCount = (el) => {
  const target = parseFloat(el.dataset.count);
  const decimals = parseInt(el.dataset.decimals || "0", 10);
  const fmt = (n) => n.toFixed(decimals).replace(".", ",");
  if (reduceMotion) { el.textContent = fmt(target); return; }
  const t0 = performance.now(), dur = 1400;
  const step = (t) => {
    const k = Math.min(1, (t - t0) / dur);
    el.textContent = fmt(target * (1 - Math.pow(1 - k, 3)));
    if (k < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
};

/* Entradas al hacer scroll */
const io = new IntersectionObserver((entries) => {
  entries.forEach((e) => {
    if (!e.isIntersecting) return;
    e.target.classList.add("in");
    e.target.querySelectorAll("[data-count]").forEach(animateCount);
    io.unobserve(e.target);
  });
}, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
document.querySelectorAll(".reveal, .stagger").forEach((el) => io.observe(el));

/* Nav: marca la sección visible */
const navLinks = [...links.querySelectorAll('a[href^="#"]')];
const spy = new IntersectionObserver((entries) => {
  entries.forEach((e) => {
    if (!e.isIntersecting) return;
    navLinks.forEach((a) => a.classList.toggle("is-active", a.getAttribute("href") === `#${e.target.id}`));
  });
}, { rootMargin: "-45% 0px -50% 0px" });
navLinks.forEach((a) => { const s = document.querySelector(a.getAttribute("href")); if (s) spy.observe(s); });

/* Barra de reserva: aparece tras el hero; flotantes se esconden al llegar al footer */
const bar = document.getElementById("reservaBar");
new IntersectionObserver(([e]) => bar.classList.toggle("show", !e.isIntersecting), { threshold: 0 })
  .observe(document.querySelector(".hero"));
new IntersectionObserver(([e]) => document.body.classList.toggle("at-end", e.isIntersecting), { threshold: 0 })
  .observe(document.getElementById("footer"));

/* Visor de fotos de la galería (<dialog> nativo) */
const lb = document.getElementById("lightbox");
const lbImg = lb.querySelector("img");
const lbCount = lb.querySelector(".lb-count");
const shots = [...document.querySelectorAll(".bento figure")]; /* casas + galería */
shots.forEach((fig) => {
  fig.setAttribute("tabindex", "0");
  fig.setAttribute("role", "button");
  if (!fig.hasAttribute("aria-label")) fig.setAttribute("aria-label", `Ampliar foto: ${fig.querySelector("img").alt}`);
});
let current = 0;
const show = (i) => {
  current = (i + shots.length) % shots.length;
  const img = shots[current].querySelector("img");
  lbImg.src = img.currentSrc || img.src;
  lbImg.alt = img.alt;
  lbCount.textContent = `${current + 1} / ${shots.length}`;
};
shots.forEach((fig, i) => {
  const open = () => { show(i); lb.showModal(); };
  fig.addEventListener("click", open);
  fig.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(); } });
});
lb.querySelector(".lb-close").addEventListener("click", () => lb.close());
lb.querySelector(".lb-prev").addEventListener("click", () => show(current - 1));
lb.querySelector(".lb-next").addEventListener("click", () => show(current + 1));
lb.addEventListener("click", (e) => { if (e.target === lb) lb.close(); });
lb.addEventListener("keydown", (e) => {
  if (e.key === "ArrowLeft") show(current - 1);
  if (e.key === "ArrowRight") show(current + 1);
});
let touchX = null;
lb.addEventListener("touchstart", (e) => { touchX = e.touches[0].clientX; }, { passive: true });
lb.addEventListener("touchend", (e) => {
  if (touchX === null) return;
  const dx = e.changedTouches[0].clientX - touchX;
  if (Math.abs(dx) > 40) show(current + (dx < 0 ? 1 : -1));
  touchX = null;
});

document.getElementById("year").textContent = new Date().getFullYear();
