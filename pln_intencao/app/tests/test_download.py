import pytest
import os
from unittest.mock import patch
from app.utils import download_from_s3

@patch("requests.get")
def test_download_from_s3(mock_get):
    class MockResponse:
        def __init__(self, status_code, content):
            self.status_code = status_code
            self.content = content

    mock_get.return_value = MockResponse(200, b"conteudo_teste")
    
    save_path = 'test_model_file.txt'
    download_from_s3('url', save_path)

    assert os.path.exists(save_path)
    with open(save_path, 'rb') as f:
        content = f.read()
    assert content == b"conteudo_teste"
    os.remove(save_path)
