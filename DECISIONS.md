AI News Agent 도구를 만들면서 Claude와 협업한 Decision Log.
단순 결과물보다 사고 과정을 남기기 위해 기록함. AI 협업의 진짜 모습은 결과물 자체가 아니라 어떤 결정을 내리고 어떤 제안을 거절했는지에 드러난다고 생각함.
각 결정에서 Claude's role 줄을 주목하면 협업 방식이 보임.

Decision #1: Core Identity

Context: 에이전트의 메인 정체성을 정하는 단계. 프로덕트 빌딩을 하다가 다른 길로 세지 않기 위해 정체성을 단단하게 잡아주는 것이 중요함.
Options Considered: 
1. Today's AI news, read through four minds
2. Four perspectives on today's AI news. You decide what matters
3. AI news, seen from four angles - every morning.
Decision: Four perspectives on today's AI news. You decide what matters.
Reasoning: 원래 의도했던대로 뉴스를 각각 다른 관점에서 해석할 수 있으면서도, 사용자가 수동적으로 정보만 학습하는 것이 아닌 본인에게 정작 중요한 정보를 판별할 수 있게끔 할 수 있어서.
Claude's role: Claude가 처음에는 hype 비판 중심의 제목들을 제안했음. 그러나 내가 비판이 메인이 되어버리면 뉴스를 오히려 객관적으로 보지 못하고 비판 자체가 목적이 된다는 점이 우려된다고 거절함. 따라서, 비판보다는 다관점에서 해석하는 것에 초점을 두자고 제안함. 이에 따라 클로드에서 제안한 옵션 중 하나를 선택함.

Decision #2: Four Lenses

Context: 뉴스를 어떤 관점에서 해석할지 4가지의 Lense를 결정하는 단계.
Options Considered: 
1. 균형형
2. Builder 친화형
3. 시간축 기반
Decision: 균형형
Reasoning: 당장 나 자신도 Builder라고 생각하지 않고 오히려 AI를 더 잘 활용하고 싶은 일반 유저라고 생각하기 때문에 해당 프로덕트가 더 와닿기 위해서는 균형형이 더 적합하다고 생각.
Claude's role: Claude는 세트를 여러가지로 제안했고 처음에는 Builder 친화형을 제안했으나, 거절하고 균형형으로 진행하자고 제안. 그 와중에 Builder 세트에 포함했던 hype 거르기 요소를 그대로 유지하고 싶다고 명시.

Decision #3: News Sources

Context: News Source를 어디서 가져올지 결정하는 단계.
Options Considered: 
1. 전통 매체
2. 커뮤니티/소셜
3. 연구/공식 자료
Decision: 전통 매체 3-4개와 Hacker News AI 키워드를 조함한 구조
Reasoning: 일반 유저용 AI 뉴스라는 정체성에 맞게 좀 더 이해하기 쉽고 접근성이 좋은 소스별로 추려서 적합하다고 생각. 현실적으로 하루 안에 해당 에이전트를 구현하려면 이 구조가 적합하다고 Claude가 제안했고, 프로덕트를 만들 때 중요한 요소라고 생각하는 확장성과도 맞닿아 있어서 선택.
Claude's role: Claude가 먼저 이 3+1 구조를 제안했고, 나는 동의. 크게 반박할 부분이 없었음.

Decision #4: Agent Architecture

Context: 
4-1. 6가지 에이전트 중 각 Lens 에이전트들이 어떤 순서로 돌아갈지 선택하는 단계.
4-2. News Curation 기준을 선택하는 단계.
4-3. Lens의 출력을 하나의 브리핑으로 묶는 방식.

Options Considered: 
4-1. Execution
    1. 병렬
    2. 순차

4-2. Curation 기준
1. 인기 기반
2. 재현 가능성
3. 영향력 추정
4. 다양성 기반

4-3. 
1. Aritcle-by-Article
2. Lens-by-Lens
3. Daily Narrative

Decision: 
4-1. 병렬
4-2. b+d 하이브리드 구조
4-3. Article-by-Article

Reasoning: 
4-1. 중복을 피할 수는 있지만 한개의 Lens의 결론이 다른 Lens들의 결과에 많은 영향을 끼칠 수 있는 것을 방지하기 위해서 병렬로 진행하는 것을 결정.
4-2. 프로덕트의 정체성과 일치. PR도 거르지 않고 그대로 통과시킨 이유 - 도구가 무엇을 거를지 결정하는 권한이 커지면 'You decide' 정체성과 충돌하기 때문.
4-3. 4개의 에이전트가 협업한 결과를 가장 가시성 좋게 보여줄 수 있는 선택지라고 생각. 사용자 스스로 4가지의 관점을 보고 스스로 생각할 수 있게끔 유도할 수 있는 결과물이라고 생각. 그리고 확장성이 있음

Claude's role: 
Claude가 먼저 구조를 제안했고, 나는 동의. 크게 반박할 부분이 없었음. 다만 4-3. Article-by-Article이 추후에 확장성이 좋다고 판단하여 해당 선택지로 결정.

Decision #5: Tech Stack

Context: 에이전트를 구현할 때의 필요한 기술 스택을 결정하는 단계.
Options Considered: Python + Anthropic SDK + Streamlit
Decision: Claude 제안대로 작업하는 것을 동의.
Reasoning: 크게 반박할 부분이 없었고 특히 기술 스택 부분은 내가 잘 아는 부분이 아니어서 이 부분에 대한 의사결정을 클로드의 제안에 의지하는 것이 낫겠다고 생각함.
Claude's role: 프로덕트에 맞춰서 적절한 방안을 제시.

Decision #6: v1 Scope

Context: 에이전트를 구현할 때의 작업 범위를 결정하는 단계. (Phase 1 / Phase 2)
Options Considered: 
1. 6개 에이전트 다 구현 및 작동
2. TechCrunch + Verge + HN 정도만 구현
3. 5개 기사 다관점 해석
4. 간단한 Streamlit UI
5. 사용자 인증, DB, 즐겨찾기
6. 알림, 이메일 발송
7. 캐시/최적화
8. Lens-by-Lens 뷰
Decision: 1-4 + 이메일 발송 기능까지 합해서 구현. 기존 v1에서 이메일은 제외였으나, 작업 도중 추가 결정. 
Reasoning: 처음부터 내가 생각한 이 뉴스 에이전트 구조는 이메일 형식이었고, 내가 기대한대로 에이전트가 구현되려면 이메일 기능을 무조건 추가하는 게 맞다고 판단함.
Claude's role: 먼저 하루라는 일정에 맞춰서 적절한 작업 범위를 제안함. 6번까지 추가하고 싶다고 하니깐 일정 기반으로 현실적으로 구현 가능한 범위가 이메일까지만이라고 추천함. 나는 이 의사결정에 동의함.

회고:
Claude와 협업하면서 의외였던 점: 생각보다 내가 주도적으로 생각할 수 있도록 판단의 여지를 주고 옵션을 제시한다는 점. 무작정 내가 AI에 끌려가는 것이 아닌 같이 생각하면서 의사결정하는 과정을 경험할 수 있었음.
다음 단계로 넘어가면서 신경 쓰이는 부분: 코드 짜는 단계에서 내가 기술적 판단력과 배경 지식이 약해서 어떻게 비판적으로 잘 협업할 수 있을지 고민됨
Phase 1에서 본인이 발견한 자기 사고 패턴: 뭔가 딱 원하는거대로 결정하는 것보단 "일단 이렇게 하자"의 사고 패턴이 자주 보임. 따라서 이것도 할 수 있고 저것도 할 수 있으면 좋겠어서 이러지도 저러지도 못해서 확장성이라는 가치를 많이 중요하게 생각하는 것 같음. 이건 아마 결정을 잘 못해서 생긴 스스로의 가치인 것 같음. 다만 프로덕트를 만들 때 확장성 자체는 가치 있는 관점이라, 약점이 강점으로 작동하는 영역인 듯.

────────────────────────────────────

Phase 2: 구현 단계 (2026-05-05)

What We Built

하루 안에 설계에서 배포까지 완성한 6개 에이전트 파이프라인.

파이프라인 흐름:
News Fetcher → Curator Agent → [4 Lens Agents 병렬] → Synthesizer → Streamlit UI + Email Dispatcher
GitHub Actions cron이 매일 UTC 23:00 (한국 오전 8시)에 전체 파이프라인을 자동 실행.

최종 파일 구조:
- news_fetcher.py: RSS 4개 소스 + Hacker News Algolia API, 중복 제거 후 시간순 정렬
- agents/curator.py: Claude가 재현가능성+다양성 기준으로 5-7개 선별, 선택 이유를 JSON으로 반환
- agents/lenses.py: Market/Tech/Society/User 4개 Lens를 ThreadPoolExecutor로 병렬 실행
- agents/synthesizer.py: Lens 결과를 Article-by-Article 구조로 조립, JSON 파일로 저장
- app.py: Streamlit 웹 뷰어 (오늘의 결과물 읽기 전용)
- email_dispatcher.py: Resend API로 HTML 이메일 발송
- .github/workflows/daily_briefing.yml: GitHub Actions cron 스케줄러

────────────────────────────────────

구현 단계 의사결정 사항

Code Decision #1: Curator 출력 형식

Options Considered:
A. "5-7개 골라라"만 지시 → 단순하지만 선택 기준 불투명
B. 명시적 기준(재현가능성+다양성)을 프롬프트에 박고, 선택 이유를 JSON으로 받아오기

Decision: B
Reasoning: Curator가 왜 이 기사를 골랐는지 투명하게 남겨야 "이 Curator가 Phase 1 기준대로 작동해?" 검증이 가능함. "You decide" 정체성은 사용자뿐 아니라 빌더도 도구를 검증할 수 있어야 한다는 의미이기도 함.
Claude's role: Claude가 먼저 두 옵션을 제시하고 B를 추천. 이유를 듣고 동의.

Code Decision #2: Lens 병렬 실행 방식

Options Considered:
A. asyncio + 비동기 Anthropic client → 진짜 동시 실행이지만 코드 복잡도 높음
B. ThreadPoolExecutor + 동기 client → 충분히 병렬, 코드 단순

Decision: B
Reasoning: v1 스코프에서 4개 API 호출이라 asyncio 오버헤드를 가져올 이유가 없음. 단순한 코드가 나중에 디버깅하기도 쉬움.
Claude's role: Claude가 먼저 두 옵션과 트레이드오프를 설명하고 B를 추천. 동의.

Code Decision #3: Synthesizer 구현 방식

Options Considered:
A. Claude API를 한 번 더 호출해서 최종 편집
B. 순수 Python 조립 로직 (추가 API 호출 없음)

Decision: B
Reasoning: 4개 Lens가 이미 완성된 분석을 썼기 때문에 Synthesizer가 할 일은 "기사별로 묶기"뿐. Claude를 한 번 더 호출하면 비용이 늘고, "You decide" 정체성에 끼어드는 편집 레이어가 하나 더 생김.
Claude's role: Claude가 먼저 이 결정을 짚고 B를 선택. 이유가 정체성과 연결되어 있어서 동의.

Code Decision #4: 이메일 발신 주소 기본값

Context: Resend 무료 티어는 자체 도메인 없이 테스트할 때 onboarding@resend.dev를 발신 주소로 사용 가능. .env에 EMAIL_FROM이 비어있을 때의 처리 필요.
Decision: EMAIL_FROM이 비어있으면 onboarding@resend.dev로 자동 fallback.
Reasoning: 도메인 설정 없이 바로 테스트 가능해야 하루 안에 완성 가능. 추후 커스텀 도메인 연결 시 .env만 수정하면 됨.

────────────────────────────────────

오늘 작업 결과 요약

완성된 것:
- 6개 에이전트 전체 작동 확인
- 실제 오늘 날짜 기사 5-7개 다관점 브리핑 생성
- Streamlit 로컬 웹 뷰어 작동 확인
- 이메일 실제 수신 확인 (ktaeyeonn09@gmail.com)
- GitHub Actions cron 설정 완료 (매일 한국 오전 8시 자동 실행)
- DECISIONS.md에 전 과정 기록

의도적으로 남긴 것 (v2):
- Streamlit Community Cloud 배포 (공개 URL)
- 커스텀 도메인 이메일 발신 주소
- 캐싱 및 API 비용 최적화
- Lens-by-Lens 뷰
- 사용자 인증, DB, 즐겨찾기

────────────────────────────────────

구현 단계 추가 결정 (2026-05-05, 작업 중)

Code Decision #5: Curator 기사 수 축소 (5-7 → 4개)

Context: 초기 설정은 5-7개였으나, 실제 결과물을 받아보고 나서 매일 다 읽히지 않는다고 판단.
Decision: 정확히 4개로 고정.
Reasoning: 선택과 집중이 더 가치 있다는 판단. 기사 수가 줄어든 만큼 재현가능성 기준을 높이고 (4개 슬롯이면 진짜 강한 신호만 통과), 다양성은 "최대 2개까지 같은 주제 허용, 4개 전부 같은 주제는 금지" 룰로 소프트하게 보장.
왜 카테고리 강제는 안 했나: Phase 1 Decision #4에서 이미 같은 이유로 거절한 결정. 카테고리를 강제하면 그날 중요하지 않은 기사를 억지로 끌고 와야 함 — "You decide" 정체성과 충돌.
Claude's role: 두 옵션(카테고리 강제 vs 주제 묶음 허용)의 트레이드오프를 설명하고 (2)를 추천. Phase 1 결정과의 일관성을 짚은 것이 결정 근거가 됨.

Code Decision #6: Lens 출력 형식 변경 (문단 → insight + bullets)

Context: 실제 이메일과 웹뷰어를 확인한 후 가독성 문제 발견. 매일 빠르게 스캔할 수 있는 형태가 필요하다고 판단.
Decision: 각 Lens를 "한 줄 insight (이탤릭) + 정확히 3개 bullet" 구조로 통일.
Reasoning: Insight는 결론을 강요하지 않고 "이 뉴스의 진짜 포인트"를 관찰로 제시 ("The real point here is..." 형태) — "You decide" 정체성 유지. Bullet 3개는 디테일·근거·맥락 순으로 스캔 가능하게.
데이터 구조 변경: 기존 analysis 문자열 → insight + bullets 분리. Streamlit과 이메일 렌더러가 각각 다르게 스타일 적용 가능해짐.
Claude's role: 사용자 요청 방향이 맞다고 확인하고, 프롬프트 변경과 함께 JSON 구조 변경도 필요하다고 먼저 짚음. 샘플 출력 먼저 보여주고 OK 받은 뒤 전체 적용.

────────────────────────────────────

Possible Next Steps (v2 후보)

즉시 할 수 있는 것:
1. Streamlit Community Cloud 배포 — GitHub 레포 연결하면 공개 URL 생성. 무료.
2. 커스텀 도메인 이메일 — Resend에서 도메인 연결 후 EMAIL_FROM 설정. 브랜드 완성도 올라감.

기능 확장:
3. Lens-by-Lens 뷰 — Streamlit에 탭 추가. "Market 관점에서만 오늘 뉴스 보기" 가능.
4. 기사 수 조정 — Curator 프롬프트에서 5-7개 → 원하는 수로 파라미터화.
5. 뉴스 소스 추가 — Reuters AI, Bloomberg Technology 등 Tier 1 확장.
6. 한국어 출력 옵션 — 프롬프트에 언어 파라미터 추가.

구조적 개선:
7. 프롬프트 캐싱 — Anthropic SDK의 prompt caching 기능으로 API 비용 절감.
8. 출력 히스토리 — 날짜별 브리핑 아카이브 뷰어 (Streamlit에서 날짜 선택).
9. 에러 핸들링 강화 — RSS 소스 장애 시 부분 실행 허용.

정체성 관련 고민거리:
10. Curator 투명성 공개 — 웹 뷰어에서 "왜 이 기사가 선택됐는지" 이유 표시 여부. 지금은 숨겨져 있음. "You decide" 정체성상 큐레이션 기준도 사용자에게 보여주는 게 맞을 수 있음.
