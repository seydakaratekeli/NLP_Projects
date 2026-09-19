"""
finnhub api ile hisse senedi bilgilerini alalim
api_key: https://finnhub.io/dashboard
"""

from langchain.tools import tool # langchainin agent sisteminde kullanilacak fonksiyonlari tanimlamak icin kullanilan "tool" dekorator
import requests # http istekleri icin kullanilan kutuphane
import os 
from dotenv import load_dotenv

load_dotenv() # .env dosyasinin yukleyetek icerisindeki api anahtarini erisilebilir hale getirir

# fonksiyonu ai agent yapısında tool olarak kullanabilir
@tool # langchain tarafindan kullanilacak olan get_stock_info fonksiyonunu isaretler
def get_stock_info(ticker: str) -> str:
    
    """
        bir hisse senedi sembolu (orn: AAPL) icni guncel fiyat bilgis doner
        Parametre:
            ticker (str): hisse senedinin sembolu (orn: "AAPL", "GOOGL")
        Output:
            str: guncel hisse bilgilerini iceren metin
    """
    try:
        # LLM'in fazladan metin veya tırnak göndermesine karşın sadece ilk kelimeyi alalım
        ticker = ticker.split()[0].strip("\"'()[]{}., ")
        
        # .env dosyasindan Finnhub api anahtarini al
        api_key = os.getenv("FINNHUB_API_KEY")

        # eger api anhatari yoksa kullaniciya hata mesajı return et
        if not api_key:
            return "API anahtari bulunamadi."
        
        # Finnhub api dan belirli bir hisse senedi icin fiyat bilgilerini alan url tanimla
        url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={api_key}" 

        #hisseyi değiştirmek için ticker parametresi değiştirilmeli
        
        # API ye get istegi gonder
        response = requests.get(url)

        # eger istek basarisiz ise (403, 404, 500 vs)
        if response.status_code != 200: 
            return f"API hatasi: {response.status_code}"
        
        # API den gelen yaniti coz
        data = response.json()

        # json icinden guncel fiyat (c), acilis fiyati (o), en yuksek fiyat (h), en dusuk fiyat (l)
        current = data.get("c") # current price
        open_ = data.get("o") # opening price
        high = data.get("h")  # day's high price
        low = data.get("l") # day's low

        return (
            f"{ticker} Hisse Bilgisi: \n"
            f"- Guncel Fiyat: {current} USD\n"
            f"- Açılış: {open_} USD\n"
            f"- Gün içi en yüksek: {high}\n"
            f"- Gün için en düşük: {low}\n"
        )
    except Exception as e:
        return f"get_stock_info: Hata oluştu: {e}"
    
if __name__ == "__main__":
    print(get_stock_info.run({"ticker": "GOOGL"}))