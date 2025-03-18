# 👋 안녕하세요! 백엔드 개발자 조수민입니다.

사용자와 개발자의 문제를 빠르게 인지하고  
기술적 해결책을 안정적이고 효율적으로 설계하는  
**Problem Solver 백엔드 개발자**입니다.

안정성과 효율성을 고려한 백엔드 개발과  
꾸준한 성능 개선, 안정적인 배포를 목표로 성장하고 있습니다.

---

## 🚀 About Me
| 구분    | 내용 |
|---------|------|
| 이름     | 조수민 |
| 포지션   | 백엔드 엔지니어 |
| 이메일   | chosm0129@naver.com |
| GitHub  | [github.com/soominn](https://github.com/soominn) |
| 블로그   | [som-ethi-ng.tistory.com](https://som-ethi-ng.tistory.com) |

---

## 💻 Tech Stack
| 분야        | 기술 |
|-------------|------|
| Language    | Java, Python |
| Framework   | Spring Framework, Spring Boot, Django |
| Database    | MySQL, MariaDB, Oracle |
| DevOps      | AWS Lightsail, Route 53 |
| API         | RESTful API |
| Tools       | Git, GitHub, Postman |
| ETC         | Linux, Nginx, Apache, Let's Encrypt (HTTPS 적용) |

---

# 📂 주요 프로젝트

---

## ✅ 무한맨틀 (Muhanmantle) - 단어 유사도 기반 단어 맞추기 게임
**2025.01 ~ 진행 중**  
Django, MariaDB, FastText, AWS Lightsail, Route 53, Nginx, Let's Encrypt

### 📌 프로젝트 개요
한국어 단어 유사도를 기반으로 정답을 유추하는 싱글 플레이 게임입니다.  
FastText 임베딩 모델을 사용하여 단어 간 유사도를 계산하고, Django 기반 API 서버를 개발했습니다.

### ✅ 주요 기능
- FastText 유사도 계산 API 제공  
- 정답 단어 랜덤 출제 및 게임 반복 기능  
- 사용자의 입력 단어 기록을 LocalStorage에 저장  
- 프론트엔드(React)와의 RESTful API 연동

### ✅ 담당 역할
- FastText 모델 기반 유사도 계산 백엔드 구현  
- Django REST API 설계 및 MariaDB 데이터 관리  
- AWS Lightsail 배포, Route 53 도메인 연결  
- Nginx 설정 및 Let's Encrypt HTTPS 적용

### ✅ 트러블슈팅 & 개선
- FastText 모델 메모리 로딩 최적화 → 응답 속도 개선  
- CORS 오류 해결 (django-cors-headers 사용)  
- Nginx와 Django 간 HTTPS 설정 오류 해결

### ✅ 주요 성과
- 단어 유사도 기반 게임 서버 구축 및 서비스 배포  
- AWS Lightsail, Route 53을 통한 인프라 셋업 및 운영  
- HTTPS 적용을 통한 보안 강화 및 사용자 경험 개선

---

## ✅ 인천환경공단 환경정보 업무지원 시스템
**2024.04 ~ 2024.09**  
Spring Framework, MariaDB, MyBatis, JSP, HTML/CSS/JavaScript/jQuery, dhtmlx, Jenkins

### 📌 프로젝트 개요
환경 데이터를 수집 및 분석하여 업무 데이터를 통합 관리하는 시스템 개발.  
현재 내부 테스트 및 시스템 안정화 진행 중입니다.

### ✅ 주요 기능
- 환경 데이터 실시간 수집 및 정제 프로세스 구축  
- 통계 분석 및 리포트 API 제공  
- 데이터베이스 인덱스 최적화 및 파티셔닝  
- Jenkins를 통한 배포 자동화 환경 구축

### ✅ 담당 역할
- 백엔드 서버 개발 및 REST API 설계  
- 데이터베이스 모델링 및 성능 최적화  
- 배포 자동화 스크립트 및 운영환경 구축

---

## ✅ 사내 협업관리 시스템 개발
**2023.12 ~ 2024.02**  
Spring Framework, MariaDB, MyBatis, JSP, HTML/CSS/JavaScript/jQuery, dhtmlx, Jenkins

### 📌 프로젝트 개요
사내 업무 및 보고서 관리를 지원하는 협업관리 시스템 개발.  
계층형 데이터 관리를 통한 업무 트리 관리 및 보고 자동화를 구현했습니다.

### ✅ 주요 기능
- 업무 등록 및 일정 관리 기능  
- 일일/주간/월간 보고서 작성 및 제출  
- 계층형 데이터 트리 관리 (부모/자식 관계)  
- 보고서 자동 생성 및 권한 기반 접근 제어

### ✅ 담당 역할
- 백엔드 시스템 설계 및 데이터 계층 구조 구현  
- 계층형 데이터 조회 및 자동 집계 로직 구현  
- 보고서 기능 및 사용자 권한 관리 개발

---

## ✅ RI 생산정보 및 유통지원 시스템
**2022.09 ~ 2023.12**  
Spring Framework, MariaDB, MyBatis, JSP, HTML/CSS/JavaScript/jQuery, dhtmlx, Chart.js

### 📌 프로젝트 개요
국내 방사성동위원소 생산 및 유통 정보를 통합 관리하는 시스템 구축.

### ✅ 주요 기능
- 대용량 생산/유통 데이터 통합 관리  
- 엑셀 데이터 업로드 성능 최적화 (30분 → 5초 개선)  
- 관리자/사용자 페이지 권한 및 기능 분리  
- dhtmlx, Chart.js를 이용한 통계 시각화 제공

### ✅ 담당 역할
- 백엔드 서버 개발 및 데이터 처리 로직 개선  
- 엑셀 업로드 프로세스 백엔드 직접 처리 및 최적화  
- 관리자/사용자 권한 분리 및 페이지 설계  
- 통계 시각화 기능 개발 및 제공

---

## ✅ 하이하비 (HiHobby)
**2022.05 ~ 2022.06**  
Spring Framework, MyBatis, MySQL, JSP, HTML/CSS/JavaScript/jQuery

### 📌 프로젝트 개요
원데이 클래스 및 온라인 클래스 서비스 플랫폼 구축.  
사용자, 크리에이터, 관리자로 역할을 구분하여 서비스 제공.

### ✅ 주요 기능
- 회원가입/로그인/로그아웃 (사용자/크리에이터/관리자)  
- 클래스 검색, 결제, 수강 기능  
- 크리에이터 센터: 클래스 등록/수정/삭제  
- 관리자 센터: 클래스 승인 및 문의 관리

### ✅ 담당 역할
- 회원가입, 로그인/로그아웃 기능 개발  
- 마이페이지(내 쿠폰, 구매 클래스) 구현  
- 메인페이지 검색 및 인기 클래스 노출 기능 구현  
- Git, GitHub를 통한 버전 관리 및 협업

---

## ✅ 모여드림 (MoyeoDream)
**2022.06 ~ 2022.07**  
Spring Boot, MyBatis, Oracle, Thymeleaf, HTML/CSS/JavaScript/jQuery

### 📌 프로젝트 개요
취준생과 직장인을 위한 스터디 그룹 매칭 서비스 개발.

### ✅ 주요 기능
- 카카오 로그인 기반 회원가입/로그인(OAuth2)  
- 스터디 게시글 작성/수정/삭제 및 댓글 관리  
- 채용공고 신청 및 관리자 승인 기능  
- 관리자 센터에서 스터디/채용공고/문의 관리 기능 제공

### ✅ 담당 역할
- 카카오 로그인 API 연동 및 회원 관리  
- 스터디 CRUD 및 댓글 비동기 처리 구현  
- Thymeleaf 기반 UI 개발 및 비동기 통신 처리  
- Git, GitHub를 통한 프로젝트 관리 및 협업

---

# 📈 시스템 아키텍처
사용자 → 웹 서버 (Apache/Nginx) → 백엔드 (Spring/Django) → DB (MySQL/MariaDB/Oracle)

---

# ✅ 배포 및 운영
- AWS Lightsail을 통한 서비스 배포 및 도메인 관리(Route 53)  
- Let's Encrypt를 통한 HTTPS 인증서 적용  
- Jenkins를 활용한 CI/CD 배포 자동화 구축 경험

---

# ✨ 성장과 회고
- 시스템의 안정성과 확장성을 고려한 백엔드 설계를 지향  
- CI/CD 파이프라인 및 클라우드 환경 학습 및 구축 경험  
- 코드 리뷰, 기술 스터디 참여를 통해 지속적인 기술 성장 중입니다.

---

# 📊 GitHub Stats
![GitHub Stats](https://github-readme-stats.vercel.app/api?username=soominn&theme=darcula&hide_border=true&include_all_commits=true&count_private=false)
![Top Langs](https://github-readme-stats.vercel.app/api/top-langs/?username=soominn&theme=darcula&hide_border=true&include_all_commits=true&count_private=false&layout=compact)
