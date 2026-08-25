FROM python:3.12-slim 

WORKDIR /production_deployment/app

COPY requirements_inference.txt .


RUN apt-get update && \
    apt-get install -y --no-install-recommends libgomp1 && \
    rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir -r requirements_inference.txt

COPY src ./src

EXPOSE 8000

CMD ["uvicorn", "src.production_deployment.app.main:app", "--host", "0.0.0.0", "--port", "8000"]

