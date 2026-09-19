import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_ID = "ai4bharat/indictrans2-indic-en-dist-200M"

print("Loading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_ID,
    trust_remote_code=True
)

print("Tokenizer loaded.")

print("Loading model...")

model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_ID,
    trust_remote_code=True
).to("cpu")

model.eval()

print("MODEL LOADED SUCCESSFULLY")

src_text = "धर्म"

src_lang = "san_Deva"
tgt_lang = "eng_Latn"

text = f"{src_lang} {tgt_lang} {src_text}"

print("SANSKRIT:", src_text)
print("MODEL INPUT:", text)

inputs = tokenizer(
    text,
    return_tensors="pt"
)

with torch.no_grad():
    output = model.generate(
        **inputs,
        max_length=256,
        num_beams=5
    )

result = tokenizer.decode(
    output[0],
    skip_special_tokens=True
)

print("TRANSLATION:", result)