"""
Demonstration Medication Knowledge Base
--------------------------------------
DISCLAIMER: This prototype knowledge base is curated exclusively for demonstration
and medication-safety decision support testing in a prototype environment.
It does NOT represent comprehensive medical literature or replace clinical judgment.
"""

from typing import Dict, List, Any

# Supported demonstration drugs with canonical metadata
DEMO_DRUGS: Dict[str, Dict[str, Any]] = {
    "Aspirin": {
        "aliases": ["acetylsalicylic acid", "asa", "ecotrin"],
        "class": "NSAID / Antiplatelet",
        "allergen_classes": ["NSAID", "Aspirin", "Salicylates"],
        "max_single_dose_mg": 1000.0,
        "max_daily_dose_mg": 4000.0,
        "geriatric_max_daily_dose_mg": 2000.0,
        "unit": "mg",
        "description": "Analgesic, antipyretic, and antiplatelet agent."
    },
    "Ibuprofen": {
        "aliases": ["advil", "motrin", "nurofen"],
        "class": "NSAID",
        "allergen_classes": ["NSAID", "Ibuprofen"],
        "max_single_dose_mg": 800.0,
        "max_daily_dose_mg": 2400.0,
        "geriatric_max_daily_dose_mg": 1200.0,
        "unit": "mg",
        "description": "Nonsteroidal anti-inflammatory drug (NSAID) for pain and inflammation."
    },
    "Naproxen": {
        "aliases": ["aleve", "naprosyn"],
        "class": "NSAID",
        "allergen_classes": ["NSAID", "Naproxen"],
        "max_single_dose_mg": 500.0,
        "max_daily_dose_mg": 1250.0,
        "geriatric_max_daily_dose_mg": 1000.0,
        "unit": "mg",
        "description": "NSAID used for arthritis, musculoskeletal pain, and dysmenorrhea."
    },
    "Warfarin": {
        "aliases": ["coumadin", "jantoven"],
        "class": "Oral Anticoagulant",
        "allergen_classes": ["Warfarin"],
        "max_single_dose_mg": 10.0,
        "max_daily_dose_mg": 15.0,
        "geriatric_max_daily_dose_mg": 5.0,
        "unit": "mg",
        "description": "Vitamin K antagonist anticoagulant for thromboembolic prophylaxis."
    },
    "Apixaban": {
        "aliases": ["eliquis"],
        "class": "Direct Oral Anticoagulant (DOAC)",
        "allergen_classes": ["DOAC", "Apixaban"],
        "max_single_dose_mg": 10.0,
        "max_daily_dose_mg": 20.0,
        "geriatric_max_daily_dose_mg": 10.0,
        "unit": "mg",
        "description": "Factor Xa inhibitor anticoagulant."
    },
    "Lisinopril": {
        "aliases": ["zestril", "prinivil"],
        "class": "ACE Inhibitor",
        "allergen_classes": ["ACE Inhibitor", "Lisinopril"],
        "max_single_dose_mg": 40.0,
        "max_daily_dose_mg": 40.0,
        "geriatric_max_daily_dose_mg": 20.0,
        "unit": "mg",
        "description": "Angiotensin-converting enzyme (ACE) inhibitor for hypertension and heart failure."
    },
    "Enalapril": {
        "aliases": ["vasotec"],
        "class": "ACE Inhibitor",
        "allergen_classes": ["ACE Inhibitor", "Enalapril"],
        "max_single_dose_mg": 40.0,
        "max_daily_dose_mg": 40.0,
        "geriatric_max_daily_dose_mg": 20.0,
        "unit": "mg",
        "description": "ACE inhibitor for blood pressure control and congestive heart failure."
    },
    "Spironolactone": {
        "aliases": ["aldactone"],
        "class": "Potassium-Sparing Diuretic",
        "allergen_classes": ["Spironolactone"],
        "max_single_dose_mg": 100.0,
        "max_daily_dose_mg": 200.0,
        "geriatric_max_daily_dose_mg": 50.0,
        "unit": "mg",
        "description": "Aldosterone receptor antagonist; potassium-sparing diuretic."
    },
    "Propranolol": {
        "aliases": ["inderal"],
        "class": "Beta Blocker (Non-selective)",
        "allergen_classes": ["Beta Blocker", "Propranolol"],
        "max_single_dose_mg": 160.0,
        "max_daily_dose_mg": 320.0,
        "geriatric_max_daily_dose_mg": 160.0,
        "unit": "mg",
        "description": "Non-selective beta-adrenergic receptor blocker."
    },
    "Metoprolol": {
        "aliases": ["lopressor", "toprol xl"],
        "class": "Beta Blocker (Cardioselective)",
        "allergen_classes": ["Beta Blocker", "Metoprolol"],
        "max_single_dose_mg": 200.0,
        "max_daily_dose_mg": 400.0,
        "geriatric_max_daily_dose_mg": 200.0,
        "unit": "mg",
        "description": "Cardioselective beta-1 adrenergic blocker."
    },
    "Amoxicillin": {
        "aliases": ["amoxil", "moxatag"],
        "class": "Penicillin Antibiotic",
        "allergen_classes": ["Penicillin", "Beta-Lactam", "Amoxicillin"],
        "max_single_dose_mg": 1000.0,
        "max_daily_dose_mg": 3000.0,
        "geriatric_max_daily_dose_mg": 2000.0,
        "unit": "mg",
        "description": "Broad-spectrum aminopenicillin antibiotic."
    },
    "Augmentin": {
        "aliases": ["amoxicillin-clavulanate", "amoxicillin and clavulanate potassium"],
        "class": "Penicillin Antibiotic",
        "allergen_classes": ["Penicillin", "Beta-Lactam", "Amoxicillin", "Clavulanate"],
        "max_single_dose_mg": 1000.0,
        "max_daily_dose_mg": 2000.0,
        "geriatric_max_daily_dose_mg": 1500.0,
        "unit": "mg",
        "description": "Aminopenicillin combined with beta-lactamase inhibitor."
    },
    "Metformin": {
        "aliases": ["glucophage", "fortamet"],
        "class": "Biguanide Antidiabetic",
        "allergen_classes": ["Metformin"],
        "max_single_dose_mg": 1000.0,
        "max_daily_dose_mg": 2550.0,
        "geriatric_max_daily_dose_mg": 2000.0,
        "unit": "mg",
        "description": "First-line oral antihyperglycemic medication for Type 2 Diabetes."
    },
    "Simvastatin": {
        "aliases": ["zocor"],
        "class": "HMG-CoA Reductase Inhibitor (Statin)",
        "allergen_classes": ["Statin", "Simvastatin"],
        "max_single_dose_mg": 40.0,
        "max_daily_dose_mg": 40.0,
        "geriatric_max_daily_dose_mg": 20.0,
        "unit": "mg",
        "description": "Lipid-lowering statin medication metabolized via CYP3A4."
    },
    "Atorvastatin": {
        "aliases": ["lipitor"],
        "class": "HMG-CoA Reductase Inhibitor (Statin)",
        "allergen_classes": ["Statin", "Atorvastatin"],
        "max_single_dose_mg": 80.0,
        "max_daily_dose_mg": 80.0,
        "geriatric_max_daily_dose_mg": 40.0,
        "unit": "mg",
        "description": "Potent statin for hypercholesterolemia and cardiovascular risk reduction."
    },
    "Clarithromycin": {
        "aliases": ["biaxin"],
        "class": "Macrolide Antibiotic",
        "allergen_classes": ["Macrolide", "Clarithromycin"],
        "max_single_dose_mg": 500.0,
        "max_daily_dose_mg": 1000.0,
        "geriatric_max_daily_dose_mg": 1000.0,
        "unit": "mg",
        "description": "Macrolide antibiotic and potent CYP3A4 enzyme inhibitor."
    },
    "Sertraline": {
        "aliases": ["zoloft"],
        "class": "SSRI Antidepressant",
        "allergen_classes": ["SSRI", "Sertraline"],
        "max_single_dose_mg": 200.0,
        "max_daily_dose_mg": 200.0,
        "geriatric_max_daily_dose_mg": 100.0,
        "unit": "mg",
        "description": "Selective serotonin reuptake inhibitor (SSRI)."
    },
    "Tramadol": {
        "aliases": ["ultram", "conzip"],
        "class": "Opioid Analgesic / Serotonergic",
        "allergen_classes": ["Opioid", "Tramadol"],
        "max_single_dose_mg": 100.0,
        "max_daily_dose_mg": 400.0,
        "geriatric_max_daily_dose_mg": 300.0,
        "unit": "mg",
        "description": "Centrally acting synthetic opioid analgesic with weak SNRI activity."
    },
    "Nitroglycerin": {
        "aliases": ["nitrostat", "nitrolingual"],
        "class": "Nitrate Vasodilator",
        "allergen_classes": ["Nitrate", "Nitroglycerin"],
        "max_single_dose_mg": 0.6,
        "max_daily_dose_mg": 2.4,
        "geriatric_max_daily_dose_mg": 1.8,
        "unit": "mg",
        "description": "Organic nitrate vasodilator for acute angina pectoris relief."
    },
    "Sildenafil": {
        "aliases": ["viagra", "revatio"],
        "class": "PDE5 Inhibitor",
        "allergen_classes": ["PDE5 Inhibitor", "Sildenafil"],
        "max_single_dose_mg": 100.0,
        "max_daily_dose_mg": 100.0,
        "geriatric_max_daily_dose_mg": 50.0,
        "unit": "mg",
        "description": "Phosphodiesterase type 5 (PDE5) inhibitor."
    },
    "Paracetamol": {
        "aliases": ["acetaminophen", "tylenol", "panadol"],
        "class": "Analgesic / Antipyretic",
        "allergen_classes": ["Paracetamol", "Acetaminophen"],
        "max_single_dose_mg": 1000.0,
        "max_daily_dose_mg": 4000.0,
        "geriatric_max_daily_dose_mg": 3000.0,
        "unit": "mg",
        "description": "Non-opioid analgesic and antipyretic agent."
    },
    "Amlodipine": {
        "aliases": ["norvasc"],
        "class": "Calcium Channel Blocker (DHP)",
        "allergen_classes": ["Calcium Channel Blocker", "Amlodipine"],
        "max_single_dose_mg": 10.0,
        "max_daily_dose_mg": 10.0,
        "geriatric_max_daily_dose_mg": 5.0,
        "unit": "mg",
        "description": "Dihydropyridine calcium channel blocker for hypertension and CAD."
    }
}

# Drug-Drug Interaction Rules
DRUG_DRUG_RULES = [
    {
        "pair": ("Warfarin", "Aspirin"),
        "severity": "High",
        "title": "Severe Bleeding & GI Hemorrhage Hazard",
        "mechanism": "Warfarin (anticoagulant) combined with Aspirin (antiplatelet & gastric irritant) produces potent synergistic anti-hemostatic activity and disrupts gastric mucosal protection, exponentially increasing the risk of life-threatening gastrointestinal hemorrhage or internal bleeding.",
        "action": "Avoid combination unless strictly indicated for high-risk cardiac prosthesis. If unavoidable, co-prescribe a proton pump inhibitor (PPI) for mucosal protection and monitor INR closely."
    },
    {
        "pair": ("Warfarin", "Ibuprofen"),
        "severity": "High",
        "title": "Major Bleeding Risk from Anticoagulant + NSAID Co-administration",
        "mechanism": "Ibuprofen displaces warfarin from albumin binding sites, inhibits platelet aggregation, and induces gastric mucosal ulceration, dramatically increasing active bleeding risk.",
        "action": "Avoid systemic NSAIDs in patients taking Warfarin. Substitute with Paracetamol (up to 2000mg/day) or topical analgesics for pain management."
    },
    {
        "pair": ("Warfarin", "Naproxen"),
        "severity": "High",
        "title": "Major Bleeding Risk from Anticoagulant + NSAID Co-administration",
        "mechanism": "Naproxen displaces warfarin from plasma protein binding sites, inhibits platelet aggregation, and promotes gastric mucosal injury, dramatically elevating the risk of severe gastrointestinal bleeding and systemic hemorrhage.",
        "action": "Avoid systemic NSAIDs including Naproxen in patients taking Warfarin. Substitute with Paracetamol (up to 2000mg/day) or consult for alternative pain management."
    },
    {
        "pair": ("Lisinopril", "Spironolactone"),
        "severity": "High",
        "title": "Severe Hyperkalemia & Arrhythmia Hazard",
        "mechanism": "Both ACE inhibitors (Lisinopril) and potassium-sparing diuretics (Spironolactone) reduce renal aldosterone-dependent potassium excretion, triggering life-threatening hyperkalemia (>5.5 mmol/L) and fatal cardiac arrhythmias.",
        "action": "Avoid concurrent use or verify strict indications (e.g. low-dose HFrEF). If co-prescribed, check serum potassium and creatinine within 1-2 weeks and discontinue potassium supplements."
    },
    {
        "pair": ("Simvastatin", "Clarithromycin"),
        "severity": "High",
        "title": "CYP3A4 Inhibition Causing Severe Rhabdomyolysis",
        "mechanism": "Clarithromycin is a potent CYP3A4 enzyme inhibitor that blocks hepatic metabolism of Simvastatin, leading to up to a 10-fold increase in statin plasma levels and precipitating acute rhabdomyolysis and renal failure.",
        "action": "Temporarily suspend Simvastatin during the Clarithromycin antibiotic course, or switch antibiotic to Azithromycin which does not strongly inhibit CYP3A4."
    },
    {
        "pair": ("Sertraline", "Tramadol"),
        "severity": "High",
        "title": "Potential Serotonin Syndrome Hazard",
        "mechanism": "Sertraline inhibits serotonin reuptake, while Tramadol enhances serotonin release and inhibits reuptake. Concomitant use causes severe central serotonin accumulation, risking Serotonin Syndrome characterized by clonus, hyperthermia, autonomic instability, and delirium.",
        "action": "Avoid concurrent administration. If analgesia is required, use non-serotonergic analgesics (e.g., Paracetamol or short-term opioid without serotonergic properties under supervision)."
    },
    {
        "pair": ("Sildenafil", "Nitroglycerin"),
        "severity": "High",
        "title": "Profound Hypotension & Cardiovascular Collapse",
        "mechanism": "Nitrates generate nitric oxide to stimulate guanylyl cyclase, while Sildenafil inhibits PDE5 breakdown of cGMP. Together they cause uncontrolled cyclic-GMP accumulation, profound systemic vasodilation, refractory hypotension, and coronary hypoperfusion.",
        "action": "Absolute contraindication. Nitroglycerin must not be administered within 24 hours of Sildenafil (or 48 hours for Tadalafil)."
    },
    {
        "pair": ("Ibuprofen", "Aspirin"),
        "severity": "Medium",
        "title": "Diminished Cardioprotective Effect & Increased GI Toxicity",
        "mechanism": "Ibuprofen competitively blocks the access of Aspirin to the platelet COX-1 catalytic site, negating aspirin's irreversible cardioprotective platelet inhibition while compounding gastric mucosal erosion.",
        "action": "Do not co-prescribe regular NSAIDs with cardioprotective low-dose Aspirin. If an NSAID is necessary, take Aspirin at least 30 minutes before or 8 hours after Ibuprofen."
    },
    {
        "pair": ("Warfarin", "Apixaban"),
        "severity": "High",
        "title": "Dual Anticoagulation Overdose",
        "mechanism": "Prescribing two therapeutic anticoagulants simultaneously creates excessive systemic anticoagulation, drastically elevating risk of fatal hemorrhage without clinical justification.",
        "action": "Confirm anticoagulation transition protocol. One anticoagulant must be discontinued or properly bridged under strict clinical monitoring."
    }
]

# Drug-Disease Contraindication Rules
DRUG_DISEASE_RULES = [
    {
        "drug": "Propranolol",
        "condition_keywords": ["asthma", "bronchospasm", "copd", "chronic obstructive pulmonary disease", "reactive airway disease"],
        "severity": "High",
        "title": "Life-Threatening Bronchospasm in Reactive Airway Disease",
        "mechanism": "Propranolol is a non-selective beta-adrenergic antagonist (blocks both Beta-1 and Beta-2 receptors). Blockade of bronchial Beta-2 receptors induces severe bronchospasm and smooth muscle bronchoconstriction, which can trigger fatal status asthmaticus.",
        "action": "Strictly contraindicated in active asthma or severe COPD. Switch to a cardioselective beta-1 blocker (e.g., Metoprolol, Bisoprolol) with extreme caution, or preferably an alternative class (e.g. Amlodipine, ACE inhibitor)."
    },
    {
        "drug": "Ibuprofen",
        "condition_keywords": ["peptic ulcer", "gastric ulcer", "duodenal ulcer", "pud", "active gi bleed", "gastritis", "ulcerative colitis"],
        "severity": "High",
        "title": "Gastrointestinal Perforation & Hemorrhage Risk",
        "mechanism": "NSAIDs non-selectively inhibit COX-1 and COX-2 enzymes, preventing protective gastric prostaglandin synthesis (PGE2, PGI2) and reducing mucosal blood flow, leading to ulcer reactivation, severe GI bleeding, or perforation.",
        "action": "Contraindicated in active peptic ulcer disease or GI bleeding history. Use Paracetamol for mild pain or co-prescribe aggressive gastroprotection (PPI) only if non-NSAID options fail."
    },
    {
        "drug": "Naproxen",
        "condition_keywords": ["peptic ulcer", "gastric ulcer", "duodenal ulcer", "pud", "active gi bleed", "gastritis"],
        "severity": "High",
        "title": "Ulcer Reactivation & GI Bleeding Risk",
        "mechanism": "Systemic NSAID action strips gastric cytoprotective prostaglandin barriers, escalating risk of recurrent ulceration and gastrointestinal bleeding.",
        "action": "Avoid systemic NSAIDs in patients with peptic ulcer disease. Review alternative pain management therapies."
    },
    {
        "drug": "Aspirin",
        "condition_keywords": ["peptic ulcer", "gastric ulcer", "active gi bleed", "bleeding diathesis", "hemophilia"],
        "severity": "High",
        "title": "Aggravation of Active Ulceration and Bleeding",
        "mechanism": "Direct mucosal erosion combined with systemic irreversible platelet inhibition prevents primary hemostasis and risks massive gastrointestinal blood loss.",
        "action": "Avoid unless specifically indicated for urgent acute coronary syndrome; if required long-term, ensure gastroprotective PPI therapy."
    },
    {
        "drug": "Metformin",
        "condition_keywords": ["chronic kidney disease", "ckd", "renal impairment", "renal failure", "severe kidney disease", "end stage renal disease"],
        "severity": "High",
        "title": "Fatal Lactic Acidosis in Renal Impairment",
        "mechanism": "Metformin is cleared almost entirely via renal excretion. In renal dysfunction, metformin accumulates in plasma, inhibiting hepatic lactate uptake and gluconeogenesis, which precipitates life-threatening Metformin-Associated Lactic Acidosis (MALA).",
        "action": "Evaluate estimated glomerular filtration rate (eGFR). Metformin is contraindicated if eGFR < 30 mL/min/1.73m2 and requires dosage restriction if eGFR is 30-44 mL/min/1.73m2."
    },
    {
        "drug": "Lisinopril",
        "condition_keywords": ["pregnancy", "pregnant", "gestational"],
        "severity": "High",
        "title": "Teratogenic & Fetotoxic Hazard in Pregnancy",
        "mechanism": "ACE inhibitors cross the placenta and act directly on the fetal renin-angiotensin system, causing severe oligohydramnios, fetal renal agenesis, pulmonary hypoplasia, skeletal deformities, and neonatal death.",
        "action": "Contraindicated in 2nd and 3rd trimesters; strongly avoided in 1st trimester. Discontinue immediately upon pregnancy detection and replace with Labetalol, Nifedipine, or Methyldopa."
    },
    {
        "drug": "Enalapril",
        "condition_keywords": ["pregnancy", "pregnant", "gestational"],
        "severity": "High",
        "title": "Teratogenic & Fetotoxic Hazard in Pregnancy",
        "mechanism": "ACE inhibitors cross the placenta, causing profound fetal renal hypoperfusion, oligohydramnios, skull hypoplasia, and fetal demise.",
        "action": "Discontinue immediately. Switch to obstetric-safe antihypertensives (e.g. Labetalol, Methyldopa)."
    },
    {
        "drug": "Atorvastatin",
        "condition_keywords": ["active liver disease", "hepatitis", "cirrhosis", "acute liver failure"],
        "severity": "High",
        "title": "Hepatotoxicity Risk in Active Hepatic Disease",
        "mechanism": "Statins undergo extensive hepatic first-pass metabolism. In active liver impairment, drug clearance is reduced, exacerbating transaminase elevations and accelerating liver decompensation.",
        "action": "Contraindicated in active liver disease or unexplained persistently elevated transaminases. Measure baseline LFTs and consider non-statin lipid options."
    }
]

# Allergen Class to Drug Mapping
ALLERGEN_MAP = {
    "penicillin": ["Amoxicillin", "Augmentin", "Ampicillin", "Penicillin V", "Piperacillin", "Ticarcillin"],
    "beta-lactam": ["Amoxicillin", "Augmentin", "Ampicillin", "Penicillin V", "Cephalexin", "Cefuroxime"],
    "nsaid": ["Aspirin", "Ibuprofen", "Naproxen", "Ketorolac", "Diclofenac", "Celecoxib", "Meloxicam"],
    "aspirin": ["Aspirin"],
    "sulfa": ["Sulfamethoxazole", "Bactrim", "Sulfasalazine", "Celecoxib"],
    "opioid": ["Tramadol", "Morphine", "Codeine", "Oxycodone", "Fentanyl"],
    "statin": ["Simvastatin", "Atorvastatin", "Rosuvastatin", "Pravastatin"],
    "ace inhibitor": ["Lisinopril", "Enalapril", "Ramipril", "Captopril"]
}

# Pre-packaged Demo Scenarios for fast, one-click demonstration
DEMO_SCENARIOS = {
    "Scenario 1: Drug-Drug Interaction": {
        "title": "Drug-Drug Interaction (Warfarin + Aspirin)",
        "description": "Patient taking Warfarin is newly prescribed Aspirin 500mg BID. Triggers severe bleeding risk alert.",
        "patient": {
            "age": 62,
            "existing_meds": ["Warfarin"],
            "allergies": [],
            "conditions": ["Atrial Fibrillation"]
        },
        "prescriptions": [
            {
                "drug": "Aspirin",
                "dose": 500.0,
                "unit": "mg",
                "frequency": "Twice daily (BID)",
                "frequency_per_day": 2.0
            }
        ]
    },
    "Scenario 2: Drug-Disease Interaction": {
        "title": "Drug-Disease Interaction (Propranolol + Asthma)",
        "description": "Patient with Bronchial Asthma is newly prescribed non-selective beta blocker Propranolol 80mg. Triggers bronchospasm alert.",
        "patient": {
            "age": 38,
            "existing_meds": ["Albuterol"],
            "allergies": [],
            "conditions": ["Asthma", "Hypertension"]
        },
        "prescriptions": [
            {
                "drug": "Propranolol",
                "dose": 80.0,
                "unit": "mg",
                "frequency": "Twice daily (BID)",
                "frequency_per_day": 2.0
            }
        ]
    },
    "Scenario 3: Duplicate Medication": {
        "title": "Duplicate Medication (Lisinopril + Enalapril)",
        "description": "Patient on Lisinopril 10mg is prescribed Enalapril 20mg (therapeutic ACE inhibitor duplicate). Triggers therapeutic overlap alert.",
        "patient": {
            "age": 55,
            "existing_meds": ["Lisinopril", "Atorvastatin"],
            "allergies": [],
            "conditions": ["Hypertension", "Hyperlipidemia"]
        },
        "prescriptions": [
            {
                "drug": "Enalapril",
                "dose": 20.0,
                "unit": "mg",
                "frequency": "Once daily (QD)",
                "frequency_per_day": 1.0
            }
        ]
    },
    "Scenario 4: Incorrect Dosage": {
        "title": "Incorrect Dosage (Amoxicillin 4000mg/dose & Paracetamol Overdose)",
        "description": "Patient is prescribed Amoxicillin 4000mg single dose (max safe is 1000mg) and Paracetamol 2000mg QID (8000mg/day, max is 4000mg). Triggers multiple dosage ceiling alerts.",
        "patient": {
            "age": 42,
            "existing_meds": [],
            "allergies": [],
            "conditions": ["Acute Sinusitis", "Fever"]
        },
        "prescriptions": [
            {
                "drug": "Amoxicillin",
                "dose": 4000.0,
                "unit": "mg",
                "frequency": "Three times daily (TID)",
                "frequency_per_day": 3.0
            },
            {
                "drug": "Paracetamol",
                "dose": 2000.0,
                "unit": "mg",
                "frequency": "Four times daily (QID)",
                "frequency_per_day": 4.0
            }
        ]
    },
    "Scenario 5: Allergy Conflict": {
        "title": "Allergy Conflict (Penicillin Allergy + Amoxicillin)",
        "description": "Patient with documented Penicillin allergy is newly prescribed Amoxicillin 500mg. Triggers high severity anaphylaxis risk alert.",
        "patient": {
            "age": 29,
            "existing_meds": [],
            "allergies": ["Penicillin"],
            "conditions": ["Streptococcal Pharyngitis"]
        },
        "prescriptions": [
            {
                "drug": "Amoxicillin",
                "dose": 500.0,
                "unit": "mg",
                "frequency": "Three times daily (TID)",
                "frequency_per_day": 3.0
            }
        ]
    },
    "Scenario 6: Safe Prescription": {
        "title": "Safe Prescription (Metformin for Type 2 Diabetes)",
        "description": "Patient with newly diagnosed Type 2 Diabetes and Hypertension (on Amlodipine) is prescribed safe standard-dose Metformin 500mg. Triggers zero warnings.",
        "patient": {
            "age": 52,
            "existing_meds": ["Amlodipine"],
            "allergies": [],
            "conditions": ["Type 2 Diabetes", "Hypertension"]
        },
        "prescriptions": [
            {
                "drug": "Metformin",
                "dose": 500.0,
                "unit": "mg",
                "frequency": "Twice daily (BID)",
                "frequency_per_day": 2.0
            }
        ]
    }
}
