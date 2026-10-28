import sys, json, os, re, importlib.util
sys.stdout.reconfigure(encoding='utf-8')
S = os.path.dirname(os.path.abspath(__file__))
RAW = json.load(open(os.path.join(S, 'raw.json'), encoding='utf-8'))['slides']
AMAP = json.load(open(os.path.join(S, 'assetmap.json'), encoding='utf-8'))
PREFIX = '08_assets/'

# background layers shared by content slides (team texture + leaf shadow + dark veil)
BG_NAMES = {'Group 2', 'Freeform 8', 'Freeform 5'}


def frag(n, drop=(), keep_bg=True):
    out = []
    for e in RAW[str(n)]:
        if e['id'] in drop or e['name'] in drop:
            continue
        out.append(e['html'])
    return '\n'.join(out)


def resolve(h):
    return re.sub(r'@@([\w.]+)', lambda m: PREFIX + AMAP.get(m.group(1), m.group(1)), h)


CSS = r'''
@font-face{font-family:'Paperlogy';src:url('https://fastly.jsdelivr.net/gh/projectnoonnu/2408-3@1.0/Paperlogy-1Thin.woff2') format('woff2');font-weight:100;font-display:swap}
@font-face{font-family:'Paperlogy';src:url('https://fastly.jsdelivr.net/gh/projectnoonnu/2408-3@1.0/Paperlogy-2ExtraLight.woff2') format('woff2');font-weight:200;font-display:swap}
@font-face{font-family:'Paperlogy';src:url('https://fastly.jsdelivr.net/gh/projectnoonnu/2408-3@1.0/Paperlogy-3Light.woff2') format('woff2');font-weight:300;font-display:swap}
@font-face{font-family:'Paperlogy';src:url('https://fastly.jsdelivr.net/gh/projectnoonnu/2408-3@1.0/Paperlogy-4Regular.woff2') format('woff2');font-weight:400;font-display:swap}
@font-face{font-family:'Paperlogy';src:url('https://fastly.jsdelivr.net/gh/projectnoonnu/2408-3@1.0/Paperlogy-5Medium.woff2') format('woff2');font-weight:500;font-display:swap}
@font-face{font-family:'Paperlogy';src:url('https://fastly.jsdelivr.net/gh/projectnoonnu/2408-3@1.0/Paperlogy-6SemiBold.woff2') format('woff2');font-weight:600;font-display:swap}
@font-face{font-family:'Paperlogy';src:url('https://fastly.jsdelivr.net/gh/projectnoonnu/2408-3@1.0/Paperlogy-7Bold.woff2') format('woff2');font-weight:700;font-display:swap}
@font-face{font-family:'Paperlogy';src:url('https://fastly.jsdelivr.net/gh/projectnoonnu/2408-3@1.0/Paperlogy-8ExtraBold.woff2') format('woff2');font-weight:800;font-display:swap}
@font-face{font-family:'Paperlogy';src:url('https://fastly.jsdelivr.net/gh/projectnoonnu/2408-3@1.0/Paperlogy-9Black.woff2') format('woff2');font-weight:900;font-display:swap}
:root{--blue:#1d4ea8;--panel:rgba(255,255,255,.14);--panel2:rgba(255,255,255,.22);--ink:#fff;--soft:rgba(255,255,255,.72)}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:100%;height:100%;background:#0b1d3d;overflow:hidden}
body{font-family:'Paperlogy','Pretendard','Malgun Gothic','Apple SD Gothic Neo',sans-serif;color:#fff;-webkit-font-smoothing:antialiased;word-break:keep-all}
#deck{position:absolute;inset:0}
.slide{position:absolute;left:50%;top:50%;width:2000px;height:1124px;overflow:hidden;background:#1d4ea8;transform-origin:center center;display:none}
.slide.on{display:block}
.el{position:absolute}
.el-g{display:contents}
.pic{overflow:hidden}
.pic img,.pic video{position:absolute;display:block;max-width:none;object-fit:fill}
.tx{position:absolute;inset:0;display:flex;flex-direction:column}
.tx p{line-height:1.2;font-size:24px;font-weight:300}
.tbl{border-collapse:collapse;table-layout:fixed}
.tbl td{position:relative;border:1.3px solid rgba(255,255,255,.9);vertical-align:middle}
.tbl td .tx{position:relative;inset:auto;height:100%;justify-content:center}
/* deck furniture added on top of the team layout */
.kick{position:absolute;left:58px;top:62px;height:50px;display:flex;align-items:center;gap:14px;font-size:33px;font-weight:300;color:#fff;padding:0 9.6px}
.kick b{font-weight:800;letter-spacing:.04em;font-size:26px;padding:3px 12px 1px;border:1.5px solid rgba(255,255,255,.85);border-radius:6px}
.ttl{position:absolute;left:53px;top:114px;width:1880px;padding:4.8px 9.6px;font-size:66.6px;font-weight:500;line-height:1.3;white-space:nowrap;text-shadow:0 2px 14px rgba(8,24,60,.55)}
.ttl strong{font-weight:800}
.band{position:absolute;display:flex;align-items:center;gap:22px;background:var(--panel);font-weight:300}
.band strong{font-weight:800}
.chev{display:inline-block;width:0;height:0}
.ph{position:absolute;display:flex;align-items:center;justify-content:center;border:2px dashed rgba(255,255,255,.55);color:rgba(255,255,255,.8);font-size:30px;font-weight:300;text-align:center;line-height:1.5}
/* UI */
#ui{position:fixed;right:18px;bottom:14px;opacity:0;transition:opacity .3s;display:flex;gap:10px;align-items:center;font:500 14px/1 'Paperlogy',sans-serif;color:rgba(255,255,255,.7);z-index:20;user-select:none}
#ui button{background:rgba(255,255,255,.12);border:0;color:#fff;font:inherit;padding:7px 11px;border-radius:6px;cursor:pointer}
#ui.on,#ui:hover{opacity:1}
#ui button:hover{background:rgba(255,255,255,.25)}
#notes{position:fixed;left:0;right:0;bottom:0;max-height:34vh;overflow:auto;background:rgba(6,16,36,.94);color:#fff;padding:18px 26px 52px;font:400 17px/1.65 'Paperlogy',sans-serif;z-index:15;display:none;border-top:2px solid #6fa0ff}
#notes.on{display:block}
#notes h4{font-weight:800;font-size:15px;color:#9cc0ff;margin:6px 0 2px;letter-spacing:.02em}
#notes .claim{font-size:20px;font-weight:700;margin-bottom:6px}
#grid{position:fixed;inset:0;background:rgba(6,16,36,.97);z-index:30;display:none;overflow:auto;padding:28px;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:18px}
#grid.on{display:grid}
#grid .th{cursor:pointer;color:#fff;font:400 14px/1.4 'Paperlogy',sans-serif}
#grid .th .sec{color:#9cc0ff;font-weight:800;margin-right:6px}
#grid .th:hover{color:#9cc0ff}
@media print{html,body{overflow:visible;height:auto;background:none}#ui,#notes,#grid{display:none!important}
 .slide{display:block!important;position:relative;left:0;top:0;transform:none!important;page-break-after:always}
 @page{size:2000px 1124px;margin:0}}
'''

JS = r'''
const slides=[...document.querySelectorAll('.slide')];let cur=0;
function fit(){const s=Math.min(innerWidth/2000,innerHeight/1124);slides.forEach(el=>el.style.transform=`translate(-50%,-50%) scale(${s})`)}
function show(i){i=Math.max(0,Math.min(slides.length-1,i));slides[cur].classList.remove('on');slides[cur].querySelectorAll('video').forEach(v=>v.pause());
 cur=i;const s=slides[cur];s.classList.add('on');s.querySelectorAll('video').forEach(v=>{v.currentTime=0;const p=v.play();if(p)p.catch(()=>{})});
 document.getElementById('pg').textContent=`${cur+1} / ${slides.length}`;document.getElementById('notes').innerHTML=s.querySelector('template.n')?.innerHTML||'';
 history.replaceState(null,'','#'+(cur+1))}
addEventListener('resize',fit);let uiT;addEventListener('mousemove',()=>{const u=document.getElementById('ui');u.classList.add('on');clearTimeout(uiT);uiT=setTimeout(()=>u.classList.remove('on'),1800)});
addEventListener('keydown',e=>{if(e.target.tagName==='INPUT')return;const k=e.key;
 if(['ArrowRight','PageDown',' ','Enter'].includes(k)){e.preventDefault();show(cur+1)}
 else if(['ArrowLeft','PageUp','Backspace'].includes(k)){e.preventDefault();show(cur-1)}
 else if(k==='Home')show(0);else if(k==='End')show(slides.length-1);
 else if(k==='n'||k==='N')document.getElementById('notes').classList.toggle('on');
 else if(k==='o'||k==='O'||k==='Escape'&&document.getElementById('grid').classList.contains('on'))toggleGrid();
 else if(k==='f'||k==='F'){document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen()}});
document.getElementById('deck').addEventListener('click',e=>{if(e.target.closest('video'))return;show(cur+(e.clientX<innerWidth*0.25?-1:1))});
function toggleGrid(){const g=document.getElementById('grid');if(!g.childElementCount){slides.forEach((s,i)=>{const d=document.createElement('div');d.className='th';
 d.innerHTML=`<span class="sec">${i+1}. ${s.dataset.sec||''}</span>${s.dataset.label||''}`;d.onclick=()=>{toggleGrid();show(i)};g.appendChild(d)})}g.classList.toggle('on')}
fit();show(Math.max(0,(parseInt(location.hash.slice(1))||1)-1));
'''


def page(slides_html, title):
    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>{CSS}</style></head>
<body><div id="deck">
{slides_html}
</div>
<div id="notes"></div><div id="grid"></div>
<div id="ui"><span id="pg"></span><button onclick="show(cur-1)">‹</button><button onclick="show(cur+1)">›</button>
<button onclick="document.getElementById('notes').classList.toggle('on')" title="N">발표 메모</button><button onclick="toggleGrid()" title="O">목차</button></div>
<script>{JS}</script></body></html>'''


def replica(out):
    parts = []
    for n in range(1, 23):
        drop = ('Group 2',) if n in (1, 2, 22) else ()
        parts.append(f'<section class="slide" data-label="원본 {n}">{frag(n, drop)}</section>')
    open(out, 'w', encoding='utf-8').write(resolve(page('\n'.join(parts), '원본 재현')))


def story(out):
    spec_path = os.path.join(S, 'spec.py')
    sp = importlib.util.spec_from_file_location('spec', spec_path)
    m = importlib.util.module_from_spec(sp)
    m.frag = frag
    m.RAW = RAW
    sp.loader.exec_module(m)
    parts = []
    for i, sl in enumerate(m.SLIDES, 1):
        body = sl['html']
        notes = sl.get('notes', '')
        parts.append(f'<section class="slide" data-sec="{sl.get("sec", "")}" data-label="{sl.get("label", "")}">\n{body}\n<template class="n">{notes}</template></section>')
    open(out, 'w', encoding='utf-8').write(resolve(page('\n'.join(parts), m.TITLE)))
    print('slides', len(m.SLIDES))


if __name__ == '__main__':
    mode, out = sys.argv[1], sys.argv[2]
    (replica if mode == 'replica' else story)(out)
