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
print(f'Load OK! : {device}')

# prepare inputs
image = Image.open('./test-a.png').convert('RGB')

import gradio as gr

def load_image(img):
    global image
    image = img

count = 1

def generate(prompt):
    prompt = build_prompt(prompt)

    global count
    print(f'\nQ: #{count}')
    print(prompt)
    count += 1

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
    return generated_text

with gr.Blocks() as demo:
    gr.Markdown('## Stability AI multi modal model')
    imgIn = gr.Image(lambda: image, type='pil')
    imgIn.change(load_image, inputs=imgIn)
    with gr.Row():
        with gr.Column():
            question = gr.Textbox(lines=3, placeholder='質問を入力してください')
            submit = gr.Button('Submit', variant='primary')
            with gr.Row():
                default = gr.Button('Default')
                clear = gr.Button('Clear')
                default.click(lambda: '画像を説明して', outputs=question)
                clear.click(lambda: '', outputs=question)
        answer = gr.Textbox(lines=3)
        submit.click(generate, inputs=question, outputs=answer)

demo.launch()
