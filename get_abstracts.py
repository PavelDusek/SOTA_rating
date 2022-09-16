# coding: utf-8
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

df = pd.read_csv("sota.csv")
url = "https://pubmed.ncbi.nlm.nih.gov/"

for i, row in df.iterrows():
    if (i > 138):
        print(i)
        pid = row['pubmed_id']
        r = requests.get(url + f"{pid}")
        s = BeautifulSoup(r.text, "html.parser")
        text = s.find("div", attrs={"id": "abstract"}).prettify()
        with open(f"abstracts/{i}.txt", "w") as f:
            f.write(text)
        time.sleep(5)
