import os
import logging
from flask import Flask
from dotenv import load_dotenv


from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry._logs import get_logger_provider, set_logger_provider

from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from azure.monitor.opentelemetry.exporter import AzureMonitorLogExporter

load_dotenv()

CONNECTION = "InstrumentationKey=0a00a0a0-00a0-0aaa-00aa-00aaa0aa00aa;IngestionEndpoint=https://eastus-8.in.applicationinsights.azure.com/;LiveEndpoint=https://eastus.livediagnostics.monitor.azure.com/"

app = Flask(__name__)
# app.config["OTEL_PYTHON_LOG_FORMAT"] = True
#
# logging.basicConfig()
# logger = logging.getLogger(__name__)
#
# FlaskInstrumentor().instrument_app(app)
# LoggingInstrumentor(set_logging_format=True).instrument()

logger_provider = LoggerProvider()
set_logger_provider(logger_provider)

log_exporter = AzureMonitorLogExporter(
    connection_string=os.getenv('APP_CONNECTION', CONNECTION)
)

get_logger_provider().add_log_record_processor(
    BatchLogRecordProcessor(log_exporter, schedule_delay_millis=6000)
)

handler = LoggingHandler()
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

logger.info("Hello, World!")

logger_provider.force_flush()

tracer_provider = TracerProvider(
        resource=Resource.create({SERVICE_NAME: str(os.getenv('SERVICE', 'service'))})
)
trace.set_tracer_provider(
    tracer_provider
)



RequestsInstrumentor().instrument()

trace_exporter = AzureMonitorTraceExporter(
    connection_string=os.getenv('APP_CONNECTION', CONNECTION)
)

tracer_provider.add_span_processor(
    BatchSpanProcessor(trace_exporter)
)

@app.route('/')
def hello():
    app.logger.info("hello info")
    return "<h1>Hello, World!<h1/>"

if __name__ == "__main__":
    app.run(debug = True, host="0.0.0.0", port=5000)
