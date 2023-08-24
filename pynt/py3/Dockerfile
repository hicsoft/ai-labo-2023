FROM nvcr.io/nvidia/pytorch:23.07-py3

RUN pip3 install diffusers[torch] transformers sentencepiece einops omegaconf

RUN pip3 install ctransformers bitsandbytes

RUN pip3 install gradio

RUN groupadd -g 1000 ubuntu && useradd -m -s /bin/bash -u 1000 -g 1000 ubuntu

USER ubuntu

WORKDIR /home/ubuntu/
