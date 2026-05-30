import json
import base64
import requests
import os
from config import Config

from repositories.api_log_repository import ApiLogRepository
from repositories.candidate_repository import (
    CandidateRepository
)
from repositories.api_log_repository import (
    ApiLogRepository
)
from repositories.verification_repository import (
    VerificationRepository
)


class RChilliService:

    @staticmethod
    def parse_resume(file_path, candidate_id):

        try:

            # ==========================================
            # CONVERT FILE TO BASE64
            # ==========================================

            with open(file_path, "rb") as file:

                file_bytes = file.read()

            encoded_file = base64.b64encode(
                file_bytes
            ).decode("utf-8")

            # ==========================================
            # REQUEST PAYLOAD
            # ==========================================

            payload = {

                "filedata": encoded_file,

                "filename": os.path.basename(file_path),

                "userkey": Config.RCHILLI_USER_KEY,

                "version": Config.RCHILLI_VERSION,

                "subuserid": Config.RCHILLI_SUBUSER_ID
            }

            headers = {

                "Content-Type": "application/json"
            }

            # ==========================================
            # API REQUEST
            # ==========================================

            response = requests.post(

                Config.RCHILLI_API_URL,

                headers=headers,

                json=payload,

                timeout=120
            )

            response_data = response.json()
            ApiLogRepository.save_log(
            provider_name="RChilli",
            api_name="Resume Parser",
            request_data=payload,
            response_data=response_data,
            status_code=response.status_code,
            status="SUCCESS"
            )
            # ==========================================
            # VALIDATE RESPONSE
            # ==========================================

            resume_data = response_data.get(
                "ResumeParserData"
            )

            if not resume_data:

                return {

                    "success": False,

                    "message": "RChilli parsing failed",

                    "provider_response": response_data
                }

            # ==========================================
            # NAME
            # ==========================================

            name_data = resume_data.get(
                "Name",
                {}
            )

            full_name = name_data.get(
                "FullName",
                ""
            )

            # ==========================================
            # EMAIL
            # ==========================================

            email = ""

            email_data = resume_data.get(
                "Email",
                []
            )

            if email_data:

                email = email_data[0].get(
                    "EmailAddress",
                    ""
                )

            # ==========================================
            # PHONE
            # ==========================================

            phone = ""

            phone_data = resume_data.get(
                "PhoneNumber",
                []
            )

            if phone_data:

                phone = phone_data[0].get(
                    "Number",
                    ""
                )

            # ==========================================
            # LINKEDIN
            # ==========================================

            linkedin = ""

            website_data = resume_data.get(
                "WebSite",
                []
            )

            for site in website_data:

                if site.get("Type") == "Linkedin":

                    linkedin = site.get(
                        "Url",
                        ""
                    )

            # ==========================================
            # ADDRESS
            # ==========================================

            city = ""
            state = ""
            country = ""

            address_data = resume_data.get(
                "Address",
                []
            )

            if address_data:

                address = address_data[0]

                city = address.get(
                    "City",
                    ""
                )

                state = address.get(
                    "State",
                    ""
                )

                country = address.get(
                    "Country",
                    ""
                )

            # ==========================================
            # EXPERIENCE
            # ==========================================

            worked_period = resume_data.get(
                "WorkedPeriod",
                {}
            )

            experience_years = worked_period.get(
                "TotalExperienceInYear",
                ""
            )

            current_company = resume_data.get(
                "CurrentEmployer",
                ""
            )

            designation = resume_data.get(
                "JobProfile",
                ""
            )

            # ==========================================
            # SKILLS
            # ==========================================

            skills = []

            skill_keywords = resume_data.get(
                "SkillKeywords",
                ""
            )

            if skill_keywords:

                skills = skill_keywords.split(",")

            # ==========================================
            # CANDIDATE PROFILE
            # ==========================================

            candidate_profile = {

                "full_name": full_name,

                "email": email,

                "phone": phone,

                "linkedin": linkedin,

                "city": city,

                "state": state,

                "country": country,

                "experience_years": (
                    experience_years
                ),

                "current_company": (
                    current_company
                ),

                "designation": designation,

                "skills": skills
            }

            # ==========================================
            # SAVE CANDIDATE
            # ==========================================

            CandidateRepository.save_candidate(
                candidate_profile
            )

            # ==========================================
            # SAVE RAW RESPONSE
            # ==========================================

            VerificationRepository.save_resume_raw_data(

                candidate_id=candidate_id,

                raw_data=json.dumps(
                    response_data
                )
            )

            # ==========================================
            # FINAL RESPONSE
            # ==========================================

            return {

                "success": True,

                "candidate_id": candidate_id,

                "candidate_profile": (
                    candidate_profile
                ),

                "raw_data": response_data
            }

        except Exception as e:
            ApiLogRepository.save_log(

                provider_name="RChilli",

                api_name="Resume Parser",

                request_data={},

                response_data=str(e),

                status_code=500,

                status="FAILED"
            )

            return {

                "success": False,

                "message": "Resume parsing failed",

                "error": str(e)
            }