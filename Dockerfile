FROM python:3.8-slim

WORKDIR /app

# Copy only necessary files
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app

CMD ["python", "evaluate_tests.py"]
