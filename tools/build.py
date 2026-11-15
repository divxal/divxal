"""Genera los SVG del perfil de GitHub de divxal con la identidad del portfolio.

Negro puro, Syne (display, tracking 0.5em), Cormorant Garamond italic (cuerpo),
JetBrains Mono (terminal), hairline #1f1f1f, verde #28c840 para estados.
Todo el texto va como paths -> el SVG no depende de fuentes externas en GitHub.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from text2path import Face  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")
PREV = os.path.join(ROOT, "_build", "preview")
STATIC = False

WHITE, GREY, GREY2, GREY3, LINE = "#ffffff", "#bbbbbb", "#888888", "#555555", "#1f1f1f"
GREEN = "#28c840"

SYNE_800 = Face("syne", 800)
SYNE_400 = Face("syne", 400)
CORM_300 = Face("cormorant", 300)
MONO_400 = Face("mono", 400)


def style(css):
    return "" if STATIC else f"<style>\n{css}\n</style>\n"


def _round_numbers(svg):
    """recorta precision numerica SOLO en los path data: menos KB, mismo dibujo.

    (Redondear todo el documento rompia los `scale(0.0105)` de las fuentes.)
    """
    import re

    def fix(m):
        d = re.sub(r"-?\d+\.\d{2,}", lambda mm: f"{round(float(mm.group(0)), 1):g}", m.group(1))
        return f'd="{d}"'

    return re.sub(r'd="([^"]*)"', fix, svg)


def wrap(w, h, body, cls="", title=""):
    return _round_numbers(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{title}" class="{cls}">\n'
        f"{body}</svg>\n"
    )


# ---------------------------------------------------------------- banner
def banner():
    W, H = 1280, 400
    cx = W / 2
    b = []
    b.append(f"""  <defs>
    <radialGradient id="glow" cx="50%" cy="42%" r="62%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.085"/>
      <stop offset="55%" stop-color="#ffffff" stop-opacity="0.02"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="50%" stop-color="#ffffff" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0H0V40" fill="none" stroke="#ffffff" stroke-opacity="0.03" stroke-width="1"/>
    </pattern>
  </defs>""")
    b.append(f'  <rect width="{W}" height="{H}" fill="#000000"/>')
    b.append(f'  <rect width="{W}" height="{H}" fill="url(#grid)"/>')
    b.append(f'  <rect width="{W}" height="{H}" fill="url(#glow)"/>')
    b.append(f'  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" fill="none" stroke="{LINE}"/>')

    # esquinas tecnicas
    L, S = 18, "#3a3a3a"
    corners = [(1, 1, 1, 1), (W - 1, 1, -1, 1), (1, H - 1, 1, -1), (W - 1, H - 1, -1, -1)]
    for x, y, dx, dy in corners:
        b.append(f'  <path d="M{x + dx*L} {y}h{-dx*L}v{dy*L}" fill="none" stroke="{S}" stroke-width="1"/>')

    # fila meta superior
    b.append(MONO_400.text("43.3623\xb0 N / 8.4117\xb0 W", 10.5, 40, 46, fill=GREY3, tracking=0.16))
    b.append(MONO_400.text("A CORU\xd1A \xb7 GALICIA \xb7 ES", 10.5, W - 40 - MONO_400.measure("A CORU\xd1A \xb7 GALICIA \xb7 ES", 10.5, 0.16), 46, fill=GREY3, tracking=0.16))
    b.append(f'  <path d="M40 64H{W-40}" stroke="{LINE}" stroke-width="1"/>')

    # eyebrow
    eb = "ARQUITECTO DE SISTEMAS"
    b.append(SYNE_400.text_centered(eb, 12.5, cx, 126, fill=GREY2, tracking=0.52))

    # wordmark con entrada letra a letra
    word, size, track = "DIVXAL", 150, 0.03
    wword = SYNE_800.measure(word, size, track)
    x0 = cx - wword / 2
    ybase = 262
    # resplandor detras
    glow_letters = []
    for i, (ch, d, gx) in enumerate(SYNE_800.paths(word, size, x0, ybase, track)):
        s = size / SYNE_800.upm
        glow_letters.append(
            f'<path d="{d}" transform="translate({gx:.2f} {ybase}) scale({s:.6f} {-s:.6f})"/>'
        )
    filt = "" if STATIC else ' filter="url(#soft)"'
    b.append(f"""  <defs>
    <filter id="soft" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="30"/>
    </filter>
  </defs>""")
    b.append(f'  <g fill="#ffffff" opacity="0.10"{filt} class="halo">' + "".join(glow_letters) + "</g>")

    for i, (ch, d, gx) in enumerate(SYNE_800.paths(word, size, x0, ybase, track)):
        s = size / SYNE_800.upm
        style_attr = "" if STATIC else f' style="animation-delay:{0.45 + i * 0.085:.3f}s"'
        b.append(
            f'  <g class="lt"{style_attr}><path d="{d}" fill="#ffffff" '
            f'transform="translate({gx:.2f} {ybase}) scale({s:.6f} {-s:.6f})"/></g>'
        )

    # subrayado que se dibuja
    half = wword / 2
    b.append(f'  <path d="M{cx - half:.1f} 292h{wword:.1f}" stroke="{LINE}" stroke-width="1"/>')

    # tagline
    tag = "sistemas, software e infraestructura \u2014 pieza a pieza"
    b.append(CORM_300.text_centered(tag, 34, cx, 336, fill=GREY, tracking=0.01))

    # fila inferior
    dot = "" if STATIC else '<circle class="pulse" cx="46" cy="367" r="3.4" fill="#28c840"/>'
    if STATIC:
        dot = f'<circle cx="46" cy="367" r="3.4" fill="{GREEN}"/>'
    b.append(dot)
    b.append(SYNE_400.text("DISPONIBLE PARA PROYECTOS", 10.5, 60, 371, fill=GREY2, tracking=0.42))
    right = "GITHUB.COM/DIVXAL"
    b.append(MONO_400.text(right, 10.5, W - 40 - MONO_400.measure(right, 10.5, 0.18), 371, fill=GREY3, tracking=0.18))

    # barrido de escaner
    if not STATIC:
        b.append(f'  <rect class="scan" x="0" y="0" width="{W}" height="1" fill="url(#sweep)"/>')

    css = """
.lt{opacity:0;transform-box:fill-box;transform-origin:50% 92%;animation:ltIn .95s cubic-bezier(.16,1,.3,1) both}
@keyframes ltIn{from{opacity:0;transform:translateY(72px) scale(.94)}to{opacity:1;transform:translateY(0) scale(1)}}
.halo{animation:halo 7s ease-in-out infinite}
@keyframes halo{0%,100%{opacity:.07}50%{opacity:.16}}
.pulse{animation:pulse 2.2s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
@keyframes pulse{0%,100%{opacity:.45;transform:scale(.85)}50%{opacity:1;transform:scale(1.15)}}
.scan{animation:scan 7.5s linear infinite}
@keyframes scan{0%{transform:translateY(-2px);opacity:0}8%{opacity:.5}92%{opacity:.5}100%{transform:translateY(400px);opacity:0}}
"""
    body = "\n".join(b) + "\n" + style(css)
    return wrap(W, H, body, title="DIVXAL \u2014 arquitecto de sistemas")


# ---------------------------------------------------------------- terminal
def terminal():
    W, H = 1040, 500
    size, lh = 15, 27
    x0, y0 = 32, 78
    lines = [
        ("cmd", [("divxal@atlas", GREY2), (":", GREY3), ("~", WHITE), ("$ ", GREY3), ("whoami", WHITE)]),
        ("out", [("abel ", WHITE), ("\u00b7 arquitecto de sistemas \u00b7 a coru\u00f1a, es", GREY3)]),
        ("blank", []),
        ("cmd", [("divxal@atlas", GREY2), (":", GREY3), ("~", WHITE), ("$ ", GREY3), ("ls proyectos/", WHITE)]),
    ]
    # columnas alineadas como un `ls` de verdad
    dirs = [("atlas-center/", WHITE), ("typokawaii/", GREY2), ("velion/", GREY2), ("orion/", GREY2),
            ("epsilon/", GREY2), ("legion/", GREY2), ("atlas-bot/", WHITE)]
    colw = max(len(n) for n, _ in dirs) + 3
    for row in (dirs[0:4], dirs[4:7]):
        lines.append(("out", [(n.ljust(colw), c) for n, c in row]))
    lines += [
        ("blank", []),
        ("cmd", [("divxal@atlas", GREY2), (":", GREY3), ("~", WHITE), ("$ ", GREY3), ("cat stack.txt", WHITE)]),
        ("out", [("python  c  c++  rust  typescript  sql  bash", GREY2)]),
        ("out", [("linux  arch  lfs  docker  nginx  systemd  git", GREY2)]),
        ("blank", []),
        ("cmd", [("divxal@atlas", GREY2), (":", GREY3), ("~", WHITE), ("$ ", GREY3), ("git log -1 --oneline", WHITE)]),
        ("out", [("a41f9c2  ", GREY3), ("atlas-center: IPC en lote cada 500 ms", GREY2)]),
        ("blank", []),
        ("cmd", [("divxal@atlas", GREY2), (":", GREY3), ("~", WHITE), ("$ ", GREY3)]),
    ]

    T = 20.0  # ciclo en segundos
    b = []
    defs = ['  <defs>', '    <linearGradient id="tglow" x1="0" y1="0" x2="0" y2="1">',
            '      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.05"/>',
            '      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>', '    </linearGradient>']
    css_lines = []

    b.append(f'  <rect width="{W}" height="{H}" rx="12" fill="#050505"/>')
    b.append(f'  <rect width="{W}" height="{H}" rx="12" fill="url(#tglow)"/>')
    b.append(f'  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="#242424"/>')
    # barra de titulo
    b.append(f'  <path d="M0 45h{W}" stroke="#191919" stroke-width="1"/>')
    for i, col in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
        b.append(f'  <circle cx="{28 + i*20}" cy="23" r="5.5" fill="{col}" opacity="0.85"/>')
    ttl = "divxal@atlas \u2014 zsh"
    b.append(MONO_400.text_centered(ttl, 11.5, W / 2, 27, fill=GREY3, tracking=0.14))
    rgt = "120\xd734"
    b.append(MONO_400.text(rgt, 10.5, W - 28 - MONO_400.measure(rgt, 10.5, 0.1), 27, fill="#3a3a3a", tracking=0.1))

    # lineas
    t = 0.55
    charw = MONO_400.measure("M", size)  # mono: ancho fijo
    for idx, (kind, segs) in enumerate(lines):
        y = y0 + idx * lh
        if kind == "blank":
            continue
        total_chars = sum(len(s) for s, _ in segs)
        parts = []
        cx = x0
        for text, col in segs:
            if text:
                parts.append(MONO_400.text(text, size, cx, y, fill=col, tracking=0))
            cx += charw * len(text)
        line_w = cx - x0 + 4
        if idx == len(lines) - 1:
            last_end = cx
        clip_id = f"cl{idx}"
        if not STATIC:
            defs.append(f'    <clipPath id="{clip_id}"><rect class="tw tw{idx}" x="{x0}" y="{y - size:.1f}" '
                        f'width="{line_w + 8:.1f}" height="{size*1.5:.1f}"/></clipPath>')
            if kind == "cmd":
                dur = 0.30 + 0.045 * total_chars
            else:
                dur = 0.12 + 0.012 * total_chars
            a = t / T * 100
            c = (t + dur) / T * 100
            d = 0.88 * 100
            e = 0.915 * 100
            css_lines.append(
                f".tw{idx}{{transform-box:fill-box;transform-origin:0 0;"
                f"animation:ty{idx} {T}s linear infinite}}"
                f"@keyframes ty{idx}{{0%{{transform:scaleX(0)}}{a:.2f}%{{transform:scaleX(0)}}"
                f"{c:.2f}%{{transform:scaleX(1)}}{d:.2f}%{{transform:scaleX(1)}}"
                f"{e:.2f}%{{transform:scaleX(0)}}100%{{transform:scaleX(0)}}}}"
            )
            parts = [f'  <g clip-path="url(#{clip_id})">' + "".join(parts) + "</g>"]
            t += dur + (0.10 if kind == "cmd" else 0.05)
        b.extend(parts)

    # cursor al final
    cy = y0 + (len(lines) - 1) * lh
    if not STATIC:
        css_lines.append(f".cur{{animation:cur {T}s steps(1) infinite}}"
                         f"@keyframes cur{{0%,62%{{opacity:1}}62.01%,88%{{opacity:0}}88.01%,91.5%{{opacity:1}}"
                         f"91.6%,100%{{opacity:0}}}}")
    b.append(f'  <rect class="cur" x="{last_end + 1:.1f}" y="{cy - size + 2:.1f}" width="{charw - 1:.1f}" height="{size + 3}" fill="{WHITE}" opacity="0.85"/>')

    defs.append("  </defs>")
    body = "\n".join(defs + b) + "\n" + style("\n".join(css_lines))
    return wrap(W, H, body, title="terminal de divxal")


# ---------------------------------------------------------------- metodo
def metodo():
    W, H = 1280, 272
    cols = [
        ("01", "SISTEMA ANTES QUE FRAMEWORK",
         ["Antes de tirar de una librería miro", "qué hace el kernel, el driver o el protocolo.", "Entender el suelo primero."]),
        ("02", "SI NO LO MIDO, NO EXISTE",
         ["IPC en lote, caché por TTL, cero polling", "gratis. Si el dato no está medido, es", "una opinión."]),
        ("03", "EL TALLER NO ES EL ESCAPARATE",
         ["Los prototipos aguantan meses de pruebas", "antes de publicarse. Lo que sale de aquí", "sostiene uso real."]),
    ]
    b = [f'  <rect width="{W}" height="{H}" fill="#000000"/>',
         f'  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" fill="none" stroke="{LINE}"/>']
    gap, margin = 44, 48
    colw = (W - margin * 2 - gap * 2) / 3
    for i, (num, title, body) in enumerate(cols):
        x = margin + i * (colw + gap)
        if i:
            b.append(f'  <path d="M{x - gap/2:.1f} 34V{H-34}" stroke="{LINE}" stroke-width="1"/>')
        b.append(MONO_400.text(num, 11.5, x, 74, fill="#4a4a4a", tracking=0.18))
        b.append(SYNE_400.text(title, 13, x, 112, fill=WHITE, tracking=0.24))
        b.append(f'  <path d="M{x:.1f} 132h58" stroke="{GREY3}" stroke-width="1"/>')
        for j, line in enumerate(body):
            b.append(CORM_300.text(line, 23, x, 174 + j * 29, fill=GREY2, tracking=0.005))
    return wrap(W, H, "\n".join(b), title="metodo de trabajo")


# ---------------------------------------------------------------- marquee
def marquee():
    W, H = 1280, 54
    phrase = ("SISTEMAS \u00b7 INGENIER\u00cdA INVERSA \u00b7 VISI\u00d3N ARTIFICIAL \u00b7 AUTOMATIZACI\u00d3N \u00b7 "
              "INTELIGENCIA ARTIFICIAL \u00b7 SOFTWARE \u00b7 INFRAESTRUCTURA \u00b7 ")
    size, track = 11.5, 0.4
    wphrase = SYNE_400.measure(phrase, size, track)
    reps = int(W * 2 / wphrase) + 2
    inner = []
    x = 0
    for _ in range(reps):
        inner.append(SYNE_400.text(phrase, size, x, 32, fill=GREY3, tracking=track))
        x += wphrase
    total_w = x
    css = "" if STATIC else """
.mq{animation:mq 34s linear infinite}
@keyframes mq{from{transform:translateX(0)}to{transform:translateX(-%.1fpx)}}
""" % (wphrase,)
    b = [f'  <path d="M0 0.5h{W}M0 {H-0.5}h{W}" stroke="#8a8a8a" stroke-opacity="0.3" stroke-width="1"/>',
         f'  <g class="mq">' + "".join(inner) + "</g>"]
    body = "\n".join(b) + "\n" + style(css)
    return wrap(W, H, body, title="stack y disciplinas")


# ---------------------------------------------------------------- etiquetas de seccion
def section(num, label, w=1280, h=40):
    b = []
    b.append(MONO_400.text(num, 12, 0, 22, fill="#6a6a6a", tracking=0.16))
    lab_w = SYNE_400.measure(label, 12.5, 0.44)
    b.append(SYNE_400.text(label, 12.5, 46, 23, fill="#9a9a9a", tracking=0.44))
    x_line = 46 + lab_w + 26
    b.append(f'  <path d="M{x_line:.1f} 17H{w}" stroke="#8a8a8a" stroke-opacity="0.3" stroke-width="1"/>')
    return wrap(w, h, "\n".join(b), title=label)


def main():
    global STATIC
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(PREV, exist_ok=True)
    files = {
        "banner.svg": banner(),
        "terminal.svg": terminal(),
        "marquee.svg": marquee(),
        "sec-identidad.svg": section("01", "IDENTIDAD"),
        "sec-proyectos.svg": section("02", "PROYECTOS"),
        "sec-stack.svg": section("03", "STACK"),
        "metodo.svg": metodo(),
        "sec-metodo.svg": section("04", "MÉTODO"),
        "sec-contacto.svg": section("05", "CONTACTO"),
    }
    for name, content in files.items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
            fh.write(content)
        if name in ("banner.svg", "terminal.svg", "marquee.svg", "sec-proyectos.svg"):
            STATIC = True
            stat = {"banner.svg": banner, "terminal.svg": terminal,
                    "marquee.svg": marquee, "sec-proyectos.svg": lambda: section("02", "PROYECTOS")}[name]()
            STATIC = False
            with open(os.path.join(PREV, name), "w", encoding="utf-8") as fh:
                fh.write(stat)
        print(f"{name:22} {len(content)/1024:6.1f} KB")
    print("wordmark DIVXAL width:", round(SYNE_800.measure("DIVXAL", 150, 0.03), 1))


if __name__ == "__main__":
    main()
