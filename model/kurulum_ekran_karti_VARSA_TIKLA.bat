@echo off
echo ========================================================
echo NVIDIA Ekran Karti Olan Bilgisayarlar Icin Kurulum
echo ========================================================
echo Gerekli kutuphaneler (YOLO ve PyTorch GPU) kuruluyor...
echo Lutfen bekleyin, bu islem internet hiziniza gore birkac dakika surebilir.
echo.

pip install ultralytics
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

echo.
echo ========================================================
echo Kurulum basariyla tamamlandi! 
echo Artik terminale 'python train.py' yazarak egitime baslayabilirsiniz.
echo ========================================================
pause
