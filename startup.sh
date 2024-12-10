#!/bin/bash
# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run app.py --server.port $PORT --server.enableCORS false
