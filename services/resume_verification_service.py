import json

from repositories.verification_repository import (
    VerificationRepository
)

from services.rchilli_service import (
    RChilliService
)

from services.verification_service import (
    VerificationService
)


class ResumeVerificationService:

    @staticmethod
    def process_resume(

        file,
        candidate_id
    ):

        try:

            # ==========================================
            # CREATE VERIFICATION SESSION
            # ==========================================

            verification_id = (
                VerificationService
                .initiate_resume_verification(
                    candidate_id
                )
            )

            # ==========================================
            # CALL RCHILLI SERVICE
            # ==========================================

            result = (
                RChilliService.parse_resume(

                    file=file,

                    candidate_id=candidate_id
                )
            )

            # ==========================================
            # VALIDATE RESULT
            # ==========================================

            if not result.get("success"):

                VerificationService.mark_verification_failed(

                    verification_id
                )

                return {

                    "success": False,

                    "verification_id": (
                        verification_id
                    ),

                    "message": result.get(
                        "message"
                    ),

                    "error": result.get(
                        "error"
                    ),

                    "provider_response": (
                        result.get(
                            "provider_response"
                        )
                    )
                }

            # ==========================================
            # EXTRACT DATA
            # ==========================================

            candidate_profile = result.get(
                "candidate_profile",
                {}
            )

            parsed_result = result.get(
                "raw_data",
                {}
            )

            # ==========================================
            # SAVE PARSED RESULT
            # ==========================================

            VerificationRepository.save_resume_parsing_result(

                candidate_id=candidate_id,

                parsed_data=json.dumps(
                    candidate_profile
                ),

                skills=str(
                    candidate_profile.get(
                        "skills",
                        ""
                    )
                ),

                experience_years=candidate_profile.get(
                    "experience_years"
                ),

                education_summary=str(
                    parsed_result.get(
                        "ResumeParserData",
                        {}
                    ).get(
                        "Qualification",
                        ""
                    )
                ),

                parsing_status="SUCCESS",

                parser_provider="RChilli",

                raw_response=json.dumps(
                    parsed_result
                )
            )

            # ==========================================
            # MARK COMPLETED
            # ==========================================

            VerificationService.mark_verification_completed(

                verification_id
            )

            # ==========================================
            # SUCCESS RESPONSE
            # ==========================================

            return {

                "success": True,

                "verification_id": (
                    verification_id
                ),

                "candidate_id": (
                    candidate_id
                ),

                "candidate_profile": (
                    result.get(
                        "candidate_profile"
                    )
                ),

                "raw_data": result.get(
                    "raw_data"
                )
            }

        except Exception as e:

            return {

                "success": False,

                "message": (
                    "Resume verification failed"
                ),

                "error": str(e)
            }