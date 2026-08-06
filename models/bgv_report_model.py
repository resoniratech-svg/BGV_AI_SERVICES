from db import db


class BGVReport(db.Model):
    __tablename__ = "bgv_reports"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)

    candidate_id = db.Column(db.BigInteger, nullable=False)

    report_reference_id = db.Column(db.String(100), unique=True, nullable=False)

    report_name = db.Column(db.String(255), nullable=False)

    report_type = db.Column(db.String(100), default="FULL_BGV")

    report_status = db.Column(db.String(50), default="COMPLETED")

    verification_status = db.Column(db.String(50), default="VERIFIED")

    file_name = db.Column(db.String(255), nullable=False)

    file_path = db.Column(db.Text, nullable=False)

    file_url = db.Column(db.Text)

    storage_provider = db.Column(db.String(100), default="LOCAL_STORAGE")

    created_at = db.Column(db.DateTime, server_default=db.func.now())
