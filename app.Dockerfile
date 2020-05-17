ARG APP_NAME
FROM $APP_NAME

ARG CORS_ALLOWS
ENV CORS_ALLOWS=${CORS_ALLOWS}

CMD ["python", "-m", "uvicorn", "src.main:app","--host","0.0.0.0","--port","5000"]