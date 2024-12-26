FROM python:3.12

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /drf_proxy

COPY requirements.txt /drf_proxy/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /drf_proxy

COPY create_superuser.sh /drf_proxy/create_superuser.sh
RUN chmod +x /drf_proxy/create_superuser.sh

ENTRYPOINT ["bash", "/drf_proxy/create_superuser.sh"]

CMD ["uvicorn", "drf_proxy.asgi:application", "--host", "0.0.0.0", "--port", "8002"]
