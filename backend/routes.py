"""HTTP endpoints for health, ingestion, retrieval, analysis, and feedback."""

import json
import os
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.config import DATA_DIR, ROOT_DIR, SPECIALTIES
from backend.schemas import Case, ClinicianFeedback, SearchRequest
from backend.services.gemini import case_to_query, generate_report
from backend.services.knowledge_base import document_inventory, ingest_documents, read_documents, search_documents

router = APIRouter()


@router.get("/health")
def health():
    return {
        "status": "ok",
        "specialties": list(SPECIALTIES),
        "data_dir_exists": DATA_DIR.exists(),
        "llm_configured": bool(os.getenv("GOOGLE_API_KEY")),
    }


@router.get("/documents")
def list_documents():
    return document_inventory()


@router.post("/ingest")
async def ingest(file: UploadFile | None = File(default=None)):
    if file:
        if not file.filename or not file.filename.lower().endswith(".md"):
            raise HTTPException(400, "Hiện chỉ hỗ trợ nạp tệp Markdown (.md).")
        payload = await file.read()
        if len(payload) > 5_000_000:
            raise HTTPException(413, "Tệp vượt quá 5 MB.")
        target = DATA_DIR / "uploaded" / Path(file.filename).name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
    try:
        return {"status": "ok", "indexed_chunks": ingest_documents(read_documents(), reset=True)}
    except Exception as exc:
        raise HTTPException(503, str(exc)) from exc


@router.post("/search")
def search(request: SearchRequest):
    try:
        return {
            "query": request.query,
            "results": search_documents(request.query, request.specialty, request.top_k),
        }
    except Exception as exc:
        raise HTTPException(503, str(exc)) from exc


@router.post("/analyze")
def analyze(case: Case):
    try:
        query = case_to_query(case)
        specialty = case.specialty
        if specialty == "Tự động":
            initial = search_documents(query, "Tất cả", 8)
            specialty = initial[0]["specialty"] if initial else "Tất cả"
        sources = search_documents(query, specialty, 5)
        if not sources:
            return {
                "answer": {
                    "impression": "Chưa đủ thông tin trong kho tri thức để đưa ra nhận định có căn cứ.",
                    "differential": [],
                    "missing_information": ["Chọn chuyên khoa có tài liệu hoặc bổ sung kho tri thức."],
                    "suggested_evaluation": [],
                    "urgency": "urgent",
                    "urgency_reason": "Không có nguồn phù hợp; bác sĩ cần tự đánh giá tình trạng lâm sàng.",
                    "limitations": "Không thể tạo báo cáo dựa trên nguồn hiện có.",
                },
                "sources": [],
                "specialty": specialty,
            }
        return {"answer": generate_report(case, sources), "sources": sources, "specialty": specialty}
    except Exception as exc:
        raise HTTPException(503, str(exc)) from exc


@router.post("/feedback")
def clinician_feedback(feedback: ClinicianFeedback):
    """Save clinician notes and timestamp without patient case details."""
    path = ROOT_DIR / "data" / "clinician_feedback.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(feedback.model_dump(), ensure_ascii=False) + "\n")
    return {"status": "saved"}
