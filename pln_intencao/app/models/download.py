# Código responsável por baixar os arquivos necessários para o funcionamento do modelo de PLN

from utils import download_from_s3, ensure_model_save_dir_exists
from config import model_url, tokenizer_url, vocab_url, config_url, cbow_s50_url, special_tokens_map_url, model_save_dir
import os

def save_files():
    ensure_model_save_dir_exists(model_save_dir)
    files = {
        'model.safetensors': model_url,
        'tokenizer_config.json': tokenizer_url,
        'vocab.txt': vocab_url,
        'config.json': config_url,
        'special_tokens_map.json': special_tokens_map_url,
        'cbow_s50.pkl': cbow_s50_url
    }

    for filename, url in files.items():
        save_path = os.path.join(model_save_dir, filename)
        download_from_s3(url, save_path)
        print(f"File {filename} saved to {save_path}")
