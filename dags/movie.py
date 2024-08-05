from datetime import datetime, timedelta
from textwrap import dedent

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator


from airflow.operators.python import (
        PythonOperator, PythonVirtualenvOperator, BranchPythonOperator
        )

with DAG(
        'movie',
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        'depends_on_past': True,
        'retries': 2,
        'retry_delay': timedelta(seconds=3)
        },
    max_active_tasks=3,
    max_active_runs=1,
    description='Movie Data',
    #schedule=timedelta(days=1),
    schedule="* 5 * * *",
    start_date=datetime(2017, 1, 1),
    end_date=datetime(2017, 4, 30),
    catchup=True,
    tags=['7_TRG','api', 'movie'],
) as dag:
    #REQUIREMENTS = "git+https://github.com/7-TRG/extract_trg.git@main"

    def extract_df(**kwargs):
        from extract_trg.extract_trg import dt2df
        df = dt2df(kwargs['ds_nodash'], kwargs['url_params'])
        print(df.head(10))
        return df
    def Icebreaking_t():
        from transform_trg.ice_breaking import ice
        ice()
    def Icebreaking_l():
        from load_trg.ice_breaking import ice_breaking
        ice_breaking()

    task_e = PythonVirtualenvOperator(
        task_id='extract',
        python_callable=extract_df,
        requirements=["git+https://github.com/7-TRG/extract_trg.git@d2.0.0"],
        system_site_packages=False,
        trigger_rule="all_done",
        op_kwargs = {'url_params' : {'multiMovieYn' : 'Y'}}
        #venv_cache_path="/home/kim1/tmp2/airflow_venv/get_data"
    )
    task_t = PythonVirtualenvOperator(
        task_id='transform',
        python_callable=Icebreaking_t,
        requirements=["git+https://github.com/7-TRG/transform_trg.git@main"],
        system_site_packages=False,
        trigger_rule="all_done",
        #venv_cache_path="/home/kim1/tmp2/airflow_venv/get_data"
    )
    task_l = PythonVirtualenvOperator(
        task_id='load',
        python_callable=Icebreaking_l,
        requirements=['git+https://github.com/7-TRG/load_trg.git@main'],
        system_site_packages=False,
        trigger_rule="all_done",
        #venv_cache_path="/home/kim1/tmp2/airflow_venv/get_data"
    )

#    task_err = BashOperator(
#        bash_command="""
#            DONE_PATH=~/data/done/{{ds_nodash}}
#            mkdir -p ${DONE_PATH}
#            touch ${DONE_PATH}/_DONE
#        """,
#    )

    task_end = EmptyOperator(task_id='end', trigger_rule="all_done")
    task_start = EmptyOperator(task_id='start')

    task_start >> task_e >> task_t >> task_l >> task_end
 

