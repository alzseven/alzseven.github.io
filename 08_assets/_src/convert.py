"""pptx -> per-slide absolutely positioned HTML fragments (JSON).
Coordinates: 1px = 9525 EMU (slide = 2000 x 1124).
"""
import sys, json, os, re, html
sys.stdout.reconfigure(encoding='utf-8')
from pptx import Presentation
from lxml import etree

NS = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main',
}
E = 9525.0
PT = 12700 / 9525.0  # px per pt
SCHEME = {'tx1': '000000', 'bg1': 'FFFFFF', 'dk1': '000000', 'lt1': 'FFFFFF',
          'tx2': '1F497D', 'bg2': 'EEECE1', 'dk2': '1F497D', 'lt2': 'EEECE1',
          'accent1': '4F81BD', 'accent2': 'C0504D', 'accent3': '9BBB59',
          'accent4': '8064A2', 'accent5': '4BACC6', 'accent6': 'F79646'}


def q(el, path):
    return el.find(path, NS)


def qa(el, path):
    return el.findall(path, NS)


def color_of(fill_parent):
    """fill_parent: element containing a:solidFill. returns (hex, alpha) or None"""
    if fill_parent is None:
        return None
    sf = q(fill_parent, 'a:solidFill')
    if sf is None:
        return None
    c = sf[0]
    if c.tag.endswith('srgbClr'):
        hx = c.get('val')
    elif c.tag.endswith('schemeClr'):
        hx = SCHEME.get(c.get('val'), 'FFFFFF')
    elif c.tag.endswith('sysClr'):
        hx = c.get('lastClr', '000000')
    else:
        hx = 'FFFFFF'
    a = 1.0
    al = q(c, 'a:alpha')
    if al is not None:
        a = int(al.get('val')) / 100000
    lm, lo = q(c, 'a:lumMod'), q(c, 'a:lumOff')
    if lm is not None or lo is not None:
        r, g, b = (int(hx[i:i + 2], 16) for i in (0, 2, 4))
        m = int(lm.get('val')) / 100000 if lm is not None else 1
        o = int(lo.get('val')) / 100000 if lo is not None else 0
        r, g, b = (min(255, int(v * m + 255 * o)) for v in (r, g, b))
        hx = '%02X%02X%02X' % (r, g, b)
    return hx, a


def rgba(c):
    hx, a = c
    r, g, b = (int(hx[i:i + 2], 16) for i in (0, 2, 4))
    return f'rgba({r},{g},{b},{a:.2f})' if a < 1 else f'#{hx}'


def weight_of(face):
    m = re.search(r'(\d)\s', face or '')
    return int(m.group(1)) * 100 if m else None


class Conv:
    def __init__(self, slide):
        self.slide = slide
        self.rels = {r.rId: os.path.basename(r.target_ref) for r in slide.part.rels.values()}
        self.assets = set()

    def xfrm(self, el):
        x = q(el, './/a:xfrm') if el.tag.endswith('grpSp') is False else None
        return x

    def box(self, el):
        sppr = el.find('p:spPr', NS)
        if sppr is None:
            sppr = el.find('p:grpSpPr', NS)
        xf = q(sppr, 'a:xfrm') if sppr is not None else None
        if xf is None:
            xf = el.find('p:xfrm', NS)
        off, ext = q(xf, 'a:off'), q(xf, 'a:ext')
        b = dict(x=int(off.get('x')), y=int(off.get('y')), w=int(ext.get('cx')), h=int(ext.get('cy')),
                 rot=int(xf.get('rot', 0)) / 60000, fh=xf.get('flipH') == '1', fv=xf.get('flipV') == '1')
        return b, xf

    def style_box(self, b, tf):
        x, y, w, h = tf(b)
        s = f'left:{x:.1f}px;top:{y:.1f}px;width:{w:.1f}px;height:{h:.1f}px;'
        t = []
        if b['rot']:
            t.append(f'rotate({b["rot"]:.2f}deg)')
        if b['fh']:
            t.append('scaleX(-1)')
        if b['fv']:
            t.append('scaleY(-1)')
        if t:
            s += 'transform:' + ' '.join(t) + ';'
        return s

    def walk(self, parent, tf, out, depth=0):
        for el in parent:
            tag = etree.QName(el).localname
            if tag in ('nvGrpSpPr', 'grpSpPr'):
                continue
            nv = el.find('.//p:cNvPr', NS)
            sid = nv.get('id') if nv is not None else '?'
            name = nv.get('name') if nv is not None else ''
            if tag == 'grpSp':
                b, xf = self.box(el)
                cho, che = q(xf, 'a:chOff'), q(xf, 'a:chExt')
                cx, cy = int(cho.get('x')), int(cho.get('y'))
                cw, ch = max(1, int(che.get('cx'))), max(1, int(che.get('cy')))
                sx, sy = b['w'] / cw, b['h'] / ch
                if b['rot'] or b['fh'] or b['fv']:
                    # wrapper rotated about group centre; children relative to group box
                    gx, gy, gw, gh = tf(b)
                    inner = []
                    def tf2(bb, cx=cx, cy=cy, sx=sx, sy=sy):
                        return ((bb['x'] - cx) * sx / E, (bb['y'] - cy) * sy / E,
                                bb['w'] * sx / E, bb['h'] * sy / E)
                    self.walk(el, tf2, inner, depth + 1)
                    st = self.style_box(b, tf)
                    out.append(dict(id=sid, name=name, kind='group',
                                    html=f'<div class="el grp" data-id="{sid}" style="{st}">' + ''.join(i['html'] for i in inner) + '</div>',
                                    children=[i['id'] for i in inner]))
                else:
                    def tf3(bb, cx=cx, cy=cy, sx=sx, sy=sy, b=b, tf=tf):
                        nb = dict(x=b['x'] + (bb['x'] - cx) * sx, y=b['y'] + (bb['y'] - cy) * sy,
                                  w=bb['w'] * sx, h=bb['h'] * sy)
                        return tf(nb)
                    inner = []
                    self.walk(el, tf3, inner, depth + 1)
                    out.append(dict(id=sid, name=name, kind='group',
                                    html=f'<div class="el-g" data-id="{sid}">' + ''.join(i['html'] for i in inner) + '</div>',
                                    children=[i['id'] for i in inner]))
                continue
            if tag == 'pic' or tag == 'sp' or tag == 'cxnSp':
                b, xf = self.box(el)
                out.append(self.shape(el, tag, sid, name, b, tf))
            elif tag == 'graphicFrame':
                b, xf = self.box(el)
                out.append(self.table(el, sid, name, b, tf))

    def blip_img(self, bf, b, tf, extra_style='', cls='img'):
        blip = q(bf, 'a:blip')
        rid = blip.get('{%s}embed' % NS['r'])
        fn = self.rels.get(rid)
        self.assets.add(fn)
        op = 1
        am = q(blip, 'a:alphaModFix')
        if am is not None:
            op = int(am.get('amt', 100000)) / 100000
        src = q(bf, 'a:srcRect')
        l = t = r = bt = 0
        if src is not None:
            l, t, r, bt = (int(src.get(k, 0)) / 100000 for k in ('l', 't', 'r', 'b'))
        x, y, w, h = tf(b)
        fr = q(bf, 'a:stretch/a:fillRect')
        fl = ft = frr = fb = 0
        if fr is not None:
            fl, ft, frr, fb = (int(fr.get(k, 0)) / 100000 for k in ('l', 't', 'r', 'b'))
        fx, fy, fw, fh = fl * w, ft * h, w * (1 - fl - frr), h * (1 - ft - fb)
        iw, ih = fw / max(1e-6, 1 - l - r), fh / max(1e-6, 1 - t - bt)
        img = f'<img src="@@{fn}" style="left:{fx - l * iw:.1f}px;top:{fy - t * ih:.1f}px;width:{iw:.1f}px;height:{ih:.1f}px" alt="">'
        return fn, op, img

    def geom_radius(self, sppr, w, h):
        g = q(sppr, 'a:prstGeom') if sppr is not None else None
        if g is None:
            return ''
        p = g.get('prst')
        if p == 'ellipse':
            return 'border-radius:50%;'
        if p in ('roundRect',):
            adj = q(g, 'a:avLst/a:gd')
            a = int(re.search(r'\d+', adj.get('fmla')).group()) / 100000 if adj is not None else 0.16667
            return f'border-radius:{a * min(w, h):.1f}px;'
        if p == 'round2SameRect':
            adj = q(g, 'a:avLst/a:gd')
            a = int(re.search(r'\d+', adj.get('fmla')).group()) / 100000 if adj is not None else 0.16667
            rr = a * min(w, h)
            return f'border-radius:{rr:.1f}px {rr:.1f}px 0 0;'
        return ''

    def shape(self, el, tag, sid, name, b, tf):
        sppr = el.find('p:spPr', NS)
        x, y, w, h = tf(b)
        st = self.style_box(b, tf)
        # picture / video
        if tag == 'pic':
            bf = el.find('p:blipFill', NS)
            fn, op, img = self.blip_img(bf, b, tf)
            vid = el.find('.//a:videoFile', NS)
            rad = self.geom_radius(sppr, w, h)
            if op < 1:
                st += f'opacity:{op:.2f};'
            ln = self.line_css(sppr)
            if vid is not None:
                m = el.find('.//p14:media', NS)
                vf = self.rels.get(m.get('{%s}embed' % NS['r'])) if m is not None else None
                self.assets.add(vf)
                v = img.replace('<img src="@@%s"' % fn, f'<video src="@@{vf}" poster="@@{fn}" muted loop playsinline preload="auto"').replace(' alt="">', '></video>')
                return dict(id=sid, name=name, kind='video', html=f'<div class="el pic" data-id="{sid}" style="{st}{rad}{ln}">{v}</div>')
            return dict(id=sid, name=name, kind='pic', html=f'<div class="el pic" data-id="{sid}" style="{st}{rad}{ln}">{img}</div>')
        # connector line
        if tag == 'cxnSp':
            lc = self.line_color(sppr) or ('FFFFFF', 1)
            lw = self.line_w(sppr)
            x1, y1, x2, y2 = 0, 0, w, h
            if b['fh']:
                x1, x2 = x2, x1
            if b['fv']:
                y1, y2 = y2, y1
            svg = (f'<svg class="el" data-id="{sid}" style="left:{x:.1f}px;top:{y:.1f}px;overflow:visible" width="{max(w, 1):.1f}" height="{max(h, 1):.1f}">'
                   f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{rgba(lc)}" stroke-width="{lw:.1f}"/></svg>')
            return dict(id=sid, name=name, kind='line', html=svg)
        # sp: freeform with image fill / autoshape / textbox
        bf = sppr.find('a:blipFill', NS) if sppr is not None else None
        inner = ''
        bg = ''
        if bf is not None:
            fn, op, img = self.blip_img(bf, b, tf)
            inner = img
            if op < 1:
                st += f'opacity:{op:.2f};'
        else:
            c = color_of(sppr)
            if c:
                bg = f'background:{rgba(c)};'
        g = q(sppr, 'a:prstGeom') if sppr is not None else None
        prst = g.get('prst') if g is not None else None
        if prst == 'chevron':
            c = color_of(sppr) or ('FFFFFF', 1)
            adj = q(g, 'a:avLst/a:gd')
            a = (int(re.search(r'\d+', adj.get('fmla')).group()) / 100000 if adj is not None else 0.5) * min(w, h)
            pts = f'0,0 {w - a:.1f},0 {w:.1f},{h / 2:.1f} {w - a:.1f},{h:.1f} 0,{h:.1f} {a:.1f},{h / 2:.1f}'
            tr = f'transform:rotate({b["rot"]:.1f}deg);' if b['rot'] else ''
            return dict(id=sid, name=name, kind='chevron', html=f'<svg class="el" data-id="{sid}" style="left:{x:.1f}px;top:{y:.1f}px;{tr}" width="{w:.1f}" height="{h:.1f}"><polygon points="{pts}" fill="{rgba(c)}"/></svg>')
        rad = self.geom_radius(sppr, w, h)
        ln = self.line_css(sppr)
        txt = self.text(el)
        kind = 'text' if txt and not inner and not bg else ('img' if inner else 'shape')
        return dict(id=sid, name=name, kind=kind, html=f'<div class="el{" pic" if inner else ""}" data-id="{sid}" style="{st}{bg}{rad}{ln}">{inner}{txt}</div>')

    def line_color(self, sppr):
        if sppr is None:
            return None
        ln = q(sppr, 'a:ln')
        if ln is None or q(ln, 'a:noFill') is not None:
            return None
        return color_of(ln)

    def line_w(self, sppr):
        ln = q(sppr, 'a:ln') if sppr is not None else None
        return int(ln.get('w', 12700)) / E if ln is not None else 1.33

    def line_css(self, sppr):
        c = self.line_color(sppr)
        if not c:
            return ''
        return f'box-shadow:inset 0 0 0 {self.line_w(sppr):.1f}px {rgba(c)};'

    def text(self, el):
        tb = el.find('p:txBody', NS)
        if tb is None:
            return ''
        if not ''.join(t.text or '' for t in tb.iter('{%s}t' % NS['a'])).strip():
            return ''
        bp = q(tb, 'a:bodyPr')
        ins = [int(bp.get(k, d)) / E for k, d in (('tIns', 45720), ('rIns', 91440), ('bIns', 45720), ('lIns', 91440))]
        anchor = {'ctr': 'center', 'b': 'flex-end'}.get(bp.get('anchor'), 'flex-start')
        nowrap = bp.get('wrap') == 'none'
        paras = []
        for p in qa(tb, 'a:p'):
            ppr = q(p, 'a:pPr')
            al = {'ctr': 'center', 'r': 'right', 'just': 'justify', 'dist': 'justify'}.get(ppr.get('algn') if ppr is not None else None, 'left')
            lh = None
            if ppr is not None:
                sp = q(ppr, 'a:lnSpc/a:spcPct')
                spp = q(ppr, 'a:lnSpc/a:spcPts')
                if sp is not None:
                    lh = f'{int(sp.get("val")) / 100000 * 1.2:.2f}'
                elif spp is not None:
                    lh = f'{int(spp.get("val")) / 100 * PT:.1f}px'
            runs = []
            maxsz = 0
            for r in p:
                rt = etree.QName(r).localname
                if rt == 'br':
                    runs.append('<br>')
                    continue
                if rt not in ('r', 'fld'):
                    continue
                rpr = q(r, 'a:rPr')
                t = q(r, 'a:t')
                txt = html.escape(t.text or '') if t is not None else ''
                css = ''
                if rpr is not None:
                    if rpr.get('sz'):
                        sz = int(rpr.get('sz')) / 100
                        maxsz = max(maxsz, sz)
                        css += f'font-size:{sz * PT:.1f}px;'
                    lat = q(rpr, 'a:latin')
                    ea = q(rpr, 'a:ea')
                    wgt = weight_of((lat.get('typeface') if lat is not None else '') or (ea.get('typeface') if ea is not None else ''))
                    if rpr.get('b') == '1':
                        wgt = max(wgt or 400, 700)
                    if wgt:
                        css += f'font-weight:{wgt};'
                    c = color_of(rpr)
                    if c:
                        css += f'color:{rgba(c)};'
                    if rpr.get('spc'):
                        css += f'letter-spacing:{int(rpr.get("spc")) / 100 * PT:.1f}px;'
                runs.append(f'<span style="{css}">{txt}</span>' if css else txt)
            if not runs:
                epr = q(p, 'a:endParaRPr')
                sz = int(epr.get('sz')) / 100 if epr is not None and epr.get('sz') else 18
                runs.append(f'<span style="font-size:{sz * PT:.1f}px">&nbsp;</span>')
            lhcss = f'line-height:{lh};' if lh else ''
            paras.append(f'<p style="text-align:{al};{lhcss}">' + ''.join(runs) + '</p>')
        pad = f'padding:{ins[0]:.1f}px {ins[1]:.1f}px {ins[2]:.1f}px {ins[3]:.1f}px;'
        return f'<div class="tx" style="{pad}justify-content:{anchor};{"white-space:nowrap;" if nowrap else ""}">' + ''.join(paras) + '</div>'

    def table(self, el, sid, name, b, tf):
        x, y, w, h = tf(b)
        tbl = el.find('.//a:tbl', NS)
        cols = [int(g.get('w')) / E for g in qa(tbl, 'a:tblGrid/a:gridCol')]
        rows = []
        for tr in qa(tbl, 'a:tr'):
            rh = int(tr.get('h')) / E
            cells = []
            for tc in qa(tr, 'a:tc'):
                tcpr = q(tc, 'a:tcPr')
                c = color_of(tcpr) if tcpr is not None else None
                bg = f'background:{rgba(c)};' if c else ''
                txt = self.text(tc.getparent() if False else tc) if False else ''
                # reuse text() via a fake wrapper
                wrapper = etree.Element('x')
                txb = q(tc, 'a:txBody')
                if txb is not None:
                    t2 = etree.SubElement(wrapper, '{%s}txBody' % NS['p'])
                    for ch in txb:
                        t2.append(etree.fromstring(etree.tostring(ch)))
                    txt = self.text(wrapper)
                cells.append(f'<td style="{bg}height:{rh:.1f}px">{txt}</td>')
            rows.append('<tr>' + ''.join(cells) + '</tr>')
        cg = ''.join(f'<col style="width:{c:.1f}px">' for c in cols)
        return dict(id=sid, name=name, kind='table',
                    html=f'<table class="el tbl" data-id="{sid}" style="left:{x:.1f}px;top:{y:.1f}px;width:{w:.1f}px"><colgroup>{cg}</colgroup>' + ''.join(rows) + '</table>')


def main(src, out):
    prs = Presentation(src)
    data, assets = {}, set()
    for i, s in enumerate(prs.slides, 1):
        c = Conv(s)
        tree = s._element.find('.//p:cSld/p:spTree', NS)
        res = []
        c.walk(tree, lambda bb: (bb['x'] / E, bb['y'] / E, bb['w'] / E, bb['h'] / E), res)
        data[i] = res
        assets |= c.assets
    json.dump(dict(slides=data, assets=sorted(a for a in assets if a)), open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for i, res in data.items():
        print(i, [(r['id'], r['name'][:12], r['kind']) for r in res])


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
