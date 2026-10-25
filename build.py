"""Build A True Travel's plain HTML pages from the curated image folders.

Run `python3 build.py` after adding or replacing a web JPEG. Requires Pillow.
"""
from pathlib import Path
from html import escape
import json
from PIL import Image
import os
import shutil
import tempfile

ROOT = Path(__file__).resolve().parent
IMG = ROOT / "assets/images"

COPYRIGHT_PATH = "copyright.html"
LICENSE_URL = "https://www.atruetravel.com/" + COPYRIGHT_PATH
ACQUIRE_LICENSE_URL = "https://www.atruetravel.com/contact.html"

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
    dict(slug="unjusa-infrared", ko="적외선으로 본 운주사 천불천탑", en="Unjusa in Infrared: Stone Buddhas and Pagodas", category="Works",
         cover="unjusa-infrared/unjusa-infrared-06.jpg", folder="unjusa-infrared", prefix="unjusa-infrared", count=6,
         intro_ko=[
             '처음 마주한 운주사의 돌부처와 돌탑은 낯설었다. 이목구비가 희미한 얼굴과 서로 다른 돌의 형태를 바라볼수록, 그 낯섦은 친근함으로 바뀌었다.',
             '나는 적외선으로 이곳을 다시 바라보았다. 나뭇잎은 밝아지고 익숙한 색은 달라졌다. 돌과 나무 사이의 공간은 눈으로 보았을 때와 다른 깊이로 다가왔다.',
             '다른 세상처럼 보이지만, 사진 속 돌과 나무는 내가 서 있던 그 자리에 있다. 이 사진들은 같은 세계가 보는 방식에 따라 얼마나 다르게 드러나는지 묻는다.'],
         intro_en=[
             'The stone Buddhas and pagodas of Unjusa felt unfamiliar at first. As I looked at their faint features and varied forms, that unfamiliarity gradually gave way to a sense of closeness.',
             'I returned to these surroundings through infrared photography. Leaves grew luminous, familiar colours shifted, and the spaces between stone and tree took on a different depth.',
             'Though it may appear to be another world, the stones and trees remain where I stood. These photographs ask how differently the same world can reveal itself through another way of seeing.']),
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
    'unjusa-infrared': """
<style>
.sequence { grid-template-columns: minmax(0, 1fr); max-width: 1120px; }
.sequence .plate.portrait { max-width: 650px; justify-self: center; }
.sequence .plate img { max-height: 82svh; }
</style>
""",
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
        ('<span class="works-menu-label">한국의 문화유산</span>' if s['category'] == 'Korean Cultural Heritage' and (i == 0 or SERIES[i-1]['category'] != s['category']) else '') +
        f'<a href="{p}works/{s["slug"]}.html"><span>{escape(s["ko"])}</span><small lang="en">{escape(s["en"])}</small></a>'
        for i, s in enumerate(SERIES)
    )
    nav = f'<div class="nav-works"><a href="{p}works.html"' + (' aria-current="page"' if current == 'Works' else '') + f'>Works</a><button class="works-toggle" type="button" aria-label="작업 목록 펼치기" aria-expanded="false" aria-controls="works-submenu">⌄</button><div class="works-menu" id="works-submenu" hidden>{menu}</div></div>'
    nav += "".join(f'<a href="{p}{url}"' + (' aria-current="page"' if title == current else '') + f'>{title}</a>' for title,url in links)
    return f'''<header class="site-header"><a class="wordmark" href="{p}index.html" aria-label="A True Travel, home">A True Travel</a><nav aria-label="Main navigation">{nav}</nav></header>'''

SEO_META = {"index.html":["서석장 사진가 | Seo Seok-Jang Photography — A True Travel","사진가 서석장(Seo Seok-Jang)의 공식 웹사이트. 바다, 산사, 기도의 흔적과 한국 문화유산을 기록한 사진 연작과 전시를 소개합니다."],"about.html":["서석장 사진작가 소개 | Seo Seok-Jang — A True Travel","사진가 서석장(Seo Seok-Jang)의 작가 소개. 시간과 기억, 인간의 흔적을 탐구하는 사진 작업과 작가 노트."],"works.html":["서석장 사진 작품 | Works — A True Travel","사진작가 서석장의 사진 연작 7개: 내 안의 바다, 기도의 흔적들, 산사의 고요함, 적외선으로 본 운주사 천불천탑, 가야고분군, 왕릉과 고분, 한국의 서원과 향교."],"exhibitions.html":["서석장 사진전 및 전시 이력 | Exhibitions — A True Travel","사진작가 서석장(Seo Seok-Jang)의 개인전과 단체전 등 전시 활동 기록."],"contact.html":["서석장 사진가 문의 | Contact — A True Travel","사진작가 서석장의 전시, 소장, 출판 및 협업 문의."]}
SERIES_SEO_META = {
    "works/unjusa-infrared.html": ("적외선으로 본 운주사 천불천탑 | 서석장 사진 연작", "사진가 서석장의 적외선 사진 연작 6점. 운주사의 돌부처와 돌탑, 밝게 드러나는 나무를 통해 같은 세계가 다르게 보이는 경험을 탐구합니다."),
    "works/sea-in-me.html": ("내 안의 바다 | 서석장 사진 연작 · The Sea in Me", "사진가 서석장의 「내 안의 바다」. 변화하는 바다와 어부의 삶, 파도와 수평선에 스민 시간과 기억을 사진 19점으로 기록한 연작."),
    "works/traces-of-prayer.html": ("기도의 흔적들 | 서석장 사진 연작 · Traces of Prayer", "사진가 서석장의 「기도의 흔적들」. 돌탑, 연등, 촛불과 봉헌물 등 사람들이 기도한 뒤 남긴 사물과 간절한 바람을 담은 사진 18점."),
    "works/silence-temple.html": ("산사의 고요함 | 서석장 사진 연작 · Mountain Temple", "사진가 서석장의 「산사의 고요함」. 숲길과 문, 마당과 처마를 지나며 드러나는 산사의 경계, 빛, 그림자와 빈 공간을 담은 사진 16점."),
    "works/gaya-tumuli.html": ("가야고분군 | 서석장 문화유산 사진 · Gaya Tumuli", "사진가 서석장의 「가야고분군」. 고분의 곡선과 능선, 안개와 나무, 산책하는 사람들이 어우러진 옛 유산과 오늘의 풍경을 담은 사진 12점."),
    "works/royal-tombs.html": ("왕릉과 고분 | 서석장 흑백사진 · Royal Tombs", "사진가 서석장의 「왕릉과 고분」. 봉분과 나무, 사람의 거리를 선명한 흑백과 거친 입자 표현으로 대비해 시간과 기억을 탐구한 사진 18점."),
    "works/seowon-hyanggyo.html": ("한국의 서원과 향교 | 서석장 문화유산 사진", "사진가 서석장의 「한국의 서원과 향교」. 전통 건축의 문과 마당, 사람들의 의례와 움직임을 흑백사진과 딥틱으로 기록한 사진 12점."),
}

PERSON_JSON_LD = "{\"@context\":\"https://schema.org\",\"@type\":\"Person\",\"name\":\"서석장\",\"alternateName\":\"Seo Seok-Jang\",\"url\":\"https://www.atruetravel.com/\",\"jobTitle\":\"사진작가\",\"mainEntityOfPage\":\"https://www.atruetravel.com/about.html\"}"

def page(title, body, depth=0, current="", description="", extra_head="", canonical_path=None):
    if canonical_path is None:
        canonical_path = {"서석장 사진 아카이브":"index.html","Works":"works.html","About":"about.html","Exhibitions":"exhibitions.html","Contact":"contact.html"}.get(title,"")
    meta = SERIES_SEO_META.get(canonical_path) or SEO_META.get(canonical_path)
    if meta:
        title = meta[0].removesuffix(" — A True Travel")
        description = meta[1]
    canonical_url = "https://www.atruetravel.com/" + ("" if canonical_path == "index.html" else canonical_path)
    canonical_tag = '<link rel="canonical" href="' + canonical_url + '">' if canonical_path else ""
    schema_tag = '<script type="application/ld+json">' + PERSON_JSON_LD + '</script>' if canonical_path == "index.html" else ""
    naver_tag = '<meta name="naver-site-verification" content="bcafe79e9535a1b90f38738731f5dd5050498dba" />' if canonical_path == "index.html" else ""
    extra_head = canonical_tag + schema_tag + naver_tag + extra_head
    p = "../" * depth
    style_version = "?v=20261017-logo" if current == "About" else ""
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{escape(description or title, quote=True)}"><title>{escape(title)} — A True Travel</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;500&display=swap" rel="stylesheet"><link rel="stylesheet" href="{p}assets/css/style-v12.css{style_version}"><script src="{p}assets/js/navigation.js?v=20260926-12" defer></script>{extra_head}</head><body><a class="skip-link" href="#main">본문으로 이동</a>{header(depth,current)}<main id="main">{body}</main><footer class="site-footer"><span>A True Travel</span><span>© 2026 Seo Seok-Jang. All photographs and texts reserved.</span></footer></body></html>'''

def paras(items, lang):
    return f'<div class="statement" lang="{lang}">' + ''.join(f'<p>{escape(x)}</p>' for x in items) + '</div>'

def files_for(s):
    a = sorted((IMG / s['folder']).rglob(f"{s['prefix']}-*.jpg"), key=lambda f:int(f.stem.rsplit('-',1)[1]))
    assert len(a) == s['count'] if 'count' in s else len(a) in (12,16,18,19), (s['slug'], len(a))
    assert [int(f.stem.rsplit('-',1)[1]) for f in a] == list(range(1,len(a)+1)), s['slug']
    return a

SERIES_ALT_CONTEXT = {
    "unjusa-infrared": "운주사의 돌부처와 돌탑, 나무를 적외선으로 바라본 사진",
    "sea-in-me": "바다의 변화와 시간, 기억을 기록한 흑백 사진",
    "traces-of-prayer": "기도를 마친 사람들이 남긴 사물과 간절한 바람을 탐구한 사진",
    "silence-temple": "산사의 문과 마당, 경계와 빈 공간을 탐구한 사진",
    "gaya-tumuli": "고분의 오랜 시간과 오늘의 일상이 만나는 풍경 사진",
    "royal-tombs": "봉분과 능선의 형태, 시간의 기억을 탐구한 사진",
    "seowon-hyanggyo": "전통 건축과 그 공간에서 이어지는 생활과 의례를 탐구한 사진",
}

ALT_DESCRIPTIONS = {
    "unjusa-infrared": {
        1: "주황빛으로 드러나는 나무를 배경으로 돌부처와 여러 석탑이 서 있는 운주사 적외선 풍경",
        2: "밝은 나뭇잎 아래 나무줄기와 크기가 다른 석탑들이 겹쳐 보이는 운주사 적외선 사진",
        3: "푸른 하늘과 소나무 가지 아래 서 있는 석탑을 세로 구도로 담은 운주사 적외선 사진",
        4: "밝은 나무와 푸른 하늘 앞에 둥근 돌들이 층층이 쌓인 운주사의 석탑",
        5: "밝은 숲과 하늘을 배경으로 거친 돌이 쌓인 석탑을 가까이 바라본 운주사 적외선 사진",
        6: "넓은 바위 위 작은 석탑과 그 위로 뻗은 소나무 가지를 담은 운주사 적외선 사진",
    },
    "sea-in-me": {
        1: "흐린 하늘 아래 잔잔한 바다와 수평선 위에 솟은 작은 바위섬",
        2: "옅은 구름이 펼쳐진 하늘과 먼 수평선에 낮게 이어진 섬들",
        3: "방파제 끝 등대와 바다 위 작업 구조물에 세워진 여러 개의 긴 기둥",
        4: "파도가 밀려오는 바다 너머 낮은 해안 건축물과 흐린 하늘",
        5: "물결무늬가 새겨진 넓은 모래 지형 위에 산책하는 사람들",
        6: "구름이 층층이 펼쳐진 하늘 아래 바다의 바위섬과 작은 배",
        7: "푸른 바다 위를 지나는 작은 어선과 멀리 수평으로 이어진 양식 시설",
        8: "노을 진 바다 위 어선들과 전경에 지는 해",
        9: "구름 사이 햇빛이 반사되는 바다와 정박한 여러 척의 작은 배",
        10: "거친 파도가 부딪히는 검은 바위들과 멀리 보이는 등대",
        11: "해안의 검은 바위 사이로 하얗게 부서지는 파도를 내려다 본 풍경",
        12: "잔잔하게 흐려진 바닷물 가운데 작은 바위 하나를 둘러싼 흰 파도",
        13: "젖은 모래 위로 길게 뻗은 물길과 먼 해안선을 담은 흑백 풍경",
        14: "짙고 옅은 푸른 물결이 촘촘하게 반복되는 바다 표면",
        15: "붉은빛에서 푸른빛으로 이어지는 수면과 잔잔한 물결의 반사",
        16: "다채로운 색의 선체와 밧줄이 비치는 초록빛 수면",
        17: "붉은 햇빛이 반사된 바다 위를 지나는 작은 배와 긴 물길",
        18: "넓은 바다와 흐린 하늘을 배경으로 해안에 서 있는 오래된 돌 등대",
        19: "갯벌의 풀, 수많은 새 무리와 얕은 물길, 먼 바다의 작은 배가 층을 이루는 흑백 풍경",
    },
    "traces-of-prayer": {
        1: "산을 배경으로 부처상과 사자상이 받치고 있는 석탑",
        2: "오래된 나무 아래 돌을 쌓아 만든 수많은 작은 돌탑",
        3: "바다를 마주한 해안에 빽빽하게 쌓인 돌탑들과 수평선 위의 배",
        4: "어두운 밤 조명을 받아 빛나는 석탑과 뒤편의 사찰 건물",
        5: "기와 위에 놓인 작은 부처상들과 앞쪽의 우물",
        6: "사찰의 기도 공간에 놓인 봉안물과 기도문이 적힌 기와",
        7: "사찰 마당을 가득 메운 연등",
        8: "대나무 숲길 끝에 하트 모양의 구조물과 각종 기도문이 겹겹히 놓인 풍경",
        9: "사찰 법당 안에서 참배하거나 기도하는 사람들의 모습",
        10: "어두운 바위굴 속 촛불 여러 개와 바위틈으로 들어오는 빛",
        11: "조각 장식이 있는 목조 공간 아래 방석에 놓인 목탁",
        12: "작은 기도 공간의 긴 선반 위에 놓인 촛불과 여러 물건",
        13: "돌과 작은 불상, 석등이 모여 있는 야외 풍경",
        14: "커다란 범종 아래 바닥에 놓여 있는 동전들",
        15: "바위에 새겨진 앉은 불상과 그 앞에 놓인 지폐",
        16: "어두운 큰 나무 앞 동전이 가득 놓인 큰 돌 위의 작은 불상",
        17: "바위를 배경으로 앉아 있는 보살상과 주변의 봉헌물",
        18: "두 개의 벽등 사이 빈 벽과 작은 제단이 있는 기도 공간",
    },
    "silence-temple": {
        1: "나무 그림자가 길게 드리운 숲속 산책로를 담은 흑백 풍경",
        2: "울창한 숲과 돌계단 너머 작은 산사 건물이 보이는 흑백 풍경",
        3: "숲속 나무 사이로 푸른 기와지붕이 부분적으로 드러나는 풍경",
        4: "짙은 녹음과 바위 사이에서 스님이 걸어가는 숲속 풍경",
        5: "낙엽이 진 나무들 사이로 기와지붕을 얹은 산사 건물들이 보이는 풍경",
        6: "화려한 단청 아래 계단을 올라가는 승려",
        7: "사찰의 기와 담장 옆 돌길을 걸으며 몸을 숙인 승려와 고양이",
        8: "숲속 산사 건물 옆 좁은 계단길과 멀리 보이는 작은 석조물",
        9: "나무와 돌계단 너머 햇빛이 비치는 산사 법당의 입구",
        10: "오래된 나무의 굽은 가지와 전통 기와지붕 처마가 겹쳐 보이는 풍경",
        11: "햇빛을 받은 작은 석등과 바위벽에 드리운 나뭇가지 그림자",
        12: "굵은 밧줄에 매달린 나무 범종 타종용 당목과 바닥의 짙은 그림자",
        13: "나무 기둥과 열린 문 사이를 지나가는 승려의 어두운 실루엣",
        14: "전통 목조 누각의 어두운 내부와 중앙 계단 너머 밝은 마당",
        15: "어두운 법당 내부 끝의 밝은 문과 바닥에 비친 가느다란 빛",
        16: "단청을 입힌 전통 누각의 처마와 그 아래 매달린 연등들",
    },
    "gaya-tumuli": {
        1: "마을과 논밭 사이에 길게 펼쳐진 가야고분군을 높은 곳에서 내려다본 풍경",
        2: "현대 도시의 건물들을 배경으로 여러 봉분이 능선처럼 이어진 가야고분군",
        3: "해 질 무렵 황금빛 햇살을 받은 둥근 고분들과 뒤편의 마을",
        4: "가을빛 풀밭 위를 산책하는 사람들과 멀리 보이는 고층 아파트",
        5: "햇빛을 받은 고분 사이의 산책로를 따라 걷는 여러 사람들",
        6: "커다란 고분을 배경으로 우산을 쓴 사람과 산책하는 방문객들",
        7: "푸른 풀로 덮인 고분과 능선을 따라 흩어져 자라는 여러 나무",
        8: "초록빛 봉분들이 이어진 고분군 사이의 구불구불한 산책로",
        9: "안개 낀 아침 햇빛 속에 겹겹이 드러나는 고분과 나무들의 실루엣",
        10: "산등성이를 넘어 들어오는 아침 햇빛과 안개 아래 둥근 고분들",
        11: "옅은 안개와 아침 빛 속에서 여러 겹의 능선처럼 펼쳐진 고분군",
        12: "해 질 무렵 둥근 고분 위에 서 있는 소나무와 멀리 보이는 마을",
    },
    "royal-tombs": {
        1: "도시 건물과 겹겹이 이어지는 먼 산을 배경으로 전경에 자리한 둥근 고분의 흑백 풍경",
        2: "작은 나무와 둥근 봉분 위로 구름이 길게 펼쳐진 하늘",
        3: "두 그루의 소나무 뒤로 솟은 커다란 봉분과 낮게 이어진 능선",
        4: "크기가 다른 여러 봉분이 겹쳐진 고분군과 뒤편의 나무들",
        5: "전경의 커다란 봉분과 뒤쪽의 작은 봉분들이 부드러운 곡선으로 겹치는 흑백 풍경",
        6: "구름 위로 드러난 햇빛이 봉분의 능선을 비추고 그 뒤로 작은 봉분들이 이어진 풍경",
        7: "커다란 봉분 아래 잔디를 깍고 있는 사람들과 나무 한 그루",
        8: "어두운 봉분의 경사면 위로 까치 두마리가 실루엣처럼 보이는 흑백 풍경",
        9: "전경의 어두운 봉분들과 먼 산, 오른쪽 소나무가 거친 흑백 입자로 표현된 풍경",
        10: "둥근 봉분 위에 선 나무와 주변 숲이 거친 흑백 입자로 표현된 풍경",
        11: "여러 그루의 나무 사이로 둥근 봉분이 부분적으로 드러나는 거친 입자의 흑백 풍경",
        12: "화면 중앙의 굵은 나무줄기 뒤로 둥근 봉분이 이어지는 거친 입자의 흑백 사진",
        13: "고분으로 걸어 올라 가는 사람과 뒤편의 봉분들이 어두운 곡선으로 겹쳐지는 거친 입자의 흑백 풍경",
        14: "크기가 다른 여러 봉분의 윤곽이 거친 흑백 입자 속에서 겹쳐지는 풍경",
        15: "화면 중앙에 솟은 커다란 봉분과 흐릿한 먼 산을 거친 입자로 표현한 흑백 사진",
        16: "여러 봉분 사이로 높게 솟은 중앙 봉분과 하늘의 작은 구름을 거친 입자로 표현한 풍경",
        17: "석축과 그림자, 그 뒤편의 봉분을 세로 구도로 담은 거친 입자의 흑백 사진",
        18: "낮게 이어지는 여러 봉분과 전경의 작은 석조물이 있는 거친 입자의 흑백 풍경",
    },
    "seowon-hyanggyo": {
        1: "위쪽의 기와지붕 아래 목조 누각과 아래쪽의 꽃 핀 나무 옆 전통 누각을 나란히 배치한 사진",
        2: "위쪽의 문틀 너머 꽃 핀 나무와 아래쪽의 담장 위로 뻗은 소나무를 담은 딥틱",
        3: "위쪽의 나뭇가지 사이 전통 건물과 아래쪽의 구름 낀 하늘 아래 서원 건물을 담은 딥틱",
        4: "위쪽의 나무와 기와집, 아래쪽의 낙엽 쌓인 언덕과 나무들을 함께 보여주는 사진",
        5: "위쪽의 단청이 있는 전통 건물과 아래쪽의 담장 너머 큰 나무를 담은 딥틱",
        6: "위쪽의 담장 아래 석조 구조물과 아래쪽의 나무 그림자가 드리운 돌담을 담은 흑백 딥틱",
        7: "돌을 쌓아 만든 긴 담장이 경사를 따라 이어지고 뒤편으로 전통 건물이 보이는 흑백 풍경",
        8: "전통 목조 건물들 사이 빈 마당에 석조 기둥 하나가 서 있는 흑백 풍경",
        9: "커다란 나무 밑동 옆 펼쳐진 천 위에 나무 조각과 여러 물건이 놓인 흑백 사진",
        10: "오래된 목조 건물 앞 돌계단과 비탈길을 따라 이동하는 전통 의복 차림의 사람들",
        11: "전통 의례 공간에서 관복을 입은 사람들이 여러 제기와 의례용 물품을 준비하는 흑백 사진",
        12: "위쪽의 제기에 물품을 담는 손과 아래쪽의 땅에 놓인 석조 시설 및 사람의 다리를 담은 흑백 딥틱",
    },
}

def plate(f, i, s):
    with Image.open(f) as im: w,h=im.size
    rel=f.relative_to(ROOT).as_posix()
    orientation='portrait' if h>w*1.14 else 'landscape'
    extra_class = SERIES_PLATE_CLASSES.get(s['slug'], {}).get(i)
    if extra_class:
        orientation += ' ' + extra_class
    alt_text = ALT_DESCRIPTIONS.get(s["slug"], {}).get(i, f"{s['ko']} — {SERIES_ALT_CONTEXT[s['slug']]}, 작품 {i:02d}")
    # No fabricated place/year: a quiet plate number serves as a sequence marker.
    return f'''<figure class="plate {orientation}"><img src="../{rel}" width="{w}" height="{h}" alt="{escape(alt_text, quote=True)}" loading="lazy" decoding="async"><figcaption><span>{i:02d} / {len(files_for(s)):02d}</span></figcaption></figure>'''

def series_schema(s, images):
    canonical = "https://www.atruetravel.com/works/" + s["slug"] + ".html"
    return {
        "@context": "https://schema.org",
        "@type": "ImageGallery",
        "@id": canonical + "#gallery",
        "url": canonical,
        "name": s["ko"] + " / " + s["en"],
        "description": SERIES_SEO_META["works/" + s["slug"] + ".html"][1],
        "inLanguage": "ko",
        "author": {"@type": "Person", "name": "서석장", "alternateName": "Seo Seok-Jang", "url": "https://www.atruetravel.com/"},
        "hasPart": [
            {
                "@type": "ImageObject",
                "contentUrl": "https://www.atruetravel.com/" + f.relative_to(ROOT).as_posix(),
                "description": ALT_DESCRIPTIONS.get(s["slug"], {}).get(i, f"{s['ko']} — {SERIES_ALT_CONTEXT[s['slug']]}, 작품 {i:02d}"),
                "creator": {"@type": "Person", "name": "서석장"},
                "creditText": "Seo Seok-Jang",
                "copyrightNotice": "© 2026 Seo Seok-Jang. All rights reserved.",
                "license": LICENSE_URL,
                "acquireLicensePage": ACQUIRE_LICENSE_URL,
            }
            for i, f in enumerate(images, 1)
        ],
    }

def gallery(s, next_s, output_root):
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
    (output_root/'works'/f"{s['slug']}.html").write_text(page(s['ko']+' / '+s['en'],content,1,'Works',s['ko']+' · '+s['en'],extra_head=SERIES_HEAD.get(s['slug'], '') + '<script type="application/ld+json">' + json.dumps(series_schema(s, a), ensure_ascii=False) + '</script>',canonical_path="works/"+s['slug']+".html"),encoding='utf-8')

def work_row(s):
    a=files_for(s);cover=s['cover']
    cover_style = ' style="height:auto;object-fit:contain"' if s['slug'] == 'unjusa-infrared' else ''
    return f'''<article class="work-row"><a class="work-image" href="works/{s['slug']}.html"><img src="assets/images/{cover}" alt="{escape(s['ko'])} 대표 작품" loading="lazy"{cover_style}></a><div class="work-copy"><span class="eyebrow">{escape(s['category'])} / {len(a):02d}</span><h3><a href="works/{s['slug']}.html">{escape(s['ko'])}</a></h3><p lang="en">{escape(s['en'])}</p><a class="view-link" href="works/{s['slug']}.html">작품 보기 <span aria-hidden="true">↗</span></a></div></article>'''

def generate(output_root):
    (output_root/'works').mkdir(exist_ok=True)
    for i,s in enumerate(SERIES): gallery(s,SERIES[(i+1)%len(SERIES)],output_root)
    home='''<section class="home-hero"><div class="home-copy"><span class="eyebrow">Photography by Seo Seok-Jang</span><h1>고요와 시간,<br>기억과 인간의 흔적</h1><p class="home-subtitle" lang="en">Silence, Time, Memory, and Human Traces</p><div class="home-manifesto"><p>진정한 여행은 가장 먼 곳이 아니라,<br>가장 오래 머문 자리에서 시작된다.</p><p lang="en">A true travel begins not in the farthest place,<br>but in the place where one has stayed the longest.</p></div><a class="view-link" href="works.html">작업 보기 <span aria-hidden="true">↗</span></a></div><figure class="home-image"><img src="assets/images/sea-in-me/sea-in-me-11.jpg" alt="파도가 바위에 스며드는 흑백 바다 풍경" width="2400" loading="eager"><figcaption>내 안의 바다 / The Sea in Me</figcaption></figure></section><section class="home-intro"><div class="home-intro-copy"><p>바다, 산사와 기도의 흔적, 고분 ...<br>한 장소에 머물며, 그곳에 남은 시간을 바라봅니다.</p><p class="home-intro-en" lang="en">The sea, mountain temples and traces of prayer, burial mounds ...<br>I stay with each place and look at the time it holds.</p></div><a href="works.html">Selected works <span aria-hidden="true">↗</span></a></section>'''
    (output_root/'index.html').write_text(page('서석장 사진 아카이브',home,description='사진작가 서석장의 작품 아카이브. 바다, 산사, 기도의 흔적, 한국의 문화유산.'),encoding='utf-8')
    works='''<div class="page-heading"><span class="eyebrow">Archive</span><h1>Works</h1><p>고요와 시간, 기억과 인간의 흔적을 바라보는 사진 프로젝트.</p></div><section class="works-list" aria-label="사진 프로젝트">'''+''.join(work_row(s) for s in SERIES if s['category'] == 'Works')+'''<div class="works-divider"><span>한국의 문화유산</span><span lang="en">Korean Cultural Heritage</span></div>'''+''.join(work_row(s) for s in SERIES if s['category'] == 'Korean Cultural Heritage')+'</section>'
    (output_root/'works.html').write_text(page('Works',works,current='Works',description='서석장의 사진 프로젝트 7개와 작품 101점.'),encoding='utf-8')
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
        (output_root/f'{name}.html').write_text(page(title,content,current=title),encoding='utf-8')
    contact='''<div class="text-page contact-page"><span class="eyebrow">Inquiries</span><h1 class="page-title">Contact</h1><p>전시, 소장, 출판 및 프로젝트 협업 문의는 이메일로 연락해 주세요.</p><p lang="en">For exhibition, collection, publishing, and project inquiries, please write by email.</p><a class="contact-email" href="mailto:sj.seo57@gmail.com">sj.seo57@gmail.com</a><p class="contact-note">서석장 · Seo Seok-Jang</p></div>'''
    (output_root/'contact.html').write_text(page('Contact',contact,current='Contact',description='서석장 사진작가 전시 및 출판 문의'),encoding='utf-8')

    copyright_body = '<div class="text-page"><span class="eyebrow">Copyright &amp; Usage Terms</span><h1 class="page-title">저작권 및 이용조건</h1><p>이 웹사이트에 게시된 모든 사진 작품의 저작권은 사진가 서석장(Seo Seok-Jang)에게 있습니다. 아래 조건은 모든 연작의 사진에 공통으로 적용됩니다.</p><p>© 2026 Seo Seok-Jang. All rights reserved.</p><h2>사진 이용조건</h2><p>사진의 무단 복제, 저장 후 재게시, 배포, 출판, 전시, 편집·변형 및 상업적 이용을 금지합니다. 출처나 작가명을 표시하는 것만으로 이용 허락을 대신할 수 없습니다.</p><p>사진을 이용하려면 이용 전에 작가의 명시적인 허락을 받아야 합니다. 이용 범위와 조건은 개별 문의를 통해 협의하며, 이 페이지는 사진의 자유 이용이나 자동 이용 허락을 부여하지 않습니다.</p><h2>사전 허락 및 이용 문의</h2><p><a href="contact.html">Contact 페이지</a>의 이메일로 작품명 또는 사진 URL, 이용 목적, 매체, 기간 및 상업적 이용 여부를 알려주세요. 허락받은 범위와 조건에 따라 이용해 주세요.</p><div lang="en"><h2>Copyright and usage terms</h2><p>All photographic works on this website are copyrighted by Seo Seok-Jang. These terms apply to photographs across all series.</p><p>Unauthorized copying, reposting, distribution, publication, exhibition, editing, modification, and commercial use are prohibited. Crediting the photographer does not replace permission.</p><p>Obtain the photographer\'s explicit permission before using a photograph. Usage scope and terms are agreed upon individually; this page does not grant an open license or automatic permission.</p><p>For prior permission, visit the <a href="contact.html">Contact page</a> and email the work title or image URL, intended use, medium, duration, and whether the use is commercial.</p></div></div>'
    (output_root/COPYRIGHT_PATH).write_text(page("저작권 및 이용조건", copyright_body, description="서석장 사진 작품의 공통 저작권 및 이용조건. 무단 사용 금지와 사전 허락 문의 안내.", canonical_path=COPYRIGHT_PATH), encoding="utf-8")


class RecoveryError(RuntimeError):
    """Keep the temporary backup when publication cannot be fully restored."""


def publish(staged_root, backup_root):
    expected = [Path('works') / f"{s['slug']}.html" for s in SERIES]
    expected += [Path(f'{name}.html') for name in
                 ('index', 'works', 'about', 'exhibitions', 'contact')]
    expected.append(Path(COPYRIGHT_PATH))
    actual = {p.relative_to(staged_root) for p in staged_root.rglob('*.html')}
    if actual != set(expected):
        raise RuntimeError('Generated HTML file set does not match the expected pages')

    changed = []
    for rel in expected:
        target = ROOT / rel
        existed = target.exists()
        if existed and target.read_bytes() == (staged_root / rel).read_bytes():
            continue
        changed.append((rel, existed))
        if existed:
            backup = backup_root / rel
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, backup)

    replaced = []
    try:
        for rel, existed in changed:
            (ROOT / rel).parent.mkdir(parents=True, exist_ok=True)
            os.replace(staged_root / rel, ROOT / rel)
            replaced.append((rel, existed))
    except BaseException as error:
        failures = []
        for rel, existed in reversed(replaced):
            try:
                if existed:
                    # Preserve the original backup even if restoration fails.
                    restore = staged_root / rel
                    shutil.copy2(backup_root / rel, restore)
                    os.replace(restore, ROOT / rel)
                else:
                    (ROOT / rel).unlink()
            except BaseException as recovery_error:
                failures.append(f'{rel}: {recovery_error}')
        if failures:
            raise RecoveryError(
                f'Publication failed: {error}; restoration failed: '
                + '; '.join(failures)
                + f'; backups preserved at {backup_root}'
            ) from error
        raise


def main():
    temporary = Path(tempfile.mkdtemp(prefix='.build-tmp-', dir=ROOT))
    keep_backup = False
    try:
        staged_root = temporary / 'generated'
        staged_root.mkdir()
        generate(staged_root)
        publish(staged_root, temporary / 'backup')
    except RecoveryError:
        keep_backup = True
        raise
    finally:
        if not keep_backup:
            shutil.rmtree(temporary)

if __name__=='__main__': main()

