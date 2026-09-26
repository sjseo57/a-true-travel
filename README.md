# A True Travel

서석장 작가의 사진 아카이브. Google Sites에서 벗어나 순수 HTML/CSS로 다시 제작한 미니멀 사이트 초안입니다.

## 폴더 구조

```
/
├── index.html                 홈
├── about.html                 작가 소개 (국/영문 병기)
├── works.html                 작업 목록
├── works/
│   └── sea-in-me.html          '내 안의 바다' 시리즈 상세 (샘플 — 나머지 3개 시리즈는 이 파일을 복제해서 만들면 됩니다)
├── exhibitions.html            전시경력 (연도 기준 타임라인, 국/영문 한 항목에 병기)
├── contact.html                연락처
├── assets/
│   └── css/style.css           디자인 시스템 (색상·타이포·레이아웃 전부 여기서 관리)
└── CNAME                       커스텀 도메인(www.atruetravel.com) 연결용
```

## 아직 해야 할 일

1. **이미지 교체**: 현재 `works.html`과 `works/sea-in-me.html`의 이미지는 기존 Google Sites에 올라가 있던 사진 URL을 임시로 가져다 쓴 것입니다(미리보기 용도). 실제 사진 파일을 `assets/images/` 아래에 직접 올려서 `<img src>`를 로컬 경로로 바꿔주세요. 외부(Google 서버) 링크에 계속 의존하면 나중에 그쪽 링크가 끊길 때 사이트 이미지가 전부 깨집니다.
2. **나머지 시리즈 페이지 제작**: `기도의 흔적들`, `산사의 고요함`, `한국의 문화유산`(하위 3개 포함) 페이지를 `works/sea-in-me.html`을 복제해서 만들어주세요. 구조(제목 → 스테이트먼트 → 이미지 시퀀스 → 영문)는 동일하게 유지하면 됩니다.
3. **캡션 채우기**: 각 사진의 `<figcaption>`에 임시로 "연도 미상"이라고 넣어뒀습니다. 실제 촬영 장소·연도로 교체해주세요.
4. **컷 선별**: 지금 샘플은 9컷으로 줄여서 리듬을 만들었습니다. 실제 게재 시에도 시리즈당 8~12컷 내외로 선별하는 것을 권장합니다.

## GitHub Pages로 배포하는 방법

1. 이 폴더의 내용을 저장소(`sjseo57/a-true-travel`) 루트에 그대로 커밋 & 푸시합니다.
   ```
   git add .
   git commit -m "Initial minimal site"
   git push origin main
   ```
2. GitHub 저장소 페이지 → **Settings → Pages**로 이동합니다.
3. **Source**를 `Deploy from a branch`로, 브랜치는 `main` / `/(root)`로 설정합니다.
4. **Custom domain** 칸에 `www.atruetravel.com`을 입력하고 저장합니다. (저장소에 이미 포함된 `CNAME` 파일과 값이 일치해야 합니다.)
5. 도메인을 구매한 곳(가비아, 후이즈 등)에서 DNS 설정을 GitHub Pages 안내에 맞게 변경합니다.
   - `www` 서브도메인 → `CNAME` 레코드로 `sjseo57.github.io`를 가리키게 설정
   - 기존에 Google Sites로 연결되어 있던 DNS 레코드가 있다면 삭제하거나 교체해야 합니다.
6. 몇 분~몇 시간 후 `https://www.atruetravel.com`으로 접속하면 새 사이트가 표시됩니다. GitHub Pages 설정에서 **Enforce HTTPS**를 함께 체크해두세요.

## 로컬에서 미리 보기

별도 빌드 도구가 필요 없는 순수 정적 사이트입니다. 다만 `/assets/...`처럼 루트 기준 절대경로를 쓰고 있어서, 파일을 더블클릭해서 여는 것보다 아래처럼 로컬 서버를 띄워서 확인하는 것을 권장합니다.

```
cd a-true-travel
python3 -m http.server 8000
```

그 다음 브라우저에서 `http://localhost:8000` 접속.
