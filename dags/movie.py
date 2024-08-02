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
    end_date=datetime(2017, 12, 31),
    catchup=True,
    tags=['7_TRG','api', 'movie'],
) as dag:
    REQUIREMENTS = "git+https://github.com/7-TRG/extract_trg.git@main"

    def Icebreaking():
        from extract_trg.ice_breaking import ice_breaking
        ice_breaking()

    task_get = PythonVirtualenvOperator(
        task_id='get.data',
        python_callable=Icebreaking,
        requirements=REQUIREMENTS,
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

    task_start >> task_get >> task_end
 

