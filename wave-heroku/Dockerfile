# Set Python version during build
ARG PYTHON_VERSION="3.8"

FROM python:${PYTHON_VERSION}-slim

# Install OS dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

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
RUN python3 -m venv "${VIRTUAL_ENV}"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY --chown=appuser:appuser . .

# Set permissions for the Entrypoint script
RUN chmod +x docker-entrypoint.sh

ARG PYTHON_MODULE="monitor_app.py"
ENV PYTHON_MODULE="${PYTHON_MODULE}"
EXPOSE 8008
ENTRYPOINT [ "./docker-entrypoint.sh" ]
