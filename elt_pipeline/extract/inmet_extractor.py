import requests, zipfile, io

def extract_inmet():
    url = "https://portal.inmet.gov.br/uploads/dadoshistoricos.zip"
    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall("data/raw/inmet/")
    print("INMET data extracted.")

if __name__ == "__main__":
    extract_inmet()
