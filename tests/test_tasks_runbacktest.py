import json
import os
import uuid

from quant_research_starter.api.tasks import tasks


def test_run_backtest_task_creates_output(tmp_path):
    job_id = uuid.uuid4().hex
    params = {"initial_capital": 100000, "weight_scheme": "rank"}

    # ensure OUTPUT_DIR points to tmp_path
    outdir = tmp_path / "output"
    os.environ["OUTPUT_DIR"] = str(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    result = tasks.run_backtest.run(job_id, params)

    # result should contain job_id and result_path
    assert result.get("job_id") == job_id
    path = result.get("result_path")
    assert path is not None
    assert os.path.exists(path)

    with open(path, "r") as f:
        data = json.load(f)
    assert "metrics" in data
