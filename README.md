# A True Travel — 사진 아카이브

사진작가 서석장의 정적 HTML 사이트. 빌드 서버나 프레임워크 없이 GitHub Pages에서 제공됩니다. 현재 `www.atruetravel.com`은 Google Sites에 연결되어 있으므로 검수 브랜치에는 `CNAME`을 넣지 않았습니다.

## 콘텐츠와 사진

- `content/about.html`, `content/exhibitions.html`: 기존 초안의 국·영문 작가 소개와 전시 이력 원문. 사실 관계와 표기는 공개 전 확인합니다.
- `build.py`: 여섯 시리즈의 현 사이트 작품 설명과 순서를 보관하고 HTML을 생성합니다. 사진을 추가·교체할 때 `python3 build.py`를 실행합니다. Python 3과 Pillow가 필요합니다. 공개되는 결과는 순수 HTML/CSS입니다.
- `assets/images/`: 제공된 Google Drive의 웹용 JPEG 95점과 프로필 사진 1개. **파일명을 바꾸지 않았습니다.** 시리즈 경로와 번호는 Drive와 같습니다. `보류` 폴더는 제외했습니다.
- `works/royal-tombs.html`: 흑백 `01–08`, 점묘 `09–18` 순서로 구성합니다.
- 사진의 촬영 장소·연도는 확인되지 않아 가공한 캡션을 만들지 않았습니다. 연속 번호만 표시합니다.

| 시리즈 | 저장 경로 | 장수 |
|---|---|---:|
| 내 안의 바다 | `assets/images/sea-in-me/` | 19 |
| 기도의 흔적들 | `assets/images/traces-of-prayer/` | 18 |
| 산사의 고요함 | `assets/images/silence-temple/` | 16 |
| 가야고분군 | `assets/images/gaya-tumuli/` | 12 |
| 왕릉과 고분 | `assets/images/royal-tombs/bw/`, `grain/` | 18 |
| 서원과 향교 | `assets/images/seowon-hyanggyo/` | 12 |

대표작 경로는 `build.py`의 `cover` 필드에서 지정합니다. 프로필 사진은 About 페이지에 사용했습니다. 새 작품의 순서·선별은 작가가 결정합니다.

## 미리보기와 출판

저장소 루트에서 `python3 -m http.server 8000`을 실행하고 `http://localhost:8000`을 엽니다. 프로젝트 기본 주소는 `https://sjseo57.github.io/a-true-travel/`입니다. 내부 링크는 상대 경로이므로 그 주소에서도 동작합니다.

**도메인 전환은 별도 작업입니다.** 모든 사진과 문안을 검수한 뒤 GitHub Pages에서 도메인 소유권을 확인하고 `www.atruetravel.com`을 설정합니다. 그때 루트에 `www.atruetravel.com`이 적힌 `CNAME`을 추가하고 DNS의 `www` 레코드를 `sjseo57.github.io`로 변경합니다. `atruetravel.com` 루트 도메인의 설정도 별도로 확인합니다. Google Sites는 전환 확인 전까지 유지합니다.

공개 전에 전시명·국영문 문안, 대표작, 작품 순서, 모바일 표시를 확인합니다. 기존 Google Sites의 작품 페이지 주소는 새 HTML 경로와 다르므로 기존 링크 공유 내역도 점검합니다. 초안의 미확인 이메일과 Instagram 링크는 공개 페이지에서 제외했습니다.

## GitHub Desktop으로 옮기기

1. [GitHub Desktop](https://desktop.github.com/)에서 `sjseo57/a-true-travel` 저장소를 복제합니다.
2. 이 압축파일을 풀고 **안쪽 `a-true-travel` 폴더의 내용**을 복제한 저장소 폴더에 복사합니다. 기존 파일은 교체하고, 기존 저장소에 남은 `CNAME`과 `contact.html`은 직접 삭제합니다. 압축파일 자체나 `.git` 폴더는 복사하지 않습니다.
3. GitHub Desktop에서 변경 파일과 삭제된 `CNAME`, `contact.html`을 확인한 뒤 `Commit to main` → `Push origin`을 실행합니다. 사진은 95점 모두 있어야 합니다.
4. 먼저 로컬에서 확인하거나 GitHub Pages의 임시 주소에서 검수합니다. 커스텀 도메인 설정은 사이트 검수 후 진행합니다.
