"""
Medication Safety Checker
-------------------------
Medication error and interaction screening prototype
A simple, rule-based clinical safety checking tool for demonstration.
"""

import streamlit as st
from typing import List
from knowledge_base import DEMO_DRUGS, DEMO_SCENARIOS
from safety_engine import (
    MedicationSafetyEngine,
    PatientProfile,
    PrescriptionItem,
    SafetyAlert,
)

# Page configuration
st.set_page_config(
    page_title="Medication Safety Checker",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Minimal clean styling: white background, clean text, simple blue accent
st.markdown("""
<style>
    .stApp {
        background-color: #FFFFFF;
        color: #1E293B;
    }
    section[data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }
    .disclaimer-text {
        font-size: 0.85rem;
        color: #64748B;
        margin-top: -0.5rem;
        margin-bottom: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)

# Frequency mapping to daily intake multiplier
FREQ_MAP = {
    "Once daily (QD)": 1.0,
    "Twice daily (BID)": 2.0,
    "Three times daily (TID)": 3.0,
    "Four times daily (QID)": 4.0,
    "Every 12 hours (Q12H)": 2.0,
    "Every 8 hours (Q8H)": 3.0,
    "Every 6 hours (Q6H)": 4.0,
    "Every 4 to 6 hours as needed (PRN)": 4.0,
}

FREQ_OPTIONS = list(FREQ_MAP.keys())
KNOWN_DRUG_NAMES = sorted(list(DEMO_DRUGS.keys()))
COMMON_CONDITIONS = [
    "Asthma",
    "Chronic Kidney Disease",
    "Peptic Ulcer Disease",
    "Hypertension",
    "Type 2 Diabetes",
    "Atrial Fibrillation",
    "Heart Failure",
    "Active Liver Disease",
    "Pregnancy",
    "Acute Sinusitis",
    "Fever"
]
COMMON_ALLERGIES = [
    "Penicillin",
    "Beta-Lactam",
    "NSAID",
    "Aspirin",
    "Sulfa",
    "Opioid",
    "Statin",
    "ACE Inhibitor"
]


# Initialize Session State
def init_session_state():
    if "widget_age" not in st.session_state:
        st.session_state["widget_age"] = 45
    if "widget_existing_meds" not in st.session_state:
        st.session_state["widget_existing_meds"] = []
    if "widget_custom_existing" not in st.session_state:
        st.session_state["widget_custom_existing"] = ""
    if "widget_allergies" not in st.session_state:
        st.session_state["widget_allergies"] = []
    if "widget_custom_allergies" not in st.session_state:
        st.session_state["widget_custom_allergies"] = ""
    if "widget_conditions" not in st.session_state:
        st.session_state["widget_conditions"] = []
    if "widget_custom_conditions" not in st.session_state:
        st.session_state["widget_custom_conditions"] = ""
    if "num_prescriptions" not in st.session_state:
        st.session_state["num_prescriptions"] = 1
        st.session_state["rx_drug_0"] = "Amoxicillin"
        st.session_state["rx_dose_0"] = 500.0
        st.session_state["rx_freq_0"] = "Three times daily (TID)"
    if "alerts" not in st.session_state:
        st.session_state["alerts"] = None

init_session_state()


def perform_analysis():
    """Gathers current inputs and executes the safety engine."""
    all_conditions = list(st.session_state.get("widget_conditions", []))
    custom_c = st.session_state.get("widget_custom_conditions", "")
    if custom_c:
        for c in custom_c.split(","):
            if c.strip():
                all_conditions.append(c.strip())

    all_allergies = list(st.session_state.get("widget_allergies", []))
    custom_a = st.session_state.get("widget_custom_allergies", "")
    if custom_a:
        for a in custom_a.split(","):
            if a.strip():
                all_allergies.append(a.strip())

    all_existing = list(st.session_state.get("widget_existing_meds", []))
    custom_e = st.session_state.get("widget_custom_existing", "")
    if custom_e:
        for m in custom_e.split(","):
            if m.strip():
                all_existing.append(m.strip())

    patient = PatientProfile(
        age=int(st.session_state.get("widget_age", 45)),
        existing_meds=all_existing,
        allergies=all_allergies,
        conditions=all_conditions
    )

    rx_objects: List[PrescriptionItem] = []
    num_rxs = st.session_state.get("num_prescriptions", 1)
    for idx in range(num_rxs):
        drug = st.session_state.get(f"rx_drug_{idx}", "Amoxicillin")
        dose = float(st.session_state.get(f"rx_dose_{idx}", 500.0))
        freq_label = st.session_state.get(f"rx_freq_{idx}", "Once daily (QD)")
        freq_multiplier = FREQ_MAP.get(freq_label, 1.0)
        rx_objects.append(
            PrescriptionItem(
                drug_name=drug,
                dose_amount=dose,
                dose_unit="mg",
                frequency_label=freq_label,
                frequency_per_day=freq_multiplier
            )
        )

    engine = MedicationSafetyEngine()
    st.session_state["alerts"] = engine.analyze(patient, rx_objects)


# Helper to load a demo scenario
def load_scenario(scenario_key: str):
    if scenario_key not in DEMO_SCENARIOS:
        return
    scenario = DEMO_SCENARIOS[scenario_key]
    pat = scenario["patient"]
    rxs = scenario["prescriptions"]

    st.session_state["widget_age"] = pat["age"]

    # Existing meds
    standard_meds = [m for m in pat["existing_meds"] if m in KNOWN_DRUG_NAMES]
    custom_meds = [m for m in pat["existing_meds"] if m not in KNOWN_DRUG_NAMES]
    st.session_state["widget_existing_meds"] = standard_meds
    st.session_state["widget_custom_existing"] = ", ".join(custom_meds)

    # Allergies
    standard_all = [a for a in pat["allergies"] if a in COMMON_ALLERGIES]
    custom_all = [a for a in pat["allergies"] if a not in COMMON_ALLERGIES]
    st.session_state["widget_allergies"] = standard_all
    st.session_state["widget_custom_allergies"] = ", ".join(custom_all)

    # Conditions
    standard_cond = [c for c in pat["conditions"] if c in COMMON_CONDITIONS]
    custom_cond = [c for c in pat["conditions"] if c not in COMMON_CONDITIONS]
    st.session_state["widget_conditions"] = standard_cond
    st.session_state["widget_custom_conditions"] = ", ".join(custom_cond)

    # Prescriptions
    st.session_state["num_prescriptions"] = len(rxs)
    for idx, rx in enumerate(rxs):
        st.session_state[f"rx_drug_{idx}"] = rx["drug"]
        st.session_state[f"rx_dose_{idx}"] = float(rx["dose"])
        st.session_state[f"rx_freq_{idx}"] = rx.get("frequency", "Once daily (QD)")

    # Execute analysis automatically upon scenario load
    perform_analysis()


# Sidebar: Clean and simple demo controls
with st.sidebar:
    st.header("Demo Scenarios")
    
    demo_choice = st.selectbox(
        "Select Scenario",
        list(DEMO_SCENARIOS.keys()),
        index=0
    )

    if st.button("Load Scenario", type="primary", use_container_width=True):
        load_scenario(demo_choice)
        st.rerun()

    st.divider()

    st.markdown("**Supported Risk Categories**")
    st.markdown("""
    - Drug-Drug Interactions
    - Drug-Disease Interactions
    - Duplicate Medications
    - Incorrect Dosage
    - Allergy Conflicts
    """)


# Main Header
st.title("Medication Safety Checker")
st.write("Medication error and interaction screening prototype")

st.markdown(
    '<div class="disclaimer-text">Notice: This prototype is intended for medication-safety decision support and demonstration purposes only. It does not replace professional clinical judgment.</div>',
    unsafe_allow_html=True
)

st.divider()

# Layout: Simple two-column input layout
col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("1. Patient Details")

    st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        key="widget_age",
        help="Patients aged 65 or older trigger geriatric safety dose thresholds."
    )

    st.multiselect(
        "Diseases / Conditions",
        options=COMMON_CONDITIONS,
        key="widget_conditions"
    )

    st.text_input(
        "Other Diseases (comma-separated)",
        key="widget_custom_conditions",
        placeholder="e.g. Angina"
    )

    st.multiselect(
        "Allergies",
        options=COMMON_ALLERGIES,
        key="widget_allergies"
    )

    st.text_input(
        "Other Allergies (comma-separated)",
        key="widget_custom_allergies",
        placeholder="e.g. Sulfa"
    )

    st.multiselect(
        "Current Medications",
        options=KNOWN_DRUG_NAMES,
        key="widget_existing_meds"
    )

    st.text_input(
        "Other Current Medications (comma-separated)",
        key="widget_custom_existing",
        placeholder="e.g. Nitroglycerin"
    )

with col2:
    st.subheader("2. New Prescription")

    num_rxs = st.session_state["num_prescriptions"]

    for idx in range(num_rxs):
        st.markdown(f"**Medicine #{idx + 1}**")
        c_name, c_dose, c_freq = st.columns([2, 1.2, 1.8])

        with c_name:
            st.selectbox(
                "Medicine",
                options=KNOWN_DRUG_NAMES,
                key=f"rx_drug_{idx}"
            )

        with c_dose:
            st.number_input(
                "Dosage (mg)",
                min_value=0.0,
                max_value=10000.0,
                step=0.5,
                format="%.2f",
                key=f"rx_dose_{idx}"
            )

        with c_freq:
            st.selectbox(
                "Frequency",
                options=FREQ_OPTIONS,
                key=f"rx_freq_{idx}"
            )

    c_add, c_del = st.columns(2)
    with c_add:
        if st.button("+ Add Medication", use_container_width=True):
            new_idx = st.session_state["num_prescriptions"]
            st.session_state[f"rx_drug_{new_idx}"] = "Aspirin"
            st.session_state[f"rx_dose_{new_idx}"] = 500.0
            st.session_state[f"rx_freq_{new_idx}"] = "Once daily (QD)"
            st.session_state["num_prescriptions"] += 1
            st.rerun()

    with c_del:
        if st.session_state["num_prescriptions"] > 1:
            if st.button("Remove Last", use_container_width=True):
                st.session_state["num_prescriptions"] -= 1
                st.rerun()

    st.write("")
    if st.button("Analyze Prescription", type="primary", use_container_width=True):
        perform_analysis()


# Section 3: Safety Analysis
st.divider()
st.subheader("3. Safety Analysis")

if st.session_state["alerts"] is None:
    st.info("Enter patient and prescription details above or load a demo scenario from the sidebar, then click Analyze Prescription.")
else:
    alerts: List[SafetyAlert] = st.session_state["alerts"]

    if not alerts:
        with st.container(border=True):
            st.markdown("### Safe Prescription - No issues detected")
            st.write("No drug-drug interactions, duplicate therapies, disease contraindications, dosage limit violations, or allergy conflicts were detected in the demonstration knowledge base.")
    else:
        high_count = sum(1 for a in alerts if a.severity == "High")
        med_count = sum(1 for a in alerts if a.severity == "Medium")
        low_count = sum(1 for a in alerts if a.severity == "Low")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Alerts", len(alerts))
        m2.metric("High Severity", high_count)
        m3.metric("Medium Severity", med_count)
        m4.metric("Low Severity", low_count)

        for idx, alert in enumerate(alerts, 1):
            with st.container(border=True):
                st.markdown(f"**Alert {idx}: {alert.detected_issue}**")
                st.markdown(f"- **Category:** {alert.risk_category}")
                st.markdown(f"- **Severity:** {alert.severity}")
                st.markdown(f"- **Medicine/condition involved:** {alert.items_involved}")
                st.markdown(f"- **What was detected:** {alert.detected_issue}")
                st.markdown(f"- **Why it matters:** {alert.clinical_risk}")
                st.markdown(f"- **Suggested professional review:** {alert.suggested_action}")
