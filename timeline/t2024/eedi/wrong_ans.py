from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from basic import Main as ObjMaker
from timeline.t2024.eedi.filterer  import MisConceptsFilterer
from timeline.t2024.eedi.visualizer import EediView
from useful.jupyterDB import jupyterDB

def WrongAns():
    ev = EediView()
    ev.process.globalState = jupyterDB._params
    ev.handlers.load()
    mcf = MisConceptsFilterer()
    customCss = Utils.get_comp({}, ComponentsLib.CSSAdder)
    classes = ['.w-min-50{', '    min-width: 50% ', '}']
    classes = "\n".join(classes)
    customCss.outputs.layout.content = classes
    btn1 = Utils.get_comp({"description":"A"}, IpywidgetsComponentsEnum.Button, className = "w-auto")
    btn2 = Utils.get_comp({"description":"B"}, IpywidgetsComponentsEnum.Button, className = "w-auto")
    btn3 = Utils.get_comp({"description":"C"}, IpywidgetsComponentsEnum.Button, className = "w-auto")
    btns = [btn1, btn2, btn3]
    btnsWid = Utils.container(btns)
    mcf.views.container.outputs.layout.add_class("flex")
    mcf.views.container.outputs.layout.add_class("flex-column")
    container = Utils.container([ev.views.container, Utils.container([btnsWid, mcf.views.container], className="flex flex-column"), customCss])
    mcf.process.oe.views.mainSection.outputs.layout.remove_class("w-50")
    ev.views.container.outputs.layout.add_class("w-min-50")
    s = ObjMaker.uisOrganize(locals())
    return s
def CosineSimilarity():
    import numpy as np
    from timeline.t2024.eedi.functions import prepare_inputs
    from sklearn.metrics.pairwise import cosine_similarity
    parent = None
    from transformers import AutoTokenizer, AutoModel
    import torch
    def loadModel(model_path):
        s.process.model_path = model_path
        device    = "cuda:0"
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model     = AutoModel.from_pretrained(model_path)
        model.eval()
        model.to(device)
        s.process.tokenizer = tokenizer
        s.process.model = model
        s.process.device = device
    def set_up(given=False):
        wa = s.process.parent
        if not given:
            s.process.allMisConceptions = wa.process.ev.process.mis_map.MisconceptionName.to_numpy()
            s.process.categories_classes = s.handlers.convert2Embedding(s.process.allMisConceptions.tolist(), s.process.model, 
                                                                        s.process.tokenizer, s.process.device)
        wa.process.ev.process.page.handlers.selectWithVal = s.handlers.onSelected
        wa.views.btnsWid.handlers.handle = s.handlers.onOptionClicked
        s.handlers.onSelected(1)
    def onSelected(val):
        wa = s.process.parent
        s.process.current_index = int(val) - 1
        wa.process.ev.process.prev_handlers.selectWithVal(val)
        wa.process.ev.handlers.onRendered(val)
        s.process.current_question = wa.process.ev.process.train.iloc[s.process.current_index].to_dict()
        labels =s.handlers.wrongAnswerOptions()
        for i, b in enumerate(wa.process.btns):
            b.outputs.layout.description = labels[i]
    def convert2Embedding(texts,model, tokenizer,device, per_gpu_batch_size = 8, ):
        all_ctx_vector = []
        for mini_batch in range(0, len(texts[:]), per_gpu_batch_size):
            mini_context          = texts[mini_batch:mini_batch+ per_gpu_batch_size]
            encoded_input         = prepare_inputs(mini_context,tokenizer,device)
            sentence_embeddings   = model(**encoded_input)[0][:, 0]
            sentence_embeddings   = torch.nn.functional.normalize(sentence_embeddings, p=2, dim=1)
            all_ctx_vector.append(sentence_embeddings.detach().cpu().numpy())
        all_ctx_vector = np.concatenate(all_ctx_vector, axis=0)
        return all_ctx_vector
    def onOptionClicked(w):
        wa = s.process.parent
        col = w.description
        allText = s.handlers.get_all_text(col)
        wa.process.mcf.process.oe.views.outputDisplayer.outputs.layout.clear_output()
        with wa.process.mcf.process.oe.views.outputDisplayer.outputs.layout:
            emb = s.handlers.convert2Embedding([allText], s.process.model, s.process.tokenizer, s.process.device)
            test_cos_sim_arr = cosine_similarity(emb, s.process.categories_classes)
            test_sorted_indices = np.argsort(-test_cos_sim_arr, axis=1)
            misc = list(zip(s.process.allMisConceptions[test_sorted_indices[0]], test_sorted_indices[0]))
            wa.process.mcf.process.oe.views.lister.outputs.layout.options = misc
    def get_all_text(option):
        qu = s.process.current_question
        allText = qu["ConstructName"] + "\n\n" + qu["QuestionText"] + " " + qu[option]
        return allText
    def wrongAnswerOptions():
        qu = s.process.current_question
        res = []
        for i in "ABCD":
            if qu["CorrectAnswer"] != i:
                res.append(f"Answer{i}Text")
        return res

    s = ObjMaker.variablesAndFunction(locals())    
    return s
class Main:
    def similarity():
        cs = CosineSimilarity()
        cs.handlers.loadModel(r"C:\Users\rajab\Desktop\stuffs\global\files\models\bge-small-en-v1.5-transformers-bge-v2")
        cs.process.parent = wa
        cs.handlers.set_up(False)
        return cs