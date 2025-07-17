FROM python:3.9.23-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /testFastAPI

RUN pip install --upgrade pip wheel

COPY req.txt ./req.txt

RUN pip install -r req.txt

COPY . .

RUN chmod +x prestart.sh

ENTRYPOINT ["prestart.sh"]

CMD ["python", "main.py"]