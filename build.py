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
             '기록되지 않은 것은 사라지기에, 변해가는 바다의 오늘을 카메라에 담아왔다.',
             '평화로운 수평선 너머에는 어부의 생업이 있다. 파도와 날씨가 어제의 흔적을 지우는 동안, 나는 다시 오지 않을 오늘의 바다를 바라본다.',
             '바다 앞에 서면 살아오며 마주한 환희와 후회, 말로 다 전하지 못한 마음을 내려놓게 된다. 끊임없이 변하는 바다를 바라보고 기록하는 동안, 나 역시 그 시간 속에서 조금씩 변해왔음을 알게 되었다.',
             '나는 어머니의 품을 닮은 깊고 푸른 바다의 위로와, 그 앞에서 마주한 나 자신의 모습을 사진으로 기록하고자 한다.'],
         intro_en=[
             'What goes unrecorded eventually disappears. For years, I have photographed the sea as it changes from one day to the next.',
             'Beyond the peaceful horizon lies the daily life of those who make their living from the sea. As waves and weather erase the traces of yesterday, I look out at a sea that will never return in quite the same way.',
             'Standing before the sea, I find myself letting go of the joys and regrets of life, along with feelings that words cannot fully express. As I watch and photograph its ceaseless changes, I have come to recognize the changes within myself as well.',
             'In the deep blue sea, I find a sense of comfort that reminds me of a mother’s embrace. Through photography, I seek to record both that solace and the self I encounter standing before it.']),
    dict(slug="traces-of-prayer", ko="기도의 흔적들", en="Traces of Prayer", category="Works",
         cover="traces-of-prayer/traces-of-prayer-10.jpg", folder="traces-of-prayer", prefix="traces-of-prayer",
         intro_ko=[
             '사람들은 돌을 쌓고 촛불을 밝히며, 말로 다 전하지 못한 바람을 동전과 지폐, 기원문에 실어 놓는다.',
             '나는 기도하는 얼굴보다 그 뒤에 남겨진 것들을 바라보았다. 돌탑과 연등, 작은 헌금은 주인이 떠난 자리에서도 누군가의 간절함을 가리킨다. 사람은 장면 밖에 있지만, 그가 행한 기도는 흔적이 되어 그 자리에 남는다.'],
         intro_en=[
             'People stack stones, light candles, and leave coins, banknotes, and written prayers, entrusting them with hopes they cannot fully express.',
             'I looked toward what had been left behind rather than toward the faces of those praying. Stone cairns, lotus lanterns, and small offerings point to a wish even after its maker has gone. The person remains outside the frame, but the prayer they performed lingers on as a trace in that place.']),
    dict(slug="silence-temple", ko="산사의 고요함", en="Silence of the Mountain Temple", category="Works",
         cover="silence-temple/silence-temple-15.jpg", folder="silence-temple", prefix="silence-temple",
         intro_ko=[
             '숲길에서 문으로, 문에서 마당으로 들어간다. 산사의 공간은 한 번에 드러나지 않고, 경계를 하나씩 지나며 조금씩 모습을 드러낸다.',
             '처마 아래의 빛과 문틈의 어둠, 아무도 없는 마당을 따라가다 보면 비어 있음은 결핍이 아니라 바라볼 여백이 된다.',
             '이 작업은 사찰의 건물을 목록처럼 보여주기보다, 경계를 지나며 달라지는 풍경과 잠시 머물게 하는 빈 공간을 담아낸다.'],
         intro_en=[
             'From forest path to gate, and from gate to courtyard, the mountain temple reveals itself gradually, one threshold at a time.',
             'Following the light beneath the eaves, the darkness through a doorway, and an empty courtyard, emptiness comes to feel not like an absence, but like space in which to look.',
             'Rather than cataloguing the temple buildings, this series captures the changing views beyond each threshold and the empty spaces that invite a moment of pause.']),
    dict(slug="gaya-tumuli", ko="가야고분군", en="Gaya Tumuli", category="Korean Cultural Heritage",
         cover="gaya-tumuli/Gaya_Tumuli-09.jpg", folder="gaya-tumuli", prefix="Gaya_Tumuli",
         intro_ko=[
             '가야고분군은 박물관 안의 유물이 아니라 마을과 들판, 현대의 건물에 맞닿은 지형이다. 사람들이 걷고 놀고 오가는 일상 속에 봉분이 자리한다.',
             '사람이 프레임에서 사라지면 나무와 안개, 빛이 같은 언덕의 표정을 바꾼다. 이 연작은 오랜 시간을 품은 고분이 오늘의 삶과 만나는 모습을 바라본다.'],
         intro_en=[
             'The Gaya tumuli are not objects enclosed in a museum, but part of a landscape that meets villages, fields, and modern buildings. The burial mounds remain within the everyday spaces where people walk, play, and pass by.',
             'When people leave the frame, trees, mist, and light transform the appearance of the same hills. This series looks at how these ancient burial mounds, carrying the passage of time, meet the life of the present.']),
    dict(slug="royal-tombs", ko="왕릉과 고분", en="Royal Tombs and Tumuli", category="Korean Cultural Heritage",
         cover="royal-tombs/bw/Royal-Tombs-Tumuli-07.jpg", folder="royal-tombs", prefix="Royal-Tombs-Tumuli",
         intro_ko=[
             '왕릉과 고분의 봉분은 산의 능선을 닮았지만, 그 형태를 선명히 보여주는 것만으로는 이 장소를 다 말할 수 없다.',
             '전반부의 흑백사진은 봉분과 나무, 사람의 크기와 거리를 또렷하게 드러낸다. 후반부에서는 같은 풍경을 거친 입자로 바꾸어 형태가 흩어지는 과정을 보여준다.',
             '두 표현의 차이를 통해 눈앞에 보이는 풍경과 시간 속에 남는 기억을 함께 바라보고자 했다.'],
         intro_en=[
             'The contours of royal tombs and ancient tumuli resemble mountain ridgelines, but a clear depiction of their form cannot tell the whole story of these places.',
             'The opening black-and-white photographs show the scale and distance between burial mounds, trees, and people. In the latter part, the same landscape becomes coarse grain, and its distinct forms begin to break apart.',
             'Through the contrast between these two approaches, I seek to consider both the landscape before us and the memories that remain over time.']),
    dict(slug="seowon-hyanggyo", ko="한국의 서원과 향교", en="Seowon and Hyanggyo of Korea", category="Korean Cultural Heritage",
         cover="seowon-hyanggyo/Seowon-Hyanggyo-11.jpg", folder="seowon-hyanggyo", prefix="Seowon-Hyanggyo",
         intro_ko=[
             '서원과 향교는 오래된 건축물로만 남아 있는 공간이 아니다. 문을 열고 마당을 건너며 의례를 준비하는 모습 속에서 오랜 전통은 지금도 이어진다.',
             '나는 전각의 모습과 그 안에서 이루어지는 작은 몸짓을 함께 바라보았다. 때로는 안에서 밖을, 밖에서 안을 바라보며 건축과 그 안에서 이루어지는 행위를 함께 바라보고자 했다. 일부 사진을 딥틱으로 구성한 것도 서로 다른 장면이 만나 하나의 이야기를 이루도록 하기 위해서다.',
             '이 연작은 옛 건축의 형태를 기록하는 데 머물지 않고, 그 공간에서 이어지는 배움과 만남, 의례를 통해 오늘까지 이어져 온 서원과 향교의 모습을 담고자 한다.'],
         intro_en=[
             'Seowon and hyanggyo are more than historic buildings preserved from the past. Their traditions continue today in the acts of opening gates, crossing courtyards, and preparing for ceremonies.',
             'I looked at both the architecture and the small gestures taking place within it. At times, I looked from inside out and from outside in, seeking to bring the architecture and the activities within it into view together. Some photographs are arranged as diptychs so that separate scenes can come together to form a single story.',
             'This series goes beyond recording the form of historic architecture. Through the learning, gatherings, and rituals that continue within these spaces, I seek to portray seowon and hyanggyo as places whose traditions remain part of the present.'])
]


# Layouts approved in the published HTML; keep them on regeneration.
SERIES_PLATE_CLASSES = {
    "sea-in-me": {2: "lower-02"},
    "royal-tombs": {5: "align-bottom-05", 7: "align-bottom-07"},
}
SERIES_HEAD = {
    'sea-in-me': """
<style>
@media (min-width: 769px) {
  .plate.lower-02 {
    transform: translateY(16px);
  }
}
</style>
<style>
@media (min-width: 769px) {
  .sequence-tail-single {
    display: flex;
    justify-content: center;
  }
  .sequence-tail-single > .plate {
    width: 100%;
  }
  .sequence-tail-pair {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
    gap: clamp(18px, 3vw, 48px);
    align-items: end;
  }
  .sequence-tail-pair > .plate {
    margin: 0;
    width: 100%;
  }
}
</style>
<style>
@media (min-width: 769px) {
  .sequence > .sequence-tail-single,
  .sequence > .sequence-tail-pair {
    grid-column: 1 / -1;
    width: 100%;
  }

  .sequence-tail-single {
    display: flex;
    justify-content: center;
  }

  .sequence-tail-single > .plate {
    width: 100%;
    margin-left: auto;
    margin-right: auto;
  }

  .sequence-tail-pair {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
    gap: clamp(18px, 3vw, 48px);
    align-items: end;
  }

  .sequence-tail-pair > .plate {
    width: 100%;
    margin: 0;
  }
}
</style>
""",
    'royal-tombs': """
<style>
@media (min-width: 769px) {
  .plate.align-bottom-05 {
    padding-top: calc((1197 - 1139) / 2400 * min(100%, 2400px));
  }
  .plate.align-bottom-07 {
    padding-top: calc((1523 - 1254) / 2400 * min(100%, 2400px));
  }
}
</style>
""",
}

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

def page(title, body, depth=0, current="", description="", extra_head=""):
    p = "../" * depth
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{escape(description or title, quote=True)}"><title>{escape(title)} — A True Travel</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;500&display=swap" rel="stylesheet"><link rel="stylesheet" href="{p}assets/css/style-v12.css"><script src="{p}assets/js/navigation.js?v=20260926-12" defer></script>{extra_head}</head><body><a class="skip-link" href="#main">본문으로 이동</a>{header(depth,current)}<main id="main">{body}</main><footer class="site-footer"><span>A True Travel</span><span>© 2026 Seo Seok-Jang. All photographs and texts reserved.</span></footer><!-- Cloudflare Web Analytics --><script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "b6760dd5d5564f1ea270358559aa7901"}}'></script><!-- End Cloudflare Web Analytics --></body></html>'''

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
    extra_class = SERIES_PLATE_CLASSES.get(s['slug'], {}).get(i)
    if extra_class:
        orientation += ' ' + extra_class
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
        if s['slug'] == 'sea-in-me' and i >= 13:
            if i == 13:
                content += '<div class="sequence-tail-single">'
            elif i in (14, 16, 18):
                content += '<div class="sequence-tail-pair">'
        content += plate(f,i,s)
        if s['slug'] == 'sea-in-me' and i in (13, 15, 17, 19):
            content += '</div>'
    content += f'''</div><a class="next-project" href="{next_s['slug']}.html"><span>Next project</span><strong>{escape(next_s['ko'])}</strong><em>{escape(next_s['en'])}</em></a>'''
    (ROOT/'works'/f"{s['slug']}.html").write_text(page(s['ko']+' / '+s['en'],content,1,'Works',s['ko']+' · '+s['en'],extra_head=SERIES_HEAD.get(s['slug'], '')),encoding='utf-8')

def work_row(s):
    a=files_for(s);cover=s['cover']
    return f'''<article class="work-row"><a class="work-image" href="works/{s['slug']}.html"><img src="assets/images/{cover}" alt="{escape(s['ko'])} 대표 작품" loading="lazy"></a><div class="work-copy"><span class="eyebrow">{escape(s['category'])} / {len(a):02d}</span><h3><a href="works/{s['slug']}.html">{escape(s['ko'])}</a></h3><p lang="en">{escape(s['en'])}</p><a class="view-link" href="works/{s['slug']}.html">작품 보기 <span aria-hidden="true">↗</span></a></div></article>'''

def main():
    (ROOT/'works').mkdir(exist_ok=True)
    for i,s in enumerate(SERIES): gallery(s,SERIES[(i+1)%len(SERIES)])
    home='''<section class="home-hero"><div class="home-copy"><span class="eyebrow">Photography by Seo Seok-Jang</span><h1>고요와 시간,<br>기억과 인간의 흔적</h1><p class="home-subtitle" lang="en">Silence, Time, Memory, and Human Traces</p><div class="home-manifesto"><p>진정한 여행은 가장 먼 곳이 아니라,<br>가장 오래 머문 자리에서 시작된다.</p><p lang="en">A true travel begins not in the farthest place,<br>but in the place where one has stayed the longest.</p></div><a class="view-link" href="works.html">작업 보기 <span aria-hidden="true">↗</span></a></div><figure class="home-image"><img src="assets/images/sea-in-me/sea-in-me-11.jpg" alt="파도가 바위에 스며드는 흑백 바다 풍경" width="2400" loading="eager"><figcaption>내 안의 바다 / The Sea in Me</figcaption></figure></section><section class="home-intro"><div class="home-intro-copy"><p>바다, 산사와 기도의 흔적, 고분 ...<br>한 장소에 머물며, 그곳에 남은 시간을 바라봅니다.</p><p class="home-intro-en" lang="en">The sea, mountain temples and traces of prayer, burial mounds ...<br>I stay with each place and look at the time it holds.</p></div><a href="works.html">Selected works <span aria-hidden="true">↗</span></a></section>'''
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

