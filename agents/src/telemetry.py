import base64
import os

from openinference.instrumentation.agno import AgnoInstrumentor
from opentelemetry import trace as trace_api
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

def start_telemetry():
    langfuse_public_key = os.getenv('LANGFUSE_PUBLIC_KEY')
    langfuse_secret_key = os.getenv('LANGFUSE_SECRET_KEY')
    langfuse_base_url = os.getenv('LANGFUSE_BASE_URL')

    if not langfuse_public_key or not langfuse_secret_key or not langfuse_base_url:
        print("[WARNING] LANGFUSE_PUBLIC_KEY/LANGFUSE_SECRET_KEY/LANGFUSE_BASE_URL environment variables are not set, telemetry is disabled.")
        return
    
    LANGFUSE_AUTH = base64.b64encode(
        f"{langfuse_public_key}:{langfuse_secret_key}".encode()
    ).decode()

    os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = f"{langfuse_base_url}/api/public/otel" # 🏠 Local deployment (>= v3.22.0)
    os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {LANGFUSE_AUTH}"

    tracer_provider = TracerProvider()
    tracer_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter()))
    trace_api.set_tracer_provider(tracer_provider=tracer_provider)

    # Start instrumenting agno
    AgnoInstrumentor().instrument()

    print(f"Connected to langfuse on {langfuse_base_url}")
