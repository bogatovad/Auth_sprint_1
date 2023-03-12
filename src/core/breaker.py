from http import HTTPStatus
from pybreaker import CircuitBreaker, CircuitBreakerError


class CustomCircuitBreakerError(CircuitBreakerError):
    ERROR_MESSAGE = "We'll be back soon!"


breaker = CircuitBreaker(fail_max=3, reset_timeout=30)


def handle_breaker_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CustomCircuitBreakerError as e:
            return {"message": e.ERROR_MESSAGE}, HTTPStatus.SERVICE_UNAVAILABLE
    return wrapper
