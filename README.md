# Towards Contamination Resistant Benchmarks

> **Abstract:** The rapid development of large language models (LLMs) has transformed the landscape of natural language processing. Evaluating LLMs properly is crucial for understanding their potential and addressing concerns such as safety. However, LLM evaluation is confronted by various factors, among which contamination stands out as a key issue that undermines the reliability of evaluations. In this work, we introduce the concept of *contamination resistance* to address this challenge. We propose a benchmark based on Caesar ciphers (e.g., "ab" &rarr; "bc" when the shift is 1), which, despite its simplicity, is an excellent example of a contamination resistant benchmark. We test this benchmark on widely used LLMs under various settings, and we find that these models struggle with this benchmark when contamination is controlled. Our findings reveal issues in current LLMs and raise important questions regarding their true capabilities. Our work contributes to the development of contamination resistant benchmarks, enabling more rigorous LLM evaluation and offering insights into the true capabilities and limitations of LLMs.

## A benchmark based on Caesar ciphers
Data location: [data/](data/)

## Inference
* Implementation for GPT-4o: [inference-azure.ipynb](inference-azure.ipynb)
* Implementation for local models: [inference-local.py](inference-local.py)
* Configuration file: [config.txt](config.txt)
* Raw outputs: [results/](results/)

## Evaluation

### Implementation
Code: [evaluation.ipynb](evaluation.ipynb)

### Evaluation scores
* Scores for GPT-4o: [evaluation_scores_gpt-4o.csv](evaluation_scores_gpt-4o.csv)
* Scores for LLaMA3.1 models: [evaluation_scores_llama.csv](evaluation_scores_llama.csv)
* Scores for Qwen models: [evaluation_scores_qwen.csv](evaluation_scores_qwen.csv)
* Scores for tokens in different positions: [evaluation_scores_position.csv](evaluation_scores_position.csv)

## Disclaimer
This repository contains experimental software and is published for the sole purpose of giving additional background details on the respective publication.
