from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter


from core.config import auth_config


def configure_tracer() -> None:
    trace.set_tracer_provider(
    TracerProvider(
            resource=Resource.create({SERVICE_NAME: "auth_service"})
        )
    )
    tracer = trace.get_tracer_provider()
    jaeger_exporter = JaegerExporter(

                agent_host_name=auth_config.jaeger_host,
                agent_port=auth_config.jaeger_port,
            )

    tracer.add_span_processor(BatchSpanProcessor(jaeger_exporter))
    # Чтобы видеть трейсы в консоли
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(ConsoleSpanExporter())
    )
