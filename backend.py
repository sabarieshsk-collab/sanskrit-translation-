import json
from pathlib import Path

import torch
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

MODEL_ID = "ai4bharat/indictrans2-indic-en-dist-200M"
DEVICE = "cpu"
SRC_LANG = "san_Deva"
TGT_LANG = "eng_Latn"
DICTIONARY_PATH = Path(__file__).parent / "data" / "sanskrit_dictionary.json"

with DICTIONARY_PATH.open(encoding="utf-8") as dictionary_file:
    SANSKRIT_DICTIONARY = json.load(dictionary_file)

# Load the tokenizer and model once when the API application starts.
print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(
    MODEL_ID,
    trust_remote_code=True,
)
print("Tokenizer loaded.")

print("Loading model on CPU...")
model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_ID,
    trust_remote_code=True,
).to(DEVICE)
model.eval()
print("MODEL LOADED SUCCESSFULLY")

app = FastAPI(title="Sanskrit-English Translation API")

# Allow the future local frontend to call this API during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5500",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
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

    # IndicTrans2 expects the source and target language codes before the text.
    model_input = f"{SRC_LANG} {TGT_LANG} {normalized_text}"
    inputs = tokenizer(model_input, return_tensors="pt").to(DEVICE)

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_length=256,
            num_beams=5,
        )

    english = tokenizer.decode(
        output[0],
        skip_special_tokens=True,
    )

    return {
        "sanskrit": normalized_text,
        "english": english,
        "meaning": english,
        "source": "AI Translation Model",
    }
