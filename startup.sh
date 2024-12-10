#!/bin/bash
# Install dependencies using pip3
python3 -m pip install -r requirements.txt

# Run Streamlit app using python3
python3 -m streamlit run app.py --server.port $PORT --server.enableCORS false
