FROM python:3.7

EXPOSE 8501

WORKDIR /workspace

COPY requirements.txt common_voice.py ./

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "common_voice.py"]
