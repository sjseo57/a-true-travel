# A True Travel — 사진 아카이브

사진가 서석장의 정적 HTML 포트폴리오. 2026-09-27 Google Sites에서 GitHub Pages로 이전해 사용자 지정 도메인으로 게시했다.

- 공개 주소: https://www.atruetravel.com/
- 저장소: https://github.com/sjseo57/a-true-travel
- 배포: GitHub Pages, `main` 브랜치의 저장소 루트
- 도메인: 루트 `CNAME` 파일에 `www.atruetravel.com`; DNS와 HTTPS 설정은 저장소 Settings → Pages에서 확인
- 운영 기록: Notion의 [A True Travel 웹사이트](https://app.notion.com/p/3c958f788969810bb94ad263be8f5bf7)

## 현재 구성

Home, Works, About, Exhibitions, Contact와 Works 아래 6개 연작(총 95점). 사진은 `assets/images/`에 있으며 프로필 사진은 별도다.

| 연작 | 사진 폴더 | 점수 |
| --- | --- | ---: |
| 내 안의 바다 | `sea-in-me/` | 19 |
| 기도의 흔적들 | `traces-of-prayer/` | 18 |
| 산사의 고요함 | `silence-temple/` | 16 |
| 가야고분군 | `gaya-tumuli/` | 12 |
| 왕릉과 고분 | `royal-tombs/bw/`, `royal-tombs/grain/` | 18 |
| 한국의 서원과 향교 | `seowon-hyanggyo/` | 12 |

## 어디를 수정하나

- `build.py`: 연작의 제목, 작품 순서, 대표 사진, 국·영문 소개와 메뉴 생성. 실행하면 `index.html`, `works.html`, `works/*.html`, `about.html`, `exhibitions.html`, `contact.html`을 다시 쓴다.
- `content/about.html`, `content/exhibitions.html`: About·Exhibitions 본문의 입력 자료.
- `assets/css/style-v12.css`: 현재 페이지가 참조하는 스타일. `assets/js/navigation.js`: Works 펼침 메뉴.
- `assets/images/`: 웹용 사진. 원본·보정본은 별도 보존한다.
- 루트 `CNAME`: 사용자 지정 도메인. 파일 전체를 교체할 때도 유지한다.

**재생성 주의:** 2026-09-30 확인 시 `build.py`의 홈 소개 문구가 게시된 `index.html`과 다르다. 게시 페이지에 수동 반영된 다른 변경도 있을 수 있다. 따라서 `python3 build.py`를 실행하기 전에 현재 생성 파일과 생성 소스의 차이를 대조하고, 확정된 문구·배치를 소스에 이식한다. 실행 뒤에는 GitHub Desktop의 Changes에서 의도하지 않은 되돌림이 없는지 확인한다. Python 3과 Pillow가 필요하다.

## PC에서 수정하고 게시

1. GitHub Desktop에서 이 저장소를 선택해 `Fetch origin` 후 원격 변경이 있으면 `Pull origin` 한다. 다른 기기나 ChatGPT가 GitHub 파일을 직접 수정했다면 이 단계가 먼저다.
2. 저장소의 해당 파일만 수정한다. 사진 추가 시 웹용 JPEG와 작품 순서·대표 이미지·링크를 함께 확인한다. 전체 폴더를 삭제한 뒤 일부 수정 압축파일만 복사하지 않는다.
3. 로컬 미리보기: 저장소 루트에서 `python3 -m http.server 8000`을 실행하고 `http://localhost:8000`을 연다.
4. PC 100% 배율과 모바일에서 메뉴, 국·영문, 사진 순서, 깨진 사진, 상대경로, 여백을 확인한다. `assets/images` 파일이 `Deleted`로 표시되지 않는지 본다.
5. GitHub Desktop의 Changes에서 변경 파일을 검토하고 Summary에 작업 내용을 적어 `Commit to main` → `Push origin` 한다.
6. [Actions](https://github.com/sjseo57/a-true-travel/actions)에서 Pages 배포 결과를 본 뒤 공개 주소를 새로고침해 확인한다. 캐시가 의심되면 Edge InPrivate 창으로 확인한다.

## 도메인과 HTTPS

[Pages 설정](https://github.com/sjseo57/a-true-travel/settings/pages)의 Custom domain은 `www.atruetravel.com`. DNS 관리업체(Namecheap)의 `www` CNAME은 `sjseo57.github.io`를 가리켜야 한다. `https://`나 `/a-true-travel`을 붙이지 않는다. 루트 `atruetravel.com`을 함께 연결하려면 `@` A 레코드는 다음 GitHub Pages 주소 네 개다.

- `185.199.108.153`
- `185.199.109.153`
- `185.199.110.153`
- `185.199.111.153`

DNS 수정은 Namecheap에서 행 오른쪽 저장 버튼을 눌러야 확정된다. 저장 후 GitHub Pages의 DNS check 및 Enforce HTTPS를 확인한다. 인증서 활성화까지 시간이 걸릴 수 있다. 메일용 MX·TXT 레코드는 웹사이트 전환 때문에 수정하지 않는다. DNS 문제 발생 시 [GitHub 공식 안내](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)를 다시 확인한다.

## 향후 개편 원칙

사진 선정·배열과 원문을 먼저 확정한 뒤 코드에 반영한다. 새 연작은 상단 메뉴를 늘리기보다 Works 아래에 추가한다. 수정 범위와 제외·교체 사진을 기록하고, 원본 파일명과 웹 파일명 대응을 보존한다. 큰 개편은 별도 브랜치에서 검토한 뒤 반영한다. 현재 게시본의 기준은 저장소 `main`이며, 이 README와 Notion 기록은 운영 안내다.
