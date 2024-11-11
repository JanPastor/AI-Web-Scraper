from langchain_ollama import OllamaLLM
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
import os

load_dotenv()

LLM_TYPE = os.getenv("LLM_TYPE", "ollama")
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.1")

def get_llm():
    """Factory function to create LLM instance based on configuration"""
    if LLM_TYPE == "ollama":
        return OllamaLLM(model=LLM_MODEL)
    elif LLM_TYPE == "openai":
        if not LLM_API_KEY:
            raise ValueError("OpenAI API key not found in environment variables")
        return ChatOpenAI(api_key=LLM_API_KEY, model_name=LLM_MODEL)
    elif LLM_TYPE == "anthropic":
        if not LLM_API_KEY:
            raise ValueError("Anthropic API key not found in environment variables")
        return ChatAnthropic(api_key=LLM_API_KEY, model_name=LLM_MODEL)
    else:
        raise ValueError(f"Unsupported LLM type: {LLM_TYPE}") 