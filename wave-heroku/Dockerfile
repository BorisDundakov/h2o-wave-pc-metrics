# Accept Python version during build


ARG PYTHON_VERSION="3.8"

FROM python:${PYTHON_VERSION}-slim

# Install OS dependencies
RUN apt-get update && apt-get -y upgrade \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends curl build-essential \
    && apt-get install python3-pip -y



# Create a non-root user
RUN useradd --create-home appuser
USER appuser
WORKDIR /home/appuser/app

# Install Wave
ARG WAVE_VERSION="0.25.2"

ENV WAVE_HOME="/home/appuser/wave"
RUN \
    mkdir -p "${WAVE_HOME}" && \
    curl -fsSL https://github.com/h2oai/wave/releases/download/v${WAVE_VERSION}/wave-${WAVE_VERSION}-linux-amd64.tar.gz | tar -C ${WAVE_HOME} -xzv 2>&1
ENV WAVE_PATH="${WAVE_HOME}/wave-${WAVE_VERSION}-linux-amd64"

# Create a virtual environment
ENV VIRTUAL_ENV=/home/appuser/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install pacakges inside virtual environment
RUN pip install psutil \
    && pip install speedtest-cli

# Install Python dependencies
WORKDIR /home/appuser/app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY --chown=appuser:appuser . .

# Set permissions for the Entrypoint script
RUN chmod +x docker-entrypoint.sh

ARG PYTHON_MODULE
ENV PYTHON_MODULE="${PYTHON_MODULE}"
EXPOSE 10101
ENTRYPOINT [ "./docker-entrypoint.sh" ]

#docker run -detached -port local_port:container_port image_tag
# container port should always be 80!!??
# run 'docker build --build-arg PYTHON_VERSION=3.8 --build-arg WAVE_VERSION=0.25.2 --build-arg PYTHON_MODULE="ai_app/app.py" -t wave-heroku:0.1.0 . '
# and then run 'docker run --rm --name wave-heroku -p 10101:8888 -e PORT=8888 wave-heroku:0.1.0'


