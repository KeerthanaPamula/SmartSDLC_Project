import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from app import prompts
import os
import PyPDF2

model = None
tokenizer = None
llm_pipeline = None

def load_model():
    global model, tokenizer, llm_pipeline
    if model is None:
        model_id = "ibm-granite/granite-3.3-2b-instruct"
        tokenizer = AutoTokenizer.from_pretrained(model_id, token=os.getenv("HF_TOKEN"))
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            device_map="auto",
            torch_dtype=torch.bfloat16,
            token=os.getenv("HF_TOKEN")
        )
        llm_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=512, temperature=0.7)

def extract_text_from_pdf(pdf_file_path):
    with open(pdf_file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        return "\n".join(page.extract_text() for page in reader.pages)

def generate_response(prompt):
    if llm_pipeline is None:
        load_model()
    formatted = f"<|user|>\n{prompt}<|endoftext|>\n<|assistant|>"
    result = llm_pipeline(formatted)
    return result[0]["generated_text"].split("<|assistant|>")[-1].strip()

def analyze_requirements(text_input, pdf_path=None):
    content = extract_text_from_pdf(pdf_path) if pdf_path else text_input
    if not content.strip():
        return "Please provide a project description in the text box or upload a PDF."
    prompt = prompts.REQUIREMENT_ANALYSIS_PROMPT.format(project_description=content)
    return generate_response(prompt)

def generate_code(requirements, language, framework):
    if not all([requirements.strip(), language.strip(), framework.strip()]):
        return "Please provide requirements, a language, and a framework."
    prompt = prompts.CODE_GENERATION_PROMPT.format(language=language, framework=framework, requirements=requirements)
    return generate_response(prompt)

def generate_tests(context):
    if not context.strip():
        return "Please provide requirements or code to generate tests for."
    prompt = prompts.TEST_CASE_GENERATION_PROMPT.format(context=context)
    return generate_response(prompt)
