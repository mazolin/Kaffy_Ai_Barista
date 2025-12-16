from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
import os
import sys

try:
    from veri_yonetimi import menu_verisini_getir
except ImportError:
    print("HATA: 'veri_yonetimi.py' dosyası bulunamadı.")
    sys.exit(1)

try:
    API_ANAHTARI = os.environ["GOOGLE_API_KEY"]
    genai.configure(api_key=API_ANAHTARI)
    print("Gemini API anahtarı başarıyla yüklendi.")
except KeyError:
    print("KRİTİK HATA: 'GOOGLE_API_KEY' ortam değişkeni bulunamadı!")
    print("Lütfen 'set GOOGLE_API_KEY=...' (Windows) veya 'export GOOGLE_API_KEY=...' (Mac/Linux) komutunu çalıştırın.")
    sys.exit(1)
except Exception as e:
    print(f"API yapılandırılırken beklenmedik bir hata oluştu: {e}")
    sys.exit(1)

print("Dahili menü 'kahve_asistani' modülüne yükleniyor...")
DAHILI_MENU_LISTESI = menu_verisini_getir()
if not DAHILI_MENU_LISTESI:
    print("KRİTİK HATA: Menü yüklenemedi.")
    sys.exit(1)
print(f"{len(DAHILI_MENU_LISTESI)} adet içecek kombini hafızaya yüklendi.")

def sistem_talimati_olustur():
    """
    Yapay zekaya ne yapması gerektiğini öğreten ana talimat (prompt) metnini oluşturur.
    """
    menu_metni = "\n".join(DAHILI_MENU_LISTESI)


    prompt = f"""
    Sen, "Kahve Asistanı" adlı bir Starbucks kahve uzmanısın.
    İki görevin var: 1) Sohbet Etmek 2) Sipariş Almak.

    GİZLİ VERİTABANIN (DAHİLİ MENÜ):
    Sadece ve sadece aşağıdaki listede bulunan içecekleri önerebilirsin.
    [MENU_BASLANGIC]
    {menu_metni}
    [MENU_BITIS]

    GÖREV 1: SOHBET ETMEK
    Kullanıcı bir içecek seçene kadar, onunla doğal ve arkadaşça sohbet et.
    * Ona seçenekler sun (İYİ ÖRNEK: "Size 70 kalorilik, yağsız sütlü bir 'Caffè Latte' önerebilirim.")
    * Asla ham menü metnini gösterme (KÖTÜ ÖRNEK: "Classic Espresso Drinks, Caffè Latte...").
    * Listede olmayan bir şeyi (örn: Limonata) ASLA uydurma. "Üzgünüm, menümde yok" de.

    GÖREV 2: SİPARİŞ ALMAK (EN ÖNEMLİ GÖREVİN!)
    Kullanıcı bir içeceği onayladığında (örn: "Evet, o latteyi istiyorum", "Tamam, alayım", "Yağsız sütlü olanı alayım"),
    SOHBETİ KESMEK ZORUNDASIN.
    
    Bu durumda, cevabın *MUTLAKA* ve *SADECE* iki satırdan oluşmalıdır:
    1.  Satır: Kısa, onaylayıcı bir cümle. (örn: "Harika bir seçim! Siparişiniz alındı.")
    2.  Satır: Seçilen içeceğin DAHİLİ MENÜ'deki tam ve ham metnini içeren `[SIPARIS:...]` etiketi.

    BU KURALI ASLA İHLAL ETME. BU İKİ SATIRDAN SONRA "Afiyet olsun", "Adınız nedir?" GİBİ ASLA ÜÇÜNCÜ BİR SATIR VEYA EK METİN YAZMA.
    Eğer sipariş belirsizse (örn: "Latte istiyorum" derse), "Elbette, hangi sütle (yağsız, soya) istersiniz?" diye sorarak belirsizliği GİDER.
    Siparişi SADECE tam olarak netleştiğinde (Kategori, Ad, Hazırlanış, Kalori belli olduğunda) GÖREV 2'yi uygula.

    ÖRNEK SİPARİŞ ONAYI:
    Kullanıcı: "Tamam, yağsız sütlü olanı alayım."
    Sen: Harika, siparişinizi onaylıyorum.
[SIPARIS:Classic Espresso Drinks, Caffè Latte, Short Nonfat Milk, 70 Kalori]
    """
    return prompt

print("Sistem talimatı oluşturuluyor...")
ANA_SISTEM_TALIMATI = sistem_talimati_olustur()

generation_config = {
    "temperature": 0.2, 
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

print("Gemini modeli sistem talimatıyla birlikte başlatılıyor...")
model = genai.GenerativeModel(
    model_name='models/gemini-2.5-flash',
    generation_config=generation_config,
    safety_settings=safety_settings,
    system_instruction=ANA_SISTEM_TALIMATI 
)

chat_session = model.start_chat(history=[])
print("Model ve sohbet oturumu başarıyla başlatıldı. Teste hazır.")


if __name__ == "__main__":
    
    print("--- Faz 2: Yapay Zeka Modülü Test Ediliyor ---")
    
    try:
        mesaj_1 = "Merhaba, bugün 100 kalorinin altında sıcak bir latte istiyorum."
        print(f"\n--- TEST 1: İlk İstek ---")
        print(f"Kullanıcı: {mesaj_1}")
        response_1 = chat_session.send_message(mesaj_1)
        yanit_1 = response_1.text.strip()
        print(f"Asistan: {yanit_1}")

        mesaj_2 = "O 70 kalorilik Caffè Latte'yi istiyorum."
        print(f"\n--- TEST 2: Belirsiz Seçim ---")
        print(f"Kullanıcı: {mesaj_2}")
        response_2 = chat_session.send_message(mesaj_2)
        yanit_2 = response_2.text.strip()
        print(f"Asistan: {yanit_2}")
        
        mesaj_3 = "Yağsız sütle (Nonfat Milk) olanı alayım lütfen."
        print(f"\n--- TEST 3: Nihai Onay ---")
        print(f"Kullanıcı: {mesaj_3}")
        response_3 = chat_session.send_message(mesaj_3)
        yanit_3 = response_3.text.strip()
        print(f"Asistan: {yanit_3}")

        if "[SIPARIS:" in yanit_3:
            print("\nBAŞARILI: Gizli [SIPARIS:...] etiketi yanıtta bulundu!")
        else:
            print("\nDİKKAT: Yanıtta [SIPARIS:...] etiketi bulunamadı. Model hala kuralı ihlal ediyor.")

        print("---------------------------------------------------------")

    except Exception as e:
        print(f"\n--- TEST SIRASINDA HATA OLUŞTU ---")
        print(f"HATA: {e}")