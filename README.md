


## Run
`docker build -t app .`
`docker run --rm -e OTLP_ENDPOINT="host.docker.internal:4317" -e INSECURE="true" app`