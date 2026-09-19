"""
AI Agent ile Yatırım Uzmanı

problem tanimi: doğal dilde yazılmış yatırım sorularını anlayıp, 
                doğru kaynaklardan bilgi toplayarak yatırımcıya net, özet ve güncel yanıtlar sunabilen 
                akıllı bir yatırım danışmanı
                - dolar bugün kaç tl
                - apple hissesi ne kadar
                - altın hakkında son haberler nedir?
                - tesla hissesi mi apple hissesi mi?

hedefler: 
- kullanıcından gelen doğal dil sorularını analiz etmek
- gerekli olması durumunda internetten arama yapmak, kur çevirisi gerçekleştirmek, hisse bilgisi almak
- bilgileri birleştirmek, özetlemek ve sadece bir dilde yazmak
- bunları profesyonel bir dil ile yapmak

teknolojiler:
- langchain: agent, tool, llm kontrolu ve iş akışı sağlamak
- openai: llm modeli (gpt-3.5-turbo)
- CoinGecko API: USD -> TRY kur çevrimi, kayıt gerekmez, api key gerekmez, ücretsiz
- Finnhub: Hisse senedi verileri, api key alalim, 
- DuckDuckGo: arama motoru, api gerekmez

plan/program:
- tool'ları ayarla: DuckDuckGo(arama motoru ile arama), CoinGecko api (kur çevirme), Finnhub api (hisse senedi bilgileri)
- llm modeli olustur
- agent olustur (merkezde dil modeli çevresinde tools ) LLM + Tools = Agent , LLM + DB =RAG
- agent ile kullanıcıdan gelen soruları cevapla

install libraries: freeze

Sonrasında eklenebilecekler: 
- memory ekle
- streamlit/fastapi 
- plan and execute- ajan ne yapacağını planlıyor birden fazla executede ise planlayıp gerçekleştiriyor şu an ki yapısının bir tık ötesi
- rag
"""
from langchain_openai import ChatOpenAI # openai sohbet modulu icin langchanin ara birimi

from langchain_classic.agents import initialize_agent, AgentType # langchain ajanini baslatmak icin gerekli olan fonksiyon ve ajanin turunu

from tools.search_tool import search # daha once tanimladigimiz duckduckgo araci
from tools.currency_converter import convert_usd_to_try # tanımladığımız doviz cevirme araci
from tools.market_api import get_stock_info #tanımladığımız  hisse senedi bilgilerini alan arac

from dotenv import load_dotenv
import os

from langchain_classic.prompts import PromptTemplate # kisisellesitirilmis yatirim uzmani icin prompt template
from langchain_classic.chains import LLMChain # model (llm) + prompt = llm zincirini
#llm zinciri + tools = ai agent
from langchain_classic.agents import AgentExecutor, ZeroShotAgent


# .env dosyasindan api anahtarlarini yukle
load_dotenv() 

# openai llm model
llm = ChatOpenAI(
    model_name = "gpt-3.5-turbo", # kullanilacak llm degeri
    temperature = 0.7, # yaratici yanitlar icin parametre 
    openai_api_key = os.getenv("OPENAI_API_KEY") # key 
)

# araclar listesini ayarlayalim (web search, doviz cevirici, hisse fiyati sorgulama)
tools = [search, convert_usd_to_try, get_stock_info]

# kullanicinin sorusu {input_soru} placeholder i ile prompt icerisine yerlesecek
investment_prompt = PromptTemplate.from_template("""
    Sen deneyimli ve güvenilir bir yatırım danışmanısın.

    Kullanıcıdan gelen yatırım ve finans sorularını analiz edip, aşağıdaki araçları kullanarak bilgi sunmalısın.

    ---

    📌 **Kullanabileceğin Araçlar ve Girdileri**

    1. 🧮 `convert_usd_to_try`
    - Görev: USD cinsinden bir miktarı TRY'ye çevirir.
    - Girdi: Sadece sayı (float) → Örnek: 100.0

    2. 📈 `get_stock_info`
    - Görev: Bir hisse sembolü (ör. AAPL) için güncel fiyat bilgisini verir.
    - Girdi: Hisse sembolü (string) → Örnek: "AAPL"

    3. 🔍 `duckduckgo_search`
    - Görev: Belirli bir konuda güncel haber veya analiz araması yapar.
    - Girdi: Aranacak konu (string) → Örnek: "altın fiyatları" veya "Ethereum analizi"

    ---

    🎯 **Kurallar**

    - Önce soruyu analiz et.
    - Gerekirse bir veya birden fazla aracı sırayla kullan.
    - Yatırım tavsiyesi verme, sadece bilgi sun.
    - Bilgiyi sade, güvenilir ve açıklayıcı biçimde aktar.
    - Tool kullanımı gerekiyorsa aşağıdaki formatı **mutlaka** uygula.

    ---

    🔧 **Yanıt Formatı (Zorunlu)**

    Thought: (Ne yapacağını anlat)
    Action: (SADECE şu 3 araçtan birinin adını yaz: duckduckgo_search, convert_usd_to_try, get_stock_info)
    Action Input: (Tool’a gönderilecek giriş)

    (Sonrasında sistem otomatik olarak Observation verecek)

    Observation: (Tool’dan gelen veri)

    (Eğer artık cevabı bulduysan ve başka bir araca ihtiyacın yoksa 👇)

    Thought: Artık son cevabı verebilirim.
    Final Answer: (Kullanıcıya gösterilecek nihai yanıt)

    ---

    ⚠️ Dikkat: Tool kullandıktan sonra `Final Answer:` yazmazsan sistem cevabını anlayamaz ve hata verir. Asla doğrudan cevap verme, önce Thought ile başla.

    ---

    Kullanıcının sorusu: {input}
    Thought:{agent_scratchpad}
""")

# llm zinciri olutur: model (gpt3.5 turbo) + prompt
llm_chain = LLMChain(llm = llm, prompt = investment_prompt)

# ekstra
agent_with_prompt = ZeroShotAgent(llm_chain=llm_chain, tools = tools)

agent = AgentExecutor.from_agent_and_tools(
    agent=agent_with_prompt,
    tools=tools,
    verbose = True,
    handle_parsing_errors = True
)

# langchain ajani baslat (ai agent tanimla)
# agent = initialize_agent(
#    tools=tools, # agent in kullanacagi araclar
#     llm = llm, # kullanilacak olan dil modeli 
#     agent = AgentType.ZERO_SHOT_REACT_DESCRIPTION, # prompt icerisinde bulunan aciklamalari kullanarak tool secer 
#     verbose = True # calisma sirasinda terminale detayli bilgi yazdirma
# )

if __name__ == "__main__":
    print("Yatırım uzmanı ai hazir, cikmak için 'q' yaz")
    
    #sonsuz dongu
    while True:
        query = input("Sorunuz: ")

        if query.lower() == "q":
            print("Program sonlandirildi")
            break

        try:
            # kullancinicin sorusunu ajan sistemine iletelim
            response = agent.invoke({"input": query})

            print(f"Yanit: \n{response}")
        except Exception as e:
            print(f"Hata olustu: {e}")