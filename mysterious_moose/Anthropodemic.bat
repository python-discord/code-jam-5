if not exist venv/ (
    python -m venv venv
    venv\Scripts\activate.bat
    python -m pip install -r requirements.txt
    python -m src
) else (
    venv\Scripts\activate.bat
    python -m src
)
