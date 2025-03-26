from pathlib import Path
import os

from dotenv import load_dotenv

from el_fmk.local_mode.el_runner import ElRunner


def main():
    config_yml_path = Path(r"./el/sql_database.yml")

    runner = ElRunner(
        config_yml_path=config_yml_path,
        domain_name="scm",
        project_name="dlt_demo",
        target="lab",
    )

    # If test_connection=True, it will test the connection to the database
    # If test_connection=False, check only yml config
    runner.check(test_connection=True)

    # limit: Run extract to local storage with a limit
    # generated_sl_models: Generate DBT Standard Layer Models
    # loader_file_format: csv, parquet, jsonl
    dfs = runner.run(limit=1, generated_sl_models=False, loader_file_format="parquet")
    if dfs:
        # preview extracted result as dataframe
        print(dfs[0])
    


if __name__ == "__main__":
    load_dotenv()
    main()
