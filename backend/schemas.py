"""Validated request shapes for the HTTP API."""

from typing import Literal

from pydantic import BaseModel, Field


class Lab(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    value: str = Field(min_length=1, max_length=100)
    unit: str = Field(default="", max_length=40)


class Case(BaseModel):
    age: int = Field(ge=0, le=120)
    sex: Literal["Nam", "Nữ", "Khác"]
    main_symptom: str = Field(min_length=1, max_length=500)
    duration: str = Field(min_length=1, max_length=200)
    associated_symptoms: list[str] = Field(default_factory=list, max_length=30)
    history: str = Field(default="", max_length=3000)
    labs: list[Lab] = Field(default_factory=list, max_length=50)
    specialty: Literal["Tự động", "Nội tiết", "Hô hấp", "Tim mạch"] = "Tự động"


class SearchRequest(BaseModel):
    query: str = Field(min_length=2, max_length=3000)
    specialty: Literal["Tất cả", "Nội tiết", "Hô hấp", "Tim mạch"] = "Tất cả"
    top_k: int = Field(default=5, ge=1, le=8)


class ClinicianFeedback(BaseModel):
    note: str = Field(min_length=1, max_length=3000)
    timestamp: str = Field(max_length=40)
