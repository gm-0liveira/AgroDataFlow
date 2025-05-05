import pandas as pd

def extract_ibge():
    url = "https://apisidra.ibge.gov.br/values/t/5457/n1/all/v/214/p/all/c782/40124"
    df = pd.read_json(url)
    df.to_csv("data/raw/ibge_producao.csv", index=False)
    print("IBGE data saved.")

if __name__ == "__main__":
    extract_ibge()
