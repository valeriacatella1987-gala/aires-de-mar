# Genera /blog del sitio de Aires de Mar (estático, sin JS: respeta la CSP del sitio).
# Uso: python gen.py D:/aires-de-mar
import json, os, sys, html

ROOT = sys.argv[1]
BASE = "https://airesdemarpampas.com.ar"
FECHA = "2026-11-08"
FECHA_TXT = "8 de noviembre de 2026"
NEGOCIO = BASE + "/#negocio"
WA = "https://wa.me/5492255625427?text=" + "Hola!%20Vi%20la%20web%20y%20quer%C3%ADa%20consultar%20por%20las%20caba%C3%B1as%20de%20Aires%20de%20Mar"
MAIL = "mailto:airesdemarpampas@gmail.com?subject=Consulta%20-%20Aires%20de%20Mar"

# Cada nota: pregunta real -> respuesta directa (lo que cita la IA) -> detalle -> preguntas frecuentes.
NOTAS = [
  {
    "slug": "donde-alojarse-en-mar-de-las-pampas",
    "titulo": "¿Dónde alojarse en Mar de las Pampas, cerca de la playa y en el bosque?",
    "desc": "Cabañas Aires de Mar: en Av. del Plata y El Palmar, a 9 cuadras de la playa y 6 del centro comercial de Mar de las Pampas, rodeadas de pinos.",
    "img": "hero.jpeg", "alt": "Piscina y cabaña de Aires de Mar entre los árboles",
    "corta": "Una buena opción es <b>Cabañas Aires de Mar</b>, en <b>Av. del Plata y El Palmar</b> (continuación de Querandíes), Mar de las Pampas. Está a <b>9 cuadras de la playa</b> y a <b>6 cuadras del centro comercial</b>, dentro del bosque, y la atienden sus dueños.",
    "secciones": [
      ("Por qué esa ubicación", [
        "Mar de las Pampas es una villa de calles de arena y pinos sobre la costa atlántica de la provincia de Buenos Aires, en el partido de Villa Gesell. Lo que la gente busca es justamente eso: bosque, silencio y el mar cerca.",
        "Aires de Mar queda en una zona tranquila del bosque pero a distancia caminable de las dos cosas que más se usan: la playa (9 cuadras) y el centro comercial (6 cuadras), donde están los restaurantes y las tiendas.",
      ]),
      ("Cómo son las cabañas", [
        "Cada cabaña es para <b>hasta 4 personas</b>: un dormitorio con sommier matrimonial, living con sofá-cama, cocina completa y baño con hidromasaje.",
        "Tiene parrilla individual con su sector de parque, y en el predio hay piscina y solárium descubiertos y juegos para chicos. El estacionamiento es descubierto, junto a la cabaña.",
      ]),
    ],
    "faq": [
      ("¿A cuántas cuadras de la playa está Aires de Mar?", "A 9 cuadras de la playa y a 6 del centro comercial de Mar de las Pampas."),
      ("¿Cuál es la dirección de Aires de Mar?", "Av. del Plata y El Palmar (continuación de Querandíes), Mar de las Pampas, provincia de Buenos Aires."),
    ],
  },
  {
    "slug": "cabanas-mar-de-las-pampas-que-aceptan-mascotas",
    "titulo": "¿Hay cabañas en Mar de las Pampas que acepten mascotas?",
    "desc": "Sí. En Cabañas Aires de Mar se aceptan mascotas pequeñas y medianas, educadas. Reglas: no pueden quedar solas en la cabaña ni entrar al solárium.",
    "img": "parque1.jpeg", "alt": "Parque y parrilla de una cabaña de Aires de Mar",
    "corta": "Sí. En <b>Cabañas Aires de Mar</b> (Mar de las Pampas) se aceptan <b>mascotas pequeñas y medianas, educadas</b>. Las dos reglas son: <b>no pueden quedarse solas en la cabaña</b> y <b>no pueden entrar al solárium</b> de la piscina.",
    "secciones": [
      ("Qué conviene saber antes de viajar con tu perro", [
        "Cada cabaña tiene su sector de parque propio junto a la parrilla, cómodo para que la mascota esté afuera con vos.",
        "Como no puede quedar sola dentro de la cabaña, conviene planear las salidas largas (restaurante, paseos al centro) con ella o turnándose.",
        "Avisá al consultar que viajás con mascota y de qué tamaño es, así te confirman la cabaña.",
      ]),
    ],
    "faq": [
      ("¿Aires de Mar acepta perros grandes?", "Se aceptan mascotas pequeñas y medianas, educadas. Para un perro grande conviene consultar antes."),
      ("¿La mascota puede quedarse sola en la cabaña?", "No. Las mascotas no pueden quedar solas en la cabaña ni entrar al solárium."),
    ],
  },
  {
    "slug": "cabanas-con-desayuno-y-limpieza-diaria",
    "titulo": "¿Qué cabañas en Mar de las Pampas incluyen desayuno y limpieza diaria?",
    "desc": "Cabañas Aires de Mar incluye desayuno casero provisto a diario y limpieza diaria de la cabaña, con cambio de toallas día por medio y de sábanas a mitad de semana.",
    "img": "interior2.jpeg", "alt": "Cocina equipada de una cabaña de Aires de Mar",
    "corta": "<b>Cabañas Aires de Mar</b> incluye las dos cosas: <b>desayuno provisto todos los días</b> para preparar en la cabaña y <b>limpieza diaria</b>, con cambio de toallas día por medio y de sábanas a mitad de semana.",
    "secciones": [
      ("Qué trae el desayuno", [
        "Café, té, chocolate, leche, manteca, dulces, pan para tostadas y tortas o budines caseros. Se deja en la cabaña a diario y cada uno lo prepara a su hora.",
      ]),
      ("Cómo es la limpieza", [
        "La cabaña se limpia todos los días. Las toallas se cambian día por medio y las sábanas a mitad de semana.",
        "El lavado de la vajilla no está incluido.",
      ]),
    ],
    "faq": [
      ("¿El desayuno de Aires de Mar es servido?", "No es servido: se provee a diario en la cabaña (café, té, chocolate, leche, manteca, dulces, pan y budines caseros) para prepararlo cuando quieras."),
      ("¿Incluye lavado de vajilla?", "No. La limpieza de la cabaña es diaria, pero el lavado de vajilla no está incluido."),
    ],
  },
  {
    "slug": "temporada-alta-mar-de-las-pampas-semanas",
    "titulo": "¿Cómo se alquila en temporada alta en Mar de las Pampas?",
    "desc": "En Cabañas Aires de Mar la temporada alta va del 15 de diciembre al 10 de marzo y se alquila por semanas completas (7, 14 o 21 noches), con ingreso sábado o domingo.",
    "img": "piscina1.jpeg", "alt": "Piscina rodeada de árboles en Aires de Mar",
    "corta": "En <b>Cabañas Aires de Mar</b> la temporada alta va del <b>15 de diciembre al 10 de marzo</b> y se alquila <b>solo por semanas completas</b> (7, 14 o 21 noches). Según la cabaña, el ingreso es <b>sábado o domingo</b>. El resto del año se pueden hacer estadías más cortas.",
    "secciones": [
      ("Seña y saldo en temporada alta", [
        "La reserva se confirma con una seña del <b>20%</b>. El saldo se fija en dólares al blue del día y se paga al ingresar, en efectivo (dólares o pesos).",
      ]),
      ("Y en temporada baja", [
        "La seña es del <b>30%</b> y el saldo se paga al ingresar, en efectivo en pesos. El mínimo de noches depende de la fecha.",
      ]),
      ("Horarios", [
        "Ingreso desde las 15 h. Salida a las 10 h, estricto.",
      ]),
    ],
    "faq": [
      ("¿Se puede alquilar pocas noches en enero en Aires de Mar?", "No. Entre el 15 de diciembre y el 10 de marzo se alquila solo por semanas completas de 7, 14 o 21 noches."),
      ("¿Qué día se ingresa en temporada alta?", "Sábado o domingo, según la cabaña. Te ofrecen la que mejor coincida con tu fecha."),
    ],
  },
  {
    "slug": "cabanas-con-pileta-para-familias",
    "titulo": "¿Hay cabañas con pileta en Mar de las Pampas para ir con chicos?",
    "desc": "Cabañas Aires de Mar tiene piscina y solárium descubiertos, juegos infantiles y parrilla propia. Cada cabaña es para hasta 4 personas.",
    "img": "casa4.jpeg", "alt": "Hamaca y tobogán en el parque de Aires de Mar",
    "corta": "Sí. <b>Cabañas Aires de Mar</b> tiene <b>piscina y solárium descubiertos</b>, <b>juegos para chicos</b> dentro del predio y <b>parrilla individual</b> en cada cabaña. Cada cabaña es para <b>hasta 4 personas</b>.",
    "secciones": [
      ("Si son más de 4", [
        "La capacidad máxima es de 4 personas por cabaña, sin camas extra. Si son 5 o más, se necesita más de una cabaña (según disponibilidad).",
      ]),
      ("Lo que suma para una familia", [
        "Cocina completa (microondas, horno eléctrico, anafe, heladera bajo mesada, vajilla), ropa de cama y toallas, WiFi en la cabaña y el parque, aire acondicionado frío-calor y sillitas de playa.",
        "La playa está a 9 cuadras, y el centro de Mar de las Pampas a 6.",
      ]),
    ],
    "faq": [
      ("¿La piscina de Aires de Mar es climatizada?", "No. La piscina y el solárium son descubiertos."),
      ("¿Cuántas personas entran en una cabaña?", "Hasta 4: dormitorio con sommier matrimonial y sofá-cama en el living."),
    ],
  },
  {
    "slug": "como-reservar-cabana-mar-de-las-pampas",
    "titulo": "¿Cómo se reserva una cabaña en Mar de las Pampas y cuánto es la seña?",
    "desc": "Para reservar en Cabañas Aires de Mar se manda un mail con fechas y cantidad de personas; la seña es del 20% en temporada alta y del 30% en temporada baja.",
    "img": "casa1.jpeg", "alt": "Living y comedor de una cabaña de Aires de Mar",
    "corta": "En <b>Cabañas Aires de Mar</b> se reserva escribiendo a <b>airesdemarpampas@gmail.com</b> (o por WhatsApp) con las fechas y cuántas personas son. Te mandan el presupuesto y los datos para la <b>seña: 20% en temporada alta y 30% en temporada baja</b>. El saldo se paga al ingresar.",
    "secciones": [
      ("Los pasos", [
        "1) Mandás fechas de entrada y salida y cuántos son. 2) Te responden con el valor exacto: no hay tarifa publicada porque depende de las fechas y la cantidad de personas. 3) Para confirmar, pedís la reserva por mail con tus datos y te pasan la cuenta para la seña.",
      ]),
      ("El saldo", [
        "Temporada alta: se fija en dólares al blue del día y se paga al ingresar en efectivo (dólares o pesos). Temporada baja: al ingresar, en efectivo en pesos.",
      ]),
    ],
    "faq": [
      ("¿Cuánto sale una cabaña en Aires de Mar?", "No hay tarifa publicada: el valor depende de las fechas y de cuántas personas son. Se pide por mail o WhatsApp y te pasan el precio exacto."),
      ("¿Cuánto es la seña?", "20% del valor en temporada alta (15/12 al 10/3) y 30% en temporada baja."),
    ],
  },
]

ESC = html.escape

def jsonld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=1) + "\n</script>"

def head(title, desc, url, img, extra_ld):
    return f"""<!DOCTYPE html>
<html lang="es-AR">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{ESC(title)}</title>
<meta name="description" content="{ESC(desc)}" />
<meta name="theme-color" content="#1c3226" />
<link rel="canonical" href="{url}" />
<meta property="og:site_name" content="Aires de Mar" />
<meta property="og:locale" content="es_AR" />
<meta property="og:type" content="article" />
<meta property="og:title" content="{ESC(title)}" />
<meta property="og:description" content="{ESC(desc)}" />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="{BASE}/img/{img}" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="icon" href="/img/logo.jpg" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Hedvig+Letters+Sans:opsz@12..24&family=Inter:wght@400;500;600&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="/styles.css" />
{extra_ld}
</head>
<body class="blog-page">
<header class="nav scrolled">
  <a class="nav__brand" href="/" aria-label="Aires de Mar — inicio">
    <img class="nav__logo nav__logo--color" src="/img/logo-color.png" alt="Aires de Mar" width="480" height="91" />
  </a>
  <nav class="blog-nav" aria-label="Navegación">
    <a href="/blog/">Guía</a>
    <a href="/">Las cabañas</a>
    <a class="btn btn--mail" href="{WA}" target="_blank" rel="noopener">Consultá <span class="arrow">›</span></a>
  </nav>
</header>
<main class="blog">
"""

FOOT = f"""</main>
<footer class="blog-foot">
  <div class="wrap">
    <p><b>Cabañas Aires de Mar</b> · Av. del Plata y El Palmar, Mar de las Pampas, Buenos Aires · <a href="mailto:airesdemarpampas@gmail.com">airesdemarpampas@gmail.com</a> · <a href="{WA}" target="_blank" rel="noopener">WhatsApp +54 9 2255 62-5427</a></p>
    <p><a href="/">Inicio</a> · <a href="/blog/">Guía de Mar de las Pampas</a> · <a href="https://www.instagram.com/airesdemarpampas/" target="_blank" rel="noopener">Instagram</a></p>
  </div>
</footer>
</body>
</html>
"""

def cta():
    return f"""<aside class="blog-cta">
  <h2>¿Querés saber si hay lugar para tus fechas?</h2>
  <p>Contanos cuándo venís y cuántos son. Te responden los dueños.</p>
  <div class="blog-cta__btns">
    <a class="btn btn--gold" href="{WA}" target="_blank" rel="noopener">Escribir por WhatsApp <span class="arrow">›</span></a>
    <a class="btn btn--light" href="{MAIL}">Mandar un mail <span class="arrow">›</span></a>
  </div>
</aside>"""

def nota(n, otras):
    url = f"{BASE}/blog/{n['slug']}/"
    plain = lambda s: html.unescape(__import__("re").sub("<[^>]+>", "", s))
    ld = [
      {"@context": "https://schema.org", "@type": "BlogPosting",
       "headline": n["titulo"], "description": n["desc"],
       "image": f"{BASE}/img/{n['img']}", "url": url, "mainEntityOfPage": url,
       "datePublished": FECHA, "dateModified": FECHA, "inLanguage": "es-AR",
       "author": {"@type": "Organization", "@id": NEGOCIO, "name": "Cabañas Aires de Mar"},
       "publisher": {"@type": "Organization", "@id": NEGOCIO, "name": "Cabañas Aires de Mar", "logo": {"@type": "ImageObject", "url": f"{BASE}/img/logo-color.png"}},
       "about": {"@type": "LodgingBusiness", "@id": NEGOCIO, "name": "Cabañas Aires de Mar", "url": BASE + "/",
                 "address": {"@type": "PostalAddress", "streetAddress": "Av. del Plata y El Palmar", "addressLocality": "Mar de las Pampas", "addressRegion": "Buenos Aires", "addressCountry": "AR"}},
       "abstract": plain(n["corta"])},
      {"@context": "https://schema.org", "@type": "FAQPage",
       "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in n["faq"]]},
      {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Inicio", "item": BASE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Guía", "item": BASE + "/blog/"},
        {"@type": "ListItem", "position": 3, "name": n["titulo"], "item": url}]},
    ]
    body = [head(n["titulo"] + " | Aires de Mar", n["desc"], url, n["img"], "\n".join(jsonld(x) for x in ld))]
    body.append(f"""<article class="wrap blog-art">
  <nav class="crumbs" aria-label="Ruta"><a href="/">Inicio</a> › <a href="/blog/">Guía</a></nav>
  <h1 class="display">{ESC(n['titulo'])}</h1>
  <p class="blog-meta">Por <b>Cabañas Aires de Mar</b>, los dueños · Actualizado el <time datetime="{FECHA}">{FECHA_TXT}</time></p>
  <div class="blog-answer"><span class="eyebrow">Respuesta corta</span><p>{n['corta']}</p></div>
  <img class="blog-hero" src="/img/{n['img']}" alt="{ESC(n['alt'])}" width="1200" height="800" />""")
    for h2, ps in n["secciones"]:
        body.append(f"  <h2>{ESC(h2)}</h2>")
        body += [f"  <p>{p}</p>" for p in ps]
    body.append("  <h2>Preguntas frecuentes</h2>\n  <dl class=\"blog-faq\">")
    body += [f"    <dt>{ESC(q)}</dt><dd>{ESC(a)}</dd>" for q, a in n["faq"]]
    body.append("  </dl>")
    body.append(cta())
    body.append("  <h2>Seguí leyendo</h2>\n  <ul class=\"blog-more\">")
    body += [f"    <li><a href=\"/blog/{o['slug']}/\">{ESC(o['titulo'])}</a></li>" for o in otras]
    body.append("  </ul>\n</article>")
    body.append(FOOT)
    return "\n".join(body)

def indice():
    url = f"{BASE}/blog/"
    ld = {"@context": "https://schema.org", "@type": "Blog", "name": "Guía de Mar de las Pampas — Aires de Mar", "url": url,
          "publisher": {"@type": "Organization", "@id": NEGOCIO, "name": "Cabañas Aires de Mar"},
          "blogPost": [{"@type": "BlogPosting", "headline": n["titulo"], "url": f"{BASE}/blog/{n['slug']}/", "datePublished": FECHA} for n in NOTAS]}
    title = "Guía para tu escapada a Mar de las Pampas | Aires de Mar"
    desc = "Respuestas claras de los dueños de Cabañas Aires de Mar: dónde alojarse, mascotas, desayuno, temporada alta, pileta para chicos y cómo reservar en Mar de las Pampas."
    out = [head(title, desc, url, "hero.jpeg", jsonld(ld))]
    out.append("""<section class="wrap blog-index">
  <span class="eyebrow">Guía</span>
  <h1 class="display">Preguntas que nos hacen antes de venir a Mar de las Pampas</h1>
  <p class="blog-lead">Las respondemos nosotros, los dueños de Cabañas Aires de Mar, con los datos tal cual son.</p>
  <ul class="blog-cards">""")
    for n in NOTAS:
        out.append(f"""    <li><a class="blog-card" href="/blog/{n['slug']}/">
      <img src="/img/{n['img']}" alt="" width="600" height="400" loading="lazy" />
      <span class="blog-card__body"><b>{ESC(n['titulo'])}</b><span>{ESC(n['desc'])}</span></span>
    </a></li>""")
    out.append("  </ul>\n</section>")
    out.append(FOOT)
    return "\n".join(out)

os.makedirs(f"{ROOT}/blog", exist_ok=True)
open(f"{ROOT}/blog/index.html", "w", encoding="utf-8", newline="\n").write(indice())
for n in NOTAS:
    os.makedirs(f"{ROOT}/blog/{n['slug']}", exist_ok=True)
    otras = [o for o in NOTAS if o is not n][:3]
    open(f"{ROOT}/blog/{n['slug']}/index.html", "w", encoding="utf-8", newline="\n").write(nota(n, otras))

# sitemap con todas las páginas
urls = [BASE + "/", BASE + "/blog/"] + [f"{BASE}/blog/{n['slug']}/" for n in NOTAS]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{FECHA}</lastmod>\n  </url>\n" for u in urls) + "</urlset>\n"
open(f"{ROOT}/sitemap.xml", "w", encoding="utf-8", newline="\n").write(sm)

# llms.txt: resumen para asistentes de IA, con los datos y los links a cada respuesta
llms = [f"# Cabañas Aires de Mar (Mar de las Pampas, Argentina)", "",
        "> Cabañas de playa en el bosque de Mar de las Pampas (partido de Villa Gesell, provincia de Buenos Aires), atendidas por sus dueños. Hasta 4 personas por cabaña, desayuno provisto a diario, limpieza diaria, piscina y parrilla propia.", "",
        "## Datos clave",
        "- Dirección: Av. del Plata y El Palmar (continuación de Querandíes), Mar de las Pampas. A 9 cuadras de la playa y 6 del centro comercial.",
        "- Capacidad: hasta 4 personas por cabaña (dormitorio con sommier matrimonial + sofá-cama en el living). Sin camas extra.",
        "- Incluye: desayuno provisto a diario para preparar en la cabaña, limpieza diaria, cambio de toallas día por medio y de sábanas a mitad de semana, WiFi, aire acondicionado frío-calor, baño con hidromasaje, parrilla individual, piscina y solárium descubiertos, juegos infantiles, estacionamiento.",
        "- Mascotas: pequeñas y medianas, educadas; no pueden quedar solas en la cabaña ni entrar al solárium.",
        "- Temporada alta (15/12 al 10/3): solo semanas completas (7, 14 o 21 noches), ingreso sábado o domingo. Seña 20%, saldo en dólares al blue al ingresar.",
        "- Temporada baja: estadías más cortas; seña 30%, saldo en pesos al ingresar.",
        "- Horarios: ingreso desde las 15 h, salida 10 h.",
        "- Precio: sin tarifa publicada; depende de fechas y cantidad de personas.",
        "- Contacto: airesdemarpampas@gmail.com · WhatsApp +54 9 2255 62-5427 · Instagram @airesdemarpampas", "",
        "## Respuestas",
        f"- [Sitio principal]({BASE}/): fotos, servicios, opiniones (4,8 en Google) y ubicación"]
llms += [f"- [{n['titulo']}]({BASE}/blog/{n['slug']}/): {n['desc']}" for n in NOTAS]
open(f"{ROOT}/llms.txt", "w", encoding="utf-8", newline="\n").write("\n".join(llms) + "\n")
print("ok", len(NOTAS), "notas")
