import yfinance as yf

def hisse_bilgisi_cek(hisse_kodu):
    try:
        hisse = yf.Ticker(hisse_kodu)
        hisse_bilgisi = hisse.history(period="1d")
        
        if hisse_bilgisi.empty:
            print(f"{hisse_kodu} için veri bulunamadı. Sembolü kontrol edin.")
            return
        
        son_fiyat = hisse_bilgisi['Close'].iloc[-1]
        gunluk_degisim = hisse_bilgisi['Close'].iloc[-1] - hisse_bilgisi['Open'].iloc[-1]
        gunluk_yuzde_degisim = (gunluk_degisim / hisse_bilgisi['Open'].iloc[-1]) * 100
        
        print(f"{hisse_kodu} Hisse Bilgileri:")
        print(f"Son Fiyat: {son_fiyat:.2f} TL")
        print(f"Günlük Değişim: {gunluk_degisim:.2f} TL")
        print(f"Günlük Yüzde Değişim: {gunluk_yuzde_degisim:.2f}%")
        print("-" * 40)
    
    except Exception as e:
        print(f"{hisse_kodu} için veri çekilirken bir hata oluştu: {e}")

def hisse_tara(hisse_listesi):
    for hisse in hisse_listesi:
        hisse_bilgisi_cek(hisse)

if __name__ == "__main__":
    # BIST hisse senetleri listesi (örnek olarak)
    hisse_listesi = ["THYAO.IS", "AKBNK.IS", "GARAN.IS", "ASELS.IS", "EREGL.IS"]
    
    hisse_tara(hisse_listesi)