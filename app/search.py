from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from app.md.prompts.prompt_read import load_md, prompt_invoke
from app.utilities import log_file
load_dotenv()

llm = ChatOpenAI()

def asterisk_list_to_strings(text):
    lines = text.strip().split('\n')
    items = [line.strip('* ').strip() for line in lines if line.strip().startswith('*')]
    return items

def clean_language(language):
    return language.lower().replace('.', '').replace(',', '')

def search_handler():
    try:
        topic = load_md("topic")
        languages = prompt_invoke("language_finder")
        languages_by_topic = prompt_invoke("language_narrower", topic=topic)

        language_results = []
        languages_visited = []
        for language in languages_by_topic.split(","):
            references_list = prompt_invoke("search", topic=topic, language=language)
            listed_items = asterisk_list_to_strings(references_list)

            citations_list = []
            for citation in listed_items:
                verification = prompt_invoke("reference_verify", topic=topic, citation=citation)
                if verification == "False":
                    continue
                citations_list.append({
                    "citation": citation,
                    "translation": prompt_invoke("translator", citation=citation),
                    "verification": verification
                })
            language_results.append({ "language": language, "citations": citations_list })
            languages_visited.append(clean_language(language))

        less_trust_language_results = []
        for language in languages.split(","):
            if clean_language(language) in languages_visited:
                continue
            
            references_list = prompt_invoke("search", topic=topic, language=language)
            listed_items = asterisk_list_to_strings(references_list)

            citations_list = []
            for citation in listed_items:
                verification = prompt_invoke("reference_verify", topic=topic, citation=citation)
                if verification == "False":
                    continue
                citations_list.append({
                    "citation": citation,
                    "translation": prompt_invoke("translator", citation=citation),
                    "verification": verification
                })
            less_trust_language_results.append({ "language": language,"citations": citations_list })
            languages_visited.append(clean_language(language))

        result  = f"# Tema de investigación: \n"
        result += f"{topic}:\n"
        result += f"* Poema, cuento o cualquier forma de texto literario (preferentemente poesía), cuya temática principal sea la muerte de una mascota, específicamente un perro (perro o perra, no importa el sexo).\n* Ensayos, artículos o estudios que hayan tratado la muerte de un animal, o la muerte de una mascota en la literatura. No importa la fecha de publicación. Es prioritaria la temática. Pueden ser poemas, literatura, ensayos, artículos, tesinas, tesis, etc.\n\n"
        result += f"## Idiomas naturales en los que la IA conoce publicaciones literarias verificables, ya sea por isbn, revistas, libros, articulos, etc.\n"
        result += f"{str(languages)}\n\n"
        result += f"## Idiomas en los que la IA conoce publicaciones relacionadas al tema '{topic}' verificables ya sea por isbn, revistas, libros, articulos, etc.\n"
        result += f"{languages_by_topic}\n\n"

        result += "# Referencias de mayor confianza\n\n\n"
        for lr in language_results:
            result += f"### Referencias en {lr["language"]}:\n"
            for citation in lr["citations"]:
                result += f"#### {citation["citation"]}\n\n"
                result += f"Verificación automática de la referencia: {citation["verification"]}\n\n"
                if clean_language(lr["language"]) != "español":
                    result += f"Traducción al español: '{citation["translation"]}'\n\n"

        result += "# Referencias de menor confianza\n\n\n"
        for lr in less_trust_language_results:
            result += f"### Referencias en {lr["language"]}:\n"
            for citation in lr["citations"]:
                result += f"#### {citation["citation"]}\n\n"
                result += f"Verificación automática de la referencia: {citation["verification"]}\n\n"
                if clean_language(lr["language"]) != "español":
                    result += f"Traducción al español: '{citation["translation"]}'\n\n"

        log_file(result, "result")

        return {
            "languages": languages,
            "languages_by_topic": languages_by_topic,
            "topic": topic
        }
    except Exception as e:
        print(f"An error has occurred: {e}")
        raise