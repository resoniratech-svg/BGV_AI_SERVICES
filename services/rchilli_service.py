import json
import base64
import requests
import os

from config import Config

from repositories.api_log_repository import (
    ApiLogRepository
)

from repositories.candidate_repository import (
    CandidateRepository
)

from repositories.verification_repository import (
    VerificationRepository
)


class RChilliService:

    @staticmethod
    def parse_resume(

        file_path,
        candidate_id
    ):

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

                "filename": os.path.basename(
                    file_path
                ),

                "userkey": (
                    Config.RCHILLI_USER_KEY
                ),

                "version": (
                    Config.RCHILLI_VERSION
                ),

                "subuserid": (
                    Config.RCHILLI_SUBUSER_ID
                )
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

            # ==========================================
            # SAVE API LOG
            # ==========================================

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
                "ResumeParserData",
                {}
            )

            if not isinstance(resume_data, dict):

                return {

                    "success": False,

                    "message": (
                        "Invalid RChilli response"
                    ),

                    "provider_response": (
                        response_data
                    )
                }

            if not resume_data:

                return {

                    "success": False,

                    "message": (
                        "RChilli parsing failed"
                    ),

                    "provider_response": (
                        response_data
                    )
                }

            # ==========================================
            # NAME
            # ==========================================

            name_data = resume_data.get(
                "Name",
                {}
            )

            if not isinstance(name_data, dict):

                name_data = {}

            full_name = str(

                name_data.get(
                    "FullName",
                    ""
                )

            ).strip()

            # ==========================================
            # EMAIL
            # ==========================================

            email = ""

            email_data = resume_data.get(
                "Email",
                []
            )

            if isinstance(email_data, list):

                for item in email_data:

                    if isinstance(item, dict):

                        email = str(

                            item.get(
                                "EmailAddress",
                                ""
                            )

                        ).strip()

                        if email:

                            break

            # ==========================================
            # PHONE
            # ==========================================

            phone = ""

            phone_data = resume_data.get(
                "PhoneNumber",
                []
            )

            if isinstance(phone_data, list):

                for item in phone_data:

                    if isinstance(item, dict):

                        phone = str(

                            item.get(
                                "FormattedNumber",
                                ""
                            )

                            or

                            item.get(
                                "Number",
                                ""
                            )

                        ).strip()

                        if phone:

                            break

            # ==========================================
            # WEBSITE DATA
            # ==========================================

            linkedin = ""
            github_url = ""
            portfolio_url = ""

            website_data = resume_data.get(
                "WebSite",
                []
            )

            if isinstance(website_data, list):

                for site in website_data:

                    if not isinstance(site, dict):

                        continue

                    site_url = str(

                        site.get(
                            "Url",
                            ""
                        )

                    ).strip()

                    if not site_url:

                        continue

                    lower_url = site_url.lower()

                    # ==========================================
                    # LINKEDIN
                    # ==========================================

                    if "linkedin.com" in lower_url:

                        linkedin = site_url

                    # ==========================================
                    # GITHUB
                    # ==========================================

                    elif "github.com" in lower_url:

                        github_url = site_url

                    # ==========================================
                    # PORTFOLIO
                    # ==========================================

                    elif (

                        "portfolio" in lower_url
                        or "behance.net" in lower_url
                        or "dribbble.com" in lower_url
                        or "netlify.app" in lower_url
                        or "vercel.app" in lower_url
                        or "wixsite.com" in lower_url
                        or "myportfolio.com" in lower_url
                        or "wordpress.com" in lower_url
                        or ".dev" in lower_url
                        or ".me" in lower_url

                    ):

                        portfolio_url = site_url

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

            if isinstance(address_data, list):

                for address in address_data:

                    if isinstance(address, dict):

                        city = str(

                            address.get(
                                "City",
                                ""
                            )

                        ).strip()

                        state = str(

                            address.get(
                                "State",
                                ""
                            )

                        ).strip()

                        country = str(

                            address.get(
                                "Country",
                                ""
                            )

                        ).strip()

                        if city:

                            break

            # ==========================================
            # CURRENT LOCATION
            # ==========================================

            current_location = ""

            current_location_data = resume_data.get(
                "CurrentLocation",
                []
            )

            if isinstance(current_location_data, list):

                for item in current_location_data:

                    if isinstance(item, dict):

                        current_location = str(

                            item.get(
                                "City",
                                ""
                            )

                        ).strip()

                        if current_location:

                            break

            if not current_location:

                current_location = city

            # ==========================================
            # PREFERRED LOCATION
            # ==========================================

            preferred_location = ""

            preferred_location_data = resume_data.get(
                "PreferredLocation",
                []
            )

            if isinstance(preferred_location_data, list):

                for item in preferred_location_data:

                    if isinstance(item, dict):

                        preferred_location = str(

                            item.get(
                                "City",
                                ""
                            )

                        ).strip()

                        if preferred_location:

                            break

            if not preferred_location:

                preferred_location = current_location

            # ==========================================
            # EXPERIENCE
            # ==========================================

            worked_period = resume_data.get(
                "WorkedPeriod",
                {}
            )

            if not isinstance(worked_period, dict):

                worked_period = {}

            experience_years = str(

                worked_period.get(
                    "TotalExperienceInYear",
                    ""
                )

            ).strip()

            total_experience_months = str(

                worked_period.get(
                    "TotalExperienceInMonths",
                    ""
                )

            ).strip()

            current_company = str(

                resume_data.get(
                    "CurrentEmployer",
                    ""
                )

            ).strip()

            # ==========================================
            # DESIGNATION
            # ==========================================

            designation = ""

            segregated_experience = resume_data.get(
                "SegregatedExperience",
                []
            )

            if isinstance(segregated_experience, list):

                for exp in segregated_experience:

                    if not isinstance(exp, dict):

                        continue

                    job_profile = exp.get(
                        "JobProfile",
                        {}
                    )

                    if isinstance(job_profile, dict):

                        designation = str(

                            job_profile.get(
                                "FormattedName",
                                ""
                            )

                            or

                            job_profile.get(
                                "Title",
                                ""
                            )

                        ).strip()

                    if designation:

                        break

            if not designation:

                designation = str(

                    resume_data.get(
                        "JobProfile",
                        ""
                    )

                ).strip()

            # ==========================================
            # QUALIFICATION
            # ==========================================

            qualification = ""

            segregated_qualification = resume_data.get(
                "SegregatedQualification",
                []
            )

            if isinstance(
                segregated_qualification,
                list
            ):

                for qualification_item in segregated_qualification:

                    if not isinstance(
                        qualification_item,
                        dict
                    ):

                        continue

                    # ==========================================
                    # DEGREE OBJECT
                    # ==========================================

                    degree_data = qualification_item.get(
                        "Degree",
                        {}
                    )

                    if isinstance(
                        degree_data,
                        dict
                    ):

                        normalize_degree = str(

                            degree_data.get(
                                "NormalizeDegree",
                                ""
                            )

                        ).strip()

                        degree_name = str(

                            degree_data.get(
                                "DegreeName",
                                ""
                            )

                        ).strip()

                        specialization = degree_data.get(
                            "Specialization",
                            []
                        )

                        specialization_text = ""

                        if isinstance(
                            specialization,
                            list
                        ):

                            specialization_text = ", ".join(

                                [

                                    str(item).strip()

                                    for item in specialization

                                    if item
                                ]

                            )

                        if normalize_degree:

                            qualification = normalize_degree

                        elif degree_name:

                            qualification = degree_name

                        if (

                            qualification
                            and specialization_text

                        ):

                            qualification = (

                                f"{qualification} "
                                f"in {specialization_text}"
                            )

                    # ==========================================
                    # DIRECT QUALIFICATION FALLBACK
                    # ==========================================

                    if not qualification:

                        qualification = str(

                            qualification_item.get(
                                "Qualification",
                                ""
                            )

                        ).strip()

                    if qualification:

                        break

            # ==========================================
            # MAIN QUALIFICATION FALLBACK
            # ==========================================

            if not qualification:

                qualification_data = resume_data.get(
                    "Qualification",
                    ""
                )

                if isinstance(
                    qualification_data,
                    str
                ):

                    qualification = qualification_data.strip()

                elif isinstance(
                    qualification_data,
                    list
                ):

                    qualification = ", ".join(

                        [

                            str(item).strip()

                            for item in qualification_data

                            if item
                        ]

                    )

            # ==========================================
            # FINAL CLEANUP
            # ==========================================

            qualification = qualification.strip()

            # ==========================================
            # SKILLS
            # ==========================================

            skills = []

            skill_keywords = resume_data.get(
                "SkillKeywords",
                ""
            )

            if isinstance(skill_keywords, str):

                skills = [

                    skill.strip()

                    for skill in skill_keywords.split(",")

                    if skill.strip()
                ]

            # ==========================================
            # FILE DETAILS
            # ==========================================

            resume_file_name = os.path.basename(
                file_path
            )

            resume_score = 85

            # ==========================================
            # CANDIDATE PROFILE
            # ==========================================

            candidate_profile = {

                "candidate_id": candidate_id,

                "full_name": full_name,

                "email": email,

                "phone": phone,

                "linkedin": linkedin,

                "city": city,

                "state": state,

                "country": country,

                "skills": skills,

                "experience_years": (
                    experience_years
                ),

                "current_company": (
                    current_company
                ),

                "designation": designation,

                "resume_score": (
                    resume_score
                ),

                "total_experience_months": (
                    total_experience_months
                ),

                "highest_qualification": (
                    qualification
                ),

                "current_location": (
                    current_location
                ),

                "preferred_location": (
                    preferred_location
                ),

                "github_url": (
                    github_url
                ),

                "portfolio_url": (
                    portfolio_url
                ),

                "resume_file_name": (
                    resume_file_name
                )
            }

            # ==========================================
            # SAVE CANDIDATE
            # ==========================================

            CandidateRepository.save_candidate(

                candidate_profile
            )

            # ==========================================
            # SAVE RAW DATA
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

                "message": (
                    "Resume parsing failed"
                ),

                "error": str(e)
            }