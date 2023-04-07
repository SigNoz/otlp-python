import logging
from opentelemetry import trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (
    OTLPLogExporter,
)
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider

trace.set_tracer_provider(TracerProvider())


import random
import string
import time
import json
import os
logger_provider = LoggerProvider(
    resource=Resource.create(
        {
            "service.name": "shoppingcart",
            "service.instance.id": "instance-12",
        }
    ),
)
set_logger_provider(logger_provider)
# exporter = OTLPLogExporter(endpoint="signoz.io:4317", insecure=False, headers= {"signoz-access-token": "Bearer"})
exporter = OTLPLogExporter(endpoint=os.getenv("OTLP_ENDPOINT", "localhost:4317"), insecure=json.loads(os.getenv("INSECURE", "true").lower()))
logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
handler = LoggingHandler(level=logging.WARNING, logger_provider=logger_provider)
# Attach OTLP handler to root logger
logging.getLogger().addHandler(handler)
# Log directly
logging.info("Jackdaws love my big sphinx of quartz.")
# Create different namespaced loggers
logger1 = logging.getLogger("myapp.area1")
logger2 = logging.getLogger("myapp.area2")

tracer = trace.get_tracer(__name__)
while True:
    time.sleep(5)
    try:
        with tracer.start_as_current_span("foo"):
            # Do something
            res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            method = random.choice(["GET", "POST", "PUT", "DELETE"])
            status = random.choice([200, 201, 203, 400, 401, 403, 404, 500, 501, 503])
            level = random.choice(["INFO", "ERROR", "WARN", "DEBUG"])
            response_time_ms = random.randint(1, 1000)
            logger2.warning(res, extra={"method": method, "status": status, "level": level, "response_time": response_time_ms})
    except KeyboardInterrupt:
        print("Exiting...")
        logger_provider.shutdown()
        break
    except:
        logger_provider.shutdown()
        continue
    # logger2.error(" 2023-03-15 17:38:08 simpleMessageListenerContainer-178 INFO  c.g.core.provider.ConsumeRestApiImpl              user-id= 42f17af5-8c73-4567-9206-2dc5a8f84bb7   trace-id=              span-id=                                     line:62  :  Consuming Rest API")
logger_provider.shutdown()