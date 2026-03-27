# Официальный образ с Python + Playwright + всеми зависимостями
FROM mcr.microsoft.com/playwright/python:v1.41.0-jammy

WORKDIR /app

# Копируем и ставим Python-зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY . .

# Запускаем приложение
CMD ["uvicorn", "task5:app", "--host", "0.0.0.0", "--port", "8080"]