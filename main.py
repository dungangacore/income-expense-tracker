import sqlite3
import csv
from datetime import datetime

conn = sqlite3.connect("gelirgider.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS islemler (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tur TEXT NOT NULL,
        miktar REAL NOT NULL,
        aciklama TEXT,
        tarih TEXT NOT NULL
    )
""")
conn.commit()

def gelir_ekle():
    miktar = float(input("Gelir miktarı: "))
    aciklama = input("Açıklama: ")
    tarih = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO islemler (tur, miktar, aciklama, tarih) VALUES (?, ?, ?, ?)", ("gelir", miktar, aciklama, tarih))
    conn.commit()
    print("✅ Gelir eklendi.\n")

def gider_ekle():
    miktar = float(input("Gider miktarı: "))
    aciklama = input("Açıklama: ")
    tarih = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO islemler (tur, miktar, aciklama, tarih) VALUES (?, ?, ?, ?)", ("gider", miktar, aciklama, tarih))
    conn.commit()
    print("✅ Gider eklendi.\n")

def toplam_bakiye():
    cursor.execute("SELECT SUM(miktar) FROM islemler WHERE tur='gelir'")
    gelir = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(miktar) FROM islemler WHERE tur='gider'")
    gider = cursor.fetchone()[0] or 0
    print(f"📊 Toplam Gelir: {gelir} TL")
    print(f"📉 Toplam Gider: {gider} TL")
    print(f"💰 Bakiye: {gelir - gider} TL\n")

def aylik_ozet():
    ay = input("Hangi ay? (örnek: 2025-07): ")
    cursor.execute("SELECT SUM(miktar) FROM islemler WHERE tur='gelir' AND tarih LIKE ?", (ay + "%",))
    gelir = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(miktar) FROM islemler WHERE tur='gider' AND tarih LIKE ?", (ay + "%",))
    gider = cursor.fetchone()[0] or 0
    print(f"\n📅 {ay} Ayı Özeti:")
    print(f"   Toplam Gelir: {gelir} TL")
    print(f"   Toplam Gider: {gider} TL")
    print(f"   Bakiye: {gelir - gider} TL\n")

def csv_aktar():
    cursor.execute("SELECT * FROM islemler")
    veriler = cursor.fetchall()
    with open("gelirgider_raporu.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Tür", "Miktar", "Açıklama", "Tarih"])
        writer.writerows(veriler)
    print("📁 Veriler 'gelirgider_raporu.csv' dosyasına aktarıldı.\n")

def menu():
    while True:
        print("======== GELİR-GİDER TAKİP UYGULAMASI ========")
        print("1. Gelir Ekle")
        print("2. Gider Ekle")
        print("3. Toplam Bakiye Göster")
        print("4. Aylık Özet")
        print("5. CSV'ye Aktar")
        print("6. Çıkış")
        secim = input("Seçim yap (1-6): ")
        print()

        if secim == "1":
            gelir_ekle()
        elif secim == "2":
            gider_ekle()
        elif secim == "3":
            toplam_bakiye()
        elif secim == "4":
            aylik_ozet()
        elif secim == "5":
            csv_aktar()
        elif secim == "6":
            print("👋 Uygulama kapatılıyor...")
            break
        else:
            print("❌ Geçersiz seçim.\n")

menu()
conn.close()