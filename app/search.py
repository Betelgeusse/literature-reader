from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from app.md.prompts.prompt_read import load_md, prompt_invoke
from app.utilities import log_file
load_dotenv()

llm = ChatOpenAI()

def search_handler():
    try:
        topic = load_md("topic")
        languages = prompt_invoke("language_finder")
        languages_by_topic = prompt_invoke("language_narrower", topic=topic)

        language_results = []
        languages_visited = []
        for language in languages_by_topic.split(","):
            newr = {}
            newr["language"] = language
            newr["references"] = prompt_invoke("search", topic=topic, language=language)
            language_results.append(newr)
            languages_visited.append(language.lower().replace('.', '').replace(',', ''))

        less_trust_language_results = []
        for language in languages.split(","):
            newr = {}
            if language.lower().replace('.', '').replace(',', '') in languages_visited:
                continue
            newr["language"] = language
            newr["references"] = prompt_invoke("search", topic=topic, language=language)
            less_trust_language_results.append(newr)

        result  = f"# Tema de investigación: \n"
        result += f"{topic}\n\n"
        result += f"## Idiomas naturales en los que la IA conoce publicaciones verificables por identificación ISBN\n"
        result += f"{str(languages)}\n\n"
        result += f"## Idiomas en los que la IA conoce publicaciones relacionadas al tema '{topic}' verificables por identificación ISBN\n"
        result += f"{languages_by_topic}\n\n"

        result += "# Referencias de mayor confianza\n\n\n"
        for lr in language_results:
            result += f"### Referencias en {lr["language"]}:\n{lr["references"]}\n\n"

        result += "# Referencias de menor confianza\n\n\n"
        for lr in less_trust_language_results:
            result += f"### Referencias en {lr["language"]}:\n{lr["references"]}\n\n"

        log_file(result, "result")

        return {
            "languages": languages,
            "languages_by_topic": languages_by_topic,
            "topic": topic
        }
    except Exception as e:
        print(f"An error has occurred: {e}")
        raise