import gradio as gr
import torch

from diffusers import DPMSolverMultistepScheduler
from lpw_stable_diffusion import StableDiffusionLongPromptWeightingPipeline

batch = 1

is_cuda = torch.cuda.is_available()
if is_cuda:
    print('cuda=OK')

pipeline = StableDiffusionLongPromptWeightingPipeline.from_single_file(
    '../models/Counterfeit-V3.0_fp32.safetensors',
    load_safety_checker=False
)

pipeline.requires_safety_checker = False
pipeline.safety_checker = None

pipeline.scheduler = DPMSolverMultistepScheduler.from_config(
    pipeline.scheduler.config,
    use_karras_sigmas=True
)

if is_cuda:
    pipeline = pipeline.to('cuda')

negative_prompt = (
    '(low quality, worst quality:1.4), (bad anatomy), (inaccurate limb:1.2), (extra arms:1.2), '
    'bad composition, inaccurate eyes, extra digit, fewer digits, '
    'large breasts'
)

# masterpiece, best quality, 2girls, back to back, touch on hand, black hair, cowboy shot, mid summer, after noon
# masterpiece, best quality, 2girls, back to back, touch on hand, black hair, cowboy shot, winter, mid night
# masterpiece, best quality, 2girls, back to back, touch on hand, black hair, cowboy shot, autumn, morning
# masterpiece, best quality, 2girls, back to back, touch on hand, black hair, cowboy shot, spring, twilight

block = gr.Blocks(css=".container { max-width: 800px; margin: auto; }")

def infer(prompt):
    images = pipeline(
        prompt=prompt, 
        negative_prompt=negative_prompt, 
        width=512, 
        height=768, 
        num_inference_steps=30 if is_cuda else 24,
        num_images_per_prompt=batch,
        max_embeddings_multiples=2,
        generator=torch.manual_seed(3407)
    )
    return images.images

with block as demo:
    gr.Markdown("<h1><center>Stable Diffusion</center></h1>")
    gr.Markdown(
        "Stable Diffusion is an AI model that generates images from any prompt you give!"
    )
    with gr.Group():
        with gr.Box():
            with gr.Row(equal_height=True):
                text = gr.Textbox(
                    label="Enter your prompt", show_label=False, max_lines=1,
                    container=False,
                )
                btn = gr.Button("Run")
               
        gallery = gr.Gallery(label="Generated images", show_label=False, columns=1, preview=True)

        text.submit(infer, inputs=[text], outputs=gallery)
        btn.click(infer, inputs=[text], outputs=gallery)

    gr.Markdown(
        """___
   <p style='text-align: center'>
   Created by CompVis and Stability AI
   <br/>
   </p>"""
    )

demo.launch(debug=True)
