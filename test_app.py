"""
Streamlit UI Integration Tests using AppTest
Verifies that the Streamlit application starts, accepts inputs,
handles scenario loading, and triggers prescription analysis for ALL demo scenarios.
"""

import pytest
from streamlit.testing.v1 import AppTest
from knowledge_base import DEMO_SCENARIOS


def test_app_loads_without_exceptions():
    at = AppTest.from_file("app.py", default_timeout=15).run()
    assert not at.exception, f"App threw unexpected exceptions: {at.exception}"
    assert len(at.sidebar.selectbox) >= 1


def test_app_analyze_button_triggers():
    at = AppTest.from_file("app.py", default_timeout=15).run()
    analyze_btn = next((b for b in at.button if "Analyze" in b.label), None)
    assert analyze_btn is not None, "Analyze Prescription button should exist"

    analyze_btn.click().run()
    assert not at.exception
    # Should display results or metrics
    assert len(at.metric) > 0 or len(at.info) > 0 or len(at.markdown) > 0


@pytest.mark.parametrize("scenario_idx, scenario_name", [
    (0, "Scenario 1: Drug-Drug Interaction"),
    (1, "Scenario 2: Drug-Disease Interaction"),
    (2, "Scenario 3: Duplicate Medication"),
    (3, "Scenario 4: Incorrect Dosage"),
    (4, "Scenario 5: Allergy Conflict"),
    (5, "Scenario 6: Safe Prescription"),
])
def test_app_load_each_demo_scenario(scenario_idx, scenario_name):
    at = AppTest.from_file("app.py", default_timeout=15).run()
    at.sidebar.selectbox[0].select_index(scenario_idx).run()

    load_btn = next((b for b in at.sidebar.button if "Load Scenario" in b.label), None)
    assert load_btn is not None, "Load Scenario button must exist"
    load_btn.click().run()
    assert not at.exception

    if "Safe Prescription" in scenario_name:
        # Check safe banner is rendered
        safe_elements = [m.value for m in at.markdown if "Safe Prescription" in m.value]
        assert len(safe_elements) >= 1, "Expected Safe Prescription banner in markdown elements"
    else:
        # Check all 4 metrics are rendered
        metric_labels = [m.label for m in at.metric]
        assert "Total Alerts" in metric_labels
        assert "High Severity" in metric_labels
        assert "Medium Severity" in metric_labels
        assert "Low Severity" in metric_labels
        total_metric = next(m for m in at.metric if m.label == "Total Alerts")
        assert int(total_metric.value) >= 1, f"Expected >= 1 alert for {scenario_name}"


def test_app_dosage_input_step_and_low_dose():
    at = AppTest.from_file("app.py", default_timeout=15).run()
    # Check dosage number input step and low-dose support
    dose_input = at.number_input[1]  # index 0 is age, index 1 is rx_dose_0
    assert dose_input.step == 0.5
    assert dose_input.format == "%.2f"

