FROM python:3.4

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
            postgresql-client libpq-dev python3-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/digitalprofessors

COPY requirements.txt ./

RUN pip install -r requirements.txt
COPY src ./
COPY local_settings.py digitalprofessors/

RUN rm requirements.txt
RUN ls

EXPOSE 8000
