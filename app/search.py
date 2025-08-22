from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from app.md.prompts.prompt_read import load_md, prompt_invoke
load_dotenv()

llm = ChatOpenAI()

def search_handler():
    try:
        topic = load_md("topic")
        languages = prompt_invoke("language_finder")
        languages_by_topic = prompt_invoke("language_narrower", topic=topic)

        return {
            "languages": languages,
            "languages_by_topic": languages_by_topic,
            "topic": topic
        }
    except Exception as e:
        print(f"An error has occurred: {e}")
        raise