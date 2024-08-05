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
        'movie2',
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        'depends_on_past': True,
        'retries': 2,
        'retry_delay': timedelta(seconds=3),
        'max_active_tasks': 3,
        'max_active_runs': 1,
        },

    description='Movie Data',
    #schedule=timedelta(days=1),
    schedule="0 5 * * *",
    start_date=datetime(2017, 5, 1),
    #end_date=datetime(2017, 4, 30),
    end_date=datetime(2017, 8, 31),
    catchup=True,
    tags=['7_TRG','api', 'movie'],
) as dag:
    #REQUIREMENTS = "git+https://github.com/7-TRG/extract_trg.git@main"
    
    def branch_fun(ds_nodash):
        import os
        home_dir = os.path.expanduser("~")
#        path = os.path.join(home_dir, f"tmp/test_parquet/load_dt={ds_nodash}") 
        path = os.path.join(home_dir, f"code/7_TRG/data_parquet/load_dt={ds_nodash}")
        if os.path.exists(path):
            return rm_dir.task_id
        else:
            return task_e.task_id

    def extract_df(*args):
        ds_nodash = args[0]
        li = args[1:]
        print(ds_nodash, li)
        from extract_trg.extract_trg import dt2df
        for dic in li:
            df = dt2df(ds_nodash, dic)
            print(df.head(10))

            for k, v in dic.items():
                df[k] = v

            p_cols = ['load_dt'] + list(dic.keys())
            df.to_parquet("~/code/7_TRG/data_parquet", partition_cols = p_cols)

    def transform_df(ds_nodash):
        from transform_trg.transform_trg import mer
        df = mer(ds_nodash)
        print(df.head())
        return df
    def Icebreaking_l():
        from load_trg.ice_breaking import ice_breaking
        ice_breaking()

    task_e = PythonVirtualenvOperator(
        task_id='extract',
        python_callable=extract_df,
        requirements=["git+https://github.com/7-TRG/extract_trg.git@d2.0.0"],
        system_site_packages=False,
        trigger_rule="all_done",
        op_args = ['{{ ds_nodash }}',{'multiMovieYn' : 'Y'}, {'repNationCd' : 'K'}, {'multiMovieYn': 'N'},{ 'repNationCd' : 'F'}]
#op_kwargs = {'url_params' : {'multiMovieYn' : 'Y', 'repNationCd' : 'K'}, 'url_params2' : {'multiMovieYn': 'N', 'repNationCd' : 'F'}}
        #venv_cache_path="/home/kim1/tmp2/airflow_venv/get_data"r
    )

    task_t = PythonVirtualenvOperator(
        task_id='transform',
        python_callable=transform_df,
        requirements=["git+https://github.com/7-TRG/transform_trg.git@dev/d2.0.0"],
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

    branch_op = BranchPythonOperator(
        task_id="branch.op",
        python_callable=branch_fun
    )

    rm_dir = BashOperator(
        task_id='rm.dir',
        bash_command='rm -rf ~/code/7_TRG/data_parquet/load_dt={{ ds_nodash }}',
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

    task_start >> branch_op  >> task_e >> task_t >> task_l >> task_end
    branch_op >> rm_dir >> task_e
