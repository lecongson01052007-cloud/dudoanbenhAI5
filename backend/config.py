"""Shared paths and environment-backed configuration."""

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")

DATA_DIR = Path(os.getenv("DATA_DIR", ROOT_DIR / "data" / "markdown"))
VECTOR_DIR = Path(os.getenv("VECTOR_DIR", ROOT_DIR / "vector_db"))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "intfloat/multilingual-e5-base")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

SPECIALTIES = ("Nội tiết", "Hô hấp", "Tim mạch")
ALL_SPECIALTIES = ("Tất cả", *SPECIALTIES)
CASE_SPECIALTIES = ("Tự động", *SPECIALTIES)
