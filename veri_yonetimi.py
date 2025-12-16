import pandas as pd
import os
CSV_DOSYASI = "starbucks_drinks.csv"
SUTUN_KATEGORI = "Beverage_category"
SUTUN_ICECEK_ADI = "Beverage"
SUTUN_HAZIRLANIS = "Beverage_prep"
SUTUN_KALORI = "Calories"
AYRAC = ", "
def menu_verisini_getir():
    """
    CSV dosyasını okur. Belirlenen dört sütunu (kategori, ad, hazırlanış, kalori)
    birleştirerek "tam tanımlayıcı" ve benzersiz (unique) bir liste oluşturur.
    
    Örnek Çıktı: "Classic Espresso Drinks, Caffè Latte, Soymilk, 190 Kalori"
    
    Döndürür:
    list: Birleştirilmiş içecek tanımlamalarının listesi veya hata olursa boş liste.
    """
    try:
        bulundugumuz_klasor = os.path.dirname(os.path.abspath(__file__))
        dosya_yolu = os.path.join(bulundugumuz_klasor, CSV_DOSYASI)
        if not os.path.exists(dosya_yolu):
            print(f"Hata: '{CSV_DOSYASI}' dosyası bulunamadı.")
            print(f"Lütfen dosyanın şu konumda olduğundan emin olun: {dosya_yolu}")
            return []
        df = pd.read_csv(dosya_yolu)
        gerekli_sutunlar = [SUTUN_KATEGORI, SUTUN_ICECEK_ADI, SUTUN_HAZIRLANIS, SUTUN_KALORI]
        for col in gerekli_sutunlar:
            if col not in df.columns:
                print(f"HATA: Gerekli sütun '{col}' CSV'de bulunamadı.")
                print(f"CSV Dosyasındaki Mevcut Sütun Başlıkları: {list(df.columns)}")
                return []
            metin_sutunlar = [SUTUN_KATEGORI, SUTUN_ICECEK_ADI, SUTUN_HAZIRLANIS]
        df[metin_sutunlar] = df[metin_sutunlar].fillna("")
        df[SUTUN_KALORI] = df[SUTUN_KALORI].astype(int).astype(str)
        df['full_description'] = (
            df[SUTUN_KATEGORI].astype(str) + AYRAC +
            df[SUTUN_ICECEK_ADI].astype(str) + AYRAC +
            df[SUTUN_HAZIRLANIS].astype(str) + AYRAC +
            df[SUTUN_KALORI].astype(str) + " Kalori"  
        )
        df['full_description'] = df['full_description'].str.strip()
        df['full_description'] = df['full_description'].str.strip(AYRAC.strip() + " ")
        df['full_description'] = df['full_description'].str.replace(f"({AYRAC.strip()}){{2,}}", AYRAC.strip(), regex=True)
        df['full_description'] = df['full_description'].str.strip(AYRAC.strip() + " ")
        icecek_listesi = df['full_description'].dropna().unique().tolist()
        icecek_listesi = [item for item in icecek_listesi if item and not item.startswith("0 Kalori")]
        if not icecek_listesi:
            print("HATA: Hiçbir içecek tanımı oluşturulamadı. CSV'niz boş olabilir.")
            return []
        print(f"BAŞARILI: {len(icecek_listesi)} adet benzersiz içecek *kombinasyonu* (kalori dahil) yüklendi.")
        return icecek_listesi
    except Exception as e:
        print(f"BEKLENMEDİK HATA: Veri yüklenirken bir sorun oluştu: {e}")
        return []

if __name__ == "__main__":

    print("--- Faz 1: Veri Yükleme Modülü Test Ediliyor ---")

    menu = menu_verisini_getir()

    if menu:
        print("\n--- Menüden İlk 20 Kombinasyon (Örnek) ---")
        for i, icecek in enumerate(menu[:20]):
            print(f"{i+1}. {icecek}")
    else:
        print("\nTest BAŞARISIZ: Menü yüklenemedi. Lütfen yukarıdaki HATA mesajlarını kontrol edin.")

    print("-------------------------------------------------")
  