@echo off
echo ========================================================
echo Environment Setup for CPU Systems (No GPU)
echo ========================================================
echo Installing required dependencies (YOLO)...
echo.

pip install ultralytics

echo.
echo ========================================================
echo Environment setup completed!
echo.
echo NOTE: Please ensure 'device='cpu'' is configured in
echo 'train.py' before running training on CPU hardware.
echo ========================================================
pause
