from schemas.input_data import InputData
from models.load_models import load_bert_model, load_pickle_file
from predicao.bert import bert_prever
from predicao.similarity import check_vectors, pegar_similaridades
from predicao.extraction import encontrar_datas, extrair_reguladores, texto_para_minusculo
from config import model_save_dir
from dotenv import load_dotenv
import os
from models.download import save_files 
import pika
import json


print('MODEL SAVE DIR', model_save_dir)

load_dotenv()

rabbitmq_url = os.getenv("RABBITMQ_URL")

def connect_to_rabbit():
    params = pika.URLParameters(rabbitmq_url)
    connection = pika.BlockingConnection(params)
    return connection

# Verifica se a pasta 'modelo' já existe, caso contrário, chama a função save_files
if not os.path.exists(model_save_dir):
    print(f"A pasta '{model_save_dir}' não existe. Baixando arquivos necessários...")
    save_files()
else:
    print(f"A pasta '{model_save_dir}' já existe. Pulando o download dos arquivos.")

# Carregando modelo e tokenizer
model, tokenizer = load_bert_model(model_save_dir)

# Carregando arquivos pickle
label_to_idx = load_pickle_file('label_to_idx.pkl')
model_w2v = load_pickle_file('./modelo/cbow_s50.pkl')

# Tags predefinidas
tags = ['crédito', 'custódia', 'Resolução CVM 175', 'investidores profissionais', 'cedente', 'Banking as a Service', 'CCBs', 'gestão de fundos', 'supervisão de securitização']


def callback(ch, method, properties, body):
    text = body.decode()

    print(f"[x] Texto recebido do Core: {text}")

    # Prevendo a intenção
    previsao = bert_prever(model, tokenizer, text, label_to_idx)
    
    # Vetorização e cálculo de similaridade
    class_vetor, tags_vetors = check_vectors(model_w2v, previsao, tags)
    top_similaridades = pegar_similaridades(class_vetor, tags_vetors, tags)

    # Extração de datas e reguladores
    datas = encontrar_datas(text)
    texto_minusculo = texto_para_minusculo(text)
    reguladores = extrair_reguladores(texto_minusculo)

    data = {
        "tema": previsao,
        "data_expedicao": datas,
        "regulador": reguladores,
        "tags": top_similaridades
    }
    
    data_json = json.dumps(data)
    print(f"dado enviado para o core: {data_json}")

    connection = connect_to_rabbit()
    channel = connection.channel()
    channel.queue_declare(queue='core_queue', durable=True)
    channel.basic_publish(exchange='', routing_key='core_queue', body=data_json)


def start_listening():
    connection = connect_to_rabbit()
    channel = connection.channel()
    channel.queue_declare(queue='pln_queue', durable=True)
    channel.basic_consume(queue='pln_queue', on_message_callback=callback, auto_ack=True)
    print('[*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

start_listening()
