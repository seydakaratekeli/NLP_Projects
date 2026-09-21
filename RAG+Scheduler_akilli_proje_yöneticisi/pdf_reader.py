from PyPDF2 import PdfReader # PDF dosyasını okumak ve içeriğini çıkarmak
import re # regular expression (duzenli ifadeler) metin içerisnde desen arama
from datetime import datetime # tarih ve saatler için date time modulu

# pdf icerisinden gorevleri cikartan fonksiyon
def extract_tasks_from_pdf(pdf_path): # pdf_path: okunacak pdf dosyasinin yolu
    reader = PdfReader(pdf_path) 
    text = "\n".join(page.extract_text() for page in reader.pages) # pdf içerisindeki her sayfa için metin çıkarılır

    # örnek desen 25.08.2025 12:00 - Kaan: Ana ekran ve butonlar icin UI taslagi ciz
    pattern = r"(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}) - (.*?): (.*)" # tarih (gg.aa.yyyy ss:dd), kişi adı ve görev açıklaması gruplar
    matches = re.findall(pattern, text)

    tasks = []
    for match in matches:
        tarih_str, kisi, gorev = match # eslesme 3 parcaya ayriliyor tarih, kişi adı ve görev
        tarih = datetime.strptime(tarih_str, "%d.%m.%Y %H:%M") # tarih stringinin datetime objesine çevir
        tasks.append({
            "timestamp":tarih,  # date
            "person": kisi.strip(), # kişi adı, çalışan
            "task": gorev.strip() # gorev açıklması
        })

    return tasks

if __name__ == "__main__":
    path = "proje_dokumani_saatli.pdf"
    try:
        tasks = extract_tasks_from_pdf(path)
        for task in tasks:
            print(f"{task["timestamp"]} -- {task["person"]}: {task["task"]}")
    except FileNotFoundError:
        print(f"{path} dosyasi bulunamadi.")
