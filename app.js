/* ============================================================
   Aires de Mar — interacciones
   ============================================================ */

/* 👉 ÚNICO lugar para cambiar el número de WhatsApp (botón flotante). */
const WA_NUMBER = "5492255625427";

// Botón flotante de WhatsApp: único [data-wa] que queda en el sitio
document.querySelectorAll("[data-wa]").forEach((el) => {
  const msg = encodeURIComponent(el.getAttribute("data-wa") || "");
  el.setAttribute("href", `https://wa.me/${WA_NUMBER}?text=${msg}`);
  el.setAttribute("target", "_blank");
  el.setAttribute("rel", "noopener");
});

/* Mail de contacto, armado en JS (no queda como texto plano en el HTML)
   para dificultarle el trabajo a los bots que rastrean mailto: en el código fuente. */
const EMAIL_USER = "airesdemarpampas";
const EMAIL_DOMAIN = "gmail.com";
document.querySelectorAll("[data-mail]").forEach((el) => {
  const address = `${EMAIL_USER}@${EMAIL_DOMAIN}`;
  const subject = encodeURIComponent(el.getAttribute("data-mail") || "Consulta - Aires de Mar");
  el.setAttribute("href", `mailto:${address}?subject=${subject}`);
});

// Nav: fondo al hacer scroll
const nav = document.getElementById("nav");
const onScroll = () => nav.classList.toggle("scrolled", window.scrollY > 40);
onScroll();
window.addEventListener("scroll", onScroll, { passive: true });

// Menú móvil
const toggle = document.getElementById("navToggle");
const links = document.getElementById("navLinks");
toggle.addEventListener("click", () => {
  const open = links.classList.toggle("open");
  toggle.setAttribute("aria-expanded", String(open));
  toggle.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
});
links.querySelectorAll("a").forEach((a) =>
  a.addEventListener("click", () => {
    links.classList.remove("open");
    toggle.setAttribute("aria-expanded", "false");
  })
);

// Reveal on scroll (IntersectionObserver, compositor-friendly)
const io = new IntersectionObserver(
  (entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) {
        e.target.classList.add("in");
        io.unobserve(e.target);
      }
    });
  },
  { threshold: 0.12, rootMargin: "0px 0px -8% 0px" }
);
document.querySelectorAll(".reveal").forEach((el) => io.observe(el));

// Barra de reserva sticky: aparece tras el hero
const bar = document.getElementById("reservaBar");
const hero = document.querySelector(".hero");
new IntersectionObserver(
  ([entry]) => bar.classList.toggle("show", !entry.isIntersecting),
  { threshold: 0 }
).observe(hero);

// Año en el footer
document.getElementById("year").textContent = new Date().getFullYear();
