import os
import sys
import requests
import datetime
import torch
from diffusers import StableDiffusionPipeline

URL = 'https://slack.com/api/files.upload'

now = datetime.datetime.now()

#

batch = 1

is_cuda = torch.cuda.is_available()
if is_cuda:
    print('cuda=OK')

pipeline = StableDiffusionPipeline.from_pretrained(
    '../models/stable-diffusion-2-1',
    use_safetensors=True
)

pipeline.requires_safety_checker = False
pipeline.safety_checker = None

if is_cuda:
    pipeline = pipeline.to('cuda')

argv = sys.argv

prompt = 'masterpiece best quality, black cat laying floor, winter' if len(argv) == 1 else argv[1]

print(prompt)

images = pipeline(
    prompt=prompt,
    width=768,
    height=768,
    num_images_per_prompt=batch,
    generator=torch.manual_seed(3407)
)

for i, img in enumerate(images.images):
    img.save(f'sd-gen-{i}.png')

#

tokens = os.environ['SLACK'] if 'SLACK' in os.environ else ''
if len(tokens) == 0:
    print('NOPOST')
    sys.exit(0)

tks = tokens.split(':')
token   = tks[0]
channel = tks[1]

data = {
   'token': token,
   'channels': channel,
   'initial_comment': f'{prompt} : TS {now.isoformat()}'
}

files = {'file': open('sd-gen-0.png', 'rb')}

res = requests.post(URL, data=data, files=files, timeout=30)
print(res)
