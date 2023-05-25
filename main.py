import logging
from opentelemetry import trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (
    OTLPLogExporter,
)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
)
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
import random
import string
import time
import json
import os

from flask import Flask, jsonify, request

resource = Resource.create(
        {
            "service.name": "shoppingcart",
            "service.instance.id": "instance-12",
        }
    )

# create the providers
trace_provider = TracerProvider(resource=resource)
logger_provider = LoggerProvider(resource=resource)

# set the providers
trace.set_tracer_provider(trace_provider)
set_logger_provider(logger_provider)

exporter = OTLPLogExporter(endpoint=os.getenv("OTLP_ENDPOINT", "localhost:4317"), insecure=json.loads(os.getenv("INSECURE", "true").lower()))
exporterspan = OTLPSpanExporter(endpoint=os.getenv("OTLP_ENDPOINT", "localhost:4317"), insecure=json.loads(os.getenv("INSECURE", "true").lower()))


# add the batch processors to the trace provider
logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(exporterspan)
)



handler = LoggingHandler(level=logging.DEBUG,logger_provider=logger_provider)
# Attach OTLP handler to root logger
# logging.getLogger().addHandler(handler)
# Log directly
logging.info("Jackdaws love my big sphinx of quartz.")
# Create different namespaced loggers
logger1 = logging.getLogger("myapp.area1")
logger2 = logging.getLogger("myapp.area2")
logger2.addHandler(handler)
logger2.setLevel(logging.DEBUG)


tracer = trace.get_tracer(__name__)


app = Flask(__name__)

app.logger.addHandler(handler)


def get_random_time():
    return random.randint(100, 1500) / 1000.0


@app.route('/', methods = ['GET', 'POST'])
def home():
    if(request.method == 'GET'):
        with tracer.start_as_current_span("home"):
            args = request.args
            user = args.get('user',  "anonymous")
            with tracer.start_as_current_span("authenticate"):
                time.sleep(get_random_time())
                logger2.debug("authenticating user: " + user)
                with tracer.start_as_current_span("authenticate_check_cache"):
                    time.sleep(get_random_time())
                with tracer.start_as_current_span("authenticate_check_db"):
                    time.sleep(get_random_time())

                with tracer.start_as_current_span("check_request limit"):
                    time.sleep(get_random_time())
            
            with tracer.start_as_current_span("get_cart"):
                logger2.debug("getting cart for user: " + user)
                with tracer.start_as_current_span("check cart in cache"):
                    time.sleep(get_random_time())
                with tracer.start_as_current_span("check cart in db"):
                    logger2.debug("checking cart from db for : " + user)
                    time.sleep(get_random_time())
            
            logger2.info("completed request for user: " + user, extra={"method": "GET", "status": 200, "level": "info"})
            return "Hello " + user
  
  
# driver function
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
    logger_provider.shutdown()
    trace_provider.shutdown()