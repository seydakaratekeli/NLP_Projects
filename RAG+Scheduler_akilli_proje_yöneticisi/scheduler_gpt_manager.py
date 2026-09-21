"""
problem tanımı: Proje Yöneticisi
    - bu proje, bir proje dokumanını (pdf formatında) okuyarak ekip üyelerine 
        gerçek zamanlı olarak görev hatırlatmaları yapan bir yapay zeka sistemi
    - Yapay zeka yöneticisi:
        - pdf te bulunan görev zamanına göre kişilere görevlerini sorar
        - çalışanların verdiği doğal dil cevabını analiz eder
        - eğer görev tamamlanmadıysa tekrardan sorar
        - tamamlanan görevleri tekrardan sormaz
        - tüm sorular gpt tarafından geçmiş cevaplara göre özelleştirilerek sorulur
    - proje 10 saniyede bir 1 dakşka ilerleyen simulasyon saati ile calisir

veri seti: bir proje planı: mobil application geliştirmek için oluşturulmuş basit bir proje planı

araçlar ve teknolojiler: openai, PyPDF2 python-dotenv rich(terminalde renkli ve biçimli çıktı oluşturur)

plan program
    - pdf reader: proje dokumanını oku
    - gpt agent: proje yönetimi yani taskların sorulması, taskların tamamlanıp tamamlanmadığının anlaşılması
    - scheduler_gpt_manager: simülasyonun başlatılması

install libraries: freeze

soru soruyor olumsuz cevap aldığında bir sonraki taskta yeniden soruyor(hatırlatma yapıyor)
ayrıca zamandan bağımsız şekilde tasklarını bitiren çalışanlar chat bot ekranı eklenirse bu proje ile iletişime geçecek şekilde daha gelişmiş olur 
"""

import time # gercek zamanli beklemeler icin
from datetime import datetime, timedelta # tarih ve zaman islemleri icin moduler bir yapi olustur
from pdf_reader import extract_tasks_from_pdf
from rich import print # zengin renkli terminal ciktisi
from gpt_agent import generate_followup_question, is_task_completed

task_memory = {} #bir görev için daha önce verilmiş cevapları saklaması için

# gpt tabanli gorev takip simülasyonu calistiran bir fonksiyon
def run_gpt_scheduler(pdf_path = "proje_dokumani_saatli.pdf", delay_sec = 10):

    # belirlitlen pdf doyasindan gorevleri cikart
    tasks = extract_tasks_from_pdf(pdf_path)

    # simülasyon başlangıç zamanı tanımla
    sim_time = datetime(2025, 8, 25, 11, 59) # 25.08.2025 saat 11:59
    # simülasyonun başladığını kullanıcıya bildir
    print(f"[bold green] Simülasyon başladı [/bold green] -> Başlangıç: {sim_time.strftime('%d.%m.%Y %H:%M')}")

    while True: # her dongude simülasyon 1 dk ilerletilir
        sim_time += timedelta(minutes=1) # simulasyon zamani 1 dk ilerletilir
        sim_time_str = sim_time.strftime('%d.%m.%Y %H:%M')
        print(f"\n[bold white on black]Simülasyon Saati: {sim_time_str}[/bold white on black]")

        # her görev için kontrol yapilir
        for task in tasks:
            ts = task["timestamp"] # gorevin hedef zamani
            kisi = task["person"] # apacak kisi
            gorev = task["task"]
            key = f"{ts}_{kisi}" # aynı gorev ve kisiyi unique (essiz) olarak tanimak icin anahtar

            if ts <= sim_time:
                # daha once verilmis cevaplari bellekten alalim
                onceki_cevaplar = task_memory.get(key, [])

                # onceki cevaplar varsa gorevin tamamlanip tamamlanmadigi sorgulanir
                if onceki_cevaplar:
                    tamam_durumu = is_task_completed(kisi, gorev, onceki_cevaplar, sim_time_str)
                    if tamam_durumu == "tamamlandı":
                        continue # gorev tamamlanmis tekrar soru sorma
                    else:
                        print(f"[yellow]{kisi} gorevini henüz tamamlamadı. Tekrar soruluyor ... [/yellow]")
                
                # gpt ile kişiye özel takip sorusu oluşturma
                soru = generate_followup_question(
                    person=kisi,
                    task=gorev,
                    current_time=sim_time_str,
                    previous_responses=onceki_cevaplar
                )

                print(f"[bold red]{kisi}[/bold red] kişisine GPT tarafından oluşturulan soru: ")
                print(f"[bold blue]{soru}[/bold blue]")

                cevap = input("Cevap: ").strip() # çalışanın cevabı

                task_memory.setdefault(key,[]).append({
                    "time": sim_time.strftime("%H:%M"),
                    "response": cevap
                })
        
    time.sleep(delay_sec)

if __name__ == "__main__":
    run_gpt_scheduler()