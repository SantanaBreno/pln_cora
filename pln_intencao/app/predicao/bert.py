#Arquivo responsável por realizar a predição de intenção
import torch

# Função para prever a intenção de um texto usando o modelo BERT
def bert_prever(model, tokenizer, texto, label_to_idx, max_length=128):
    real_encodings = tokenizer(texto, truncation=True, padding=True, max_length=max_length, return_tensors='pt')
    
    model.eval()
    
    with torch.no_grad():
        predictions = model(**real_encodings).logits
        predicted_labels = torch.argmax(predictions, dim=1)

    idx_to_label = {idx: label for label, idx in label_to_idx.items()}
    decoded_predictions = [idx_to_label[pred.item()] for pred in predicted_labels]

    return decoded_predictions
