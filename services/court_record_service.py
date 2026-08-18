import json
import requests

from config import Config

from repositories.court_record_repository import CourtRecordRepository

from services.verification_service import VerificationService


class CourtRecordService:
    @staticmethod
    def search_court_records(candidate_id, full_name):

        try:
            # ==========================================
            # CREATE VERIFICATION SESSION
            # ==========================================

            verification_id = VerificationService.initiate_watchlist_verification(
                candidate_id
            )

            # ==========================================
            # SEARCH QUERY
            # ==========================================

            query = f'"{full_name}"'

            # ==========================================
            # API URL
            # ==========================================

            url = f"{Config.INDIANKANOON_BASE_URL}/search/"

            params = {"formInput": query, "pagenum": 0}

            headers = {"Authorization": f"Token {Config.INDIANKANOON_API_TOKEN}"}

            # ==========================================
            # API REQUEST
            # ==========================================

            response = requests.post(url, headers=headers, json=params)

            response_json = response.json()

            # ==========================================
            # SAVE API LOG
            # ==========================================

            CourtRecordRepository.save_court_record_log(
                candidate_id=candidate_id,
                request_url=response.url,
                request_headers=str(headers),
                response_data=json.dumps(response_json),
                status_code=response.status_code,
            )

            # ==========================================
            # EXTRACT RESULTS
            # ==========================================

            docs = response_json.get("docs", [])

            total_cases = len(docs)

            case_found = total_cases > 0

            # ==========================================
            # SAVE RESULTS
            # ==========================================

            if docs:
                for doc in docs:
                    CourtRecordRepository.save_court_record_result(
                        candidate_id=candidate_id,
                        verification_id=verification_id,
                        full_name=full_name,
                        query_used=query,
                        case_found=True,
                        total_cases=total_cases,
                        court_name=doc.get("docsource"),
                        case_title=doc.get("title"),
                        document_id=doc.get("tid"),
                        judgment_date=doc.get("publishdate"),
                        risk_level="MEDIUM",
                        provider_name="Indian Kanoon",
                        raw_response=json.dumps(doc),
                    )

            else:
                CourtRecordRepository.save_court_record_result(
                    candidate_id=candidate_id,
                    verification_id=verification_id,
                    full_name=full_name,
                    query_used=query,
                    case_found=False,
                    total_cases=0,
                    court_name=None,
                    case_title=None,
                    document_id=None,
                    judgment_date=None,
                    risk_level="CLEAR",
                    provider_name="Indian Kanoon",
                    raw_response=json.dumps(response_json),
                )

            # ==========================================
            # MARK COMPLETED
            # ==========================================

            VerificationService.mark_verification_completed(verification_id)

            # ==========================================
            # SUCCESS RESPONSE
            # ==========================================

            return {
                "success": True,
                "candidate_id": candidate_id,
                "verification_id": verification_id,
                "case_found": case_found,
                "total_cases": total_cases,
                "results": docs,
            }

        except Exception as e:
            return {
                "success": False,
                "message": ("Court record verification failed"),
                "error": str(e),
            }
