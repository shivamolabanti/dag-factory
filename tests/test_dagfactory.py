import os
import datetime

import pytest

from dagfactory import dagfactory

here = os.path.dirname(__file__)


TEST_DAG_FACTORY = os.path.join(here, "fixtures/dag_factory.yml")
INVALID_YAML = os.path.join(here, "fixtures/invalid_yaml.yml")
INVALID_DAG_FACTORY = os.path.join(here, "fixtures/invalid_dag_factory.yml")


def test_validate_config_filepath_valid():
    dagfactory.DagFactory._validate_config_filepath(TEST_DAG_FACTORY)


def test_validate_config_filepath_invalid():
    with pytest.raises(Exception):
        dagfactory.DagFactory._validate_config_filepath("config.yml")


def test_load_config_valid():
    expected = {
        "default": {
            "default_args": {
                "owner": "default_owner",
                "start_date": datetime.date(2018, 3, 1),
            },
            "max_active_runs": 1,
            "schedule_interval": "0 1 * * *",
        },
        "example_dag": {
            "default_args": {"owner": "custom_owner", "start_date": "2 days"},
            "description": "this is an example dag",
            "schedule_interval": "0 3 * * *",
            "tasks": {
                "task_1": {
                    "operator": "airflow.operators.bash_operator.BashOperator",
                    "bash_command": "echo 1",
                },
                "task_2": {
                    "operator": "airflow.operators.bash_operator.BashOperator",
                    "bash_command": "echo 2",
                    "dependencies": ["task_1"],
                },
                "task_3": {
                    "operator": "airflow.operators.bash_operator.BashOperator",
                    "bash_command": "echo 3",
                    "dependencies": ["task_1"],
                },
            },
        },
        "example_dag2": {
            "tasks": {
                "task_1": {
                    "operator": "airflow.operators.bash_operator.BashOperator",
                    "bash_command": "echo 1",
                },
                "task_2": {
                    "operator": "airflow.operators.bash_operator.BashOperator",
                    "bash_command": "echo 2",
                    "dependencies": ["task_1"],
                },
                "task_3": {
                    "operator": "airflow.operators.bash_operator.BashOperator",
                    "bash_command": "echo 3",
                    "dependencies": ["task_1"],
                },
            }
        },
    }
    actual = dagfactory.DagFactory._load_config(TEST_DAG_FACTORY)
    assert actual == expected


def test_load_config_invalid():
    with pytest.raises(Exception):
        dagfactory.DagFactory._load_config(INVALID_YAML)


def test_get_dag_configs():
    td = dagfactory.DagFactory(TEST_DAG_FACTORY)
    expected = {
        "example_dag": {
            "default_args": {"owner": "custom_owner", "start_date": "2 days"},
            "description": "this is an example dag",
            "schedule_interval": "0 3 * * *",
            "tasks": {
                "task_1": {
                    "operator": "airflow.operators.bash_operator.BashOperator",
                    "bash_command": "echo 1",
                },
                "task_2": {
                    "operator": "airflow.operators.bash_operator.BashOperator",
                    "bash_command": "echo 2",
                    "dependencies": ["task_1"],
                },
                "task_3": {
                    "operator": "airflow.operators.bash_operator.BashOperator",
                    "bash_command": "echo 3",
                    "dependencies": ["task_1"],
                },
            },
        },
        "example_dag2": {
            "tasks": {
                "task_1": {
                    "operator": "airflow.operators.bash_operator.BashOperator",
                    "bash_command": "echo 1",
                },
                "task_2": {
                    "operator": "airflow.operators.bash_operator.BashOperator",
                    "bash_command": "echo 2",
                    "dependencies": ["task_1"],
                },
                "task_3": {
                    "operator": "airflow.operators.bash_operator.BashOperator",
                    "bash_command": "echo 3",
                    "dependencies": ["task_1"],
                },
            }
        },
    }
    actual = td.get_dag_configs()
    assert actual == expected


def test_get_default_config():
    td = dagfactory.DagFactory(TEST_DAG_FACTORY)
    expected = {
        "default_args": {
            "owner": "default_owner",
            "start_date": datetime.date(2018, 3, 1),
        },
        "max_active_runs": 1,
        "schedule_interval": "0 1 * * *",
    }
    actual = td.get_default_config()
    assert actual == expected


def test_generate_dags_valid():
    td = dagfactory.DagFactory(TEST_DAG_FACTORY)
    td.generate_dags(globals())
    assert "example_dag" in globals()
    assert "example_dag2" in globals()
    assert "fake_example_dag" not in globals()


def test_generate_dags_invalid():
    td = dagfactory.DagFactory(INVALID_DAG_FACTORY)
    with pytest.raises(Exception):
        td.generate_dags(globals())
