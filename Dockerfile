FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .

# Añadir la variable de entorno para la depuración
ENV PYTHONUNBUFFERED=1


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-dir", "./"]

EXPOSE 8000