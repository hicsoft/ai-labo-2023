import sys
import torch
from transformers import LlamaTokenizer, AutoModelForVision2Seq, BlipImageProcessor
from PIL import Image

MODEL = '../models/JPN-instructblip-alpha'

# helper function to format input prompts
def build_prompt(prompt='', sep='\n\n### '):
    sys_msg = '以下は、タスクを説明する指示と、文脈のある入力の組み合わせです。要求を適切に満たす応答を書きなさい。'
    p = sys_msg
    roles = ['指示', '応答']
    user_query = '与えられた画像について、詳細に述べてください。'
    msgs = [': \n' + user_query, ': ']
    if prompt:
        roles.insert(1, '入力')
        msgs.insert(1, ': \n' + prompt)
    for role, msg in zip(roles, msgs):
        p += sep + role + msg
    return p

# load model
model = AutoModelForVision2Seq.from_pretrained(MODEL, trust_remote_code=True, variant='fp16', device_map='auto', load_in_8bit=True)
processor = BlipImageProcessor.from_pretrained(MODEL)
tokenizer = LlamaTokenizer.from_pretrained(MODEL, additional_special_tokens=['▁▁'])
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# prepare inputs
image = Image.open('./test-a.png').convert('RGB')

# input empty string for image captioning. You can also input questions as prompts
# 空の色は？
argv = sys.argv
prompt = '' if len(argv) == 1 else argv[1]
prompt = build_prompt(prompt)
print(prompt)

inputs = processor(images=image, return_tensors='pt')
text_encoding = tokenizer(prompt, add_special_tokens=False, return_tensors='pt')
text_encoding['qformer_input_ids']      = text_encoding['input_ids']     .clone()
text_encoding['qformer_attention_mask'] = text_encoding['attention_mask'].clone()
inputs.update(text_encoding)

# generate
outputs = model.generate(
    **inputs.to(device, dtype=model.dtype),
    num_beams=5,
    max_new_tokens=32,
    min_length=1,
    pad_token_id=tokenizer.pad_token_id,
)

generated_text = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0].strip()
print(generated_text)
# 桜と東京スカイツリー
