# import time

# from repositories.aadhaar_repository import AadhaarRepository

# from services.ongrid.aadhaar_generate_qr_service import AadhaarGenerateQRService


# class AadhaarConsentService:
#     @staticmethod
#     def get_consent_qr(candidate_id, bgv_id):

#         session = AadhaarRepository.get_aadhaar_session(candidate_id)

#         if session:
#             # =====================================
#             # CONSENT ALREADY COMPLETED
#             # =====================================

#             if session["session_status"] == "SUCCESS":
#                 return {
#                     "success": True,
#                     "status": "SUCCESS",
#                     "message": "Aadhaar consent already completed",
#                 }

#             # =====================================
#             # QR STILL ACTIVE
#             # =====================================

#             expires_at = session.get("expires_at")

#             current_time = int(time.time() * 1000)

#             if expires_at and current_time < expires_at:
#                 return {
#                     "success": True,
#                     "status": "PENDING",
#                     "message": "Existing QR is active",
#                     "scan_uri": session["scan_uri"],
#                 }

#         # =====================================
#         # QR EXPIRED OR SESSION NOT FOUND
#         # =====================================

#         return AadhaarGenerateQRService.generate_qr(candidate_id, bgv_id)
