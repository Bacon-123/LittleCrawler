@echo off
chcp 65001 >nul
title LittleCrawler 启动器

echo.
echo ========================================
echo   LittleCrawler 一键启动
echo ========================================
echo.

REM 启动后端（新窗口）
echo [1/2] 正在启动后端 API...
start "LittleCrawler-后端-8080" cmd /k ".venv\Scripts\activate && python -m uvicorn api.main:app --host 0.0.0.0 --port 8080"

REM 等待后端启动
timeout /t 3 /nobreak >nul

REM 启动前端（新窗口）
echo [2/2] 正在启动前端...
start "LittleCrawler-前端-3000" cmd /k "cd web && npm run dev"

timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo   启动完成！
echo ========================================
echo.
echo   后端 API: http://localhost:8080
echo   前端界面: http://localhost:3000
echo.
echo   关闭此窗口不会停止服务
echo   请分别关闭后端/前端窗口来停止服务
echo ========================================
echo.
pause
