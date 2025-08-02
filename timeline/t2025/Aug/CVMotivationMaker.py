from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama

MODEL = "gemma3n:e4b" # gemma3:4b deepseek-r1:1.5b deepseek-r1:7b
TEMPERATURE = 0.2


def runModel(prompt, model = MODEL, temperature = TEMPERATURE, **params ):
    llm = ChatOllama(model=model, temperature=temperature, **params)
    response = llm.invoke([HumanMessage(content=prompt)])
    return response
    
