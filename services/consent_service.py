from datetime import datetime

from repositories.consent_repository import (
    ConsentRepository
)


class ConsentService:

    ####################################################
    # SAVE / UPDATE CANDIDATE CONSENT
    ####################################################

    @staticmethod
    def save_candidate_consent(

            candidate_id,
            bgv_id,
            verification_type,
            consent_status,
            consent_text,
            consent_version,
            consent_source,
            ip_address,
            user_agent

    ):

        ####################################################
        # CHECK EXISTING CONSENT
        ####################################################

        existing = (

            ConsentRepository
            .get_candidate_consent(

                candidate_id=candidate_id,

                bgv_id=bgv_id,

                verification_type=verification_type

            )

        )

        ####################################################
        # UPDATE
        ####################################################

        if existing:

            ConsentRepository.update_candidate_consent(

                candidate_id=candidate_id,

                bgv_id=bgv_id,

                verification_type=verification_type,

                consent_status=consent_status,

                consent_text=consent_text,

                consent_version=consent_version,

                consent_source=consent_source,

                consent_given_at=datetime.now(),

                ip_address=ip_address,

                user_agent=user_agent,

                provider_name=None,

                api_reference_id=None,

                raw_response=None

            )

            return {

                "success": True,

                "message": "Candidate consent updated successfully."

            }

        ####################################################
        # INSERT
        ####################################################

        consent_id = (

            ConsentRepository
            .save_candidate_consent(

                candidate_id=candidate_id,

                bgv_id=bgv_id,

                verification_type=verification_type,

                consent_status=consent_status,

                consent_text=consent_text,

                consent_version=consent_version,

                consent_source=consent_source,

                consent_given_at=datetime.now(),

                ip_address=ip_address,

                user_agent=user_agent,

                provider_name=None,

                api_reference_id=None,

                raw_response=None

            )

        )

        return {

            "success": True,

            "message": "Candidate consent saved successfully.",

            "consent_id": consent_id

        }

    ####################################################
    # GET CONSENT
    ####################################################

    @staticmethod
    def get_candidate_consent(

            candidate_id,
            bgv_id,
            verification_type

    ):

        return (

            ConsentRepository
            .get_candidate_consent(

                candidate_id,

                bgv_id,

                verification_type

            )

        )
    
    @staticmethod
    def get_candidate_consent(

            candidate_id,
            bgv_id,
            verification_type

    ):

        return (

            ConsentRepository
            .get_candidate_consent(

                candidate_id=candidate_id,

                bgv_id=bgv_id,

                verification_type=verification_type

            )

        )