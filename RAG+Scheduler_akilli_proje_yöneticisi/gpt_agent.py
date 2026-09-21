import os
from openai import OpenAI 
from dotenv import load_dotenv

load_dotenv() # .env icerisinden openai api anahtarini yukle

# openai istemcisi
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_followup_question(person, task, current_time, previous_responses = None):
    """
    GPT ye kişi, görev, zaman ve geçmiş yanıtları vererek en uygun soruyu üretmesini ister

    person: çalışan ismi
    task: görev
    current_time: şuanki zaman
    previous_responses: kişinin bu göreve daha önce verdiği yanıtlar
    """

# history ve memory arasındaki fark?
# history => konuşma geçmişi => ekranda yazdırmak için
# memory => kalıcı hafıza. veritabanına kaydedilen bilgiler 
    history = ""
    if previous_responses: # eger gecmis cevaplar varsa
        for item in previous_responses: 
            history += f"Saat {item["time"]}: {item["response"]}\n" # formatli şekilde history oluştur

    # gpt modeline gonderilecek olan prompt
    prompt = f"""
            Şu anda saat {current_time}.
            Sen bir proje yöneticisisin.

            Görev: "{task}"
            Kişi: {person}

            Bu kişiye bu görev daha önce verildi.
            Şimdiye kadar verdiği cevaplar:
            {history if history else "Henüz cevap yok."}

            Lütfen {person}'a doğrudan hitap ederek görevle ilgili ne durumda olduğunu soran net ve kısa bir soru yaz.

            Soru şunları içermeli:
            - Kişinin ismiyle hitap et
            - Görevin ne olduğu açıkça tekrar geçsin
            - Görevin tamamlanma durumu yada üzerinde çalışılıp çalışılmadığı sorgulansın
            - Sadece doğrudan bir soru cümlesi döndür, başka açıklama yazma
    """  
    # gpt apisine çağrı yap, yukarıdaki prompt ile ceavp oluşturmasını iste
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature= 0.7 # biraz yaratıcı olabilirsin
    )

    # cevabı dondurur
    return response.choices[0].message.content.strip()

# görevi tamamlanıp tamamlanmadığını anlayan fonksiyon
def is_task_completed(person, task, responses, current_time):
    """
        gpt ye goevin tamamlanıp tamamlanmadığını sorar
        yalnızca 3 cevaptan birini return ederiz: tamamlandı / devam ediyor / yapılmadı
    """
    history = ""
    for item in responses:
        history += f"Saat {item["time"]}: {item["response"]}\n"
    
    # prompt
    prompt = f"""
            Saat: {current_time}
            Kişi: {person}
            Görev: "{task}"

            Bu görevle ilgili şimdiye kadar {person} tarafından verilen cevaplar:
            {history}
            Lütfen sadece tek bir kelime ile cevap ver:
            - tamamlandı
            - devam ediyor
            - yapılmadı

            Yalnızca bu üç kelimeden birini döndür. Açıklama yapma.
    """

    # gpt den cevap alinir
    responses = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages=[{"role":"user", "content":prompt}],
        temperature=0
    )

    return responses.choices[0].message.content.strip().lower()

if __name__ == "__main__":
    example_history = [
        {"time":"12:02", "response": "Başladım ama eksik bir şeyler var"},
        {"time":"12.04", "response": "Veritabanı bağlantısını henüz kurmadım"}
    ]

    # ornek takip sorgusu
    soru = generate_followup_question(
        person="Yılmaz",
        task="fast api ile hello world end pointi yazılması",
        current_time="25.08.2025 12:06", # simüle edilen guncel zaman
        previous_responses=example_history
    )

    print("gpt'nin olusturdugu soru")
    print(soru)

    soru = is_task_completed(
        person="Yılmaz",
        task="fast api ile hello world end pointi yazılması",
        responses = [{"time":"12:02", "response": "ben bu task ı sevmedim, yapmayacağım"}],
        current_time="25.08.2025 12:06", # simüle edilen guncel zaman
    )

    print("gpt'nin is_task_completed cevabı")
    print(soru)
