@echo off
echo ========================================================
echo Environment Setup for NVIDIA GPU Systems
echo ========================================================
echo Installing required dependencies (YOLO and PyTorch GPU)...
echo Please wait, this process may take several minutes.
echo.

pip install ultralytics
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

echo.
echo ========================================================
echo Environment setup completed successfully!
echo You can now execute 'python train.py' to start training.
echo ========================================================
pause
