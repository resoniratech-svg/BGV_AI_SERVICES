from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.lib.pagesizes import letter

import os

from repositories.report_repository import (
    ReportRepository
)

import uuid


class ReportService:

    @staticmethod
    def generate_bgv_report(

        candidate_id
    ):

        # ==========================================
        # FETCH DATABASE DATA
        # ==========================================

        bgv_data = (
            ReportRepository
            .get_candidate_bgv_data(
                candidate_id
            )
        )

        # ==========================================
        # CREATE REPORT FOLDER
        # ==========================================

        os.makedirs(

            "generated_reports",

            exist_ok=True
        )

        file_name = (
            f"bgv_report_"
            f"{candidate_id}.pdf"
        )

        file_path = os.path.join(

            "generated_reports",

            file_name
        )

        # ==========================================
        # CREATE PDF DOCUMENT
        # ==========================================

        document = SimpleDocTemplate(

            file_path,

            pagesize=letter
        )

        styles = getSampleStyleSheet()

        elements = []

        # ==========================================
        # TITLE
        # ==========================================

        title = Paragraph(

            "Background Verification Report",

            styles["Title"]
        )

        elements.append(title)

        elements.append(

            Spacer(1, 20)
        )

        # ==========================================
        # PASSPORT DATA
        # ==========================================

        passport = bgv_data.get(
            "passport"
        )

        if passport:

            passport_content = f"""

            <b>PASSPORT VERIFICATION</b>
            <br/><br/>

            Passport Number:
            {passport.get('passport_number')}
            <br/><br/>

            Full Name:
            {passport.get('full_name')}
            <br/><br/>

            Nationality:
            {passport.get('nationality')}
            <br/><br/>

            Verification Status:
            {passport.get('verification_status')}
            <br/><br/>
            """

            elements.append(

                Paragraph(

                    passport_content,

                    styles["BodyText"]
                )
            )

            elements.append(

                Spacer(1, 20)
            )

        # ==========================================
        # DRIVING LICENSE DATA
        # ==========================================

        driving_license = bgv_data.get(
            "driving_license"
        )

        if driving_license:

            dl_content = f"""

            <b>DRIVING LICENSE VERIFICATION</b>
            <br/><br/>

            License Number:
            {driving_license.get('license_number')}
            <br/><br/>

            Full Name:
            {driving_license.get('full_name')}
            <br/><br/>

            Verification Status:
            {driving_license.get('verification_status')}
            <br/><br/>
            """

            elements.append(

                Paragraph(

                    dl_content,

                    styles["BodyText"]
                )
            )

            elements.append(

                Spacer(1, 20)
            )

        # ==========================================
        # AML DATA
        # ==========================================

        aml = bgv_data.get(
            "aml"
        )

        if aml:

            aml_content = f"""

            <b>AML SCREENING</b>
            <br/><br/>

            Full Name:
            {aml.get('full_name')}
            <br/><br/>

            Country:
            {aml.get('country')}
            <br/><br/>

            AML Status:
            {aml.get('aml_status')}
            <br/><br/>

            Risk Level:
            {aml.get('risk_level')}
            <br/><br/>
            """

            elements.append(

                Paragraph(

                    aml_content,

                    styles["BodyText"]
                )
            )

            elements.append(

                Spacer(1, 20)
            )

        # ==========================================
        # WATCHLIST DATA
        # ==========================================

        watchlist = bgv_data.get(
            "watchlist"
        )

        if watchlist:

            watchlist_content = f"""

            <b>GLOBAL WATCHLIST SCREENING</b>
            <br/><br/>

            Match Found:
            {watchlist.get('match_found')}
            <br/><br/>

            Risk Level:
            {watchlist.get('risk_level')}
            <br/><br/>

            AML Status:
            {watchlist.get('aml_status')}
            <br/><br/>
            """

            elements.append(

                Paragraph(

                    watchlist_content,

                    styles["BodyText"]
                )
            )

            elements.append(

                Spacer(1, 20)
            )

        # ==========================================
        # FINAL STATUS
        # ==========================================

        final_content = """

        <b>FINAL BGV STATUS</b>
        <br/><br/>

        APPROVED
        """

        elements.append(

            Paragraph(

                final_content,

                styles["BodyText"]
            )
        )

        # ==========================================
        # BUILD PDF
        # ==========================================

        document.build(elements)

        # ==========================================
        # STORE REPORT DETAILS IN DATABASE
        # ==========================================

        reference_id = (

            f"BGV-"
            f"{uuid.uuid4().hex[:10].upper()}"
        )

        report_data = {

            "candidate_id": candidate_id,

            "report_reference_id": reference_id,

            "report_name":
                "Full Background Verification Report",

            "report_type": "FULL_BGV",

            "report_status": "COMPLETED",

            "verification_status": "VERIFIED",

            "file_name": file_name,

            "file_path": file_path,

            "file_url": file_path,

            "storage_provider": "LOCAL_STORAGE"
        }

        ReportRepository.save_report_details(

            report_data
        )

        return file_path

    @staticmethod
    def get_report_history():

        reports = (
            ReportRepository
            .get_report_history()
        )

        return reports