import os
import json
import time
import torch
import random
from tqdm import tqdm
from collections import defaultdict
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from accelerate import Accelerator
from torch.utils.data import Dataset, DataLoader

prompts_encode = {
    'base': "Encode the following text to a Caesar cipher. The shift is $SHIFT$. Output the cipher text only.",
    'cot-like': "Encode the following text to a Caesar cipher. The shift is $SHIFT$. Output a lookup table and the cipher text in a json dictionary: {\"lookup_table\": {}, \"cipher_text\":...}. Output the dictionary only.",
    'code': "Encode the following text to a Caesar cipher. The shift is $SHIFT$. Write a Python function and generate the answer. Output the function and the cipher text only.",
    'default': "Encode the following text to a Caesar cipher. The shift is $SHIFT$."
    }

prompts_decode = {
    'base': "Decode the following Caesar cipher text. The shift is $SHIFT$. Output the plain text only.",
    'cot-like': "Decode the following Caesar cipher text. The shift is $SHIFT$. Output a lookup table and the plain text in a json dictionary: {\"lookup_table\": {}, \"plain_text\":...}. Output the dictionary only.",
    'code': "Decode the following Caesar cipher text. The shift is $SHIFT$. Write a Python function and generate the answer. Output the function and the plain text only.",
    'default': "Decode the following Caesar cipher text. The shift is $SHIFT$."
    }

for pretrained in [
    'Qwen/QwQ-32B-Preview',
    '/storage/ukp/shared/shared_model_weights/models--Qwen2.5-32B-Instruct',
    '/storage/ukp/shared/shared_model_weights/models--llama-3.1/hf/8B-Instruct/',
    '/storage/ukp/shared/shared_model_weights/models--llama-3.1/hf/70B-Instruct/'
]:

    accelerator = Accelerator()
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type='nf4',
        bnb_4bit_compute_dtype=torch.bfloat16
    )
    tokenizer = AutoTokenizer.from_pretrained(pretrained, padding_side='left')
    tokenizer.add_special_tokens({'pad_token': '<|end_of_text|>'})
    model = AutoModelForCausalLM.from_pretrained(pretrained, quantization_config=bnb_config, local_files_only=True)
    model = accelerator.prepare(model)
    pretrained = pretrained.replace('/storage/ukp/shared/shared_model_weights/', '')

    for setting in ['decrypt', 'encrypt']:
        for type_of_plain_text in ['natural', 'random']: ## check here
            for prompt_type in ['base', 'default']: ## check here
                
                shot = '0' ## check here
                
                with open(f'data/{type_of_plain_text}.json') as file:
                    data = json.loads(file.read())
                
                if shot != '0':
                    with open(f'prompts/natural_{prompt_type}_{setting}_{shot}.txt') as file:
                        few_shot_prompt = file.read()
                
                experiment_id = time.strftime('%Y%m%d_%H%M%S', time.localtime())
                temperature = 0.01
                seed = 2266
                if prompt_type == 'base':
                    max_tokens = 2048
                if prompt_type == 'cot-like':
                    max_tokens = 2048
                if prompt_type == 'default':
                    max_tokens = 2048
                
                random.seed(seed)
                torch.cuda.manual_seed_all(seed)
                
                output = defaultdict(dict)
                with tqdm(total=len(data)) as t:
                    with torch.no_grad():
                        for i, item in data.items():
                            
                            if setting == 'encrypt':
                                prompts = prompts_encode
                                input_field = 'plain_text'
                                gold_field = 'cipher_text'
                                answer_text = '\n\nOUTPUT: '
                            
                            if setting == 'decrypt':
                                prompts = prompts_decode
                                input_field = 'cipher_text'
                                gold_field = 'plain_text'
                                answer_text = '\n\nOUTPUT: '
                
                            if prompt_type == 'cot-like':
                                answer_text = '\n\nOUTPUT: '
                    
                            if shot == '0':
                                messages = [
                                    {"role": "system", "content": prompts[prompt_type].replace('$SHIFT$', str(item['shift']))},
                                    {"role": "user", "content": item[input_field]}
                                ]
                                input = tokenizer.apply_chat_template(
                                    messages,
                                    tokenize=False,
                                    add_generation_prompt=True
                                )
                                tokenized = tokenizer(input, return_tensors='pt').to(accelerator.device)
                                result = model.generate(
                                    **tokenized,
                                    # eos_token_id=[128001,128008,128009], ## check here
                                    eos_token_id=[151645],
                                    pad_token_id=tokenizer.vocab[tokenizer.special_tokens_map['pad_token']],
                                    max_new_tokens=max_tokens,
                                    temperature=temperature
                                )
                                output[i]['input'] = item[input_field]
                                output[i]['shift'] = item['shift']
                                output[i]['output'] = tokenizer.decode(result[0], skip_special_tokens=True)
                                output[i]['gold'] = item[gold_field]
                            
                            if shot != '0':
                                if item['shift'] == 9:
                                    input = few_shot_prompt + '\n' + item[input_field] + answer_text
                                    tokenized = tokenizer(input, return_tensors='pt').to(accelerator.device)
                                    result = model.generate(
                                        **tokenized,
                                        eos_token_id=[151645],
                                        pad_token_id=tokenizer.vocab[tokenizer.special_tokens_map['pad_token']],
                                        max_new_tokens=max_tokens,
                                        temperature=temperature
                                    )
                                    output[i]['input'] = item[input_field]
                                    output[i]['shift'] = item['shift']
                                    output[i]['output'] = tokenizer.decode(result[0], skip_special_tokens=True)
                                    output[i]['gold'] = item[gold_field]
                            
                            with open(f'results-{experiment_id}.json', 'w') as file:
                                json.dump(output, file, ensure_ascii=False, indent=4)
                            
                            t.update(1)
                
                number_of_data = len(output)
                with open('config.txt', 'a') as file:
                    file.write(f'{experiment_id}\t{number_of_data}\t{type_of_plain_text}\t{prompt_type}\t{setting}\t{shot}\t{pretrained}\t{temperature}\t{max_tokens}\n')

    del model
    torch.cuda.empty_cache()
    time.sleep(2)