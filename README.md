# Opentelemetry-distro sitecustomize (auto-instrument) testing

Steps to setup the project:
1. Setup virtual environment: `python3 -m venv venv`
2. Activate the virtual env: `source venv/bin/activate`
3. Install the required pip packages: `pip install -r requirements.txt`
4. Activate the required opentelemetry env variables: `source fds_env`

## NOTE: PYTHONPATH env variable is required for sitecustomize. It needs to be set according to your operating system and virtual environment path.


To run the django app:
`PYTHONPATH=<your-python-path> OTEL_LOG_LEVEL=debug gunicorn -c NGANROCIAPI/gunicorn.py NGANROCIAPI.wsgi`

To check the test API endpoint: `curl http://localhost:10500/health -kv`

The health endpoint itself does nothing, just returns an OKAY message. But as the OTEL collector is not setup and unreachable,
the BatchSpanProcessor thread keeps retrying to send the traces exponentially, and during this time, django is unable to process
any other requests. Running the above curl command few times consecutively should reproduce this behavior.
