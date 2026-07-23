from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import uuid

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware para adicionar cabeçalhos de segurança nas respostas e injetar um ID de requisição.
    """
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        
        # Cabeçalhos de segurança básicos
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # Injeção de ID de requisição
        request_id = str(uuid.uuid4())
        response.headers["X-Request-ID"] = request_id
        
        return response
