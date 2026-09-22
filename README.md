# H2O Wave PC Metrics

![Screenshot from 2023-07-08 21-05-26](https://github.com/BorisDundakov/h2o-wave-pc-metrics/assets/71731579/558791b5-82c5-4fa0-8acc-39067212bebd)

A containerized real-time system monitoring dashboard built with **Python**, **H2O Wave**, and **Docker**, with CI/CD automation through **GitHub Actions**.

The application collects system and network metrics from the machine on which it is running and displays them through an H2O Wave dashboard.

The main purpose of the project is to demonstrate the combination of a Python monitoring application with containerization and CI/CD automation.

## What the Application Does

The application continuously collects and displays system information including:

- CPU utilization
- CPU core count
- Memory utilization
- Battery level
- CPU temperature
- Last system boot time
- Download speed
- Upload speed

System information is collected primarily using Python's `psutil` library, while network performance is measured using `speedtest-cli`.

The dashboard is built using H2O Wave and is continuously updated while the application is running.

## Architecture

```text
Host System
    │
    │ System metrics
    │
    ├── CPU
    ├── Memory
    ├── Battery
    ├── Temperature
    ├── Boot time
    └── Network speed
    │
    ▼
Python Monitoring Application
    │
    │ psutil / speedtest-cli
    ▼
H2O Wave
    │
    ▼
Web Dashboard
```

The complete application is packaged and executed inside a Docker container.

```text
GitHub Repository
       │
       │ git push
       ▼
 GitHub Actions
       │
       │ CI/CD
       ▼
  Docker Image
       │
       ▼
Docker Container
       │
       ▼
Python + H2O Wave
       │
       ▼
Monitoring Dashboard
```

## Technologies

| Technology | Purpose |
|---|---|
| Python | Monitoring application |
| psutil | Collection of host system metrics |
| speedtest-cli | Network speed measurements |
| H2O Wave | Web dashboard |
| Docker | Application containerization |
| GitHub Actions | CI/CD automation |
| GitHub | Source control |

## Repository Structure

```text
h2o-wave-pc-metrics/
├── .github/
│   └── workflows/          # GitHub Actions workflows
│
├── app/
│   └── monitor_app.py      # System monitoring application
│
├── Dockerfile              # Container image definition
├── docker-entrypoint.sh    # Starts Wave server and application
├── requirements.txt        # Python dependencies
└── README.md
```

## How the Container Works

The Docker image provides both the Python runtime and H2O Wave environment required by the application.

When the container starts:

1. `docker-entrypoint.sh` starts the H2O Wave server.
2. Wave listens on the configured container port.
3. The Python monitoring application is started using `wave run`.
4. The application begins collecting system metrics.
5. Metrics are continuously displayed through the Wave dashboard.

## Running Locally

### Build the Docker Image

```bash
docker build \
  --build-arg PYTHON_VERSION=3.10 \
  --build-arg WAVE_VERSION=0.25.2 \
  --build-arg PYTHON_MODULE="app/monitor_app.py" \
  -t h2o-wave-pc-metrics:2.0.0 .
```

### Start the Container

```bash
docker run --rm \
  --name h2o-wave-pc-metrics \
  -p 10101:8008 \
  -e PORT=8008 \
  h2o-wave-pc-metrics:2.0.0
```

The dashboard can then be accessed at:

```text
http://localhost:10101
```

## CI/CD

GitHub Actions is used to automate the build and delivery process.

```text
Code Change
    │
    ▼
Git Push
    │
    ▼
GitHub Actions
    │
    ▼
Build Docker Image
    │
    ▼
Deploy / Publish Application
```

This removes the need to manually rebuild the application after every code change and demonstrates a basic container-based CI/CD workflow.

## What This Project Demonstrates

The project provides practical experience with:

- Python-based system monitoring
- Linux system metrics
- Docker image creation
- Running applications as a non-root container user
- Container entrypoint scripts
- H2O Wave application deployment
- GitHub Actions CI/CD
- Dependency management
- Build-time and runtime configuration