FROM python:3.12-slim

WORKDIR /app

COPY app ./app
COPY scripts ./scripts

ENV RULEDESK_HOST=0.0.0.0
ENV RULEDESK_PORT=8000
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["python", "-m", "app.main"]
