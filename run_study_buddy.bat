@echo off
REM Run the study buddy app using the workspace virtual environment.
if not exist ".venv\Scripts\python.exe" (
  echo 正在创建虚拟环境 .venv ...
  python -m venv .venv
  if errorlevel 1 (
    echo 无法创建虚拟环境，请检查 Python 安装。
    exit /b 1
  )
  echo 正在安装依赖 ...
  .venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel
  .venv\Scripts\python.exe -m pip install -r requirements.txt
  if errorlevel 1 (
    echo 依赖安装失败，请检查网络或 requirements.txt。
    exit /b 1
  )
)
.venv\Scripts\python.exe study_buddy.py
