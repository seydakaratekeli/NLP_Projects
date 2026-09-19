"""
ducjducjgosearchrun, langchain kutuphanesi icerisinde gelen hazir bir arac
web aramasi yapmak icin duckduckgo motorunu kullan
"""

# eski: from langchain.tools import DuckDuckGoSearchRun
from langchain_community.tools import DuckDuckGoSearchRun
# duckduckgo arama aracinin bir ornegini olustur
search = DuckDuckGoSearchRun()

if __name__ == "__main__": # burasi sadece test icin, search_tool.py dosyasini direkt calistirmak icin
    
    # aranacak terimi belirle (ingilizce olmali)
    query = "What is the dolar/TL exchange rate?"

    # arama motoruna sorgu gonder ve sonucu al
    result = search.run(query)

    # arama sonucunu ekrana yazdir
    print(f"Arama sonucu: \n{result}")