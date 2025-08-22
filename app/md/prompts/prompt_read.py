from langchain_openai import ChatOpenAI
from pathlib import Path

from dotenv import load_dotenv
from datetime import datetime


from app.utilities import log_prompt
load_dotenv()

llm = ChatOpenAI()

def prompt_invoke(prompt_name, **kwargs):
    try:
        prompt_dir_path = Path(__file__).resolve().parent / prompt_name
        prompt_template = ""
        with open(f"{prompt_dir_path}.md", "r", encoding="utf-8") as file:
            prompt_template = file.read()

        prompt = prompt_template.format(**kwargs)
        bnow = datetime.now()
        time_before_str = f"{bnow.hour:02d}{bnow.minute:02d}{bnow.second:02d}-{bnow.microsecond // 1000:02d}"

        prompt_result = llm.invoke(prompt)

        anow = datetime.now()
        time_after_str = f"{anow.hour:02d}{anow.minute:02d}{anow.second:02d}-{anow.microsecond // 1000:02d}"
        
        duration = (anow - bnow).total_seconds()
        timing = f"# Request took {duration:.3f} seconds."

        log_prompt(f"{timing}\n{prompt}", prompt_result.content, 0, f"{prompt_name}/{time_before_str}_{time_after_str}")
        return prompt_result.content
    except Exception as e:
        print(f"An error has ocurred while calling the prompt: {e}")
        raise


def load_md(md_name):
    try:
        prompt_dir_path = Path(__file__).resolve().parent / md_name
        md = ""
        with open(f"{prompt_dir_path}.md", "r", encoding="utf-8") as file:
            md = file.read()
        return md
    except Exception as e:
        print(f"An error has ocurred while calling the prompt: {e}")
        raise