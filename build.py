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
             "평화로운 수평선 너머에는 어부의 생업이 있다. 파도와 날씨가 어제의 모습을 지우는 동안, 나는 다시 오지 않을 오늘의 바다를 바라본다.",
             "바다 앞에 서면 살아가며 마주한 환희와 후회, 말로 다 전하지 못한 마음을 내려놓게 된다. 매번 달라지는 수면을 찍는 일은 동시에 내 안의 변화를 확인하는 일이었다.",
             "나는 어머니의 품을 닮은 그 깊고 푸른 위로와, 그 안에서 마주한 나 자신의 모습을 사진이라는 문장으로 기록하고자 한다."],
         intro_en=[
             "What is not recorded eventually disappears. Through my camera, I have sought to preserve the sea as it changes from one day to the next.",
             "Beyond the peaceful horizon lies the work of fishing. As waves and weather erase yesterday’s appearance, I look at a sea that will never be quite the same again.",
             "Standing before it, I release joys, regrets, and feelings I cannot put into words. Photographing the changing surface has also become a way of noticing change within myself.",
             "Through photography, I seek to record its deep blue consolation, reminiscent of a mother’s embrace, and the image of myself encountered within it."]),
    dict(slug="traces-of-prayer", ko="기도의 흔적들", en="Traces of Prayer", category="Works",
         cover="traces-of-prayer/traces-of-prayer-10.jpg", folder="traces-of-prayer", prefix="traces-of-prayer",
         intro_ko=["사람들은 돌을 쌓고 촛불을 밝히며, 동전과 지폐, 기원문에 말로 다 전하지 못한 바람을 맡긴다.",
                   "나는 기도하는 얼굴보다 손이 놓고 간 사물을 바라보았다. 돌탑과 연등, 작은 헌금은 주인이 떠난 뒤에도 누군가의 간절함을 가리킨다. 사람은 화면 밖에 있지만, 그가 행한 기도는 사물의 배열 속에 남는다."],
         intro_en=["People stack stones, light candles, and leave coins, banknotes, and written wishes, entrusting them with hopes they cannot fully express.",
                   "I looked toward what hands had left behind rather than toward the faces of those praying. Stone cairns, lanterns, and small offerings point to a wish even after its maker has gone. The person remains outside the frame; the act of prayer is visible in the arrangement of things."]),
    dict(slug="silence-temple", ko="산사의 고요함", en="Silence of the Mountain Temple", category="Works",
         cover="silence-temple/silence-temple-15.jpg", folder="silence-temple", prefix="silence-temple",
         intro_ko=["숲길에서 문으로, 문에서 마당으로 들어간다. 산사의 공간은 한 번에 드러나지 않고, 경계를 지날 때마다 시선의 속도를 바꾼다.",
                   "처마 아래의 빛과 문틈의 어둠, 아무도 없는 마당을 따라가다 보면 비어 있음은 결핍이 아니라 바라볼 여백이 된다.",
                   "이 작업은 사찰의 건축을 목록처럼 보여주기보다, 안과 밖을 오가는 동선과 잠시 멈추게 하는 빈 공간을 따라간다."],
         intro_en=["From forest path to gate, and from gate to courtyard, the temple does not reveal itself at once. Each threshold changes the pace of looking.",
                   "Light beneath the eaves, darkness inside a doorway, and an unoccupied courtyard make emptiness feel less like an absence than a space in which to look.",
                   "Rather than cataloguing temple buildings, this series follows movement between inside and outside and the open spaces that ask me to pause."]),
    dict(slug="gaya-tumuli", ko="가야고분군", en="Gaya Tumuli", category="Korean Cultural Heritage",
         cover="gaya-tumuli/Gaya_Tumuli-09.jpg", folder="gaya-tumuli", prefix="Gaya_Tumuli",
         intro_ko=["가야고분군은 박물관 안의 유물이 아니라 마을과 들판, 현대의 건물에 맞닿은 지형이다. 사람들이 걷고 놀고 지나가는 길 곁에 봉분이 놓인다.",
                   "사람이 프레임에서 사라지면 나무와 안개, 빛이 같은 언덕의 표정을 바꾼다. 이 연작은 고분을 과거의 증거로만 보지 않고, 오늘의 일상과 접촉하는 장소로 바라본다."],
         intro_en=["The Gaya tumuli are not objects enclosed in a museum. They are a terrain beside villages, fields, and modern buildings, with burial mounds near paths where people walk, play, and pass by.",
                   "When people leave the frame, trees, mist, and light alter the appearance of the same hills. This series looks at the tumuli as places in contact with everyday life, beyond their role as evidence of the past."]),
    dict(slug="royal-tombs", ko="왕릉과 고분", en="Royal Tombs and Tumuli", category="Korean Cultural Heritage",
         cover="royal-tombs/bw/Royal-Tombs-Tumuli-07.jpg", folder="royal-tombs", prefix="Royal-Tombs-Tumuli",
         intro_ko=["왕릉과 고분의 봉분은 산의 능선을 닮았지만, 그 형태를 선명히 보여주는 것만으로는 이 장소를 다 말할 수 없다.",
                   "전반부의 흑백사진은 봉분과 나무, 사람의 크기와 거리를 또렷하게 드러낸다. 후반부에서는 같은 풍경을 거친 입자로 바꾸어 형태가 흩어지는 과정을 보여준다.",
                   "두 표현의 차이는 무엇을 볼 수 있고 무엇을 기억하게 되는가를 묻는다. 마지막에 남는 문과 봉분은 보이는 풍경과 사라진 존재 사이에 놓인 경계처럼 다가온다."],
         intro_en=["The contours of royal tombs and ancient tumuli resemble mountain ridgelines, but a clear depiction of their form cannot tell the whole story of these places.",
                   "The opening black-and-white photographs show the scale and distance between burial mounds, trees, and people. In the latter part, the same landscape becomes coarse grain, and its distinct forms begin to break apart.",
                   "The shift between these two modes asks what can be seen and what stays in memory. The final doorway and mound suggest a threshold between the visible landscape and those no longer present."]),
    dict(slug="seowon-hyanggyo", ko="한국의 서원과 향교", en="Seowon and Hyanggyo of Korea", category="Korean Cultural Heritage",
         cover="seowon-hyanggyo/Seowon-Hyanggyo-11.jpg", folder="seowon-hyanggyo", prefix="Seowon-Hyanggyo",
         intro_ko=["서원과 향교에서 배움과 제향은 건물의 이름만으로 설명되지 않는다. 문을 열고 마당을 건너며 의례를 준비하는 몸짓 속에서 전통은 지금도 실행된다.",
                   "나는 전각 전체와 손의 동작, 내부와 외부를 번갈아 보았다. 일부 사진을 딥틱으로 묶은 까닭은 한 장면만으로는 건축과 행위의 관계를 다 보여줄 수 없기 때문이다.",
                   "이 연작은 옛 건물을 보존된 형태로만 제시하지 않고, 사람들이 그 안에서 배우고 모이고 예를 행하는 방식에 주목한다."],
         intro_en=["At seowon and hyanggyo, learning and ancestral rites cannot be understood from the names of buildings alone. Tradition is enacted in opening a gate, crossing a courtyard, and preparing a ceremony.",
                   "I move between the whole hall and the gesture of a hand, between interior and exterior. Some photographs form diptychs because a single view cannot fully show the relationship between architecture and action.",
                   "This series considers historic buildings through the ways people learn, gather, and perform rites within them, beyond their preserved form."])
]

def header(depth=0, current=""):
    p = "../" * depth
    links = [("About", "about.html"), ("Exhibitions", "exhibitions.html"), ("Contact", "contact.html")]
    menu = ''.join(
        ('<span class="works-menu-label">한국의 문화유산</span>' if i == 3 else '') +
        f'<a href="{p}works/{s["slug"]}.html"><span>{escape(s["ko"])}</span><small lang="en">{escape(s["en"])}</small></a>'
        for i, s in enumerate(SERIES)
    )
    nav = f'<div class="nav-works"><a href="{p}works.html"' + (' aria-current="page"' if current == 'Works' else '') + f'>Works</a><button class="works-toggle" type="button" aria-label="작업 목록 펼치기" aria-expanded="false" aria-controls="works-submenu">⌄</button><div class="works-menu" id="works-submenu" hidden>{menu}</div></div>'
    nav += "".join(f'<a href="{p}{url}"' + (' aria-current="page"' if title == current else '') + f'>{title}</a>' for title,url in links)
    return f'''<header class="site-header"><a class="wordmark" href="{p}index.html" aria-label="A True Travel, home">A True Travel</a><nav aria-label="Main navigation">{nav}</nav></header>'''

def page(title, body, depth=0, current="", description=""):
    p = "../" * depth
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{escape(description or title, quote=True)}"><title>{escape(title)} — A True Travel</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;500&display=swap" rel="stylesheet"><link rel="stylesheet" href="{p}assets/css/style.css?v=20260926-11"><script src="{p}assets/js/navigation.js?v=20260926-11" defer></script></head><body><a class="skip-link" href="#main">본문으로 이동</a>{header(depth,current)}<main id="main">{body}</main><footer class="site-footer"><span>A True Travel</span><span>© 2026 Seo Seok-Jang. All photographs and texts reserved.</span></footer></body></html>'''

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
    home='''<section class="home-hero"><div class="home-copy"><span class="eyebrow">Photography by Seo Seok-Jang</span><h1>고요와 시간,<br>기억과 인간의 흔적</h1><p class="home-subtitle" lang="en">Silence, Time, Memory, and Human Traces</p><div class="home-manifesto"><p>진짜 여행은 가장 먼 곳이 아니라,<br>가장 오래 머문 자리에서 시작된다.</p><p lang="en">A true travel begins not in the farthest place,<br>but in the place where one has stayed the longest.</p></div><a class="view-link" href="works.html">작업 보기 <span aria-hidden="true">↗</span></a></div><figure class="home-image"><img src="assets/images/sea-in-me/sea-in-me-11.jpg" alt="파도가 바위에 스며드는 흑백 바다 풍경" width="2400" loading="eager"><figcaption>내 안의 바다 / The Sea in Me</figcaption></figure></section><section class="home-intro"><div class="home-intro-copy"><p>바다와 산사, 기도의 흔적과 오래된 땅.<br>한 장소에 머물며, 그곳에 남은 시간을 바라봅니다.</p><p class="home-intro-en" lang="en">The sea, mountain temples, traces of prayer, and ancient ground.<br>I stay with each place and look at the time it holds.</p></div><a href="works.html">Selected works <span aria-hidden="true">↗</span></a></section>'''
    (ROOT/'index.html').write_text(page('서석장 사진 아카이브',home,description='사진작가 서석장의 작품 아카이브. 바다, 산사, 기도의 흔적, 한국의 문화유산.'),encoding='utf-8')
    works='''<div class="page-heading"><span class="eyebrow">Archive</span><h1>Works</h1><p>고요와 시간, 기억과 인간의 흔적을 바라보는 사진 프로젝트.</p></div><section class="works-list" aria-label="사진 프로젝트">'''+''.join(work_row(s) for s in SERIES[:3])+'''<div class="works-divider"><span>한국의 문화유산</span><span lang="en">Korean Cultural Heritage</span></div>'''+''.join(work_row(s) for s in SERIES[3:])+'</section>'
    (ROOT/'works.html').write_text(page('Works',works,current='Works',description='서석장의 사진 프로젝트 6개와 작품 95점.'),encoding='utf-8')
    # Preserve the supplied draft's author-approved-looking biography and CV entries verbatim pending fact review.
    for name,title in [('about','About'),('exhibitions','Exhibitions')]:
        old=(ROOT/'content'/f'{name}.html').read_text(encoding='utf-8')
        content=old.split('<main>',1)[1].split('</main>',1)[0]
        content=content.replace('<div class="wrap">','<div class="text-page">').replace('<h1 class="section-title">','<h1 class="page-title">')
        if name == 'exhibitions':
            content=content.replace('<div class="text-page">','<div class="text-page exhibitions-page">',1)
        if name=='about':
            content=content.replace('<div class="text-page">','<div class="text-page about-page">',1)
            content=content.replace('</h1>', '</h1><div class="about-intro"><figure class="author-portrait"><img src="assets/images/profile-sjseo.jpg" alt="사진작가 서석장 흑백 인물 사진" width="1855" height="2400" loading="eager"></figure>', 1)
            content=content.replace('<div class="bi-divider">','</div><div class="bi-divider">',1)
        (ROOT/f'{name}.html').write_text(page(title,content,current=title),encoding='utf-8')
    contact='''<div class="text-page contact-page"><span class="eyebrow">Inquiries</span><h1 class="page-title">Contact</h1><p>전시, 소장, 출판 및 프로젝트 협업 문의는 이메일로 연락해 주세요.</p><p lang="en">For exhibition, collection, publishing, and project inquiries, please write by email.</p><a class="contact-email" href="mailto:sj.seo57@gmail.com">sj.seo57@gmail.com</a><p class="contact-note">서석장 · Seo Seok-Jang</p></div>'''
    (ROOT/'contact.html').write_text(page('Contact',contact,current='Contact',description='서석장 사진작가 전시 및 출판 문의'),encoding='utf-8')

if __name__=='__main__': main()
