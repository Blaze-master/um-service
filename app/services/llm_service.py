from langchain_core.prompts import PromptTemplate
from langchain.chat_models import init_chat_model
from ..config import get_settings


def prompt_llm(prompt, params):
    settings = get_settings()
    prompt = PromptTemplate.from_template(prompt).invoke(params)
    llm = init_chat_model(settings.model_name,model_provider=settings.model_provider, api_key=settings.model_api_key)
    return llm.invoke(prompt).content