if not exist venv (
    echo Virtual environment not found. Creating it...
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)

python main.py

exist /b