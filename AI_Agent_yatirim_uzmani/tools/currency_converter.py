"""
-- bunu LLM kullanacak --
usd to try 
bir converter yapılacak ; usd -> TL
fonks üstüne @tool dekoratörü koyarak langchain kendi toollarına bakacak @toolu gördüğünde o fonksiyonu tool olarak kullanabilecek
100 usd yi gösterecek
CoinGeckodan güncel çevrim rate alınacak

# Genelleme yapmak istersek (farklı kurlar arası çevirim için) şunları değiştirelim:
#
# 1. Fonksiyon tanımını ve aldığı parametreleri değiştirelim:
# @tool
# def currency_converter(from_currency: str, to_currency: str, amount: float) -> str: 
#     ... 
#     try:
#         ...
#         # 2. URL'yi dinamik hale getirelim (f-string ile): 
#         url = f"https://api.exchangerate-api.com/v4/latest/{from_currency.upper()}"
#         ...
#         # 3. Kuru değişkene göre sözlükten alalım:
#         rate = data["rates"][to_currency.upper()]
#         ... 
#         # 4. Dönüş stringini güncelleyelim:
#         return f"{amount} {from_currency.upper()} = {result:.2f} {to_currency.upper()} (Kur: {rate})" 



"""
from langchain.tools import tool # bu dekoratör sayesinde fonksiyonumuz bir langchain araci (tool) olarak tanimlanabilecek
import requests # http istekleri yapmak icin gerkli olan kutuphane


@tool # @tool sayesinde convert_usd_to_try fonksiyonu langchain ahanlari tarafindan kullanilabilecek bir arac oldugu belirtilir
def convert_usd_to_try(amount: float) -> str:
    """
        usd miktarini try ye cevir
        amount parametresi sadece sayi olmali
    """
    try: 
        # eger kullanıcıdan gelen "amount" degeri bir string ise ornegin "100 usd" 
        # sayisal olmayan karakterleri cikarmak ve floata cevirmek
        if isinstance(amount, str):
            # rakamlar ve noktalari birakalim, diger karakterleri filtrele ve floata cevir
            amount = float("".join(filter(lambda c: c.isdigit() or c == ".", amount)))
        
        # ExchangeRate-API den guncel kurlari alalim
        url = "https://api.exchangerate-api.com/v4/latest/USD"

        # bu url e get istegi gonder
        response = requests.get(url)

        # eger api istegi basarisiz olursa ornegin 404 veya 500 seklinde
        if response.status_code != 200:
            return f"API hatasi. Kod: {response.status_code}"
        
        # api den donen json verisini dictionary olarak alalim
        data = response.json()

        # dictionary icerisinden dolarin rate degerini alalim
        rate = data["rates"]["TRY"]

        # kullanicinin verdigi amount ile doviz kurunu carpalim
        result = amount*rate

        # "100 usd = 4000 TRY (Kur: 40)"
        return f"{amount} usd = {result:.2f} TRY (Kur: {rate:.2f})"
    except Exception as e:
        return f"convert_usd_to_try: Hata olustu: {e}"

if __name__ == "__main__":

    # test etmek icin 100 dolar yazalim
    test_amount = 100

    print(f"{test_amount} USD -> TRY")

    print(convert_usd_to_try.run({"amount":test_amount}))
    


