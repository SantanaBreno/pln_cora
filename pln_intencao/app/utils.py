# Funções para download de arquivos e garantir diretório de salvamento do modelo
import os
import requests

def download_from_s3(file_url: str, save_path: str):
    response = requests.get(file_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
    else:
        raise Exception(f"Failed to download file from {file_url}")

def ensure_model_save_dir_exists(model_save_dir: str):
    if not os.path.exists(model_save_dir):
        os.makedirs(model_save_dir)
