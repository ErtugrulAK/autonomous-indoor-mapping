# live_slam_simulation.py
# Bu dosya, YouTube videosundaki gibi canlı haritalama simülasyonu yapar.
# Çalıştırmak için: python live_slam_simulation.py
# (pip install numpy matplotlib) komutları ile kütüphanelerin kurulu olması gerekir.

import numpy as np
import matplotlib.pyplot as plt
import math
import time

class VirtualWorld:
    """
    Kullanıcının istediği 2D Array (dizi) mantığını kullanarak sanal bir oda oluşturur.
    Harita: 1 = Duvar, 0 = Boş Alan
    """
    def __init__(self, width_cm, height_cm):
        self.width = width_cm
        self.height = height_cm
        # 0'larla dolu bir 2D array oluştur (1cm = 1 piksel)
        self.grid = np.zeros((height_cm, width_cm), dtype=np.uint8)

        # Duvarları çizelim (1 = Duvar)
        self.grid[10:height_cm-10, 10] = 1  # Sol duvar
        self.grid[10:height_cm-10, width_cm-10] = 1 # Sağ duvar
        self.grid[10, 10:width_cm-10] = 1  # Üst duvar
        self.grid[height_cm-10, 10:width_cm-10] = 1 # Alt duvar
        
        # Ortaya bir "engel" (cisim) koyalım
        self.grid[150:200, 200:250] = 1
        
        # Odanın içine bir "girinti" (L-şekli) yapalım
        self.grid[100:200, 10] = 0 # Sol duvarda bir boşluk
        self.grid[100, 10:100] = 1 # Girintinin üst duvarı
        self.grid[200, 10:100] = 1 # Girintinin alt duvarı
        self.grid[100:200, 99] = 1 # Girintinin iç duvarı


class SimulatedRobot:
    """
    Sanal dünyada hareket eden ve sensör verisi üreten robot.
    """
    def __init__(self, start_x, start_y, virtual_world):
        self.x = start_x
        self.y = start_y
        self.theta = math.pi / 2  # Radyan cinsinden açı (yukarı bakarak başla)
        self.world = virtual_world
        
        self.move_speed = 2.0  # Her adımda 2 cm gitsin
        self.turn_speed = math.radians(5) # Her adımda 5 derece dönsün
        
        # Keşif mantığı için
        self.state = "moving_forward"

    def scan(self, max_range=400):
        """
        Sensör simülasyonu (Raycasting).
        Robotun açısından bir ışın gönderir ve duvara (1) çarpana kadar gider.
        """
        for distance in range(1, max_range):
            # Işının o anki ucunun koordinatı
            ray_x = int(self.x + distance * math.cos(self.theta))
            ray_y = int(self.y + distance * math.sin(self.theta))

            # Haritanın dışına çıktı mı?
            if not (0 <= ray_x < self.world.width and 0 <= ray_y < self.world.height):
                return distance  # Dışarı çıktıysa, maksimum mesafeyi ver
            
            # Bir duvara (1) çarptı mı?
            if self.world.grid[ray_y, ray_x] == 1:
                return distance  # Çarptıysa, mesafeyi döndür
        
        return max_range # Hiçbir şeye çarpmadıysa

    def move_and_scan(self):
        """
        Robotun karar verme ve hareket etme mantığı.
        """
        # 1. Önce mevcut konumdan bir tarama yap
        distance = self.scan()

        # 2. Karar ver: Önü açık mı?
        if distance < 20: # Duvara çok yaklaştıysa
            self.state = "turning_left"
        else:
            self.state = "moving_forward"
            
        # 3. Hareketi uygula
        if self.state == "moving_forward":
            self.x += self.move_speed * math.cos(self.theta)
            self.y += self.move_speed * math.sin(self.theta)
        elif self.state == "turning_left":
            self.theta += self.turn_speed
            
        return distance


# --- Ana Simülasyon Kodu ---

if __name__ == "__main__":
    
    # 1. Dünyayı ve Robotu Oluştur
    world_cm = 500  # 500cm x 500cm bir oda (5 metre)
    world = VirtualWorld(world_cm, world_cm)
    robot = SimulatedRobot(start_x=250, start_y=250, virtual_world=world)

    # 2. Canlı Çizim (Live Plotting) Ayarları
    plt.ion()  # İnteraktif modu AÇ
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Boş çizim nesneleri oluştur (hızlı güncelleme için)
    map_plot, = ax.plot([], [], 'r.', markersize=0.5) # Harita (videodaki kırmızı noktalar)
    robot_plot, = ax.plot([], [], 'bo', markersize=5) # Robotun konumu
    
    ax.set_title("Live SLAM Simulation (Arena Recording)")
    ax.set_xlabel("X (cm)")
    ax.set_ylabel("Y (cm)")
    ax.set_xlim(0, world_cm)
    ax.set_ylim(0, world_cm)
    ax.set_aspect('equal') # Eksenleri eşit tut (kareler kare görünsün)
    ax.grid(True)

    # Verileri saklamak için listeler
    map_points_x = []
    map_points_y = []

    print("Simülasyon başlıyor. Kapatmak için pencereyi kapatın.")

    # 3. Ana Simülasyon Döngüsü
    try:
        while True:
            # Robotu hareket ettir ve sensör verisini al
            distance = robot.move_and_scan()
            
            # Harita için kırmızı noktanın global (x,y) koordinatını hesapla
            obstacle_x = robot.x + distance * math.cos(robot.theta)
            obstacle_y = robot.y + distance * math.sin(robot.theta)
            
            # Yeni noktayı harita verisine ekle
            map_points_x.append(obstacle_x)
            map_points_y.append(obstacle_y)
            
            # Grafiği YENİDEN ÇİZMEDEN GÜNCELLE (Hızlı Yöntem)
            map_plot.set_data(map_points_x, map_points_y)
            robot_plot.set_data(robot.x, robot.y)
            
            # Pencerenin güncellenmesi için çok kısa bekle
            plt.pause(0.001)

    except plt.TclError:
        print("Simülasyon penceresi kapatıldı.")
    except KeyboardInterrupt:
        print("Simülasyon durduruldu.")
    finally:
        plt.ioff()
        print("Bitti.")