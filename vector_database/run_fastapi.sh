rm __pycache__/*;
uvicorn second:app --host 0.0.0.0 --port 8080;