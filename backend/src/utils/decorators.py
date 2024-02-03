import logging
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Dict, List

from fastapi import Response, status, Request


def fail_gracefully(func: Callable[..., Any]):
    @wraps(func)  # needed to play nice with FastAPI decorator
    def wrapper(response: Response, *args: List[Any], **kwargs: Dict[str, Any]) -> Any:
        start = datetime.now()
        try:
            data = func(response, *args, **kwargs)
            return {"data": data, "message": "200 OK", "time": datetime.now() - start}
        except Exception as e:
            logging.exception(e)
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {
                "data": [],
                "message": f"Error {str(e)}",
                "time": datetime.now() - start,
            }

    return wrapper


def async_fail_gracefully(func: Callable[..., Any]):
    @wraps(func)  # needed to play nice with FastAPI decorator
    async def wrapper(
        response: Response, *args: List[Any], **kwargs: Dict[str, Any]
    ) -> Any:
        start = datetime.now()
        try:
            data = await func(response, *args, **kwargs)
            return {"data": data, "message": "200 OK", "time": datetime.now() - start}
        except Exception as e:
            logging.exception(e)
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {
                "data": [],
                "message": f"Error {str(e)}",
                "time": datetime.now() - start,
            }

    return wrapper


def async_fail_gracefully_api_singular(func: Callable[..., Any]):
    @wraps(func)  # needed to play nice with FastAPI decorator
    async def wrapper(
        response: Response, *args: List[Any], **kwargs: Dict[str, Any]
    ) -> Any:
        try:
            return await func(response, *args, **kwargs)
        except Exception as e:
            logging.exception(e)
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {}

    return wrapper


def async_fail_gracefully_api_plural(func: Callable[..., Any]):
    @wraps(func)  # needed to play nice with FastAPI decorator
    async def wrapper(
        response: Response, *args: List[Any], **kwargs: Dict[str, Any]
    ) -> Any:
        try:
            return await func(response, *args, **kwargs)
        except Exception as e:
            logging.exception(e)
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return []

    return wrapper


def async_fail_gracefully_api_plural_testing(func: Callable[..., Any]):
    @wraps(func)  # needed to play nice with FastAPI decorator
    async def wrapper(
        request: Request, response: Response, *args: List[Any], **kwargs: Dict[str, Any]
    ) -> Any:
        print(request.headers)
        try:
            return await func(request, response, *args, **kwargs)
        except Exception as e:
            logging.exception(e)
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return []

    return wrapper
