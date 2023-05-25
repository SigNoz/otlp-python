# OTLP-Python

## Run

```bash
docker run --name otlp-python -p 5002:5002 --add-host signoz:host-gateway -e OTLP_ENDPOINT="signoz:4317" -e INSECURE="true" signoz/otlp-python
```

## Build

```bash
docker build -t otlp-python .

docker run --name otlp-python -p 5002:5002 --add-host signoz:host-gateway -e OTLP_ENDPOINT="signoz:4317" -e INSECURE="true" otlp-python
```

## Generate Data

```bash
curl http://127.0.0.1:5002/?user=alice
```

## Screenshots

**Traces page:**

![traces page](https://i.imgur.com/LgP4CGT.png)

**Logs page:**

![logs page](https://i.imgur.com/kpq2JrQ.png)

