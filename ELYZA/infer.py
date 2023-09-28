from ctransformers import AutoModelForCausalLM

llm = AutoModelForCausalLM.from_pretrained(
    'ELYZA-japanese-Llama-2-7b-instruct-q5_K_M.gguf',
    model_type='llama',
    temperature=0.7,
    context_length=1024,
    max_new_tokens=512,
    batch_size=8,
    gpu_layers=100
)

prompt='''\
クマが海辺に行ってアザラシと友達になり、最終的には家に帰るというプロットの短編小説を書いてください。'''

formated_prompt=f'''\
<s>[INST] <<SYS>>
あなたは誠実で優秀な日本人のアシスタントです。
<</SYS>>

{prompt} [/INST]'''

print(formated_prompt)

for x in range(12):
    count = 0
    print(f'\n\nRESPONSE: #{x + 1}')
    s = llm(formated_prompt, stream=True)
    for text in s:
        print(text, end="", flush=True)
        count += 1
    print(f'\n\nDONE. ({count})')
