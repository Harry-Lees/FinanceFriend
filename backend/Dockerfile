FROM python3:8

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNONBUFFERED 1

ADD requirements.txt
RUN python -m pip install -r requirements.txt

WORKDIR /app
ADD ./app

RUN useradd appuser && chown -R appuser /app
USER appuser

CMD ["uvicorn", "main:app"]
