# Why-Who-What-How-So What storyline on top of the team deck (피피티_최종_261027_1222.pptx)
# `frag(n, drop)` is injected by build.py: original slide n as positioned HTML.
import re

TITLE = '코코차차 쇼룸 활성화 제안'
ACC = '#95B3D7'      # team accent (step numbers, chevrons)
PANEL = 'rgba(230,230,230,0.28)'  # team translucent panel
CARD = 'background:rgba(184,204,228,0.26);box-shadow:inset 0 0 0 3px #D8D8D8;border-radius:24px'

BG = ('53', '66', '48', '64')  # shared background layers on slides 7-21


def head(sec, label, title):
    return (f'<div class="kick"><b>{sec}</b>{label}</div>'
            f'<div class="ttl">{title}</div>')


def wrap(html, css):
    return f'<div style="position:absolute;inset:0;{css}">{html}</div>'


def only(n, ids):
    """original elements `ids` of slide n (in z-order)"""
    return '\n'.join(e['html'] for e in RAW[str(n)] if e['id'] in ids)


def keep_except(n, ids):
    return frag(n, ids)  # noqa: F821


def box(x, y, w, h, inner, style=''):
    return f'<div class="el" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;{style}">{inner}</div>'


def txt(x, y, w, html, size=32, weight=300, align='left', lh=1.35, color='#fff', extra=''):
    return (f'<div class="el" style="left:{x}px;top:{y}px;width:{w}px;font-size:{size}px;font-weight:{weight};'
            f'text-align:{align};line-height:{lh};color:{color};{extra}">{html}</div>')


def chev(x, y, w=56, h=72, rot=0, color=ACC):
    a = w / 2
    t = f'transform:rotate({rot}deg);' if rot else ''
    return (f'<svg class="el" style="left:{x}px;top:{y}px;{t}" width="{w}" height="{h}">'
            f'<polygon points="0,0 {a},0 {w},{h/2} {a},{h} 0,{h} {a},{h/2}" fill="{color}"/></svg>')


def img(fn, x, y, w, h, rot=0, extra=''):
    t = f'transform:rotate({rot}deg);' if rot else ''
    return (f'<div class="el pic" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;{t}{extra}">'
            f'<img src="@@{fn}" style="left:0;top:0;width:100%;height:100%" alt=""></div>')


def logo(x, y, w):
    h = w * 584 / 1069
    iw, ih = w * 1200 / 1069, h * 1600 / 584
    return (f'<div class="el pic" style="left:{x}px;top:{y}px;width:{w}px;height:{h:.1f}px">'
            f'<img src="@@image1.png" style="left:{-58 / 1200 * iw:.1f}px;top:{-419 / 1600 * ih:.1f}px;width:{iw:.1f}px;height:{ih:.1f}px" alt=""></div>')


def notes(claim, say, nxt=''):
    h = f'<div class="claim">{claim}</div><h4>말하기</h4><p>{say}</p>'
    if nxt:
        h += f'<h4>다음 장으로</h4><p>{nxt}</p>'
    return h


S = []

# ── 표지 ─────────────────────────────────────────────
S.append(dict(sec='표지', label='숨은 매장을 찾아오는 곳으로',
              html=frag(1, ('2',)),
              notes=notes('숨은 매장을, 일부러 찾아오는 곳으로.',
                          '코코차차의 쇼룸을 활성화하기 위한 집객 콘텐츠와 체험 프로그램을 제안드립니다. 원픽팀 발표 시작하겠습니다.',
                          '먼저 오늘 이야기의 흐름을 보여드리겠습니다.')))

# ── 목차 ─────────────────────────────────────────────
toc = [('01', 'WHY', '기업 이해', '코코차차에 지금 필요한 것', 3),
       ('02', 'WHO', '고객', '방문할 이유가 통할 고객과 경험의 조건', 7),
       ('03', 'WHAT', '프로그램', '예약형 A · 워크인 B · 구성과 가격', 12),
       ('04', 'HOW', '홍보 · 운영', '고객이 오는 길 · 2주 파일럿', 16),
       ('05', 'SO WHAT', '기대효과', '4주 · 3개월 · 6개월 목표와 재는 것', 22)]
t = []
for k, (no, sec, lab, sub, pg) in enumerate(toc):
    y = 214 + 144 * k
    t.append(f'<svg class="el" style="left:988px;top:{y}px;overflow:visible" width="893" height="1"><line x1="0" y1="0" x2="893" y2="0" stroke="#fff" stroke-width="1.3"/></svg>')
    t.append(txt(998, y + 22, 120, no, 48, 800))
    t.append(txt(1127, y + 16, 640, f'{lab}<span style="font-size:26px;font-weight:800;color:{ACC};letter-spacing:.06em;margin-left:18px;vertical-align:6px">{sec}</span>', 48, 800))
    t.append(txt(1127, y + 86, 680, sub, 26.7, 300))
    t.append(txt(1780, y + 26, 96, str(pg), 32, 300, 'right'))
t.append('<svg class="el" style="left:988px;top:934px;overflow:visible" width="893" height="1"><line x1="0" y1="0" x2="893" y2="0" stroke="#fff" stroke-width="1.3"/></svg>')
S.append(dict(sec='목차', label='Why · Who · What · How · So What',
              html=frag(2, ('2',) + tuple(str(i) for i in range(17, 46) if i not in (21, 26, 28))) + ''.join(t),
              notes=notes('왜 필요한지 → 누구에게 → 무엇을 → 어떻게 → 그래서 무엇이 달라지는지 순서로 말씀드립니다.',
                          '기업 이해에서 출발해, 고객, 프로그램, 홍보와 운영, 기대효과 순서로 이어집니다.',
                          '먼저 코코차차가 어떤 브랜드인지부터 보겠습니다.')))

# ── WHY ──────────────────────────────────────────────
S.append(dict(sec='WHY', label='콘크리트무드 안의 코코차차',
              html=frag(3, ('24', '26')) + head('WHY', '기업 이해', '콘크리트무드 안에서 <strong>‘휴가’</strong>를 맡은 브랜드, <strong>코코차차</strong>'),
              notes=notes('코코차차는 워크웨어 브랜드 콘크리트무드 안에서 ‘휴가·경쾌함·소품’을 맡은 브랜드다.',
                          '콘크리트무드에는 작업복·실용성을 보여주는 러스티호미스와, 휴가·경쾌함·소품을 보여주는 코코차차가 있습니다. 오늘 제안은 코코차차 쪽입니다.',
                          '그렇다면 코코차차는 어떤 결을 가진 브랜드일까요?')))

S.append(dict(sec='WHY', label='코코차차의 컨셉',
              html=frag(4, ('24', '26', '32')) + wrap(only(4, ('32',)), 'transform:translate(70px,80px)') + head('WHY', '기업 이해', '휴가를 <strong>손으로 만드는</strong> 브랜드'),
              notes=notes('코코차차의 핵심은 ‘휴가’와 ‘핸드메이드’다. 직접 만드는 체험과 결이 맞는다.',
                          '바다의 조각을 패브릭에 담는 브랜드, “차차, 내 것이 되는 중”이라는 말처럼 휴가·여유·힐링·키치·핸드메이드가 코코차차의 키워드입니다. 이 결은 뒤에서 제안할 ‘직접 만드는 체험’과 그대로 이어집니다.',
                          '이런 브랜드가 지금 매장을 어떻게 운영하고 있는지 보겠습니다.')))

S.append(dict(sec='WHY', label='기업 현황',
              html=frag(5, ('24', '26')) + head('WHY', '기업 현황', '기반은 <strong>이미 있다</strong>'),
              notes=notes('매장, 네이버 플레이스 예약 버튼, 인스타그램까지 기반은 이미 갖춰져 있다.',
                          '원도심의 매장, 네이버 플레이스의 예약 버튼, 인스타그램 계정까지 고객을 받을 기반은 이미 있습니다.',
                          '그런데 실제로 가 보면 —')))

why_chips = (
    box(330, 690, 1340, 112, f'<div style="display:flex;gap:28px;height:100%">'
        f'<div style="flex:1;background:rgba(255,255,255,.16);box-shadow:inset 0 0 0 2px rgba(255,255,255,.55);border-radius:56px;display:flex;align-items:center;justify-content:center;font-size:34px;font-weight:300">일부러 <strong style="font-weight:800;margin:0 .25em">찾아올 이유</strong> → 체험</div>'
        f'<div style="flex:1;background:rgba(255,255,255,.16);box-shadow:inset 0 0 0 2px rgba(255,255,255,.55);border-radius:56px;display:flex;align-items:center;justify-content:center;font-size:34px;font-weight:300">발견부터 예약까지 <strong style="font-weight:800;margin:0 .25em">이어지는 길</strong> → 홍보</div>'
        f'</div>'))
S.append(dict(sec='WHY', label='공간은 있는데, 채워져 있지 않다',
              html=frag(6, ('24', '26')) + why_chips + head('WHY', '기업 현황', '필요한 건, <strong>찾아올 이유</strong>'),
              notes=notes('공간은 있는데 채워져 있지 않다. 필요한 건 ‘일부러 찾아올 이유’와 ‘발견에서 예약까지 이어지는 길’이다.',
                          '공간은 있는데, 채워져 있지 않습니다. 그래서 저희는 두 가지가 필요하다고 봤습니다. 고객이 일부러 찾아올 이유가 되는 체험, 그리고 그 체험을 발견하고 예약까지 이어지게 하는 길입니다.',
                          '그렇다면 어떤 고객에게, 어떤 체험이 이곳을 찾아올 이유가 될까요?')))

# ── WHO ──────────────────────────────────────────────
S.append(dict(sec='WHO', label='페르소나',
              html=frag(7, ('24', '26', '29')) + wrap(only(7, ('29',)), 'transform:scale(.8);transform-origin:1000px 1042px')
              + head('WHO', '페르소나', '제주에 혼자 머물며, <strong>직접 만든 것</strong>을 남기고 싶은 고객'),
              notes=notes('우리가 먼저 만날 고객은 제주에 혼자 머물며, 직접 만든 결과물을 남기고 싶은 사람이다.',
                          '29살 프리랜서 일러스트레이터 한소율 씨입니다. 즉흥적이고 혼자 여행하는 걸 좋아합니다. 혼자서도 편한 체험, SNS에 올릴 결과물, 가격 대비 납득되는 구성, 그리고 기념품보다는 직접 만든 것을 원합니다.',
                          '이런 고객이 실제로 얼마나 있을까요?')))

S.append(dict(sec='WHO', label='페르소나 근거',
              html=frag(8, ('24', '26')) + head('WHO', '페르소나 근거', '20·30은 제주를 <strong>많이 찾고, 길게 머문다</strong>'),
              notes=notes('20·30은 제주 관광객의 절반 이상이고, 워케이션으로 평균 4박 5일을 머문다.',
                          '제주 내국인 관광객 중 20·30이 56.6%, 원도심 방문객 중 20·30 여성이 20.4%입니다. 워케이션 평균 기간은 4박 5일로, 여행 중 체험에 시간을 쓸 여유가 있습니다.',
                          '이 고객들은 체험, 특히 원데이클래스를 찾을까요?')))

S.append(dict(sec='WHO', label='원데이클래스인 이유',
              html=frag(9, ('24', '26')) + head('WHO', '원데이클래스인 이유', '20·30은 원데이클래스를 <strong>찾고, 또 찾는다</strong>'),
              notes=notes('원데이클래스는 20·30이 주로 찾고, 한 번 해본 사람이 다시 찾는 체험이다.',
                          '원데이클래스 검색의 72.8%가 20·30이고, 이용자의 85%가 20·30입니다. 2회 이상 참여 비율도 82.7%로 높습니다.',
                          '그럼 이 고객들은 무엇을 만들고 싶어 할까요? 요즘 흐름을 보겠습니다.')))

S.append(dict(sec='WHO', label='트렌드 · 백꾸',
              html=frag(10, ('24', '26', '51', '57', '58'))
              + wrap(only(10, ('51', '57', '58')), 'transform:scale(.86);transform-origin:1420px 1030px')
              + head('WHO', '트렌드 분석', '가방을 꾸며 취향을 드러내는 <strong>‘백꾸’</strong>가 흐름이다'),
              notes=notes('키링·패치로 가방을 꾸미는 ‘백꾸’가 유행이다. 결과물에 취향을 담고 싶어 한다.',
                          '키링에서 시작해 패치, 스티커로 가방을 커스터마이징하는 ‘백꾸’가 코치, 루이비통 런웨이에도 등장할 만큼 흐름이 됐습니다.',
                          '지금까지 본 고객과 흐름을 모으면, 체험이 갖춰야 할 조건이 보입니다.')))

cond = [('01', '혼자서도 <strong>편하게</strong>', ['혼자 여행하는 페르소나', 'Needs · 혼자서도 편한 체험']),
        ('02', '여행 중 <strong>부담 없이</strong>', ['워케이션 평균 4박 5일', 'Needs · 가격 대비 납득되는 구성']),
        ('03', '<strong>내 취향</strong>을 담은 결과물', ['Needs · 기념품보단 직접 만든 것', '트렌드 · 가방을 꾸미는 ‘백꾸’'])]
c = []
for k, (no, head_, ev) in enumerate(cond):
    x = 120 + k * 600
    c.append(box(x, 300, 560, 560, '', f'background:{PANEL}'))
    c.append(txt(x + 48, 340, 470, no, 96, 800, color=ACC, lh=1))
    c.append(txt(x + 48, 470, 480, head_, 50, 500, lh=1.3))
    c.append(f'<svg class="el" style="left:{x + 48}px;top:640px" width="464" height="2"><line x1="0" y1="1" x2="464" y2="1" stroke="rgba(255,255,255,.7)" stroke-width="1.5"/></svg>')
    c.append(txt(x + 48, 668, 480, '<br>'.join(ev), 28, 300, lh=1.7, color='rgba(255,255,255,.88)'))
c.append(logo(120, 925, 250))
c.append(txt(400, 940, 1430, '의 <strong style="font-weight:800">휴가 · 핸드메이드</strong> 결과도 맞닿아 있다 &nbsp;→&nbsp; <strong style="font-weight:800">매장에서 직접 만드는 체험</strong>', 40, 300, lh=1.4))
S.append(dict(sec='WHO', label='경험의 조건',
              html=only(9, BG) + ''.join(c)
              + head('WHO', '정리', '그래서 이 고객에게 맞는 경험은, <strong>세 가지 조건</strong>을 갖춰야 한다'),
              notes=notes('혼자서도 편하게, 여행 중 부담 없이, 내 취향을 담은 결과물 — 이 세 조건을 갖춘 체험이어야 한다.',
                          '혼자 참여하기 편하고, 여행 일정 안에서 부담 없이 시간을 쓰면서, 자기 취향을 담은 결과물을 가져갈 수 있어야 한다고 봤습니다. 그리고 이건 휴가와 핸드메이드를 말하는 코코차차의 결과도 맞닿아 있습니다.',
                          '그래서 저희는 이 조건에 맞춰 두 가지 체험을 설계했습니다.')))

# ── WHAT ─────────────────────────────────────────────
what = [
    txt(553, 400, 94, '경<br>험', 63.9, 600, lh=1.2),
    txt(1237, 400, 94, '경<br>험', 63.9, 600, lh=1.2),
    txt(555, 768, 94, '방<br>식', 63.9, 600, lh=1.2),
    txt(1239, 768, 94, '방<br>식', 63.9, 600, lh=1.2),
    txt(681, 380, 540, '에코백 몸통·손잡이를 <strong style="font-weight:800">고르고</strong><br>도안을 실크스크린으로 <strong style="font-weight:800">찍고</strong><br>파우치까지 <strong style="font-weight:800">내 가방으로</strong> 완성', 34, 300, lh=1.75),
    txt(1365, 380, 290, '키링을 <strong style="font-weight:800">고르고</strong><br>와펜을 <strong style="font-weight:800">골라</strong><br>다림질로 <strong style="font-weight:800">완성</strong>', 34, 300, lh=1.75),
    txt(681, 752, 540, f'<strong style="font-weight:800">예약제</strong> · 약 60분<br><span style="font-size:52px;font-weight:800">45,000~55,000</span>원', 34, 300, lh=1.6),
    txt(1365, 752, 290, f'<strong style="font-weight:800">워크인</strong> · 예약 없이<br><span style="font-size:52px;font-weight:800">21,000</span>원', 34, 300, lh=1.6),
]
S.append(dict(sec='WHAT', label='프로그램 구성 A · B',
              html=frag(11, ('24', '26', '22', '25', '28', '31', '50', '51', '54', '40')) + ''.join(what)
              + head('WHAT', '프로그램 구성', '충분히 만드는 <strong>A</strong>, 잠깐 들러 꾸미는 <strong>B</strong>'),
              notes=notes('A는 예약하고 한 시간 동안 가방을 완성하는 클래스, B는 예약 없이 들러 키링을 꾸미는 체험이다.',
                          '시간을 충분히 쓰고 싶은 고객에게는 예약제 클래스 A를, 지나가다 잠깐 들른 고객에게는 워크인 키링 커스텀 B를 제안합니다. 두 체험 모두 혼자서도 참여할 수 있고, 내 취향이 담긴 결과물을 바로 가져갑니다.',
                          'A부터 자세히 보겠습니다.')))

steps = [('1.', '고르기', '10'), ('2.', '찍기', '20'), ('3.', '잇기', '15'), ('4.', '다림질', '10'), ('5.', '완성', '5')]
a = [box(102, 250, 1180, 664, '<video src="@@media3.mp4" muted loop playsinline preload="auto" style="left:0;top:0;width:100%;height:100%;object-fit:cover"></video>', 'overflow:hidden;background:#0b1d3d')]
for k, (n_, s_, m_) in enumerate(steps):
    a.append(txt(1350, 258 + k * 110, 560, f'<span style="color:{ACC}">{n_}</span> <span style="font-size:58.7px">{s_}</span> <span style="font-weight:300;color:{ACC}">{m_}분</span>', 53.3, 700, lh=1.6))
a.append(txt(1350, 820, 560, f'<span style="font-weight:300">총</span> 60분', 40, 800, lh=1.6, extra='border-top:1.5px solid rgba(255,255,255,.7);padding-top:14px'))
for k, (fn, desc, price) in enumerate([('image18.png', '큰 에코백 + 실크스크린 + 파우치<br>+ 와펜 기본 구성 2개 + 패브릭 마커로 커스텀', '55,000'),
                                       ('image54.png', '작은 에코백 + 실크스크린 + 파우치', '45,000')]):
    x = 102 + k * 912
    a.append(box(x, 946, 886, 140, '', f'background:{PANEL}'))
    a.append(img(fn, x + 14, 948, 140, 134))
    a.append(txt(x + 170, 946, 440, desc, 26, 500, lh=1.4, extra='height:140px;display:flex;align-items:center'))
    a.append(txt(x + 560, 946, 306, f'{price}<span style="font-size:40px">원</span>', 60, 800, 'right', lh=1, extra='height:140px;display:flex;align-items:center;justify-content:flex-end'))
S.append(dict(sec='WHAT', label='A 예약제 클래스',
              html=frag(12, BG[:0] + ('24', '26', '44', '51', '58', '65', '77', '83', '96', '3')) + ''.join(a)
              + head('WHAT', '프로그램 A · 예약제', '한 시간 동안, <strong>내 가방을 처음부터</strong> 완성한다'),
              notes=notes('A는 고르기부터 완성까지 60분, 내가 고른 조합으로 가방을 처음부터 만드는 클래스다.',
                          '에코백 몸통과 손잡이를 고르고(10분), 실크스크린으로 도안을 찍고(20분), 손잡이를 잇고(15분), 와펜을 다림질로 붙여(10분) 완성합니다(5분). 큰 에코백 구성은 와펜 2개와 패브릭 마커까지 포함해 55,000원, 작은 에코백 구성은 45,000원입니다.',
                          '시간이 없는 고객을 위한 B도 있습니다.')))

b = [box(102, 960, 1796, 120, '', f'background:{PANEL}'),
     txt(140, 960, 900, '키링 + 와펜 기본 구성 4개', 36, 500, lh=1, extra='height:120px;display:flex;align-items:center'),
     txt(700, 960, 420, '21,000<span style="font-size:40px">원</span>', 60, 800, 'right', lh=1, extra='height:120px;display:flex;align-items:center;justify-content:flex-end'),
     chev(1180, 984, 56, 72),
     txt(1260, 960, 630, '<div>큰 에코백까지 원하면 <strong style="font-weight:800">A 클래스로 안내</strong><br><span style="font-size:24px;color:rgba(255,255,255,.8)">큰 에코백은 클래스가 더 저렴</span></div>', 30, 300, lh=1.35, extra='height:120px;display:flex;align-items:center;white-space:nowrap')]
S.append(dict(sec='WHAT', label='B 워크인 키링',
              html=only(13, BG) + wrap(frag(13, ('24', '26') + BG), 'transform:translateY(-58px)') + ''.join(b)
              + head('WHAT', '프로그램 B · 워크인', '들른 김에, <strong>내 취향대로</strong> 키링 하나'),
              notes=notes('B는 예약 없이 들러 바탕을 고르고, 와펜을 골라 다림질로 붙이면 끝나는 짧은 체험이다.',
                          '바탕 재료를 고르고, 와펜을 고르고, 결제 후 다림질로 붙이면 끝입니다. 키링과 와펜 기본 4개 구성으로 21,000원입니다. 큰 에코백까지 만들고 싶은 고객은 클래스가 더 저렴하기 때문에 A로 안내합니다.',
                          '그렇다면 이 체험을 왜 다른 곳이 아니라 코코차차에서 해야 할까요?')))

S.append(dict(sec='WHAT', label='코코차차여야 하는 이유',
              html=frag(14, ('24', '26')) + head('WHAT', '차별점', '고르고, 만들고, 꾸미기를 한 번에 — <strong>브랜드가 직접</strong>'),
              notes=notes('선택 폭, 체험, 희소성, 커스텀 자유도를 모두 갖춘 곳은 브랜드가 직접 운영하는 코코차차다.',
                          '일반 소품샵은 고르는 것까지, 오브젝트는 일부 체험까지 가능합니다. 코코차차는 브랜드가 직접 만든 소재로 고르고, 만들고, 꾸미는 것까지 한 번에 할 수 있습니다.',
                          '이제 이 체험에 고객을 어떻게 데려올지 말씀드리겠습니다.')))

# ── HOW ──────────────────────────────────────────────
lanes = [('A', '예약형', [('발견', '인스타 릴스', 'p.17'), ('확인', '플레이스 · 블로그 후기', 'p.18–19'), ('예약', '네이버 예약', 'p.18'), ('남기기', '리뷰 → 와펜 1개', 'p.18')]),
         ('B', '워크인', [('발견', '매장 앞 입간판', 'p.20'), ('이해', '짧게 할 수 있는 체험', 'p.20'), ('입장', '키링 커스텀', 'p.14'), ('연결', '큰 에코백은 A로', 'p.14')])]
h = []
for r, (code, name, st) in enumerate(lanes):
    y = 300 + r * 380
    h.append(box(80, y, 230, 320, '', f'{CARD}'))
    h.append(txt(80, y + 60, 230, code, 120, 800, 'center', lh=1))
    h.append(txt(80, y + 200, 230, name, 40, 500, 'center', lh=1.2))
    for k, (lab, main, ref) in enumerate(st):
        x = 360 + k * 395
        h.append(box(x, y, 330, 320, '', f'background:{PANEL}'))
        h.append(txt(x + 30, y + 34, 280, lab, 32, 300, color=ACC))
        h.append(txt(x + 30, y + 96, 280, main, 42, 800, lh=1.3))
        h.append(txt(x + 30, y + 262, 280, ref, 22, 200, color='rgba(255,255,255,.75)'))
        if k < 3:
            h.append(chev(x + 340, y + 134, 44, 56))
S.append(dict(sec='HOW', label='고객이 오는 두 가지 길',
              html=only(9, BG) + ''.join(h)
              + head('HOW', '고객 유입', 'A는 <strong>찾아보고 예약</strong>하고, B는 <strong>지나가다 들어온다</strong>'),
              notes=notes('A와 B는 고객이 오는 길이 다르다. A는 발견→확인→예약, B는 매장 앞에서 바로 입장.',
                          '예약형 A의 고객은 영상으로 체험을 발견하고, 검색으로 구성과 후기를 확인한 뒤 예약합니다. 워크인 B의 고객은 매장 앞 안내를 보고, 짧게 할 수 있는 체험임을 이해하고 들어옵니다. 이 순서대로 홍보 채널을 하나씩 보겠습니다.',
                          'A 고객의 첫 접점, 릴스입니다.')))

S.append(dict(sec='HOW', label='A · 발견 — 릴스',
              html=frag(15, ('24', '26')) + head('HOW', 'A · 발견', '릴스로 <strong>무엇을 만드는 곳인지</strong> 먼저 보여준다'),
              notes=notes('20대의 국내여행 정보 채널 1위는 SNS다. 릴스로 제작 과정과 체험 장면을 먼저 보여준다.',
                          '20대 국내여행 정보 채널 1위가 SNS, 27%입니다. 상품 제작 영상과 클래스 체험 영상으로, 이곳이 무엇을 만드는 곳인지 먼저 알게 합니다.',
                          '영상을 본 고객은 검색해서 확인합니다.')))

S.append(dict(sec='HOW', label='A · 확인·예약 — 네이버 플레이스',
              html=frag(16, ('22', '26')) + head('HOW', 'A · 확인 → 예약', '보고 온 고객이 <strong>바로 예약하고, 리뷰를 남기도록</strong>'),
              notes=notes('원데이클래스 고객의 74.7%는 위치보다 프로그램을 보고 온다. 플레이스에 예약 창구와 리뷰 동선을 만든다.',
                          '원데이클래스 고객의 74.7%가 위치보다 프로그램을 보고 옵니다. 네이버 플레이스에 클래스를 등록해 바로 예약할 수 있게 하고, 리뷰를 쓰면 와펜 1개를 드려 다음 고객이 볼 후기를 쌓습니다.',
                          '예약 전, 한 번 더 확인하는 곳이 블로그입니다.')))

S.append(dict(sec='HOW', label='A · 확인 — 블로그',
              html=frag(17, ('9', '26')) + head('HOW', 'A · 확인', '후기로 <strong>‘방문할 만한 곳’</strong>이라는 확신을 준다'),
              notes=notes('30.3%는 SNS·블로그·커뮤니티 검색으로 클래스를 찾는다. 블로거 체험단으로 첫 후기를 만든다.',
                          '원데이클래스를 찾는 경로의 30.3%가 SNS, 블로그, 커뮤니티 검색입니다. 원데이·제주 여행 블로거 2명에게 체험을 협찬해, 약 8만 원으로 첫 후기를 만듭니다.',
                          '여기까지가 예약 고객의 길이고, 이제 매장 앞을 지나가는 고객입니다.')))

S.append(dict(sec='HOW', label='B · 입장 — 입간판',
              html=frag(18, ('24', '26')) + head('HOW', 'B · 발견 → 입장', '입간판 하나로, <strong>지나가던 사람을 들어오게</strong> 한다'),
              notes=notes('지나가던 사람이 들어오려면, 무엇을 하는 곳인지 매장 앞에서 바로 보여야 한다.',
                          '지금의 입간판을 공간·브랜드·제품 정보, 인스타그램, 영업시간이 한눈에 보이도록 바꿉니다. 짧게 할 수 있는 키링 체험이 있다는 걸 매장 앞에서 바로 알게 합니다.',
                          '그럼 이 유입을 실제로 감당할 수 있을까요?')))

# 파일럿 · 기대효과 · 정원 단계: deliverables/파일럿_html/파일럿_슬라이드.html (1920 기준) 을 2000 무대로 옮김
K = 2000 / 1920
SOFT = 'rgba(255,255,255,.72)'
SKY2 = '#bcd3f2'
CARDLINE = 'box-shadow:inset 0 0 0 3px #D9D9D9,0 0 40px rgba(166,166,166,.15);border-radius:24px 24px 0 0'
pc = []
for k, (when, what, how, fill) in enumerate([('2주', '작게 시작', '클래스 4회 · 회당 최대 3명<br>초기 구매비 15만원', False),
                                             ('2주 뒤', '운영을 고친다', '매니저 혼자<br>돌릴 수 있나?', True),
                                             ('4주 뒤', '다음을 정한다', '계속 · 보완 · 보류', True)]):
    x = round((90 + 610 * k) * K)
    bg = 'background:rgba(185,205,229,.26);' if fill else ''
    pc.append(box(x, 1124 - 730 + 3, 542, 730, '', bg + CARDLINE))
    pc.append(txt(x, 1124 - 730 + 3 + 94, 542, when, 88, 800, 'center', lh=1, extra='letter-spacing:-.02em'))
    pc.append(txt(x, 1124 - 730 + 3 + 94 + 88 + 73, 542, what, 56, 500, 'center', lh=1.2, extra='letter-spacing:-.02em'))
    pc.append(txt(x + 40, 1124 - 730 + 3 + 94 + 88 + 73 + 67 + 29, 462, how, 31, 300, 'center', lh=1.5, color=SOFT))
    if k < 2:
        pc.append(chev(round((632 + 610 * k) * K), round(640 * K), 48, 62))
S.append(dict(sec='HOW', label='운영 — 2주 파일럿',
              html=only(9, BG) + ''.join(pc) + head('HOW', '운영 · 파일럿', '작게 시작해, <strong>2주 뒤 고치고</strong>, <strong>4주 뒤 정한다</strong>'),
              notes=notes('바로 확장하지 않는다. 2주 작게 열어 보고, 2주 뒤 운영을 고치고, 4주 뒤 계속·보완·보류를 정한다.',
                          '확인할 것은 두 가지입니다. 매니저 한 명이 클래스 3명과 워크인을 함께 감당할 수 있는지, 그리고 지금 가격으로 유료 예약이 생기는지. 그래서 클래스 4회, 회당 최대 3명, 신규 구매 약 15만 원으로 작게 시작합니다. 2주 뒤에는 시간·재고·예산과 운영 문제를 보고 2주를 더 할지 보류할지 정하고, 4주 뒤에는 2명 이상 온 회차가 있으면 그런 회차만 이어 가고, 없으면 한 번 보완한 뒤 보류를 판단합니다.',
                          '이렇게 운영했을 때 기대하는 변화입니다.')))

ld = []
for k, (when, num, sub) in enumerate([('첫 4주', '10명', '리뷰 5건'), ('3개월', '24명', '주 2회 × 3명'), ('6개월', '48명', '평균 3명이 유지되면')]):
    cx = 156 + k * 640  # column left; 3 columns of 520 + 2 gaps of 120 (chevrons)
    ld.append(txt(cx, 375, 520, when, 37.5, 500, 'center', lh=1.2, color=SKY2))
    ld.append(txt(cx, 438, 520, f'월<b style="font-size:156px;font-weight:800;letter-spacing:-.03em;margin-left:6px">{num}</b>', 48, 500, 'center', lh=1))
    ld.append(txt(cx, 640, 520, sub, 29, 300, 'center', lh=1.3, color=SOFT))
    if k < 2:
        ld.append(chev(cx + 520 + 36, 500, 48, 62))
chips = ''.join(f'<div style="flex:1;background:{PANEL};display:flex;flex-direction:column;justify-content:center;padding:0 40px">'
                f'<div style="font-size:30px;font-weight:500;color:{SKY2}">{a}</div><div style="font-size:38px;font-weight:300;margin-top:6px">{b}</div></div>'
                for a, b in [('공간', '<strong style="font-weight:800">체험객</strong> 수'), ('홍보', '<strong style="font-weight:800">리뷰 · 태그</strong>'), ('매출', '<strong style="font-weight:800">상품 구매</strong>')])
ld.append(txt(156, 800, 600, '재는 것', 30, 300, lh=1, color=SOFT))
ld.append(box(156, 850, 1688, 170, f'<div style="display:flex;gap:24px;height:100%">{chips}</div>'))
S.append(dict(sec='SO WHAT', label='기대효과',
              html=only(9, BG) + ''.join(ld) + head('SO WHAT', '기대효과', '첫 4주 10명에서 시작해, <strong>6개월 월 48명</strong>까지'),
              notes=notes('첫 4주 유료 10명·리뷰 5건에서 시작해, 3개월 월 24명, 6개월 월 48명까지. 공간·홍보·매출 세 가지로 잰다.',
                          '첫 4주 목표는 유료 10명, 리뷰 5건입니다. 이후 주 2회, 회당 3명이 차면 3개월에 월 24명, 평균 3명이 유지되면 6개월에 월 48명입니다. 비어 있던 공간에 체험객이 오는지, 리뷰와 태그가 쌓이는지, 상품 구매로 이어지는지로 확인합니다. (참고: 파일럿은 프로젝트 기간에 운영하지 않았고, 숫자는 실측 전 추정입니다.)',
                          '정리하면, 숨은 매장을 일부러 찾아오는 곳으로 만드는 제안이었습니다.')))

S.append(dict(sec='끝', label='감사합니다',
              html=frag(22, ('2',)),
              notes=notes('감사합니다.', '들어주셔서 감사합니다. 질문 받겠습니다.')))

st = []
for k, (n_, lv, fill) in enumerate([('3', '파일럿', False), ('4', '정규', True), ('5', '정규', True), ('6', '공간 최대', True)]):
    cx = 208 + k * 437  # 4 columns of 271 + 3 gaps of 166
    bg = 'background:rgba(185,205,229,.26);' if fill else ''
    st.append(box(cx, 375, 271, 271, f'<div style="height:100%;display:flex;align-items:center;justify-content:center;font-size:146px;font-weight:800;line-height:1">{n_}<span style="font-size:46px;font-weight:500;margin-left:4px">명</span></div>', bg + 'border-radius:50%;box-shadow:inset 0 0 0 3px #D9D9D9'))
    st.append(txt(cx - 40, 675, 351, lv, 31, 300, 'center', lh=1.2, color=SKY2))
    if k < 3:
        st.append(chev(cx + 271 + 59, 480, 48, 62))
st.append(txt(0, 870, 2000, '6명이 차면 같은 <strong style="font-weight:800">월 48명</strong>을 <strong style="font-weight:800">주 2회</strong>로', 40, 300, 'center', lh=1.3))
S.append(dict(sec='부록', label='정원 단계',
              html=only(9, BG) + ''.join(st) + head('부록', '운영 · 정원 단계', '결과가 좋으면 <strong>3명에서 6명까지</strong>, 한 단계씩'),
              notes=notes('정원은 파일럿 3명에서 시작해, 결과가 좋을 때만 한 단계씩 6명(공간 최대)까지 늘린다.',
                          '질문이 나오면 보여 드리는 부록입니다. 파일럿은 3명, 정규 운영에서 4명, 5명으로 한 단계씩 올리고, 공간 최대는 6명입니다. 6명이 차면 같은 월 48명을 주 2회로 운영할 수 있습니다.')))

SLIDES = S
