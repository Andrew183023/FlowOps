from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

class Empresa(BaseModel):
    cnpj: str
    razao_social: str
    regime_tributario: str
    faturamento_anual: float
    funcionarios: int
    tem_filiais: bool

@app.post("/flowops/analisar")
def analisar_empresa(empresa: Empresa):
    prompt = f"""
    Realize uma análise tributária com sugestões de otimização fiscal.
    Dados:
    - Razão Social: {empresa.razao_social}
    - CNPJ: {empresa.cnpj}
    - Regime Tributário: {empresa.regime_tributario}
    - Faturamento Anual: R$ {empresa.faturamento_anual}
    - Funcionários: {empresa.funcionarios}
    - Tem Filiais: {"Sim" if empresa.tem_filiais else "Não"}
    """

    try:
        resposta = requests.post("http://flowmind:8001/api/ia/processar", json={"prompt": prompt})
        resposta_json = resposta.json()
        return {"resposta_da_flowmind": resposta_json.get("resposta", "Erro na resposta da IA")}
    except Exception as e:
        return {"erro": str(e)}
