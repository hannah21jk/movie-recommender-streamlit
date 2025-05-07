#!/bin/bash

pip install -r requirements.txt


echo "Environment setup complete."


streamlit run app.py --server.port $PORT --server.enableCORS false --headless true
