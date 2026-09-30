"""
Comprehensive unit tests for the Medication Safety Engine
Validates all 5 required safety check categories:
1. Drug-Drug Interactions
2. Drug-Disease Interactions
3. Duplicate Medications & Class Overlaps
4. Incorrect Dosage (Single, Cumulative Daily, Geriatric)
5. Allergy Conflicts
Also validates Safe Prescriptions and Demo Scenarios.
"""

import pytest
from safety_engine import (
    MedicationSafetyEngine,
    PatientProfile,
    PrescriptionItem,
    normalize_drug_name
)
from knowledge_base import DEMO_SCENARIOS


@pytest.fixture
def engine():
    return MedicationSafetyEngine()


def test_drug_normalization():
    assert normalize_drug_name("aspirin") == "Aspirin"
    assert normalize_drug_name("Advil") == "Ibuprofen"
    assert normalize_drug_name("Coumadin") == "Warfarin"
    assert normalize_drug_name("glucophage") == "Metformin"
    assert normalize_drug_name("Zestril") == "Lisinopril"


# 1. Drug-Drug Interaction Tests
def test_drug_drug_interaction_warfarin_aspirin(engine):
    patient = PatientProfile(
        age=60,
        existing_meds=["Warfarin"],
        allergies=[],
        conditions=[]
    )
    prescriptions = [
        PrescriptionItem(
            drug_name="Aspirin",
            dose_amount=100.0,
            dose_unit="mg",
            frequency_label="Once daily",
            frequency_per_day=1.0
        )
    ]
    alerts = engine.analyze(patient, prescriptions)
    dd_alerts = [a for a in alerts if a.risk_category == "Drug-Drug Interaction"]
    assert len(dd_alerts) >= 1
    alert = dd_alerts[0]
    assert alert.severity == "High"
    assert "Warfarin" in alert.items_involved and "Aspirin" in alert.items_involved
    assert "bleeding" in alert.clinical_risk.lower()
    assert alert.suggested_action != ""


def test_drug_drug_interaction_warfarin_naproxen(engine):
    patient = PatientProfile(
        age=65,
        existing_meds=["Warfarin"],
        allergies=[],
        conditions=[]
    )
    prescriptions = [
        PrescriptionItem(
            drug_name="Naproxen",
            dose_amount=250.0,
            dose_unit="mg",
            frequency_label="Twice daily",
            frequency_per_day=2.0
        )
    ]
    alerts = engine.analyze(patient, prescriptions)
    dd_alerts = [a for a in alerts if a.risk_category == "Drug-Drug Interaction"]
    assert len(dd_alerts) >= 1
    alert = dd_alerts[0]
    assert alert.severity == "High"
    assert "Warfarin" in alert.items_involved and "Naproxen" in alert.items_involved
    assert "bleeding" in alert.clinical_risk.lower()


def test_drug_drug_interaction_warfarin_ibuprofen(engine):
    patient = PatientProfile(
        age=60,
        existing_meds=["Warfarin"],
        allergies=[],
        conditions=[]
    )
    prescriptions = [
        PrescriptionItem(
            drug_name="Ibuprofen",
            dose_amount=400.0,
            dose_unit="mg",
            frequency_label="Three times daily",
            frequency_per_day=3.0
        )
    ]
    alerts = engine.analyze(patient, prescriptions)
    dd_alerts = [a for a in alerts if a.risk_category == "Drug-Drug Interaction"]
    assert len(dd_alerts) >= 1
    assert dd_alerts[0].severity == "High"
    assert "bleeding" in dd_alerts[0].clinical_risk.lower()


def test_low_dosage_decimal_support(engine):
    # Nitroglycerin 0.6mg is standard within limit, 3.0mg/day exceeds daily limit 2.4mg
    patient = PatientProfile(age=60, existing_meds=[], allergies=[], conditions=[])
    prescriptions = [
        PrescriptionItem(
            drug_name="Nitroglycerin",
            dose_amount=0.6,
            dose_unit="mg",
            frequency_label="Once daily PRN",
            frequency_per_day=1.0
        )
    ]
    alerts = engine.analyze(patient, prescriptions)
    assert not any(a.risk_category == "Incorrect Dosage" for a in alerts)


def test_drug_drug_interaction_sildenafil_nitroglycerin(engine):
    patient = PatientProfile(
        age=58,
        existing_meds=["Nitroglycerin"],
        allergies=[],
        conditions=["Angina"]
    )
    prescriptions = [
        PrescriptionItem(
            drug_name="Sildenafil",
            dose_amount=50.0,
            dose_unit="mg",
            frequency_label="Once daily PRN",
            frequency_per_day=1.0
        )
    ]
    alerts = engine.analyze(patient, prescriptions)
    dd_alerts = [a for a in alerts if a.risk_category == "Drug-Drug Interaction"]
    assert len(dd_alerts) >= 1
    assert any("hypotension" in a.clinical_risk.lower() for a in dd_alerts)


# 2. Drug-Disease Interaction Tests
def test_drug_disease_propranolol_asthma(engine):
    patient = PatientProfile(
        age=40,
        existing_meds=[],
        allergies=[],
        conditions=["Asthma", "Hypertension"]
    )
    prescriptions = [
        PrescriptionItem(
            drug_name="Propranolol",
            dose_amount=40.0,
            dose_unit="mg",
            frequency_label="Twice daily (BID)",
            frequency_per_day=2.0
        )
    ]
    alerts = engine.analyze(patient, prescriptions)
    dis_alerts = [a for a in alerts if a.risk_category == "Drug-Disease Interaction"]
    assert len(dis_alerts) >= 1
    assert dis_alerts[0].severity == "High"
    assert "bronchospasm" in dis_alerts[0].clinical_risk.lower()


def test_drug_disease_metformin_ckd(engine):
    patient = PatientProfile(
        age=68,
        existing_meds=[],
        allergies=[],
        conditions=["Chronic Kidney Disease Stage 4"]
    )
    prescriptions = [
        PrescriptionItem(
            drug_name="Metformin",
            dose_amount=500.0,
            dose_unit="mg",
            frequency_label="Twice daily (BID)",
            frequency_per_day=2.0
        )
    ]
    alerts = engine.analyze(patient, prescriptions)
    dis_alerts = [a for a in alerts if a.risk_category == "Drug-Disease Interaction"]
    assert len(dis_alerts) >= 1
    assert "lactic acidosis" in dis_alerts[0].clinical_risk.lower()


# 3. Duplicate Medication Tests
def test_duplicate_exact_match(engine):
    patient = PatientProfile(
        age=50,
        existing_meds=["Lisinopril"],
        allergies=[],
        conditions=["Hypertension"]
    )
    prescriptions = [
        PrescriptionItem(
            drug_name="Lisinopril",
            dose_amount=10.0,
            dose_unit="mg",
            frequency_label="Once daily (QD)",
            frequency_per_day=1.0
        )
    ]
    alerts = engine.analyze(patient, prescriptions)
    dup_alerts = [a for a in alerts if a.risk_category == "Duplicate Medication"]
    assert len(dup_alerts) >= 1
    assert dup_alerts[0].severity == "High"
    assert "exact duplicate" in dup_alerts[0].detected_issue.lower()


def test_duplicate_class_overlap(engine):
    patient = PatientProfile(
        age=55,
        existing_meds=["Lisinopril"],
        allergies=[],
        conditions=["Hypertension"]
    )
    prescriptions = [
        PrescriptionItem(
            drug_name="Enalapril",
            dose_amount=10.0,
            dose_unit="mg",
            frequency_label="Once daily (QD)",
            frequency_per_day=1.0
        )
    ]
    alerts = engine.analyze(patient, prescriptions)
    dup_alerts = [a for a in alerts if a.risk_category == "Duplicate Medication"]
    assert len(dup_alerts) >= 1
    assert any("ace inhibitor" in a.detected_issue.lower() for a in dup_alerts)


# 4. Incorrect Dosage Tests
def test_dosage_single_overdose(engine):
    patient = PatientProfile(age=30, existing_meds=[], allergies=[], conditions=[])
    prescriptions = [
        PrescriptionItem(
            drug_name="Amoxicillin",
            dose_amount=4000.0,  # Max single is 1000mg
            dose_unit="mg",
            frequency_label="Once daily",
            frequency_per_day=1.0
        )
    ]
    alerts = engine.analyze(patient, prescriptions)
    dose_alerts = [a for a in alerts if a.risk_category == "Incorrect Dosage"]
    assert len(dose_alerts) >= 1
    assert any("single dose" in a.detected_issue.lower() for a in dose_alerts)


def test_dosage_daily_cumulative_overdose(engine):
    patient = PatientProfile(age=45, existing_meds=[], allergies=[], conditions=[])
    prescriptions = [
        PrescriptionItem(
            drug_name="Paracetamol",
            dose_amount=1500.0,  # 1500 * 4 = 6000mg/day, max is 4000mg
            dose_unit="mg",
            frequency_label="Four times daily (QID)",
            frequency_per_day=4.0
        )
    ]
    alerts = engine.analyze(patient, prescriptions)
    dose_alerts = [a for a in alerts if a.risk_category == "Incorrect Dosage"]
    assert len(dose_alerts) >= 1
    assert any("cumulative daily dose" in a.detected_issue.lower() for a in dose_alerts)


def test_dosage_geriatric_threshold(engine):
    # Patient age 75 with 30mg Lisinopril (Geriatric max is 20mg, adult max is 40mg)
    patient = PatientProfile(age=75, existing_meds=[], allergies=[], conditions=[])
    prescriptions = [
        PrescriptionItem(
            drug_name="Lisinopril",
            dose_amount=30.0,
            dose_unit="mg",
            frequency_label="Once daily",
            frequency_per_day=1.0
        )
    ]
    alerts = engine.analyze(patient, prescriptions)
    dose_alerts = [a for a in alerts if a.risk_category == "Incorrect Dosage"]
    assert len(dose_alerts) >= 1
    assert any("geriatric" in a.detected_issue.lower() for a in dose_alerts)


# 5. Allergy Conflict Tests
def test_allergy_class_conflict(engine):
    patient = PatientProfile(
        age=28,
        existing_meds=[],
        allergies=["Penicillin"],
        conditions=["Bacterial Infection"]
    )
    prescriptions = [
        PrescriptionItem(
            drug_name="Amoxicillin",
            dose_amount=500.0,
            dose_unit="mg",
            frequency_label="Three times daily (TID)",
            frequency_per_day=3.0
        )
    ]
    alerts = engine.analyze(patient, prescriptions)
    allergy_alerts = [a for a in alerts if a.risk_category == "Allergy Conflict"]
    assert len(allergy_alerts) >= 1
    assert allergy_alerts[0].severity == "High"
    assert "anaphylaxis" in allergy_alerts[0].clinical_risk.lower()


# 6. Safe Prescription Test
def test_safe_prescription(engine):
    patient = PatientProfile(
        age=52,
        existing_meds=["Amlodipine"],
        allergies=[],
        conditions=["Type 2 Diabetes", "Hypertension"]
    )
    prescriptions = [
        PrescriptionItem(
            drug_name="Metformin",
            dose_amount=500.0,
            dose_unit="mg",
            frequency_label="Twice daily (BID)",
            frequency_per_day=2.0
        )
    ]
    alerts = engine.analyze(patient, prescriptions)
    assert len(alerts) == 0


# 7. Predefined Demonstration Scenarios Test
def test_all_demo_scenarios(engine):
    for scenario_name, scenario_data in DEMO_SCENARIOS.items():
        pat_data = scenario_data["patient"]
        patient = PatientProfile(
            age=pat_data["age"],
            existing_meds=pat_data["existing_meds"],
            allergies=pat_data["allergies"],
            conditions=pat_data["conditions"]
        )
        prescriptions = [
            PrescriptionItem(
                drug_name=rx["drug"],
                dose_amount=rx["dose"],
                dose_unit=rx.get("unit", "mg"),
                frequency_label=rx.get("frequency", "Once daily"),
                frequency_per_day=rx.get("frequency_per_day", 1.0)
            )
            for rx in scenario_data["prescriptions"]
        ]
        alerts = engine.analyze(patient, prescriptions)

        if "Safe Prescription" in scenario_name:
            assert len(alerts) == 0, f"Expected 0 alerts for {scenario_name}, got {len(alerts)}"
        elif "Drug-Drug" in scenario_name:
            assert any(a.risk_category == "Drug-Drug Interaction" for a in alerts)
        elif "Drug-Disease" in scenario_name:
            assert any(a.risk_category == "Drug-Disease Interaction" for a in alerts)
        elif "Duplicate Medication" in scenario_name:
            assert any(a.risk_category == "Duplicate Medication" for a in alerts)
        elif "Incorrect Dosage" in scenario_name:
            assert any(a.risk_category == "Incorrect Dosage" for a in alerts)
        elif "Allergy Conflict" in scenario_name:
            assert any(a.risk_category == "Allergy Conflict" for a in alerts)
