from langchain_openai import ChatOpenAI
from langchain.messages import SystemMessage, HumanMessage 
import json 

# kariyer planlama ajani sinifi tanimla
class CareerGoalAgent:
    # constructor fonksiyonu
    def __init__(self, model_name = "gpt-4"):
        self.llm = ChatOpenAI(model_name=model_name, temperature = 0.5)
    
    # kullanicdan gelen hedef meslek bilgisine gore kariyer yol haritası oluşturma
    def ask_career_goal(self, user_input):
        messages = [
            SystemMessage(content = (
                "Sen bir kariyer planlama asistanısın. Kullanıcı bir meslek söylediğinde, "
                "bu mesleğe ulaşmak için adım adım bir yol haritası üret. "
                "Sonuçları *sadece* aşağıdaki formatta JSON olarak döndür: \n\n"
                "{\n  \"adimlar\": [\"...\", \"...\", ...]\n}"
            )),
            HumanMessage(content=f"Hedef mesleğim: {user_input}.")
        ]

        response = self.llm.invoke(messages)

        # yanitin icerigi parse edilerek json formatinda return ediliyor
        return self.parse_response(response.content)
    
    # modelin dondurduğu yaniti json formatına dönüştürür
    def parse_response(self, response_text):
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            return {"hata": "Modelden gelen yanıt JSON formatında değil."}
        
