from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from .prompts import job_summarization, cv_maker, motivation_writer
from .db import readAsDic, readWhere, addData, updateData

MODEL = "gemma3n:e4b" # gemma3:4b deepseek-r1:1.5b deepseek-r1:7b
TEMPERATURE = 0.2
candidate_profile_info = ""

def runModel(prompt, model = MODEL, temperature = TEMPERATURE, **params ):
    llm = ChatOllama(model=model, temperature=temperature, **params)
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content

def get_candidate_profile_info():
    return candidate_profile_info

def generateAndReadCV(jobId, regenerate = False):
    job = readAsDic("Job", jobId)
    cv = readWhere("JobCV", {"job": jobId})
    def generate(job):
        content = job["summary"]
        if content is None:
            content = job["description"]
        res = runModel(cv_maker.format(job_summarization = content, candidate_profile_info = candidate_profile_info))
        return res
    if len(cv) > 0:
        if not regenerate:
            return cv[0]["content"]
        else: 
            res = generate(job)
            updateData("JobCV",cv[0]["id"], {"content": res, "all_content": res})
            return res
    else:
        res = generate(job)
        addData("JobCV", {"job_id": jobId, "all_content": res, "content": res})
        return res

def generateAndReadMotivation(jobId):
    prompt = motivation_writer.format(job_description = jobId)
    return runModel(prompt)

def generateAndReadSummary(jobId, regenerate = False):
    job = readAsDic("Job", jobId)
    summary = job["summary"]
    if summary is not None and not regenerate:
        return summary
    res = runModel(job_summarization.format(job_description = job["description"]))
    updateData("Job", jobId, {"summary": res})
    return res