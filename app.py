from dotenv import load_dotenv
load_dotenv()
import os
import re
from flask import Flask, render_template, request, jsonify, session


try:
    from kahve_asistani import model 
    
except ImportError:
    print("KRİTİK HATA: 'kahve_asistani.py' dosyasından 'model' import edilemedi.")
    print("Lütfen 'kahve_asistani.py' dosyasının 'model' nesnesini global olarak tanımladığından emin olun.")
    exit()
try:
    from qr_uretici import qr_kodu_base64_olustur
except ImportError:
    print("KRİTİK HATA: 'qr_uretici.py' dosyası bulunamadı.")
    exit()

app = Flask(__name__)
app.secret_key = 'buraya_cok_gizli_bir_sey_yaz_12345!'

@app.route("/")
def ana_sayfa():
    """
    Kullanıcı web sitesine girdiğinde (http://localhost:5000/)
    bu fonksiyon çalışır.
    """

    session['chat_history'] = [] 
    print("Yeni kullanıcı bağlandı, sohbet geçmişi sıfırlandı.")
    

    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def sohbet_et():
    """
    Kullanıcının web sayfasından gönderdiği her mesaj
    bu fonksiyona (JavaScript aracılığıyla) gelir.
    """
    try:
        kullanici_mesaji = request.json.get("message")
        if not kullanici_mesaji:
            return jsonify({"hata": "Mesaj boş olamaz."}), 400
        sohbet_gecmisi = session.get('chat_history', [])
        chat = model.start_chat(history=sohbet_gecmisi)
        
        print(f"Kullanıcıdan gelen mesaj: {kullanici_mesaji}")
        response = chat.send_message(kullanici_mesaji)
    
        yeni_gecmis_listesi = []
        for entry in chat.history:
            yeni_gecmis_listesi.append({
                'role': entry.role,
                'parts': [part.text for part in entry.parts]
            })
        
        session['chat_history'] = yeni_gecmis_listesi

        ham_yanit = response.text.strip()
        print(f"Gemini'den gelen ham yanıt: {ham_yanit}")

        qr_code_base64 = None
        kullaniciya_yanit = ham_yanit
        
        if "[SIPARIS:" in ham_yanit:

            parcalar = re.split(r'\[SIPARIS:(.*?)\]', ham_yanit, flags=re.DOTALL)
            
            kullaniciya_yanit = parcalar[0].strip()
            siparis_metni = parcalar[1].strip()     

            print(f"SİPARİŞ TESPİT EDİLDİ: {siparis_metni}")
            
            qr_code_base64 = qr_kodu_base64_olustur(siparis_metni)
            

            session['chat_history'] = []

        return jsonify({
            "reply": kullaniciya_yanit, 
            "qr_code": qr_code_base64    
        })

    except Exception as e:
        print(f"HATA (/chat route): {e}")
        return jsonify({"hata": "Sunucuda bir hata oluştu."}), 500

if __name__ == "__main__":
    print("Flask sunucusu http://127.0.0.1:5000 adresinde başlatılıyor...")
    print("Lütfen 'kahve_asistani.py' modülünün yüklenmesini bekleyin...")
    app.run(debug=True, port=5000,host='0.0.0.0')