import matplotlib.pyplot as plt
import numpy as np

def load_map_points(filename="arena_data.txt"):
    """
    Sadece x,y koordinatlarını içeren TXT dosyasını okur.
    """
    x_points = []
    y_points = []
    
    print(f"Harita verisi {filename} dosyasından okunuyor...")
    
    try:
        # ÖNEMLİ: encoding='utf-8' ekledik
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#') or not line:
                    continue  # Yorumları veya boş satırları atla
                
                try:
                    parts = line.split(',')
                    if len(parts) == 2:
                        x_points.append(float(parts[0]))
                        y_points.append(float(parts[1]))
                except ValueError:
                    print(f"Hatalı satır atlanıyor: {line}")
                    
    except FileNotFoundError:
        print(f"HATA: {filename} dosyası bulunamadı!")
        return None, None
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        return None, None

    print(f"Toplam {len(x_points)} harita noktası yüklendi.")
    return x_points, y_points

if __name__ == "__main__":
    
    # 1. Veriyi dosyadan yükle
    x_coords, y_coords = load_map_points()
    
    if x_coords:
        print("Harita çizdiriliyor...")
        
        # 2. Grafiği oluştur
        plt.figure(figsize=(10, 10))
        
        # 3. Tüm (x,y) noktalarını kırmızı ve küçük noktalar olarak çiz
        # Tıpkı videodaki "Arena Recording" gibi
        plt.scatter(x_coords, y_coords, s=1, c='red', label='Duvarlar (Ham Veri)')
        
        # 4. Grafik ayarları
        plt.title("Final Harita Çıktısı (Arena Recording)", fontsize=16)
        plt.xlabel("X Koordinatı (cm)")
        plt.ylabel("Y Koordinatı (cm)")
        plt.grid(True)
        plt.axis('equal') # Eksenleri eşit tut (bu çok önemli)
        
        # Ortadaki robotun başladığı yeri (varsa) göstermek için
        plt.plot(250, 250, 'bo', markersize=8, label='Robot Başlangıç') 
        plt.legend()
        
        # Grafiği göster
        plt.show()
        
    else:
        print("Harita çizdirilemedi çünkü veri yüklenemedi.")