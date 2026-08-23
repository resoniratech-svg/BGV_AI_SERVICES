from services.ollama_resume_service import (
    OllamaResumeService
)


class ResumeVerificationService:

    @staticmethod
    def process_resume(
        file,
        candidate_id
    ):
        return (
            OllamaResumeService.parse_resume(
                file_path=file,
                candidate_id=candidate_id
            )
        )