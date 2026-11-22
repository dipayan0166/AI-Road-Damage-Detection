@echo off
title Smart Road Damage Detection & Geo-Tagged Inspection System
echo ======================================================================
echo   IPCV PROJECT: SMART ROAD DAMAGE DETECTION SYSTEM
echo   Target: NVIDIA GeForce RTX 3050 Ti / AMD Ryzen 7 6800H
echo ======================================================================
echo.
echo Launching Streamlit Interactive Web Application...
echo Local URL: http://localhost:8501
echo.
.venv\Scripts\streamlit.exe run app\app.py
pause

