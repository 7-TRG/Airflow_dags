# Airflow_dags

release/d2.0.0
=======
## d1.0.0
- [X] Git 연동
- [X] Airflow 변수 변경, gitignore 확인하기
- [X] Airflow Dag에 사용할 .py 만들기 -> 24 * 7 설정 변경하기
- [X] Ice-breaking 함수 개발(디렉토리 생성 후 -> pdm init -> 모듈 개발 -> git push)
- [ ] 회고 작성

### 기능 분배

- 수집 + 처리 +보관 및 활용
- 수집 : JSON -> Parquet [지현] 
- 처리 : Pandas [원준]
- 보관 및 활용 : Airflow [령래]  

### 작업 플로우

하나의 컴퓨터
- dev branch에서 작업 후 release branch로 merge
각자 컴퓨터
- 모듈 작업 시 dev 브랜치에서 각자 디렉토리에서 작업 한 뒤에 각자 git에 push
- .py 생성 -> git checkout dev<버전> -> git pull -> git merge (dev <- simple) -> git push


[git 사용법]
작업을 완료하면 git pull ->  git add . -> git commit  -> 잘 작동되는지 확인 -> git push하기

### ISSUE, PULL REQUEST, MIlESTONE

***
- MILESTONE : DAY1
- ISSUE : DAY1(7개)
- PR : 1(release <- dev)
***

### 에러 정보 공유

### 문제 발생 및 해결

### [Git 연동]
- Git Clone 시 HTTPS 대신 SSH URL 사용

### [Git 사용]
문제1
- 문제 : Airflow_dag를 git pull 하는 과정에서 로컬에서도 똑같은 파일이 존재. 그래서 다음과 같은 오류 발생
```
branch            dev/d1.0.0 -> FETCH_HEAD
업데이트 중 56ddef6..31383e9
error: 병합 때문에 추적하지 않는 다음 작업 폴더의 파일을 덮어씁니다:
        .gitignore
        airflow.cfg
        webserver_config.py
병합하기 전에 이 파일을 옮기거나 제거하십시오.
중지함
```
- 해결 : 브랜치 삭제 후 git reset --hard origin/dev/d1.0.0 명령 실행'

문제2
- 상황 : A가 로컬 컴퓨터에서 Airflow를 사용하고 싶은 상황, Github에 airflow의 환경설정을 저장하는 airflow.cfg 파일이 올라가 있는 상태
- 문제 : A가 Github(airflow_dags)를 pull하면  airflow.cfg 파일이 같이 딸려들어오는 상황
- 해결 : Github 상의 airflow.cfg를 삭제, gitignore에서 airflow.cfg를 추가한 뒤에 push
- 결과 : 팀원들도 Github를 활용해서 Airflow를 실행시킬 수 있다.
