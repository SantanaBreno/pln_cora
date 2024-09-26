# Arquivo responsável por carregar os modelos

from transformers import BertTokenizer, BertForSequenceClassification
# import torch
import pickle

def load_bert_model(model_save_dir):
    model = BertForSequenceClassification.from_pretrained(model_save_dir)
    tokenizer = BertTokenizer.from_pretrained(model_save_dir)
    return model, tokenizer

def load_pickle_file(filepath: str):
    with open(filepath, 'rb') as f:
        return pickle.load(f)
