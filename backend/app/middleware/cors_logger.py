from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class CORSLoggerMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log CORS-related information for debugging
    """
    async def dispatch(self, request: Request, call_next):
        # Log all request details
        logger.info(f"[CORS] Request method: {request.method}, Path: {request.url.path}")
        
        # Log all request headers
        logger.info(f"[CORS] Request headers: {dict(request.headers)}")
        
        # Log specific CORS-related headers
        if "origin" in request.headers:
            origin = request.headers.get("origin")
            logger.warning(f"[CORS] Origin header: {origin}")
            
            # Check if origin is in allowed list
            if origin in settings.BACKEND_CORS_ORIGINS:
                logger.info(f"[CORS] Origin {origin} is in allowed CORS origins")
            else:
                logger.warning(f"[CORS] Origin {origin} NOT in allowed CORS origins: {settings.BACKEND_CORS_ORIGINS}")
        
        if request.method == "OPTIONS":
            logger.warning(f"[CORS] Preflight OPTIONS request for path: {request.url.path}")
            acr_method = request.headers.get("access-control-request-method")
            acr_headers = request.headers.get("access-control-request-headers")
            logger.warning(f"[CORS] Access-Control-Request-Method: {acr_method}")
            logger.warning(f"[CORS] Access-Control-Request-Headers: {acr_headers}")
        
        # Process the request
        response = await call_next(request)
        
        # Log the response status
        logger.info(f"[CORS] Response status: {response.status_code}")
        
        # Log all response headers
        response_headers = dict(response.headers)
        logger.info(f"[CORS] Response headers: {response_headers}")
        
        # Log CORS-related response headers
        cors_headers = {k: v for k, v in response_headers.items() if "access-control" in k.lower()}
        if cors_headers:
            logger.warning(f"[CORS] Response CORS headers: {cors_headers}")
        else:
            logger.error(f"[CORS] NO CORS HEADERS in response for {request.method} {request.url.path}")
            
            # For preflight requests, try to add CORS headers if they're missing
            if request.method == "OPTIONS" and "origin" in request.headers:
                origin = request.headers.get("origin")
                if origin in settings.BACKEND_CORS_ORIGINS:
                    logger.warning(f"[CORS] Adding missing CORS headers to OPTIONS response")
                    response.headers["Access-Control-Allow-Origin"] = origin
                    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
                    response.headers["Access-Control-Allow-Headers"] = "*"
                    response.headers["Access-Control-Allow-Credentials"] = "true"
                    response.headers["Access-Control-Max-Age"] = "600"
            
        return response
