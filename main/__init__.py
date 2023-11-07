import os
# import logging
from flask import Flask
from dotenv import load_dotenv
# OpenTelemetry
from opentelemetry import trace
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
# from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
# from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
# from opentelemetry._logs import set_logger_provider
# Azure Monitor
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
# from azure.monitor.opentelemetry.exporter import AzureMonitorLogExporter
from main.utils.logger import logger


load_dotenv()

logger.info("Creating app...")

def create_app():
    app = Flask(__name__)
    
    # logger_provider = LoggerProvider()
    # set_logger_provider(logger_provider)
    #
    # log_exporter = AzureMonitorLogExporter(
    #     connection_string=os.getenv('APP_CONNECTION')
    # )
    #
    # logger_provider.add_log_record_processor(
    #     BatchLogRecordProcessor(log_exporter)
    # )
    #
    # handler = LoggingHandler()
    # logger = logging.getLogger(__name__)
    # logger.addHandler(handler)
    # logger.setLevel(logging.INFO)
    #
    # # Info
    # logger.info("Hello, World!")
    # # Exception
    # properties = {'custom_dimensions': str({'key_1': 'value_1', 'key_2': 'value_2'})}
    # # Use properties in exception logs
    # try:
    #     pass  # generate a ZeroDivisionError
    # except Exception:
    #     logger.exception('Capture an exception.', extra=properties)
    # # Error
    # logger.error('This is an error message.')
    #
    # logger_provider.force_flush()

    tracer_provider = TracerProvider(
        resource=Resource.create({SERVICE_NAME: str(os.getenv('SERVICE'))})
    )
    trace.set_tracer_provider(tracer_provider)

    RequestsInstrumentor().instrument()

    trace_exporter = AzureMonitorTraceExporter(
        connection_string=os.getenv('APP_CONNECTION')
    )

    tracer_provider.add_span_processor(
        BatchSpanProcessor(trace_exporter)
    )

    from main.routes import routes
    app.register_blueprint(routes.main)

    return app
