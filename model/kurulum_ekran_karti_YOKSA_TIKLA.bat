@echo off
echo ========================================================
echo Ekran Karti OLMAYAN (Sadece CPU) Bilgisayarlar Icin Kurulum
echo ========================================================
echo Gerekli kutuphaneler (YOLO) kuruluyor...
echo.

pip install ultralytics

echo.
echo ========================================================
echo Kurulum tamamlandi!
echo.
echo LUTFEN DIKKAT: Kodun calismasi icin lutfen 'train.py' dosyasini acip
echo icerisindeki "device='0'" yazan yeri "device='cpu'" olarak degistirin!
echo ========================================================
pause
