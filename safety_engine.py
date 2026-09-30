"""
Safety Engine for AI-Based Medication Error & Interaction Detection
-------------------------------------------------------------------
Implements 5 core safety check modules:
1. Drug-Drug Interactions
2. Drug-Disease Interactions
3. Duplicate Medications & Therapeutic Overlaps
4. Incorrect Dosage (Single, Daily, and Geriatric thresholds)
5. Allergy Conflicts

All warnings include:
- Risk category
- Severity (High / Medium / Low)
- Medicines or condition involved
- What was detected
- WHY it may be a risk (clinical mechanism)
- Suggested action for healthcare professional review
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set, Tuple
from knowledge_base import (
    DEMO_DRUGS,
    DRUG_DRUG_RULES,
    DRUG_DISEASE_RULES,
    ALLERGEN_MAP,
)


@dataclass
class PrescriptionItem:
    drug_name: str
    dose_amount: float
    dose_unit: str = "mg"
    frequency_label: str = "Once daily (QD)"
    frequency_per_day: float = 1.0


@dataclass
class PatientProfile:
    age: int
    existing_meds: List[str] = field(default_factory=list)
    allergies: List[str] = field(default_factory=list)
    conditions: List[str] = field(default_factory=list)


@dataclass
class SafetyAlert:
    risk_category: str  # "Drug-Drug Interaction", "Drug-Disease Interaction", etc.
    severity: str       # "High", "Medium", "Low"
    items_involved: str # E.g. "Warfarin + Aspirin" or "Propranolol & Asthma"
    detected_issue: str # What was detected
    clinical_risk: str  # WHY it may be a risk
    suggested_action: str # Action for healthcare professional to review


def normalize_drug_name(name: str) -> str:
    """Finds the canonical drug name in DEMO_DRUGS by direct name or alias match."""
    if not name:
        return ""
    clean = name.strip()
    clean_lower = clean.lower()

    # Exact key match (case-insensitive)
    for canonical in DEMO_DRUGS:
        if canonical.lower() == clean_lower:
            return canonical

    # Alias search
    for canonical, data in DEMO_DRUGS.items():
        aliases = [a.lower() for a in data.get("aliases", [])]
        if clean_lower in aliases:
            return canonical
        # Substring alias match if word boundary matches
        for alias in aliases:
            if clean_lower == alias or f" {clean_lower} " in f" {alias} ":
                return canonical

    return clean.capitalize()


def get_drug_info(drug_name: str) -> Optional[Dict[str, Any]]:
    """Retrieves drug metadata from DEMO_DRUGS if known."""
    canonical = normalize_drug_name(drug_name)
    return DEMO_DRUGS.get(canonical)


class MedicationSafetyEngine:
    """Core rule-based clinical safety checking engine."""

    def __init__(self):
        self.drugs_kb = DEMO_DRUGS
        self.dd_rules = DRUG_DRUG_RULES
        self.disease_rules = DRUG_DISEASE_RULES
        self.allergen_map = ALLERGEN_MAP

    def analyze(
        self,
        patient: PatientProfile,
        prescriptions: List[PrescriptionItem]
    ) -> List[SafetyAlert]:
        """Runs all 5 safety check categories and returns aggregated alerts."""
        alerts: List[SafetyAlert] = []

        if not prescriptions:
            return alerts

        # 1. Allergy Conflicts
        alerts.extend(self.check_allergies(patient.allergies, prescriptions))

        # 2. Duplicate Medications & Class Overlaps
        alerts.extend(self.check_duplicates(patient.existing_meds, prescriptions))

        # 3. Drug-Drug Interactions
        alerts.extend(self.check_drug_interactions(patient.existing_meds, prescriptions))

        # 4. Drug-Disease Interactions
        alerts.extend(self.check_drug_diseases(patient.conditions, prescriptions))

        # 5. Dosage Errors
        alerts.extend(self.check_dosages(patient.age, prescriptions))

        # Sort alerts: High -> Medium -> Low
        severity_order = {"High": 0, "Medium": 1, "Low": 2}
        alerts.sort(key=lambda a: severity_order.get(a.severity, 3))

        return alerts

    def check_allergies(
        self,
        patient_allergies: List[str],
        prescriptions: List[PrescriptionItem]
    ) -> List[SafetyAlert]:
        """Checks if any prescribed medication conflicts with known patient allergies."""
        alerts: List[SafetyAlert] = []
        if not patient_allergies or not prescriptions:
            return alerts

        normalized_allergies = [a.strip().lower() for a in patient_allergies if a.strip()]

        for rx in prescriptions:
            canonical_rx = normalize_drug_name(rx.drug_name)
            rx_info = get_drug_info(canonical_rx)
            rx_lower = canonical_rx.lower()

            # Gather all allergen tags for this drug
            allergen_tags: Set[str] = {rx_lower}
            if rx_info:
                for tag in rx_info.get("allergen_classes", []):
                    allergen_tags.add(tag.lower())

            for allergy in normalized_allergies:
                matched = False
                matched_reason = ""

                # Direct match
                if allergy in allergen_tags:
                    matched = True
                    matched_reason = f"Prescribed drug '{canonical_rx}' matches documented allergy to '{allergy.capitalize()}'."

                # Allergen map check (e.g. patient allergic to penicillin -> amoxicillin)
                if not matched:
                    for map_key, mapped_drugs in self.allergen_map.items():
                        if allergy == map_key or map_key in allergy:
                            if any(normalize_drug_name(d).lower() == rx_lower for d in mapped_drugs):
                                matched = True
                                matched_reason = (
                                    f"Prescribed drug '{canonical_rx}' belongs to allergen family "
                                    f"'{map_key.capitalize()}', conflicting with patient's documented allergy '{allergy.capitalize()}'."
                                )
                                break

                # Reverse check: allergy in drug aliases
                if not matched and rx_info:
                    for alias in rx_info.get("aliases", []):
                        if allergy == alias.lower() or alias.lower() in allergy:
                            matched = True
                            matched_reason = f"Prescribed drug '{canonical_rx}' ({alias}) conflicts with documented allergy to '{allergy.capitalize()}'."
                            break

                if matched:
                    alerts.append(
                        SafetyAlert(
                            risk_category="Allergy Conflict",
                            severity="High",
                            items_involved=f"{canonical_rx} ↔ Allergy: {allergy.capitalize()}",
                            detected_issue=f"Severe allergy contraindication: {matched_reason}",
                            clinical_risk=(
                                f"Administering {canonical_rx} to an allergic patient risks severe immune-mediated "
                                "hypersensitivity reactions including acute anaphylaxis, bronchospasm, urticaria, "
                                "angioedema, and hemodynamic shock."
                            ),
                            suggested_action=(
                                f"STOP {canonical_rx} administration immediately. Verify patient allergy history and "
                                "select an alternative therapeutic class without cross-reactivity."
                            )
                        )
                    )

        return alerts

    def check_duplicates(
        self,
        existing_meds: List[str],
        prescriptions: List[PrescriptionItem]
    ) -> List[SafetyAlert]:
        """Detects identical drug duplications and therapeutic class redundancy."""
        alerts: List[SafetyAlert] = []

        all_rx_canonical: List[Tuple[str, PrescriptionItem]] = [
            (normalize_drug_name(p.drug_name), p) for p in prescriptions
        ]
        all_existing_canonical: List[str] = [
            normalize_drug_name(m) for m in existing_meds if m.strip()
        ]

        # 1. Exact Duplicate: Prescribed vs Existing
        for canon_rx, rx_item in all_rx_canonical:
            if canon_rx in all_existing_canonical:
                alerts.append(
                    SafetyAlert(
                        risk_category="Duplicate Medication",
                        severity="High",
                        items_involved=f"{canon_rx} (Prescribed) & {canon_rx} (Existing Active)",
                        detected_issue=f"Exact duplicate medication detected: '{canon_rx}' is already on the patient's active medication list.",
                        clinical_risk=(
                            f"Prescribing '{canon_rx}' while the patient is already taking it risks accidental dual-dosing, "
                            "supratherapeutic blood levels, and dose-dependent organ toxicity or adverse drug reactions."
                        ),
                        suggested_action=(
                            f"Verify whether this is an intentional dose modification for '{canon_rx}'. "
                            "If updating the regimen, explicitly reconcile and discontinue the existing order."
                        )
                    )
                )

        # 2. Exact Duplicate: Within Prescriptions list
        seen_rx: Dict[str, PrescriptionItem] = {}
        for canon_rx, rx_item in all_rx_canonical:
            if canon_rx in seen_rx:
                alerts.append(
                    SafetyAlert(
                        risk_category="Duplicate Medication",
                        severity="High",
                        items_involved=f"{canon_rx} (Repeated in order)",
                        detected_issue=f"Multiple orders for identical active ingredient: '{canon_rx}' appears more than once in this prescription.",
                        clinical_risk=(
                            f"Concurrent duplicate orders for '{canon_rx}' will result in cumulative overdosing."
                        ),
                        suggested_action=f"Consolidate multiple orders of '{canon_rx}' into a single intended dosage and frequency."
                    )
                )
            else:
                seen_rx[canon_rx] = rx_item

        # 3. Therapeutic Class Overlap
        # Build comprehensive list of (drug_name, class, source)
        full_list: List[Tuple[str, str, str]] = []
        for canon_rx, rx_item in all_rx_canonical:
            info = get_drug_info(canon_rx)
            if info and "class" in info:
                full_list.append((canon_rx, info["class"], "Prescribed"))

        for canon_exist in all_existing_canonical:
            info = get_drug_info(canon_exist)
            if info and "class" in info:
                full_list.append((canon_exist, info["class"], "Existing"))

        # Check pairs for class equivalence
        detected_pairs: Set[Tuple[str, str]] = set()
        for i in range(len(full_list)):
            for j in range(i + 1, len(full_list)):
                drug1, class1, src1 = full_list[i]
                drug2, class2, src2 = full_list[j]

                if drug1 == drug2:
                    continue  # Handled by exact duplicate check

                # Check if they share the same base class
                # Normalize classes (e.g. "ACE Inhibitor", "NSAID", "Statin", "Beta Blocker")
                base_classes = [
                    "NSAID",
                    "ACE Inhibitor",
                    "HMG-CoA Reductase Inhibitor (Statin)",
                    "Beta Blocker",
                    "Oral Anticoagulant",
                    "Direct Oral Anticoagulant (DOAC)",
                    "Penicillin Antibiotic"
                ]

                matched_class = None
                for bc in base_classes:
                    if bc.lower() in class1.lower() and bc.lower() in class2.lower():
                        matched_class = bc
                        break

                if matched_class:
                    pair_key = tuple(sorted([drug1, drug2]))
                    if pair_key not in detected_pairs:
                        detected_pairs.add(pair_key)
                        alerts.append(
                            SafetyAlert(
                                risk_category="Duplicate Medication",
                                severity="Medium",
                                items_involved=f"{drug1} ({src1}) & {drug2} ({src2})",
                                detected_issue=(
                                    f"Therapeutic class duplication: Both '{drug1}' and '{drug2}' are members of the "
                                    f"'{matched_class}' therapeutic class."
                                ),
                                clinical_risk=(
                                    f"Concurrent administration of two agents from the same therapeutic class ({matched_class}) "
                                    "rarely offers additional therapeutic efficacy but significantly increases cumulative toxicity, "
                                    "organ strain, and adverse event incidence."
                                ),
                                suggested_action=(
                                    f"Review clinical rationale for dual {matched_class} therapy. Select a single optimal agent "
                                    "or adjust dose rather than prescribing redundant pharmacotherapy."
                                )
                            )
                        )

        return alerts

    def check_drug_interactions(
        self,
        existing_meds: List[str],
        prescriptions: List[PrescriptionItem]
    ) -> List[SafetyAlert]:
        """Detects potentially hazardous drug-drug interactions between all active medicines."""
        alerts: List[SafetyAlert] = []

        all_drugs_canonical: List[Tuple[str, str]] = []  # (canonical_name, source)
        for rx in prescriptions:
            all_drugs_canonical.append((normalize_drug_name(rx.drug_name), "Prescribed"))
        for ex in existing_meds:
            if ex.strip():
                all_drugs_canonical.append((normalize_drug_name(ex), "Existing"))

        seen_rules: Set[Tuple[str, str]] = set()

        for i in range(len(all_drugs_canonical)):
            for j in range(i + 1, len(all_drugs_canonical)):
                d1, src1 = all_drugs_canonical[i]
                d2, src2 = all_drugs_canonical[j]

                # Match against defined interaction rules
                for rule in self.dd_rules:
                    pair = rule["pair"]
                    p1_canon = normalize_drug_name(pair[0])
                    p2_canon = normalize_drug_name(pair[1])

                    pair_match = (
                        (d1.lower() == p1_canon.lower() and d2.lower() == p2_canon.lower()) or
                        (d1.lower() == p2_canon.lower() and d2.lower() == p1_canon.lower())
                    )

                    if pair_match:
                        interaction_key = tuple(sorted([d1, d2]))
                        if interaction_key not in seen_rules:
                            seen_rules.add(interaction_key)
                            alerts.append(
                                SafetyAlert(
                                    risk_category="Drug-Drug Interaction",
                                    severity=rule["severity"],
                                    items_involved=f"{d1} ({src1}) + {d2} ({src2})",
                                    detected_issue=f"{rule['title']} between {d1} and {d2}.",
                                    clinical_risk=rule["mechanism"],
                                    suggested_action=rule["action"]
                                )
                            )

                # Class-level check for Warfarin + Any NSAID (Aspirin, Ibuprofen, Naproxen, etc.)
                interaction_key = tuple(sorted([d1, d2]))
                if interaction_key not in seen_rules:
                    is_warfarin_1 = d1.lower() == "warfarin"
                    is_warfarin_2 = d2.lower() == "warfarin"
                    info1 = get_drug_info(d1)
                    info2 = get_drug_info(d2)
                    is_nsaid_1 = bool(info1 and "nsaid" in info1.get("class", "").lower())
                    is_nsaid_2 = bool(info2 and "nsaid" in info2.get("class", "").lower())

                    if (is_warfarin_1 and is_nsaid_2) or (is_warfarin_2 and is_nsaid_1):
                        nsaid_name = d2 if is_warfarin_1 else d1
                        seen_rules.add(interaction_key)
                        alerts.append(
                            SafetyAlert(
                                risk_category="Drug-Drug Interaction",
                                severity="High",
                                items_involved=f"{d1} ({src1}) + {d2} ({src2})",
                                detected_issue=f"Major Bleeding Risk from Anticoagulant + NSAID Co-administration between Warfarin and {nsaid_name}.",
                                clinical_risk=(
                                    f"{nsaid_name} (NSAID) impairs platelet aggregation, displaces Warfarin from plasma binding sites, "
                                    "and damages gastric mucosa, dramatically escalating risk of severe internal bleeding and GI hemorrhage."
                                ),
                                suggested_action=(
                                    f"Avoid co-prescribing {nsaid_name} with Warfarin. Consider non-interacting analgesics like "
                                    "Paracetamol (up to 2000mg/day) or consult for alternative pain management under close INR monitoring."
                                )
                            )
                        )

        return alerts

    def check_drug_diseases(
        self,
        conditions: List[str],
        prescriptions: List[PrescriptionItem]
    ) -> List[SafetyAlert]:
        """Detects drug-disease contraindications between prescribed medicines and patient diseases."""
        alerts: List[SafetyAlert] = []
        if not conditions or not prescriptions:
            return alerts

        normalized_conditions = [c.strip().lower() for c in conditions if c.strip()]

        for rx in prescriptions:
            canon_rx = normalize_drug_name(rx.drug_name)

            for rule in self.disease_rules:
                rule_drug = normalize_drug_name(rule["drug"])
                if canon_rx.lower() == rule_drug.lower():
                    # Check condition keywords
                    for cond in normalized_conditions:
                        matched = any(kw in cond for kw in rule["condition_keywords"])
                        if matched:
                            alerts.append(
                                SafetyAlert(
                                    risk_category="Drug-Disease Interaction",
                                    severity=rule["severity"],
                                    items_involved=f"{canon_rx} & Condition: {cond.title()}",
                                    detected_issue=f"Contraindicated in patient condition: {rule['title']}",
                                    clinical_risk=rule["mechanism"],
                                    suggested_action=rule["action"]
                                )
                            )
                            break  # Avoid duplicate alerts for same rule/drug

        return alerts

    def check_dosages(
        self,
        patient_age: int,
        prescriptions: List[PrescriptionItem]
    ) -> List[SafetyAlert]:
        """Validates prescribed single dose and daily cumulative dose against defined demonstration limits."""
        alerts: List[SafetyAlert] = []

        for rx in prescriptions:
            canon_rx = normalize_drug_name(rx.drug_name)
            info = get_drug_info(canon_rx)

            # Check for non-positive dose
            if rx.dose_amount <= 0:
                alerts.append(
                    SafetyAlert(
                        risk_category="Incorrect Dosage",
                        severity="Medium",
                        items_involved=f"{canon_rx} ({rx.dose_amount} {rx.dose_unit})",
                        detected_issue=f"Non-therapeutic or zero dosage specified: {rx.dose_amount} {rx.dose_unit}.",
                        clinical_risk="A dose of zero or a negative value provides zero therapeutic efficacy and indicates a prescription entry error.",
                        suggested_action="Review and enter a valid therapeutic dose amount."
                    )
                )
                continue

            if not info:
                # If drug not in demonstration rules, skip dosage limit checks
                continue

            max_single = info.get("max_single_dose_mg")
            max_daily = info.get("max_daily_dose_mg")
            geriatric_daily = info.get("geriatric_max_daily_dose_mg")

            # 1. Single Dose Check
            if max_single and rx.dose_amount > max_single:
                alerts.append(
                    SafetyAlert(
                        risk_category="Incorrect Dosage",
                        severity="High",
                        items_involved=f"{canon_rx} (Prescribed: {rx.dose_amount:g} mg per dose)",
                        detected_issue=(
                            f"Single dose of {canon_rx} ({rx.dose_amount:g} mg) exceeds maximum recommended single dose limit "
                            f"of {max_single:g} mg."
                        ),
                        clinical_risk=(
                            f"Supratherapeutic single doses of {canon_rx} drastically spike peak serum concentrations (Cmax), "
                            "substantially elevating acute toxicity, cardiovascular or gastrointestinal adverse reactions, "
                            "and organ strain."
                        ),
                        suggested_action=(
                            f"Reduce single dose of {canon_rx} to at or below the recommended maximum threshold of {max_single:g} mg."
                        )
                    )
                )

            # Calculate total daily dose
            total_daily = rx.dose_amount * (rx.frequency_per_day if rx.frequency_per_day > 0 else 1.0)

            # 2. Maximum Daily Dose Check
            if max_daily and total_daily > max_daily:
                alerts.append(
                    SafetyAlert(
                        risk_category="Incorrect Dosage",
                        severity="High",
                        items_involved=f"{canon_rx} (Cumulative: {total_daily:g} mg/day)",
                        detected_issue=(
                            f"Cumulative daily dose of {canon_rx} ({total_daily:g} mg/day) exceeds maximum daily ceiling "
                            f"of {max_daily:g} mg/day (Prescribed: {rx.dose_amount:g} mg × {rx.frequency_label})."
                        ),
                        clinical_risk=(
                            f"Cumulative daily exposure beyond {max_daily:g} mg leads to drug accumulation, saturation of clearance "
                            "pathways, and high incidence of severe systemic toxicity (e.g. hepatotoxicity for paracetamol, "
                            "bleeding for NSAIDs/anticoagulants)."
                        ),
                        suggested_action=(
                            f"Reduce daily administration frequency or single dose so total daily dose does not exceed {max_daily:g} mg/day."
                        )
                    )
                )

            # 3. Geriatric Dosage Check (Age >= 65)
            if patient_age >= 65 and geriatric_daily and total_daily > geriatric_daily and total_daily <= (max_daily or float("inf")):
                alerts.append(
                    SafetyAlert(
                        risk_category="Incorrect Dosage",
                        severity="Medium",
                        items_involved=f"{canon_rx} in Elderly Patient (Age: {patient_age})",
                        detected_issue=(
                            f"Daily dose of {canon_rx} ({total_daily:g} mg/day) exceeds recommended geriatric safety threshold "
                            f"of {geriatric_daily:g} mg/day for patients aged 65 and older."
                        ),
                        clinical_risk=(
                            f"Elderly patients exhibit age-related physiological declines in renal clearance, hepatic metabolism, "
                            "and increased receptor sensitivity. Standard adult doses frequently result in unintended toxic drug accumulation."
                        ),
                        suggested_action=(
                            f"Apply geriatric dosing guidelines for {canon_rx}: titrate cautiously and target a maximum "
                            f"maintenance dose of {geriatric_daily:g} mg/day. Monitor renal function and clinical tolerability."
                        )
                    )
                )

        return alerts
