# Medication Safety Checker

Screening prototype for medication errors, dangerous drug interactions, contraindications, dosage boundaries, and allergy conflicts.

---

## Notice & Clinical Disclaimer

> **"This prototype is intended for medication-safety decision support and demonstration purposes only. It does not replace professional clinical judgment."**
> 
> *The medication rules and interactions in this system represent prototype demonstration knowledge and should not be used as clinical medical advice or to instruct patients to start, stop, or change treatments.*

---

## Launch Command

To launch the Streamlit application:

```bash
python -m streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`.

---

## Demo Scenarios

Use the **Demo Scenarios** selector in the sidebar to test:

1. **Scenario 1: Drug-Drug Interaction**
   * *Profile:* Patient on Warfarin prescribed Aspirin 500mg BID.
   * *Detection:* High-severity bleeding & gastrointestinal hemorrhage hazard.
2. **Scenario 2: Drug-Disease Interaction**
   * *Profile:* Patient with Asthma prescribed non-selective beta blocker Propranolol 80mg BID.
   * *Detection:* High-severity bronchospasm and bronchoconstriction hazard.
3. **Scenario 3: Duplicate Medication**
   * *Profile:* Patient on Lisinopril 10mg prescribed Enalapril 20mg.
   * *Detection:* Therapeutic class overlap (ACE inhibitor duplication).
4. **Scenario 4: Incorrect Dosage**
   * *Profile:* Amoxicillin 4000mg single dose + Paracetamol 2000mg QID (8000mg/day).
   * *Detection:* Single dose ceiling violation & cumulative daily dose hepatotoxicity hazard.
5. **Scenario 5: Allergy Conflict**
   * *Profile:* Patient with documented Penicillin allergy prescribed Amoxicillin 500mg.
   * *Detection:* High-severity anaphylaxis & hypersensitivity hazard.
6. **Scenario 6: Safe Prescription**
   * *Profile:* 52yo hypertensive patient on Amlodipine prescribed standard Metformin 500mg BID for Type 2 Diabetes.
   * *Detection:* All safety checks pass with green confirmation banner.

---

## Automated Tests

Run the full automated test suite (21 tests):

```bash
python -m pytest
```

---

## Architecture

- `app.py`: Streamlit application with four straightforward sections (Patient Details, Current Medications, New Prescription, Safety Analysis).
- `safety_engine.py`: Rule-based clinical safety engine verifying all 5 risk categories.
- `knowledge_base.py`: Demonstration knowledge base of canonical medications, dosage limits, allergen cross-reactivity mapping, and interaction rules.
- `test_safety_engine.py`: Unit tests for all 5 safety risk categories.
- `test_app.py`: Streamlit AppTest integration tests for UI and demo scenarios.
