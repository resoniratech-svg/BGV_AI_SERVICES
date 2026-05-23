import re


def parse_pan_details(text):

    result = {

        "pan_number": None,
        "candidate_name": None,
        "dob": None

    }

    # ==========================
    # PAN NUMBER
    # ==========================
    pan_pattern = r"[A-Z]{5}[0-9]{4}[A-Z]"

    pan_match = re.search(pan_pattern, text)

    if pan_match:

        result["pan_number"] = pan_match.group()


    # ==========================
    # DOB
    # ==========================
    dob_pattern = r"\d{2}/\d{2}/\d{4}"

    dob_match = re.search(dob_pattern, text)

    if dob_match:

        result["dob"] = dob_match.group()


    # ==========================
    # NAME EXTRACTION
    # ==========================
    lines = text.split("\n")

    cleaned_lines = [

        line.strip()

        for line in lines

        if len(line.strip()) > 3

    ]

    for i, line in enumerate(cleaned_lines):

        if "Name" in line or "NAME" in line:

            if i + 1 < len(cleaned_lines):

                result["candidate_name"] = cleaned_lines[i + 1]

                break

    return result
def parse_aadhaar_details(text):

    import re

    result = {

        "aadhaar_number": None,
        "candidate_name": None,
        "dob": None

    }

    # ==========================
    # Aadhaar Number
    # ==========================
    aadhaar_pattern = r"\d{4}\s\d{4}\s\d{4}"

    aadhaar_match = re.search(aadhaar_pattern, text)

    if aadhaar_match:

        result["aadhaar_number"] = aadhaar_match.group()


    # ==========================
    # DOB
    # ==========================
    dob_pattern = r"\d{2}/\d{2}/\d{4}"

    dob_match = re.search(dob_pattern, text)

    if dob_match:

        result["dob"] = dob_match.group()


    # ==========================
    # Candidate Name
    # ==========================
    lines = text.split("\n")

    cleaned_lines = [

        line.strip()

        for line in lines

        if len(line.strip()) > 3

    ]

    if len(cleaned_lines) >= 2:

        result["candidate_name"] = cleaned_lines[1]

    return result