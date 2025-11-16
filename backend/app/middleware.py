import time
import logging
import traceback
import json
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.datastructures import MutableHeaders

logger = logging.getLogger("api")

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging all HTTP requests with full error details"""
    
    async def dispatch(self, request: Request, call_next):
        # Extract request info
        request_id = request.headers.get("X-Request-ID", "N/A")
        method = request.method
        path = request.url.path
        query_params = dict(request.query_params)
        client_ip = request.client.host if request.client else "unknown"
        
        # Log request details
        logger.info(f"[{request_id}] {method} {path} from {client_ip}")
        if query_params:
            logger.debug(f"[{request_id}] Query params: {query_params}")
        
        # Log request body for POST/PUT/PATCH
        if method in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.body()
                if body:
                    logger.debug(f"[{request_id}] Request body: {body.decode('utf-8')}")
            except Exception as e:
                logger.warning(f"[{request_id}] Could not read request body: {e}")
        
        # Measure time
        start_time = time.time()
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # Log response with full details
            status_code = response.status_code
            logger.info(
                f"[{request_id}] {method} {path} - Status: {status_code} - "
                f"Duration: {process_time:.3f}s"
            )
            
            # Log full response body for errors
            if status_code >= 400:
                try:
                    # Read response body
                    body = b''
                    async for chunk in response.body_iterator:
                        body += chunk
                    
                    logger.warning(
                        f"[{request_id}] Error response body: {body.decode('utf-8')}"
                    )
                    
                    # Create a new response with the same body
                    from starlette.responses import Response
                    response = Response(
                        content=body,
                        status_code=response.status_code,
                        headers=dict(response.headers)
                    )
                except Exception as e:
                    logger.error(f"[{request_id}] Could not read error response: {e}")
            
            # Add custom headers
            response.headers["X-Process-Time"] = str(process_time)
            response.headers["X-Request-ID"] = request_id
            
            return response
            
        except Exception as exc:
            process_time = time.time() - start_time
            error_msg = str(exc)
            error_type = type(exc).__name__
            error_trace = traceback.format_exc()
            
            logger.error(
                f"[{request_id}] EXCEPTION: {method} {path} - "
                f"Type: {error_type} - Message: {error_msg} - "
                f"Duration: {process_time:.3f}s",
                exc_info=True
            )
            logger.debug(f"[{request_id}] Full traceback:\n{error_trace}")
            
            raise
