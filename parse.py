# This file contains the code to parse the DOM content using Ollama
# It can also use other LLMs, but Ollama is used here for simplicity

from utils.llm_config import get_llm
from langchain_core.prompts import ChatPromptTemplate

# Define the prompt template
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}."
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

def parse_with_ollama(dom_chunks, parse_description):
    model = get_llm()  # Get configured LLM
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []
    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke(
            {"dom_content": chunk, "parse_description": parse_description}
        )
        print(f"Parsed batch: {i} of {len(dom_chunks)}")
        # Extract content from AIMessage or similar message types
        if hasattr(response, 'content'):
            parsed_results.append(response.content)
        else:
            parsed_results.append(str(response))

    return "\n".join(parsed_results)

