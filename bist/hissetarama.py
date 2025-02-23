import yfinance as yf
import time


def hisse_listesi_oku(dosya_adi="bist_hisse_listesi.txt"):
    try:
        with open(dosya_adi, "r", encoding="utf-8") as dosya:
            hisse_listesi = [satir.strip() for satir in dosya if satir.strip()]
        return hisse_listesi
    except FileNotFoundError:
        print(f"{dosya_adi} dosyası bulunamadı. Lütfen hisse listesini içeren bir TXT dosyası oluşturun.")
        return []


def hisse_bilgisi_cek(hisse_kodu):
    try:
        hisse = yf.Ticker(hisse_kodu)
        hisse_bilgisi = hisse.history(period="1d")
        
        if hisse_bilgisi.empty:
            print(f"{hisse_kodu} için veri bulunamadı. Sembolü kontrol edin.")
            return None
        
        son_fiyat = hisse_bilgisi['Close'].iloc[-1]
        gunluk_degisim = hisse_bilgisi['Close'].iloc[-1] - hisse_bilgisi['Open'].iloc[-1]
        gunluk_yuzde_degisim = (gunluk_degisim / hisse_bilgisi['Open'].iloc[-1]) * 100
        
        print(f"{hisse_kodu} Hisse Bilgileri:")
        print(f"Son Fiyat: {son_fiyat:.2f} TL")
        print(f"Günlük Değişim: {gunluk_degisim:.2f} TL")
        print(f"Günlük Yüzde Değişim: {gunluk_yuzde_degisim:.2f}%")
        print("-" * 40)
        
        return {
            "Sembol": hisse_kodu,
            "Son Fiyat": son_fiyat,
            "Günlük Değişim": gunluk_degisim,
            "Günlük Yüzde Değişim": gunluk_yuzde_degisim
        }
    
    except Exception as e:
        print(f"{hisse_kodu} için veri çekilirken bir hata oluştu: {e}")
        return None


favori_hisseler = []

def favori_hisse_ekle(hisse_kodu):
    if hisse_kodu not in favori_hisseler:
        favori_hisseler.append(hisse_kodu)
        print(f"{hisse_kodu} favori listesine eklendi.")
    else:
        print(f"{hisse_kodu} zaten favori listesinde.")

def favori_hisseleri_goster():
    if favori_hisseler:
        print("Favori Hisse Senetleri:")
        for hisse in favori_hisseler:
            print(hisse)
    else:
        print("Favori listenizde hisse senedi bulunmamaktadır.")


def hisse_detaylari_goster(hisse_kodu):
    try:
        hisse = yf.Ticker(hisse_kodu)
        hisse_bilgisi = hisse.history(period="1d")
        
        if hisse_bilgisi.empty:
            print(f"{hisse_kodu} için veri bulunamadı. Sembolü kontrol edin.")
            return
        
        print(f"\n{hisse_kodu} Hisse Detayları:")
        print(f"Açılış Fiyatı: {hisse_bilgisi['Open'].iloc[-1]:.2f} TL")
        print(f"Günlük Yüksek: {hisse_bilgisi['High'].iloc[-1]:.2f} TL")
        print(f"Günlük Düşük: {hisse_bilgisi['Low'].iloc[-1]:.2f} TL")
        print(f"Kapanış Fiyatı: {hisse_bilgisi['Close'].iloc[-1]:.2f} TL")
        print(f"Hacim: {hisse_bilgisi['Volume'].iloc[-1]:.0f}")
        print("-" * 40)
    
    except Exception as e:
        print(f"{hisse_kodu} için detaylar çekilirken bir hata oluştu: {e}")


def menu_goster():
    print("\n--- BIST Hisse Senedi Tarama Menüsü ---")
    print("1. İsim ile Arama")
    print("2. Tüm Hisse Senetlerini Getir")
    print("3. Hisse Senedi Detaylarını Görüntüle")
    print("4. Fiyat Aralığına Göre Filtrele")
    print("5. Günlük Yüzde Değişime Göre Sırala")
    print("6. Favori Hisse Senetlerini Yönet")
    print("7. Çıkış")
    secim = input("Lütfen bir seçenek girin (1-7): ")
    return secim


def main():
    hisse_listesi = hisse_listesi_oku("bist_hisse_listesi.txt")
    
    while True:
        secim = menu_goster()
        
        if secim == "1":  
            while True:
                hisse_kodu = input("Hisse senedi sembolü girin (Ana menüye dönmek için 'm' tuşuna basın): ").upper()
                if hisse_kodu == "M":
                    break
                if hisse_kodu + ".IS" in hisse_listesi:
                    hisse_bilgisi_cek(hisse_kodu + ".IS")
                else:
                    print(f"{hisse_kodu} geçerli bir hisse senedi sembolü değil.")
        
        elif secim == "2":  
            for hisse in hisse_listesi:
                hisse_bilgisi_cek(hisse)
                time.sleep(0.5)  
        
        elif secim == "3":  
            while True:
                hisse_kodu = input("Hisse senedi sembolü girin (Ana menüye dönmek için 'm' tuşuna basın): ").upper()
                if hisse_kodu == "M":
                    break
                if hisse_kodu + ".IS" in hisse_listesi:
                    hisse_detaylari_goster(hisse_kodu + ".IS")
                else:
                    print(f"{hisse_kodu} geçerli bir hisse senedi sembolü değil.")
        
        elif secim == "4":  
            min_fiyat = float(input("Minimum fiyat girin: "))
            max_fiyat = float(input("Maksimum fiyat girin: "))
            for hisse in hisse_listesi:
                veri = hisse_bilgisi_cek(hisse)
                if veri and min_fiyat <= veri["Son Fiyat"] <= max_fiyat:
                    print(f"{hisse} - Son Fiyat: {veri['Son Fiyat']:.2f} TL")
        
        elif secim == "5": 
            veriler = []
            for hisse in hisse_listesi:
                veri = hisse_bilgisi_cek(hisse)
                if veri:
                    veriler.append(veri)
            veriler.sort(key=lambda x: x["Günlük Yüzde Değişim"], reverse=True)
            print("Günlük Yüzde Değişime Göre Sıralanmış Hisse Senetleri:")
            for veri in veriler:
                print(f"{veri['Sembol']} - Yüzde Değişim: {veri['Günlük Yüzde Değişim']:.2f}%")
        
        elif secim == "6": 
            while True:
                print("\n--- Favori Hisse Senetleri Menüsü ---")
                print("1. Favori Hisse Ekle")
                print("2. Favori Hisse Senetlerini Göster")
                print("3. Ana Menüye Dön")
                alt_secim = input("Lütfen bir seçenek girin (1-3): ")
                if alt_secim == "1":
                    hisse_kodu = input("Favori listesine eklemek istediğiniz hisse senedi sembolü girin: ").upper()
                    favori_hisse_ekle(hisse_kodu + ".IS")
                elif alt_secim == "2":
                    favori_hisseleri_goster()
                elif alt_secim == "3":
                    break
                else:
                    print("Geçersiz seçenek.")
        
        elif secim == "7":  
            print("Programdan çıkılıyor...")
            break
        
        else:
            print("Geçersiz seçenek. Lütfen 1-7 arasında bir sayı girin.")

if __name__ == "__main__":
    main()