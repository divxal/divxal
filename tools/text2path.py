"""Convierte texto a paths SVG exactos (sin depender de fuentes en el cliente).

GitHub sirve los SVG del README como <img>: no cargan fuentes externas, asi que
todo texto se dibuja como path con las tipografias reales del portfolio
(Syne = display, Cormorant Garamond Italic = cuerpo, JetBrains Mono = terminal).
"""
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen

HERE = __file__.rsplit("\\", 1)[0].rsplit("/", 1)[0]
FONTS = {
    "syne": ("Syne.ttf", "wght"),
    "cormorant": ("CormorantItalic.ttf", "wght"),
    "mono": ("JetBrainsMono.ttf", "wght"),
}


class Face:
    def __init__(self, font_key, wght=None, fonts_dir=None):
        import os

        fname, axis = FONTS[font_key]
        base = fonts_dir or os.path.join(HERE, "fonts")
        path = os.path.join(base, fname)
        f = TTFont(path)
        if wght is not None and "fvar" in f:
            f = instantiateVariableFont(f, {axis: wght})
        self.upm = f["head"].unitsPerEm
        self.cmap = f.getBestCmap()
        self.gs = f.getGlyphSet()
        self.hmtx = f["hmtx"]

    def glyph(self, ch):
        """devuelve (path_d, ancho_em) en unidades de em (1.0 = font-size)."""
        gname = self.cmap.get(ord(ch))
        if gname is None:
            return "", 0.5
        pen = SVGPathPen(self.gs)
        self.gs[gname].draw(pen)
        return pen.getCommands(), self.hmtx[gname][0] / self.upm

    def measure(self, text, size, tracking=0.0):
        w = 0.0
        for ch in text:
            w += self.glyph(ch)[1] * size + tracking * size
        return w - (tracking * size if text else 0)

    def paths(self, text, size, x, y, tracking=0.0):
        """lista de (ch, d, x_absoluta) con baseline en y."""
        out, cx = [], x
        for ch in text:
            d, adv_em = self.glyph(ch)
            if d:
                out.append((ch, d, cx))
            cx += adv_em * size + tracking * size
        return out

    def text(self, text, size, x, y, fill="#fff", tracking=0.0, opacity=None,
             cls=None, extra=""):
        """<g> con el texto ya centrado en paths; x = borde izquierdo."""
        s = size / self.upm
        body = []
        for ch, d, cx in self.paths(text, size, x, y, tracking):
            body.append(f'<path d="{d}" transform="translate({cx:.2f} {y}) scale({s:.6f} {-s:.6f})"/>')
        attrs = f' fill="{fill}"'
        if opacity is not None:
            attrs += f' opacity="{opacity}"'
        if cls:
            attrs += f' class="{cls}"'
        return f"  <g{attrs}{extra}>\n    " + "\n    ".join(body) + "\n  </g>"

    def text_centered(self, text, size, cx, y, **kw):
        w = self.measure(text, size, kw.get("tracking", 0.0))
        return self.text(text, size, cx - w / 2, y, **kw)
