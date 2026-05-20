from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.instrumentation.botocore import BotocoreInstrumentor
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from src.config import settings

def configure_tracing() -> None:
    resource = Resource.create(
        {
            "service.name": settings.otel_service_name,
        }
    )

    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(ConsoleSpanExporter())

    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    BotocoreInstrumentor().instrument()


def get_tracer():
    return trace.get_tracer(settings.otel_service_name)
