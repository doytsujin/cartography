from unittest.mock import patch
from tests.integration import settings

from cartography.driftdetect.detect_drift import perform_drift_detection, run
from cartography.driftdetect.cli import CLI


@patch('cartography.driftdetect.cli.run')
def test_cli_main(mock_run):
    cli = CLI(prog="driftdetect")
    cli.main(["--neo4j-uri", settings.get("NEO4J_URL"), "--drift-detector-directory", "tests/data/detectors"])
    mock_run.assert_called_once()


def test_configure():
    cli = CLI(prog="driftdetect")
    config = cli.configure([
        "--neo4j-uri",
        settings.get("NEO4J_URL"),
        "--drift-detector-directory",
        "tests/data/detectors"
    ])
    assert config.drift_detector_directory == "tests/data/detectors"
    assert config.neo4j_uri == settings.get("NEO4J_URL")


def test_perform_drift_detection(neo4j_session):
    """
    Test that a full run through with the CLI works
    :param neo4j_session:
    :return:
    """
    data = [
        ["1", "8", ["15", "22", "29"]],
        ["2", "9", ["16", "23", "30"]],
        ["3", "10", ["17", "24", "31"]],
        ["4", "11", ["18", "25", "32"]],
        ["5", "12", ["19", "26", "33"]],
        ["6", "13", ["20", "27", "34"]],
        ["7", "14", ["21", "28", "35"]],
        ["36", "37", ["38", "39", "40"]]
    ]
    ingest_nodes = """
    MERGE (person:Person{test: {test}})
    SET person.test2 = {test2},
    person.test3 = {test3}
    """
    for node in data:
        test = node[0]
        test2 = node[1]
        test3 = node[2]
        neo4j_session.run(
            ingest_nodes,
            test=test,
            test2=test2,
            test3=test3
        )

    drift_pairs = perform_drift_detection(neo4j_session, "tests/data/detectors", update=False)
    drift_info = [pair[0] for pair in drift_pairs]
    assert {"d.test": "7"} in drift_info
    assert {"d.test": "7", "d.test2": "14"} in drift_info
    assert {"d.test": "7", "d.test2": "14", "d.test3": ["21", "28", "35"]} in drift_info
    assert {"d.test": "36", "d.test2": "37", "d.test3": ["38", "39", "40"]} in drift_info


@patch("cartography.driftdetect.detect_drift.perform_drift_detection")
def test_run(mock_perform_drift_detection, neo4j_session):
    cli = CLI(prog="driftdetect")
    config = cli.configure([
        "--neo4j-uri",
        settings.get("NEO4J_URL"),
        "--drift-detector-directory",
        "tests/data/detectors"
    ])
    run(config)
    assert mock_perform_drift_detection.called_once_with(neo4j_session, config.drift_detector_directory, False)
