# browser
- &lt;밑바닥부터 시작하는 웹 브라우저> 실습
- 목표 : 웹과 웹 브라우저의 원리 이해

# 실습 후 정리
## 1일차: HTTP Socket 통신
- 입력받은 URL값으로 스킴, 호스트, 경로 확인 
- 해당 정보로 socket 연결, 요청, 응답 받기 
- 응답 값 중 헤더, 바디 확인
- HTML 바디 값 중 태그를 제외한 모든 텍스트 출력

## 2일차: HTTPS Socket 통신
- HTTP vs HTTPS
  - HTTP는 HTTP over TLS 즉 HTTP에 TLS 레이어를 추가하였음을 의미함
  - 브라우저와 호스트 간의 모든 통신이 암호화 되는 점이 HTTP와의 차이임
  - SSL 라이브러리가 암호화 세부 사항을 구현해줌 (암호화 알고리즘, 공통 암호화 키, 올바른 호스트 연결되었음 확인)
- 기본 포트 443

## 3일차: 웹페이지 다운로드 연습문제
- [1-1] HTTP/1.1 지원
  - 헤더 리팩터링
  - 헤더에 Connection: close 포함하여 연결 종료 처리
- [1-2] 파일 URL 지원
  - 파일 형식의 url일 경우 파일 읽기
  - 예 : file:///C:/workspace-study/browser/README.md
  - url 없이 실행시 기본 로컬 파일 읽기
- [1-3] data: 스킴
  - data 스킴 처리
  - 예: "data:text/html,..." 형식의 url일 경우 