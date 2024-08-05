# 7_TRG movie Airflow
- 7조 영화 데이터 ETL airflow DAG 코드                                            
- 소스 데이터: [kobis open API](https://www.kobis.or.kr/kobisopenapi/homepg/apiservice/searchServiceInfo.do)   
- API access를 위하여 사이트에서 키 발급받은 후 실행
```bash
export MOVIE_API_KEY="<키값>"
```
# 환경변수 설정
```bash
export AIRFLOW_HOME=~/code/7_TRG/airflow_dags
export AIRFLOW__CORE__DAGS_FOLDER=~/code/7_TRG/airflow_dags/dags
export AIRFLOW__CORE__LOAD_EXAMPLES=False
```
# 실행
```bash
pyenv shell air
airflow standalone 
```
- airflow admin password
```
cat $AIRFLOW_HOME/standalone_admin_password.txt
```
# 실행 환경
```bash
$ uname -a
Linux playdata 5.15.153.1-microsoft-standard-WSL2 #1 SMP Fri Mar 29 23:14:13 UTC 2024 x86_64 x86_64 x86_64 GNU/Linux

$ cat /etc/issue
Ubuntu 22.04.3 LTS \n \l

$ pyenv -v
pyenv 2.4.7

$ pyenv shell air
(air) $  python -V
Python 3.11.9
(air) $ airflow version
2.9.3
```


