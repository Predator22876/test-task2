FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN python -m pip install --upgrade pip

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY docker-entrypoint.sh /app/
COPY . /app
RUN chmod +x /app/docker-entrypoint.sh
RUN addgroup --system app && adduser --system --ingroup app app && chown -R app:app /app

USER app

EXPOSE 8000

ENTRYPOINT ["/app/docker-entrypoint.sh"]
