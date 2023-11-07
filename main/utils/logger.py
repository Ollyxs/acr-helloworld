import os
import logging
from dotenv import load_dotenv

from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry._logs import set_logger_provider

from azure.monitor.opentelemetry.exporter import AzureMonitorLogExporter

load_dotenv()

logger_proiver = LoggerProvider()
set_logger_provider(logger_proiver)

log_exporter = AzureMonitorLogExporter(
    connection_string=os.getenv('APP_CONNECTION')
)

logger_proiver.add_log_record_processor(
    BatchLogRecordProcessor(log_exporter)
)

handler = LoggingHandler()
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Info
logger.info("Hello, World!")
# warning
logger.warning("This is a warning message.")
# Error
logger.error("This is an error message.")
# Exception
properties = {'custom_dimensions': str({'key_1': 'value_1', 'key_2': 'value_2'})}
# Use properties in exception logs
try:
    pass
except Exception:
    logger.exception('Capture an exception.', extra=properties)

logger_proiver.force_flush()
