from __future__ import annotations
import os
import base64
from contextlib import contextmanager
from typing import Any
from langfuse import get_client

class _NoOpObservation:
    def update(self, **kwargs): pass
    def end(self): pass

class _NoOpClient:
    @contextmanager
    def start_as_current_observation(self, **kwargs):
        yield _NoOpObservation()
    def update_current_span(self, **kwargs): pass
    def create_score(self, **kwargs): pass
    def flush(self): pass

_client = None

def get_langfuse_client():
    # daca nu punem global s ar crea o variabila nou _client in alta zona din memoria 
    global _client
    if _client is not None:
        return _client

    pk = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
    sk = os.environ.get("LANGFUSE_SECRET_KEY", "")
    host = os.environ.get("LANGFUSE_HOST", "http://localhost:3000")

    if not pk or not sk or "placeholder" in pk:
        _client = _NoOpClient()
        return _client

    try:
        #we are doing this to communicate the SDK with Langfuse 
        token = base64.b64encode(f"{pk}:{sk}".encode()).decode()
        os.environ["LANGFUSE_HOST"] = host
        os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = f"{host}/api/public/otel"
        os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {token}"

        _client = get_client()
    except Exception as e:
        print(f"Langfuse init error: {e}")
        _client = _NoOpClient()

    return _client
