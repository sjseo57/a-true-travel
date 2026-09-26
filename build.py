"""Build A True Travel's plain HTML pages from the curated image folders.

Run `python3 build.py` after adding or replacing a web JPEG. Requires Pillow.
"""
from pathlib import Path
from html import escape
from PIL import Image

ROOT = Path(__file__).resolve().parent
IMG = ROOT / "assets/images"

SERIES = [
    dict(slug="sea-in-me", ko="내 안의 바다", en="The Sea in Me", category="Works",
         cover="sea-in-me/sea-in-me-11.jpg", folder="sea-in-me", prefix="sea-in-me",
         intro_ko=[
             "기록되지 않은 것은 사라지기에, 변해가는 바다의 오늘을 카메라에 담아왔다.",
             "내가 사랑하는 바다는 고요한 본연의 모습을 간직한 곳이다. 어부의 노랫가락이 들리는 평화로운 수평선 너머에는 치열한 삶의 현장이 공존하지만, 바다는 그 모든 거칠고 고단한 시간을 묵묵히 품어 안는다.",
             "바다 앞에 서면 살아가며 마주한 환희와 후회, 말로 다 전하지 못한 마음을 가감 없이 내려놓게 된다. 오랫동안 바라본 바다는 어느새 풍경을 넘어 나의 기억과 시간을 비추는 내면의 장소가 되었다.",
             "나는 어머니의 품을 닮은 그 깊고 푸른 위로와, 그 안에서 마주한 나 자신의 모습을 사진이라는 문장으로 기록하고자 한다."],
         intro_en=[
             "What is not recorded eventually disappears. Through my camera, I have sought to preserve the sea as it changes from one day to the next.",
             "The sea I love retains a quiet, essential presence. Beyond the peaceful horizon, where fishermen’s songs can be heard, life unfolds with urgency. Yet the sea silently embraces all its roughness, hardship, and passing time.",
             "Standing before the sea, I find myself releasing the joys, regrets, and unspoken feelings gathered through life. Over the years, the sea has become more than a landscape; it has become an inward place where my memories and sense of time are reflected.",
             "Through photography, I seek to record its deep blue consolation, reminiscent of a mother’s embrace, and the image of myself encountered within it."]),
    dict(slug="traces-of-prayer", ko="기도의 흔적들", en="Traces of Prayer", category="Works",
         cover="traces-of-prayer/traces-of-prayer-10.jpg", folder="traces-of-prayer", prefix="traces-of-prayer",
         intro_ko=["사람들은 돌을 쌓고 촛불을 밝히며, 동전과 지폐, 기원문에 말로 다 전하지 못한 마음을 맡긴다.",
                   "나는 기도하는 사람보다 그들이 떠난 뒤 남은 사물과 공간을 바라보았다. 이 사진들은 보이지 않는 간절함이 돌탑과 연등, 작은 헌금에 머물다가 침묵으로 이어지는 시간을 기록한다."],
         intro_en=["People stack stones, light candles, and leave coins, banknotes, and written wishes, entrusting them with feelings that cannot be fully expressed in words.",
                   "Rather than photographing those who pray, I looked at the objects and spaces left behind. These photographs record the time in which invisible longing lingers in stone cairns, lanterns, and small offerings before returning to silence."]),
    dict(slug="silence-temple", ko="산사의 고요함", en="Silence of the Mountain Temple", category="Works",
         cover="silence-temple/silence-temple-15.jpg", folder="silence-temple", prefix="silence-temple",
         intro_ko=["산사로 들어가는 길에서 시간은 느려진다. 숲을 지나 전각을 발견하고, 문과 마당을 통과하는 동안 일상의 소음은 점차 멀어진다.",
                   "나는 산사의 건축을 설명하기보다 그 공간을 채우는 침묵과 시간을 바라본다. 처마 아래의 빛과 문틈의 어둠, 비어 있는 마당과 오래된 나무에는 수많은 사람이 머물다 간 시간이 남아 있다.",
                   "때때로 나타나는 사람의 작은 기척마저 자연과 건축 안으로 스며든다. 이 사진들은 산사의 외형이 아니라, 그 안에서 잠시 마주한 고요의 깊이를 기록한다."],
         intro_en=["Time slows along the path into a mountain temple. As I pass through the forest, encounter temple halls, and cross gates and courtyards, the noise of everyday life gradually recedes.",
                   "Rather than describing temple architecture, I look toward the silence and time that inhabit these spaces. Light beneath the eaves, darkness within doorways, empty courtyards, and old trees retain the traces of countless people who have passed through.",
                   "Even the occasional presence of a person dissolves into nature and architecture. These photographs record not the outward appearance of the temple, but the depth of stillness briefly encountered within it."]),
    dict(slug="gaya-tumuli", ko="가야고분군", en="Gaya Tumuli", category="Korean Cultural Heritage",
         cover="gaya-tumuli/Gaya_Tumuli-09.jpg", folder="gaya-tumuli", prefix="Gaya_Tumuli",
         intro_ko=["가야의 고분은 과거에 멈춘 유적이 아니다. 마을과 들판, 현대의 건물들 사이에서 사람들이 걷고 놀고 머무는 살아 있는 풍경이다.",
                   "사람들이 멀어지면 고분은 다시 나무와 산, 안개와 빛의 리듬으로 돌아간다. 이 작업은 오래된 땅과 오늘의 삶이 공존하는 모습, 그리고 천년의 풍경 속에 인간의 짧은 시간이 잠시 머무는 순간을 바라본다."],
         intro_en=["The tumuli of Gaya are not relics suspended in the past. Surrounded by villages, fields, and modern buildings, they remain living landscapes where people walk, play, and pause in their everyday lives.",
                   "When the people recede, the ancient mounds return to the rhythms of trees, mountains, mist, and light. This work observes the quiet coexistence of ancient ground and contemporary life—and the brief moments when human time enters a thousand-year-old landscape."]),
    dict(slug="royal-tombs", ko="왕릉과 고분", en="Royal Tombs and Tumuli", category="Korean Cultural Heritage",
         cover="royal-tombs/bw/Royal-Tombs-Tumuli-07.jpg", folder="royal-tombs", prefix="Royal-Tombs-Tumuli",
         intro_ko=["왕릉과 고분은 죽은 자를 위한 무덤이면서, 오랜 시간 살아 있는 풍경이기도 합니다. 산의 능선을 닮은 봉분들은 도시와 들판 사이에서 계절을 지나고, 나무와 새, 그곳을 돌보는 사람들의 삶과 함께 오늘까지 이어집니다.",
                   "작업의 전반부는 선명한 흑백사진으로 고분의 실제 풍경과 형태를 바라봅니다. 산과 봉분, 나무와 인간이 한 공간에 놓이며, 고분은 과거에 멈춘 유적이 아니라 현재의 삶과 호흡하는 존재로 나타납니다.",
                   "후반부에서 풍경은 거친 입자로 변화합니다. 선명했던 형태는 점차 기억처럼 흐려지고, 봉분과 나무와 사람은 시간의 입자 속으로 스며듭니다. 마지막에 남는 문과 봉분은 삶과 죽음, 현재와 과거 사이의 조용한 경계를 보여줍니다."],
         intro_en=["Royal tombs and ancient tumuli are resting places for the dead, yet they also remain living landscapes shaped by time. Resembling the ridgelines of distant mountains, the burial mounds endure through changing seasons, sharing the present with trees, birds, surrounding towns, and the people who continue to care for them.",
                   "The first part of the series observes the physical presence of the tombs through clear black-and-white photographs. Mountains, burial mounds, trees, and human figures inhabit the same space, revealing these sites not as relics suspended in the past, but as living places that continue to breathe within the rhythms of contemporary life.",
                   "In the latter part, the visible landscape gradually dissolves into coarse particles. Once-distinct forms become blurred like memories, while the mounds, trees, and human traces merge into the grain of accumulated time. The final images of a doorway and a burial mound suggest a quiet threshold between life and death, the present and the past."]),
    dict(slug="seowon-hyanggyo", ko="한국의 서원과 향교", en="Seowon and Hyanggyo of Korea", category="Korean Cultural Heritage",
         cover="seowon-hyanggyo/Seowon-Hyanggyo-11.jpg", folder="seowon-hyanggyo", prefix="Seowon-Hyanggyo",
         intro_ko=["서원과 향교는 건축물로 남아 있지만, 그 공간의 본질은 오랫동안 이어져 온 배움과 의례, 그리고 사람들의 움직임 속에 있다.",
                   "나는 전각의 형태를 기록하는 데 머물지 않고, 문과 마당, 제향을 준비하는 손과 몸짓, 비어 있는 공간에 남은 시간의 결을 바라보았다. 자연과 건축, 의례와 일상이 만나는 순간을 통해 과거가 오늘의 삶 안에서 어떻게 지속되는지를 기록하고자 했다.",
                   "일부 작품은 서로 다른 시선과 시간을 한 화면에 병치한 딥틱으로 구성했다. 부분과 전체, 내부와 외부, 의례의 움직임과 공간의 침묵이 서로 응답하도록 했다."],
         intro_en=["Seowon and hyanggyo remain as architecture, yet their essence lies in the traditions of learning, ritual, and human movement that have continued within them over time.",
                   "Rather than merely documenting their structures, I looked toward gates and courtyards, hands and gestures preparing for ancestral rites, and the texture of time retained in empty spaces. Through moments in which nature and architecture, ritual and daily life meet, these photographs consider how the past continues within the present.",
                   "Several works are composed as diptychs, bringing different viewpoints and moments together within a single frame. Detail and whole, interior and exterior, ritual movement and spatial silence respond to one another."])
]

def header(depth=0, current=""):
    p = "../" * depth
    links = [("Works", "works.html"), ("About", "about.html"), ("Exhibitions", "exhibitions.html")]
    nav = "".join(f'<a href="{p}{url}"' + (' aria-current="page"' if title == current else '') + f'>{title}</a>' for title,url in links)
    return f'''<header class="site-header"><a class="wordmark" href="{p}index.html" aria-label="A True Travel, home">A True Travel</a><nav aria-label="Main navigation">{nav}</nav></header>'''

def page(title, body, depth=0, current="", description=""):
    p = "../" * depth
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{escape(description or title, quote=True)}"><title>{escape(title)} — A True Travel</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;500;600&display=swap" rel="stylesheet"><link rel="stylesheet" href="{p}assets/css/style.css"></head><body><a class="skip-link" href="#main">본문으로 이동</a>{header(depth,current)}<main id="main">{body}</main><footer class="site-footer"><span>A True Travel</span><span>© 2026 Seo Seok-Jang. All photographs and texts reserved.</span></footer></body></html>'''

def paras(items, lang):
    return f'<div class="statement" lang="{lang}">' + ''.join(f'<p>{escape(x)}</p>' for x in items) + '</div>'

def files_for(s):
    a = sorted((IMG / s['folder']).rglob(f"{s['prefix']}-*.jpg"), key=lambda f:int(f.stem.rsplit('-',1)[1]))
    assert len(a) in (12,16,18,19), (s['slug'], len(a))
    assert [int(f.stem.rsplit('-',1)[1]) for f in a] == list(range(1,len(a)+1)), s['slug']
    return a

def plate(f, i, s):
    with Image.open(f) as im: w,h=im.size
    rel=f.relative_to(ROOT).as_posix()
    orientation='portrait' if h>w*1.14 else 'landscape'
    # No fabricated place/year: a quiet plate number serves as a sequence marker.
    return f'''<figure class="plate {orientation}"><img src="../{rel}" width="{w}" height="{h}" alt="{escape(s['ko'])} 시리즈 작품 {i:02d}" loading="lazy" decoding="async"><figcaption><span>{i:02d} / {len(files_for(s)):02d}</span></figcaption></figure>'''

def gallery(s, next_s):
    a=files_for(s)
    content=f'''<div class="series-heading"><a class="back-link" href="../works.html">Works</a><span class="eyebrow">{escape(s['category'])} · {len(a):02d} photographs</span><h1>{escape(s['ko'])}</h1><p class="english-title" lang="en">{escape(s['en'])}</p></div><div class="series-statement">{paras(s['intro_ko'],'ko')}{paras(s['intro_en'],'en')}</div><div class="sequence">'''
    if s['slug']=='royal-tombs':
        content += '<h2 class="sequence-chapter">I. 풍경의 형태 <span>Form of the Landscape</span></h2>'
    for i,f in enumerate(a,1):
        if s['slug']=='royal-tombs' and i==9:
            content += '<h2 class="sequence-chapter">II. 시간의 입자 <span>Grain of Time</span></h2>'
        content += plate(f,i,s)
    content += f'''</div><a class="next-project" href="{next_s['slug']}.html"><span>Next project</span><strong>{escape(next_s['ko'])}</strong><em>{escape(next_s['en'])}</em></a>'''
    (ROOT/'works'/f"{s['slug']}.html").write_text(page(s['ko']+' / '+s['en'],content,1,'Works',s['ko']+' · '+s['en']),encoding='utf-8')

def work_row(s):
    a=files_for(s);cover=s['cover']
    return f'''<article class="work-row"><a class="work-image" href="works/{s['slug']}.html"><img src="assets/images/{cover}" alt="{escape(s['ko'])} 대표 작품" loading="lazy"></a><div class="work-copy"><span class="eyebrow">{escape(s['category'])} / {len(a):02d}</span><h3><a href="works/{s['slug']}.html">{escape(s['ko'])}</a></h3><p lang="en">{escape(s['en'])}</p><a class="view-link" href="works/{s['slug']}.html">작품 보기 <span aria-hidden="true">↗</span></a></div></article>'''

def main():
    (ROOT/'works').mkdir(exist_ok=True)
    for i,s in enumerate(SERIES): gallery(s,SERIES[(i+1)%len(SERIES)])
    home='''<section class="home-hero"><div class="home-copy"><span class="eyebrow">Photography by Seo Seok-Jang</span><h1>고요와 시간,<br>기억과 인간의 흔적</h1><p lang="en">Silence, Time, Memory, and Human Traces</p><a class="view-link" href="works.html">작업 보기 <span aria-hidden="true">↗</span></a></div><figure class="home-image"><img src="assets/images/sea-in-me/sea-in-me-11.jpg" alt="파도가 바위에 스며드는 흑백 바다 풍경" width="2400" loading="eager"><figcaption>내 안의 바다 / The Sea in Me</figcaption></figure></section><section class="home-intro"><p>바다와 산사, 기도의 흔적과 오래된 땅.<br>한 장소에 머물며, 그곳에 남은 시간을 바라봅니다.</p><a href="works.html">Selected works <span aria-hidden="true">↗</span></a></section>'''
    (ROOT/'index.html').write_text(page('서석장 사진 아카이브',home,description='사진작가 서석장의 작품 아카이브. 바다, 산사, 기도의 흔적, 한국의 문화유산.'),encoding='utf-8')
    works='''<div class="page-heading"><span class="eyebrow">Archive</span><h1>Works</h1><p>고요와 시간, 기억과 인간의 흔적을 바라보는 사진 프로젝트.</p></div><section class="works-list" aria-label="사진 프로젝트">'''+''.join(work_row(s) for s in SERIES[:3])+'''<div class="works-divider"><span>한국의 문화유산</span><span lang="en">Korean Cultural Heritage</span></div>'''+''.join(work_row(s) for s in SERIES[3:])+'</section>'
    (ROOT/'works.html').write_text(page('Works',works,current='Works',description='서석장의 사진 프로젝트 6개와 작품 95점.'),encoding='utf-8')
    # Preserve the supplied draft's author-approved-looking biography and CV entries verbatim pending fact review.
    for name,title in [('about','About'),('exhibitions','Exhibitions')]:
        old=(ROOT/'content'/f'{name}.html').read_text(encoding='utf-8')
        content=old.split('<main>',1)[1].split('</main>',1)[0]
        content=content.replace('<div class="wrap">','<div class="text-page">').replace('<h1 class="section-title">','<h1 class="page-title">')
        if name=='about':
            content=content.replace('</h1>', '</h1><figure class="author-portrait"><img src="assets/images/profile-sjseo.jpg" alt="사진작가 서석장 흑백 인물 사진" width="1855" height="2400" loading="lazy"></figure>', 1)
        (ROOT/f'{name}.html').write_text(page(title,content,current=title),encoding='utf-8')
    # The draft contact page contains an unverified mailbox and a '#' Instagram link.
    (ROOT/'contact.html').unlink(missing_ok=True)

if __name__=='__main__': main()
