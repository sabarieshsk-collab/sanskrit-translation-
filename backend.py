import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator

DICTIONARY_PATH = Path(__file__).parent / "data" / "sanskrit_dictionary.json"

with DICTIONARY_PATH.open(encoding="utf-8") as dictionary_file:
    SANSKRIT_DICTIONARY = json.load(dictionary_file)

app = FastAPI(title="Sanskrit-English Translation API")

# Allow local development and the deployed Vercel frontend to call the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TranslationRequest(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def text_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("text must contain at least one non-space character")
        return value


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "Sanskrit-English Translation API is running",
        "status": "success",
    }


@app.post("/translate")
def translate(request: TranslationRequest) -> dict[str, str]:
    normalized_text = " ".join(request.text.split())
    known_word = SANSKRIT_DICTIONARY.get(normalized_text)

    if known_word is not None:
        return {
            "sanskrit": normalized_text,
            "english": known_word["english"],
            "meaning": known_word["meaning"],
            "source": "IKS Knowledge Base",
        }

    unavailable_message = "Meaning not available in the IKS knowledge base."

    return {
        "sanskrit": normalized_text,
        "english": unavailable_message,
        "meaning": unavailable_message,
        "source": "IKS Knowledge Base",
    }
