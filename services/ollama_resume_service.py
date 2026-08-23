import os
import json
import re
import fitz
import traceback
from ollama import chat
from dateutil.parser import parse
from repositories.candidate_repository import CandidateRepository


class OllamaResumeService:
    @staticmethod
    def parse_resume(file_path, candidate_id):
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()

        print("\nRESUME TEXT")
        print(text)

        # Precise Regex Extractions
        email_matches = re.findall(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text
        )

        phone_matches = re.findall(r"(?:\+91[- ]?)?[6789]\d{9}", text)

        linkedin_matches = re.findall(r"https?://(?:www\.)?linkedin\.com/in/\S+", text)

        github_matches = re.findall(r"https?://(?:www\.)?github\.com/\S+", text)

        lines = [line.strip() for line in text.splitlines() if line.strip()]

        # ==========================================
        # NAME FALLBACK EXTRACTION (Improved)
        # ==========================================
        candidate_name = ""
        for line in lines[:10]:
            line = line.strip()
            if (
                len(line.split()) >= 2
                and len(line) < 40
                and "@" not in line
                and "|" not in line
                and not any(c.isdigit() for c in line)
            ):
                candidate_name = line
                break
        print(candidate_name)

        # ==========================================
        # DETERMINISTIC SKILLS EXTRACTION (Section-Agnostic)
        # ==========================================
        skills = []
        skill_sections = [
            "Programming Languages",
            "Programming and Data",
            "Web Technologies",
            "Front End Development",
            "Back - End Development",
            "Database Systems",
            "Tools",
        ]

        for line in lines:
            for section in skill_sections:
                if section in line:
                    if ":" in line:
                        parts = line.split(":", 1)
                        skills.extend(parts[1].split(","))
                    break

        skills = list(set([s.strip() for s in skills if s.strip()]))

        # Schema Prompt
        prompt = f"""
Extract information from the resume.

Rules:

1.Return ONLY valid JSON.
2.Never hallucinate.
3.If field missing use "".
4.If list missing use [].
5.Do not explain anything.
6.Extract languages.
7.Extract achievements.
8.Extract interests.
9.Extract certifications.
10.Extract portfolio url.
11.Extract city,state,country.


Schema


{{
"name":"",
"email":"",
"phone":"",
"linkedin":"",
"github":"",
"portfolio":"",
"city":"",
"state":"",
"country":"",

"skills":[],

"education":[],

"experience":[],

"projects":[],

"certifications":[],

"achievements":[],

"languages":[],

"interests":[]

}}



Resume


{text}



Return ONLY JSON

"""

        print("\nCALLING QWEN\n")

        # 10. System prompt added
        response = chat(
            model="qwen3:14b",
            messages=[
                {
                    "role": "system",
                    "content": """
You are a resume parser.

Return only valid JSON.

Never explain.

Never use markdown.

Never use code blocks.
""",
                },
                {"role": "user", "content": prompt},
            ],
        )

        print("\nQWEN FINISHED\n")

        content = response["message"]["content"]
        print("QWEN RESPONSE:")
        print(content)

        # Clean up output formatting
        content = content.replace("```json", "")
        content = content.replace("```", "")
        re_pattern = re.compile(r"<think>.*?</think>", re.S)
        content = re.sub(re_pattern, "", content)

        match = re.search(r"\{.*\}", content, re.S)

        if not match:
            return {
                "success": False,
                "message": "No JSON found",
                "raw_response": content,
            }

        json_text = match.group()

        try:
            parsed = json.loads(json_text)

            # 2. Regex fallback additions
            parsed["email"] = parsed.get("email") or (
                email_matches[0] if email_matches else ""
            )
            parsed["phone"] = parsed.get("phone") or (
                phone_matches[0] if phone_matches else ""
            )
            parsed["linkedin"] = parsed.get("linkedin") or (
                linkedin_matches[0] if linkedin_matches else ""
            )
            parsed["github"] = parsed.get("github") or (
                github_matches[0] if github_matches else ""
            )
            parsed["name"] = parsed.get("name") or candidate_name

            # 3. Add missing defaults even when JSON is valid
            parsed.setdefault("certifications", [])
            parsed.setdefault("achievements", [])
            parsed.setdefault("languages", [])
            parsed.setdefault("interests", [])
            parsed.setdefault("education", [])
            parsed.setdefault("experience", [])
            parsed.setdefault("projects", [])
            parsed.setdefault("skills", [])
            parsed.setdefault("portfolio", "")
            parsed.setdefault("city", "")
            parsed.setdefault("state", "")
            parsed.setdefault("country", "")

        except Exception:
            print()
            print("INVALID JSON FROM QWEN")
            print(json_text)

            parsed = {}
            parsed["name"] = candidate_name
            parsed["email"] = email_matches[0] if email_matches else ""
            parsed["phone"] = phone_matches[0] if phone_matches else ""
            parsed["linkedin"] = linkedin_matches[0] if linkedin_matches else ""
            parsed["github"] = github_matches[0] if github_matches else ""
            parsed["skills"] = skills
            parsed["education"] = []
            parsed["experience"] = []
            parsed["projects"] = []
            parsed["certifications"] = []
            parsed["achievements"] = []
            parsed["languages"] = []
            parsed["interests"] = []
            parsed["portfolio"] = ""
            parsed["city"] = ""
            parsed["state"] = ""
            parsed["country"] = ""

        print()
        print("FINAL JSON")
        print(json.dumps(parsed, indent=4))

        # -----------------------------------------------------------------
        # Range-Based Date String Math Engine
        # -----------------------------------------------------------------
        experience_list = parsed.get("experience", [])
        experience_months = 0

        for item in experience_list:
            try:
                # 4. Handle multiple dash formats and standard variations
                date_string = item.get("dates", "")
                date_string = date_string.replace("–", "-")
                date_string = date_string.replace("to", "-")

                if "-" not in date_string:
                    continue

                start, end = date_string.split("-", 1)

                s = parse(start.strip())
                e = parse(end.strip())

                months = (e.year - s.year) * 12
                months += e.month - s.month
                experience_months += months
            except:
                pass

        experience_years = round(experience_months / 12, 1)

        # -----------------------------------------------------------------
        # Priority-based Highest Qualification Parser
        # -----------------------------------------------------------------
        education = parsed.get("education", [])
        priority = [
            "PhD",
            "M.Tech",
            "MBA",
            "B.Tech",
            "B.E",
            "BSc",
            "PUC",
            "Intermediate",
        ]

        highest = ""
        for p in priority:
            for item in education:
                if p.lower() in item.get("degree", "").lower():
                    highest = item["degree"]
                    break
            if highest:
                break

        # 8. Qualification Fallback
        if not highest and education:
            highest = education[0].get("degree", "")

        highest_qualification = highest

        # -----------------------------------------------------------------
        # Extract Current Employer Variables
        # -----------------------------------------------------------------
        company = ""
        designation = ""

        if experience_list:
            latest = experience_list[-1]
            company = latest.get("company", "")
            # 5. Adjusted title key to position mapping
            designation = latest.get("position", "")

        # 9. Dynamic Resume Scoring Math Engine
        score = 100
        if not parsed.get("email"):
            score -= 10
        if not parsed.get("phone"):
            score -= 10
        if not parsed.get("education"):
            score -= 10
        if not parsed.get("skills"):
            score -= 10

        # -----------------------------------------------------------------
        # Extended Profile Data Payload Map
        # -----------------------------------------------------------------
        candidate_profile = {
            "candidate_id": candidate_id,
            "full_name": parsed.get("name", ""),
            "email": parsed.get("email", ""),
            "phone": parsed.get("phone", ""),
            "linkedin": parsed.get("linkedin", ""),
            "github_url": parsed.get("github", ""),
            "portfolio_url": parsed.get("portfolio", ""),
            "city": parsed.get("city", ""),
            "state": parsed.get("state", ""),
            "country": parsed.get("country", ""),
            # 6. Handled parsing as lists; database layer maps it to CSV formatting string
            "skills": parsed.get("skills", []),
            "experience_years": experience_years,
            "total_experience_months": experience_months,
            "highest_qualification": highest_qualification,
            "current_location": "",
            "preferred_location": "",
            "resume_file_name": os.path.basename(file_path),
            "resume_score": score,
            "current_company": company,
            "designation": designation,
            "education": json.dumps(parsed.get("education", [])),
            "experience": json.dumps(parsed.get("experience", [])),
            "projects": json.dumps(parsed.get("projects", [])),
            "certifications": json.dumps(parsed.get("certifications", [])),
            "achievements": json.dumps(parsed.get("achievements", [])),
            "languages": json.dumps(parsed.get("languages", [])),
            "interests": json.dumps(parsed.get("interests", [])),
            # 7. Serialized structured dataset preserving safe encoding format
            "parsed_json": json.dumps(parsed, ensure_ascii=False),
            "raw_resume_text": text,
        }

        # Complete serialized debug prints right before candidate storage write
        print()
        print("FINAL PARSED JSON")
        print(json.dumps(parsed, indent=4))

        print()
        print("FINAL PROFILE")
        print(json.dumps(candidate_profile, indent=4, default=str))

        saved = CandidateRepository.save_candidate(candidate_profile)
        if not saved:
            return {"success": False, "message": "Unable to save parsed candidate"}

        return {
            "success": True,
            "candidate_profile": candidate_profile,
            "raw_data": parsed,
        }
