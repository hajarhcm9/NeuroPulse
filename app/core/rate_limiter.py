"""Smart Guardian - Rate limiting middleware"""

import time
from collections import defaultdict
from typing import Dict, List
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger("smart-guardian")


class RateLimiter:
    """Sliding window rate limiter."""

    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self._windows: Dict[str, List[float]] = defaultdict(list)

    def is_allowed(self, key: str) -> bool:
        now = time.time()
        window = self._windows[key]
        self._windows[key] = [t for t in window if now - t < 60]
        window = self._windows[key]
        if len(window) >= self.requests_per_minute:
            return False
        self._windows[key].append(now)
        return True


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware for API endpoints."""

    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.limiter = RateLimiter(requests_per_minute)

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if path.startswith("/api/"):
            client_ip = request.client.host if request.client else "unknown"
            key = client_ip + ":" + path
            if not self.limiter.is_allowed(key):
                logger.warning("Rate limit exceeded: %s", key)
                return Response(
                    content='{"detail":"Rate limit exceeded. Try again later."}',
                    status_code=429,
                    media_type="application/json",
                )
        response = await call_next(request)
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        return response