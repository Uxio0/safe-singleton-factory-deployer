FROM python:3.10-slim

ARG APP_HOME=/app
WORKDIR ${APP_HOME}
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP flaskr

COPY requirements.txt ./
RUN set -ex \
	&& buildDeps=" \
		build-essential \
        git \
		libssl-dev \
		" \
    && apt-get update \
    && apt-get install -y --no-install-recommends $buildDeps \
    && pip install -U --no-cache-dir wheel setuptools pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove $buildDeps \
    && rm -rf /var/lib/apt/lists/* \
    && find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' +

COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8888", "flaskr:create_app()"]
