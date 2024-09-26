# Arquivo para definir a validação dos dados de entrada
from pydantic import BaseModel

class InputData(BaseModel):
    text: str
