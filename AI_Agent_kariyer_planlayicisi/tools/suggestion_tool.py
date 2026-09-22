from ddgs import DDGS
# burada ddgs kütüphanesini kullanarak web üzerinde kaynak arama yapacağız
class SuggestionTool:
    def __init__(self):
        self.ddgs = DDGS()
    
    # belirli bir sorguyu(queryi)kaynak arama için kullanacağız
    def search_resources(self, query):
        results = self.ddgs.text(query, max_results=5) # kaç kaynak dönsün default 5
       
       # sonuçlardan alınan başlıkları bağlantı bilgileri ve özet bilgilerini tutmak için bir liste
        suggestions = []
        for item in results:
            suggestions.append({
                "title":item.get("title"), #sonucun başlığı
                "link":item.get("href"), #sonucun bağlantı bilgisi
                "snippet":item.get("body") #sonucun özeti
            })
        return suggestions #beş tane kaynak önerisini döndürdük

       