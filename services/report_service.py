import os
import uuid
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from repositories.report_repository import ReportRepository


class ReportService:
    
    @staticmethod
    def generate_bgv_report(candidate_id):

        # ==========================================
        # FETCH DATABASE DATA & HANDLE MISSING RECORDS
        # ==========================================
        summary = ReportRepository.get_candidate_summary(candidate_id)
        if not summary:
            raise Exception(
                f"No verification summary found for candidate {candidate_id}"
            )

        candidate = ReportRepository.get_candidate_details(candidate_id)
        if not candidate:
            raise Exception(
                f"Candidate not found: {candidate_id}"
            )

        # ==========================================
        # CREATE REPORT FOLDER
        # ==========================================
        os.makedirs("generated_reports", exist_ok=True)

        candidate_name = candidate["full_name"].replace(" ", "_")
        file_name = f"{candidate_name}_{candidate_id}_BGV_Report.pdf"
        file_path = os.path.join("generated_reports", file_name)

        # ==========================================
        # CREATE PDF DOCUMENT
        # ==========================================
        document = SimpleDocTemplate(file_path, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # ==========================================
        # HELPER FUNCTION
        # ==========================================
        def get_status(value):
            if not value:
                return "Pending"
            return value

        # ==========================================
        # TITLE
        # ==========================================
        title = Paragraph("Background Verification Report", styles["Title"])
        elements.append(title)
        elements.append(Spacer(1, 20))

        # ==========================================
        # 1. CANDIDATE SUMMARY (With Fixed Widths)
        # ==========================================
        elements.append(
            Paragraph("1. CANDIDATE SUMMARY", styles["Heading2"])
        )

        candidate_table = Table(
            [
                ["Full Name", summary.get("candidate_name", "-")],
                ["Email", summary.get("email", "-")],
                ["Phone", summary.get("phone", "-")],
                ["Candidate ID", str(candidate_id)]
            ],
            colWidths=[150, 300]
        )

        candidate_table.setStyle(
            TableStyle([
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey)
            ])
        )

        elements.append(candidate_table)
        elements.append(Spacer(1, 20))

        # ==========================================
        # 2. VERIFICATION MODULE STATUS (With Fixed Widths)
        # ==========================================
        elements.append(
            Paragraph("2. VERIFICATION MODULE STATUS", styles["Heading2"])
        )

        verification_table = Table(
            [
                ["Verification Module", "Status"],
                ["Aadhaar", get_status(summary.get("aadhaar_status"))],
                ["PAN", get_status(summary.get("pan_status"))],
                ["Passport", get_status(summary.get("passport_status"))],
                ["Driving License", get_status(summary.get("dl_status"))],
                ["Face Match", get_status(summary.get("face_match_status"))],
                ["Resume Parsing", get_status(summary.get("resume_status"))],
                ["Education", get_status(summary.get("education_status"))],
                ["Employment", get_status(summary.get("employment_status"))],
                ["Salary Slip", get_status(summary.get("salary_slip_status"))],
                ["Credit Bureau", get_status(summary.get("credit_status"))],
                ["Court Record", get_status(summary.get("court_status"))],
                ["Watchlist", get_status(summary.get("watchlist_status"))],
                ["Deepfake Detection", get_status(summary.get("deepfake_status"))]
            ],
            colWidths=[250, 200]
        )

        verification_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold")
            ])
        )

        elements.append(verification_table)
        elements.append(Spacer(1, 20))

        # ==========================================
        # 3. FINAL EXECUTIVE ASSESSMENT
        # ==========================================
        elements.append(
            Paragraph("3. FINAL EXECUTIVE ASSESSMENT", styles["Heading2"])
        )

        # Cleaned & Deduplicated Status Determinations
        overall_status_db_value = summary.get("overall_status")
        overall_status = overall_status_db_value or "UNDER_VERIFICATION"

        db_status = (summary.get("overall_status") or "").upper()

        if db_status == "VERIFIED":
            verification_status = "VERIFIED"
        elif db_status in ["FRAUD", "FRAUD_ALERT", "REJECTED", "NOT VERIFIED"]:
            verification_status = "REJECTED"
        else:
            verification_status = "IN_PROGRESS"

        risk_level = get_status(summary.get("risk_level"))

        final_table = Table(
            [
                ["Overall Status", overall_status],
                ["Risk Level", risk_level]
            ],
            colWidths=[150, 300]
        )

        final_table.setStyle(
            TableStyle([
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey)
            ])
        )

        elements.append(final_table)
        elements.append(Spacer(1, 40))

        elements.append(
            Paragraph("Authorized Signature __________________", styles["BodyText"])
        )
        elements.append(Spacer(1, 10))
        elements.append(
            Paragraph("Date __________________", styles["BodyText"])
        )

        # ==========================================
        # BUILD PDF
        # ==========================================
        print(file_name)
        document.build(elements)

        # ==========================================
        # STORE REPORT DETAILS IN DATABASE
        # ==========================================
        reference_id = f"BGV-{uuid.uuid4().hex[:10].upper()}"

        report_data = {
            "candidate_id": candidate_id,
            "report_reference_id": reference_id,
            "report_name": "Full Background Verification Report",
            "report_type": "FULL_BGV",
            "report_status": "COMPLETED",
            "verification_status": verification_status,
            "file_name": file_name,
            "file_path": file_path,
            "file_url": file_path,
            "storage_provider": "LOCAL_STORAGE"
        }

        print("REPORT DATA")
        print(report_data)

        try:
            # Inline Trace Boundaries Added Right Before Query Execution
            print("=" * 50)
            print("DB STATUS =", overall_status)
            print("ENUM STATUS =", verification_status)
            print("REPORT DATA =", report_data)
            print("=" * 50)

            ReportRepository.save_report_details(report_data)
            print("REPORT SAVED")

        except Exception as e:
            print("SAVE FAILED")
            print(type(e))
            print(str(e))
            raise  # Bubbles up genuine context directly back to Flask runtime

        return file_path

    @staticmethod
    def get_report_history():
        reports = ReportRepository.get_report_history()
        return reports
    
    @staticmethod
    def get_latest_report(candidate_id):
        return ReportRepository.get_latest_report(candidate_id)