
FROM python:3.12-slim AS build

WORKDIR /book14

COPY ./requirements.txt /book14/requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r /book14/requirements.txt

FROM python:3.12-slim

WORKDIR /book14

COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=build /usr/local/bin /usr/local/bin
COPY --from=build /book14 /book14
COPY ./app /book14/app
COPY ./.env /book14
ENV PYTHONPATH=/book14
CMD ["uvicorn", "app.server.app:app"]