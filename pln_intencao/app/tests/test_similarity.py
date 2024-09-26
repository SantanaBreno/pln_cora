import pytest
import numpy as np
from app.predicao.similarity import check_vectors, pegar_similaridades

# Mock do modelo w2v com os métodos e atributos necessários
class MockModelW2V:
    def __init__(self):
        self.vector_size = 50  # Definindo o tamanho do vetor

    def __getitem__(self, key):
        return np.array([0.5] * self.vector_size)  # Retorna um vetor mock

    def __contains__(self, key):
        return True  # Assume que qualquer token está no modelo para fins de teste

# Instanciando o modelo mock
model_w2v = MockModelW2V()

def test_similaridade():
    previsao_exemplo = ["crédito"]
    tags = ['crédito', 'custódia', 'investidores profissionais', 'supervisão de securitização']
    
    try:
        class_vetor, tags_vetors = check_vectors(model_w2v, previsao_exemplo, tags)
        similaridades = pegar_similaridades(class_vetor, tags_vetors, tags)
        
        # Verifica se similaridades é uma lista
        assert isinstance(similaridades, list), "Esperava-se que similaridades fosse uma lista."
        
        # Verifica se a lista não está vazia
        assert len(similaridades) > 0, "A lista de similaridades está vazia."
        
        tags_resultantes = [tag for tag, _ in similaridades]
        
        # Verifica se 'crédito' está entre as tags retornadas
        assert 'crédito' in tags_resultantes, f"Esperava que 'crédito' estivesse presente nas similaridades, recebeu apenas: {tags_resultantes}"
    
    except Exception as e:
        pytest.fail(f"Erro ao calcular similaridades: {e}")
