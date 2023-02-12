# FastAPI
문제 은행 웹 만들기

DB:postgresql - 테이블을 미리 만들어준 뒤 진행(db명:testdb, 테이블명:problems)

순서도:https://drive.google.com/file/d/1cSDo9bO715IK7e8TTqMJKSDYJSMsTWSl/view?usp=share_link


현재까지 만든 API

1.db 조회1:테이블 내에 모든 데이터 return

2.db 조회2:테이블 내의 한 문제 데이터 return

3.db post:request body로 받은 데이터 db에 넣기

4.db delete:특정 아이디 값의 문제 삭제

5.db put:특정 아이디 값의 문제 수정


처리한 에러케이스

1.db와 연결 오류 - 미리 저장되었던 이미지 파일도 삭제

2.db에 저장된 경로에 사진이 없는 경우


프론트에서 개발해야할 부분

1.이미지 자동 저장, path를 request body에 함깨 보내기

2.테스트 기능


참고 문헌

https://yihoeyiho.tistory.com/44 - db 연결과 CRUD API

https://blog.neonkid.xyz/253 - CRUD API

https://rianshin.tistory.com/68 - psql 명령어
