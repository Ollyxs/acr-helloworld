import os
import sys
from flask import Flask
from dotenv import load_dotenv


from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

load_dotenv()

app = Flask(__name__)
tracer_provider = TracerProvider(
        resource=Resource.create({SERVICE_NAME: str(os.getenv('SERVICE'))})
)
trace.set_tracer_provider(
    tracer_provider
)

FlaskInstrumentor().instrument_app(app)

RequestsInstrumentor().instrument()

trace_exporter = AzureMonitorTraceExporter(
    connection_string=os.getenv('APP_CONNECTION')
)

tracer_provider.add_span_processor(
    BatchSpanProcessor(trace_exporter)
)

@app.route('/')
def hello():
    return "<h1>Hello, World!<h1/>"

if __name__ == "__main__":
    app.run(debug = True, host="0.0.0.0", port=5000)
