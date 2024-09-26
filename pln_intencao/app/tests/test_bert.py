import pytest
from unittest.mock import MagicMock
import torch
from app.predicao.bert import bert_prever

@pytest.fixture
def mock_tokenizer():
    mock = MagicMock()
    mock.return_value = {
        'input_ids': torch.tensor([[1, 2, 3]]),
        'attention_mask': torch.tensor([[1, 1, 1]])
    }
    return mock

@pytest.fixture
def mock_model():
    mock = MagicMock()
    mock.return_value = MagicMock()
    mock.return_value.logits = torch.tensor([[0.1, 0.9]])
    return mock

def test_bert_prever(mock_tokenizer, mock_model):
    texto = "Texto teste"
    label_to_idx = {'label1': 0, 'label2': 1}
    
    mock_model.return_value.logits = torch.tensor([[0.1, 0.9]])
    
    predicted_labels = bert_prever(mock_model, mock_tokenizer, texto, label_to_idx)

    assert predicted_labels == ['label2']

    mock_tokenizer.assert_called_once_with(
        texto,
        truncation=True,
        padding=True,
        max_length=128,
        return_tensors='pt'
    )

    mock_model.assert_called_once_with(
        input_ids=mock_tokenizer.return_value['input_ids'],
        attention_mask=mock_tokenizer.return_value['attention_mask']
    )
