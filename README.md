# Towards Contamination Resistant Benchmarks

> **Abstract:** The rapid development of large language models (LLMs) has transformed the landscape of natural language processing. Evaluating these models properly is crucial for understanding their potential and addressing concerns such as safety. However, LLM evaluation is confronted by various factors, among which task contamination stands out as a key issue that undermines the reliability of evaluations. In this work, we introduce the concept of *task contamination resistance* to address this challenge. We show that a benchmark based on Caesar ciphers (e.g., "ab" &rarr; "bc" when the shift is 1), despite its simplicity, is an excellent example of a task contamination resistant benchmark. We test this benchmark on popular state-of-the-art LLMs under various settings. We find that current LLMs struggle with this seemingly simple benchmark, and our findings reveal substantial issues and raises important questions regarding their true capabilities. Our work contributes to the development of task contamination resistant benchmarks, enabling more rigorous LLM evaluation and offering insights into the true capabilities and limitations of LLMs.

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
