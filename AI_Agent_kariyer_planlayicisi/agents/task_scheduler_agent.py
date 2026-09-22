import datetime
import json

# takvim oluşturucu ajan sınıfı tanımla
class TaskSchedulerAgent:
    def __init__(self, weeks = 4): #kaç haftalık plan yapilacagi, default 4
        self.weeks = weeks

    # verilen kariyer yol haritasına göre haftalık görev planı oluşturan agent
    def create_schedule(self, roadmap):
        today = datetime.date.today() #Bugünün tarihini alıyoruz

        schedule = {} #boş bir dictionary oluşturuyoruz içine zamanlanmış görevleri tutuyoruz

        for i, step in enumerate(roadmap.get("adimlar", [])):

            week = i% self.weeks # görevin atanacağı haftanın belirlenmesi

            start_date = today + datetime.timedelta(days=7*week)
            #görevin başlangıç tarihi hesaplanıyor. bugünden itibaren ilgili haftaya karşılık gelen gün belirleniyor

            if f"Hafta {week+1}" not in schedule: #eğer schedule sözlüğünde ilgili hafta anahtarı yoksa
                schedule[f"Hafta {week+1}"] = [] #schedule sözlüğüne ilgili hafta için boş bir liste ekliyoruz

            schedule[f"Hafta {week+1}"].append({ #haftalık plan içine görev ve başlangıç tarihini ekliyoruz
                "gorev":step,
                "baslangic": str(start_date)
            })

        return schedule # olusuturulan haftalik gorev takvimi donduruluyor

    def save_schedule(self, schedule, filename = "schedule.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(schedule, f, ensure_ascii=False, indent=2)