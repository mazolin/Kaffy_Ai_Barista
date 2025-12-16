import qrcode
import io     
import base64 

def qr_kodu_base64_olustur(siparis_metni):
    """
    Verilen metin için bir QR kod oluşturur ve bunu bir web sayfasında
    gösterilebilecek Base64 formatlı bir metin olarak döndürür.
    
    Parametreler:
    siparis_metni (str): QR koda gömülecek metin.
    
    Döndürür:
    str: PNG formatındaki QR kod resminin Base64 kodlanmış metni.
    """
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=8,  
            border=4,      
        )
        
        qr.add_data(siparis_metni)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        
        img_bytes = buf.getvalue()
        
        qr_base64_str = base64.b64encode(img_bytes).decode('utf-8')
        
        return qr_base64_str

    except Exception as e:
        print(f"HATA: QR kod oluşturulurken hata: {e}")
        return None

if __name__ == "__main__":
    
    print("--- Faz 3: QR Kod Üretici Modülü Test Ediliyor ---")
    
    test_siparis = "Classic Espresso Drinks, Caffè Latte, Short Nonfat Milk, 70 Kalori"
    
    print(f"'{test_siparis}' metni için QR kod oluşturuluyor...")
    
    base64_kodu = qr_kodu_base64_olustur(test_siparis)
    
    if base64_kodu:
        print("BAŞARILI: Base64 kodu oluşturuldu.")
        print(f"Kodun ilk 50 karakteri: {base64_kodu[:50]}...")
        
        try:
            img_data = base64.b64decode(base64_kodu)
            
            with open("test_qr.png", "wb") as f:
                f.write(img_data)
            print("\nDOĞRULAMA BAŞARILI: Base64 kodu 'test_qr.png' olarak kaydedildi.")
            print("Lütfen klasörünüzdeki 'test_qr.png' dosyasını açıp kontrol edin.")
            
        except Exception as e:
            print(f"\nDOĞRULAMA HATASI: Test dosyası kaydedilemedi: {e}")
            
    else:
        print("Test BAŞARISIZ: QR kod oluşturulamadı.")
        
    print("---------------------------------------------------------")