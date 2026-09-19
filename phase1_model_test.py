import torch
print('torch', torch.__version__)
print('cuda', torch.cuda.is_available())
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
model_id = 'ai4bharat/indictrans2-indic-en-dist-200M'
print('MODEL NAME:', model_id)
print('loading tokenizer...')
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
print('tokenizer loaded')
print('loading model on CPU...')
model = AutoModelForSeq2SeqLM.from_pretrained(model_id, trust_remote_code=True).to('cpu')
model.eval()
print('MODEL LOADED SUCCESSFULLY')
text = '????'
print('SANSKRIT INPUT:', text)
inputs = tokenizer(text, return_tensors='pt')
with torch.no_grad():
    generated = model.generate(**inputs.to('cpu'), use_cache=True, max_length=256, num_beams=5)
translation = tokenizer.decode(generated[0], skip_special_tokens=True)
print('ENGLISH TRANSLATION:', translation)
print('PHASE 1 STATUS: SUCCESS')
