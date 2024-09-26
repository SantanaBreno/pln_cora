import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Função para vetorizar tokens
def vetorizar(tokens, modelo):
    vetores = [modelo[token] for token in tokens if token in modelo]

    if len(vetores) > 0:
        return np.mean(vetores, axis=0)
    else:
        return np.zeros(modelo.vector_size)

# Função para criar os vetores de classe e tags
def check_vectors(modelo, prediction, tags):
    class_vetor = vetorizar(prediction[0].split(), modelo)

    tags_vetors = np.array([vetorizar(tag.split(), modelo) for tag in tags])

    if np.all(class_vetor == 0):
        print("Erro: o vetor da classe é um vetor de zeros. A palavra pode não estar no vocabulário.")

    for tag, vetor in zip(tags, tags_vetors):
        if np.all(vetor == 0):
            print(f"Erro: o vetor da tag '{tag}' é um vetor de zeros. A palavra pode não estar no vocabulário.")
    
    return class_vetor, tags_vetors

# Função para pegar similaridades
def pegar_similaridades(class_vetor, tags_vetors, tags, n=5):
    similaridades = cosine_similarity([class_vetor], tags_vetors)[0]

    top_indices = np.argsort(similaridades)[-n:][::-1]

    top_tags = [tags[i] for i in top_indices]
    top_similaridades = [similaridades[i] for i in top_indices]

    return list(zip(top_tags, top_similaridades))
