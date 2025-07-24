from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from useful.basic import Main as ObjMaker
from timeline.t2024.generic_logger.generic_loggerV3 import Pagination
import pandas as pd
import os
from IPython.display import display, HTML
from pylatexenc.latex2text import LatexNodes2Text

def EediView():
    label = Utils.get_comp({"value": "Display the question"},IpywidgetsComponentsEnum.Label, className = "w-auto", bind=False)
    renderLatex = Utils.get_comp({"indent":False, "description": "render latex"}, IpywidgetsComponentsEnum.Checkbox, className="w-auto")
    page = Pagination()
    
    outArea = Utils.get_comp({}, IpywidgetsComponentsEnum.Output, bind=False)
    container = Utils.container([label, renderLatex, page.views.container, outArea], className="flex flex-column")
    path = None
    prev_handlers = ObjMaker.namespace()
    globalState = {}
    def set_filepath_root(path):
        s.process.trainPath = path + os.sep + "train.csv"
        s.process.misPath = path + os.sep + "misconception_mapping.csv"
        s.process.path = path
    def load():
        s.process.train = pd.read_csv(s.process.trainPath)
        s.process.mis_map = pd.read_csv(s.process.misPath)
        misTable = {}
        for i in range(s.process.mis_map.shape[0]):
            misTable[s.process.mis_map.MisconceptionId.values[i]] = s.process.mis_map.MisconceptionName.values[i]
        s.process.misTable = misTable
        s.process.page.handlers.update_total_pages(len(s.process.train))
        s.process.globalState["eedi"] = s 
        
    def onQuestionSelected(val):
        s.process.prev_handlers.selectWithVal(val)
        s.handlers.onRendered(val)
    def onRendered(wid):
        val = int(s.process.page.vals.currentBtnSelected.outputs.layout.description)
        s.views.outArea.outputs.layout.clear_output()
        index = int(val) - 1
        s.process.globalState["current_task"] = s.process.train.iloc[index]
        with s.views.outArea.outputs.layout:
            display(s.handlers.generate_html(s.process.train.iloc[index],index, not s.views.renderLatex.outputs.layout.value))
    def generate_html(questionRow, index,lat2text=1):
        question = questionRow.QuestionText
        if lat2text==1 :
            question = LatexNodes2Text().latex_to_text(question)
        correct_answer = questionRow.CorrectAnswer
        construct_name = questionRow.ConstructName
        subject_name = questionRow.SubjectName
        fontSize = 12
        html = f"""
        <div style='font-family: Arial, sans-serif; border: 1px solid #007bff; padding: 15px; border-radius: 10px; margin: 0 auto; background-color: #f4f9ff;'>
            <div style='font-size: {fontSize}px; color: #007bff;'><strong>Subject Name:</strong> {subject_name}</div>
            <div style='font-size: {fontSize}px; color: #007bff;'><strong>Construct Name:</strong> {construct_name}</div>
            
            <hr style='border: 1px solid #007bff; margin: 10px 0;'>
            <div style='font-size: {fontSize+2}px; font-weight: bold; color: #ff6f61;'>Problem:</div>
            <div style='font-size: {fontSize+4}px; color: #333; '>{question.replace("\n", "<br>")}</div>
            <ul style='list-style-type: none; padding: 0;'>
        """
        option_letters = ['A', 'B', 'C', 'D']
        
        for opt in "ABCD":
            color = "#e0f2ff"
            if opt == correct_answer:
                color = "#ace4b9"
            html += f"""
            <li style='background-color: {color}; padding: 3px; margin: 2px 0; border-radius: 5px;'>
                <span style='font-weight: bold; color: #007bff;'>{opt}.</span> {questionRow[f'Answer{opt}Text']}
            </li>
            """
        html += f"""</ul> <hr style='border: 1px solid #007bff; margin: 10px 0;'>"""
    
        for opt in "ABCD":
            misId = questionRow[f'Misconception{opt}Id']
            if opt != correct_answer and not pd.isna(misId):
                html += f""" <div style='font-size: {fontSize}px; color: #333;'><strong>Misconception {opt}:</strong> {int(misId)} - {s.process.misTable[misId.astype(int)]}</div> \n"""
        html += f"""</div>"""
        return (HTML(html))
    prev_handlers.selectWithVal = page.handlers.selectWithVal
    page.handlers.selectWithVal = onQuestionSelected
    renderLatex.handlers.handle = onRendered
    s = ObjMaker.uisOrganize(locals())
    set_filepath_root(r"C:\Users\rajab\Downloads\eedi-mining-misconceptions-in-mathematics")
    return s