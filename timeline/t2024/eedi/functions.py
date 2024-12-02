import pandas as pd
from tqdm import tqdm
import torch
import numpy as np

def make_all_question_text(df: pd.DataFrame) -> pd.DataFrame:
    df["all_question_text"] = df["ConstructName"] + "\n\n" + df["QuestionText"]
    return df
def make_all_text(df: pd.DataFrame) -> pd.DataFrame:
    df["all_text"] = df["all_question_text"] +" " +df["value"]
    return df
def prepare_inputs(text, tokenizer, device):
    tokenizer_outputs = tokenizer.batch_encode_plus(
        text,
        padding        = True,
        return_tensors = 'pt',
        max_length     = 1024,
        truncation     = True
    )
    result = {
        'input_ids': tokenizer_outputs.input_ids.to(device),
        'attention_mask': tokenizer_outputs.attention_mask.to(device),
    }
    return result
def convert2Embedding(texts,model, tokenizer,device, per_gpu_batch_size = 8,showProgress = True ):
    all_ctx_vector = []
    pr = lambda x: x
    if showProgress:
        pr = lambda x: tqdm(x)
    for mini_batch in pr(range(0, len(texts[:]), per_gpu_batch_size)):
        mini_context          = texts[mini_batch:mini_batch+ per_gpu_batch_size]
        encoded_input         = prepare_inputs(mini_context,tokenizer,device)
        sentence_embeddings   = model(**encoded_input)[0][:, 0]
        sentence_embeddings   = torch.nn.functional.normalize(sentence_embeddings, p=2, dim=1)
        all_ctx_vector.append(sentence_embeddings.detach().cpu().numpy())
    all_ctx_vector = np.concatenate(all_ctx_vector, axis=0)
    return all_ctx_vector
def prepare_dataset(df, test_per = 0.1):
    data = newWide2long(make_all_question_text(df)).dropna().reset_index()
    data = make_all_text(data)
    X = data[["SubjectId", "all_text"]]
    y = data.MisconV.tolist()
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_per, random_state=42)
    y_train = list(map(lambda x: [x], y_train))
    y_test = list(map(lambda x: [x], y_test))
    return (X_train, y_train), (X_test, y_test)
def score(actual, predicted, k =25):
    counted = set()
    hits = 0
    predicted = predicted[:k]
    res = 0
    for i, p in enumerate(predicted):
        if p in actual and p not in counted: 
            hits += 1
            res += hits / (i+1)
            counted.add(p)
    return res
def score_calc(yte, ypred):
    total = 0
    for ac, pr in zip(yte, ypred):
        total += score(ac, pr)
    accuracy = total/ len(ypred)
    return (accuracy)
def newWide2long(df):
    m1  = pd.melt(
        df[
            [
                "QuestionId", "SubjectId",
                "all_question_text",
                "CorrectAnswer",
                "AnswerAText",
                "AnswerBText",
                "AnswerCText",
                "AnswerDText",
                "MisconceptionAId",
                "MisconceptionBId",
                "MisconceptionCId",
                "MisconceptionDId"
            ]
        ],
        id_vars    = ["QuestionId", "SubjectId","all_question_text", "CorrectAnswer", 
                      "MisconceptionAId", "MisconceptionBId", "MisconceptionCId", "MisconceptionDId"],
        var_name   = 'Answer',
        value_name = 'value'
    )
    m2 = pd.melt(
        m1[
            [
                "QuestionId", "SubjectId",
                "all_question_text",
                "CorrectAnswer",
                "Answer", "value",
                "MisconceptionAId",
                "MisconceptionBId",
                "MisconceptionCId",
                "MisconceptionDId"
            ]
        ],
        id_vars    = ["QuestionId", "SubjectId","all_question_text", "CorrectAnswer", "Answer", "value"],
        var_name   = 'Miscon',
        value_name = 'MisconV'
    )
    return m2
