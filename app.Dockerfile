ARG BASE_IMAGE
FROM $BASE_IMAGE

ARG CORS_ALLOWS
ENV CORS_ALLOWS=${CORS_ALLOWS}

ARG USER_REPOSITORY_PATH
ENV USER_REPOSITORY_PATH=${USER_REPOSITORY_PATH}

RUN mkdir run data

COPY src/apps/auth/repository/users.json ${USER_REPOSITORY_PATH}

CMD ["python", "-m", "uvicorn", "src.main:app","--host","0.0.0.0","--port","5000"]