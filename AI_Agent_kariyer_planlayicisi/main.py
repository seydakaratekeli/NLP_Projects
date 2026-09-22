"""
problem tanımı: Kariyer Planlayıcısı
    - insanlar kariyerleri ile ilgili nasıl bir yol izlemeleri greektigini sorabilecekler
    - kişiye özel, dinamik, takip edilebilir

araçlar ve teknolojiler
    - langchain, openai, duckduckgo (kurs makale video gibi kaynak önerilerini almak için)
    pip install openai langchain python-dotenv ddgs langchain-community
    - 
    
plan/program
    - Hedef belirleme: 
        - kullanıcı terminalde meslek hedefini belirler
        - gpt buna uygun adımları json formatinda uretir
    - Yol haritası planlama
        - görevler haftalara bölünür
        - her hafta için net hedefler belirlenir
    - Kaynak önerisi
        - kullanıcı terminal uzerinde istedigi konuyu yazar
        - sistem web üzerinden önerileri getirir (video, kurs ...)
    - Gelişim takibi 
        - kullanıcıdan ilerleme bilgisi alınır ve hafızada görev başarı durumu saklanır

install libraries: freeze

"""

from agents.career_goal_agent import CareerGoalAgent
from agents.task_scheduler_agent import TaskSchedulerAgent
from tools.suggestion_tool import SuggestionTool
from memory.user_memory import UserMemory
from dotenv import load_dotenv
import json

load_dotenv()

if __name__ == "__main__":
    print("Kariyer Planlayıcısı")

    user_memory = UserMemory()

    goal = input("Hedef mesleğiniz nedir?")
    user_memory.update_goal(goal)

    # yol haritasi olustur
    goal_agent = CareerGoalAgent()
    roadmap = goal_agent.ask_career_goal(goal)
    

    print("Yol Haritanız: \n")
    print(json.dumps(roadmap, indent=2, ensure_ascii=False))

    # zamanlama yapalım
    num_week = 4
    scheduler = TaskSchedulerAgent(weeks = num_week)
    schedule = scheduler.create_schedule(roadmap)
    scheduler.save_schedule(schedule)

    print(f"\n {num_week} Haftalık Plan: ")
    print(json.dumps(schedule, indent = 2, ensure_ascii=False))

    # kaynak önerisi
    suggestor = SuggestionTool()
    topic = input("Bir beceri başlığı girin (kaynak önerisi için)")
    results = suggestor.search_resources(topic)
    print("Kaynak Önerileri")
    for r in results:
        print(f" - {r["title"]} \n {r["link"]} \n {r["snippet"]}\n")