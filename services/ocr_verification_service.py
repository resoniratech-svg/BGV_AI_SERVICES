import re


def normalize_text(text):
    return text.strip().upper()


def verify_pan_fields(extracted_data, expected_data):

    score = 0
    total = 3

    results = {}

    # =========================
    # NAME MATCH
    # =========================
    extracted_name = normalize_text(
        extracted_data.get("candidate_name", "")
    )

    expected_name = normalize_text(
        expected_data.get("candidate_name", "")
    )

    name_match = extracted_name == expected_name

    results["name_match"] = name_match

    if name_match:
        score += 1

    # =========================
    # PAN MATCH
    # =========================
    extracted_pan = normalize_text(
        extracted_data.get("pan_number", "")
    )

    expected_pan = normalize_text(
        expected_data.get("pan_number", "")
    )

    pan_match = extracted_pan == expected_pan

    results["pan_match"] = pan_match

    if pan_match:
        score += 1

    # =========================
    # DOB MATCH
    # =========================
    extracted_dob = normalize_text(
        extracted_data.get("dob", "")
    )

    expected_dob = normalize_text(
        expected_data.get("dob", "")
    )

    dob_match = extracted_dob == expected_dob

    results["dob_match"] = dob_match

    if dob_match:
        score += 1

    # =========================
    # FINAL SCORE
    # =========================
    match_score = int((score / total) * 100)

    verification_status = (
        "VERIFIED"
        if match_score >= 80
        else "MISMATCH"
    )

    return {
        "verification_status": verification_status,
        "match_score": match_score,
        "fields": results
    }