FROM public.ecr.aws/docker/library/python:3.12-slim

COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.3 /lambda-adapter /opt/extensions/lambda-adapter
ENV PORT=8000

WORKDIR /var/task

COPY ./Pipfile ./
COPY ./Pipfile.lock ./
RUN pip install pipenv
RUN pipenv sync --system
COPY ./app ./app

CMD exec uvicorn --port=$PORT app.main:app