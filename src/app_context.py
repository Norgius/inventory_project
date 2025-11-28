from contextvars import ContextVar

from slowapi import Limiter

limiter_var: ContextVar[Limiter] = ContextVar('limiter_var')
