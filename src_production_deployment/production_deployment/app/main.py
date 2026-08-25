import uuid
from fastapi import FastAPI, HTTPException
from src_production_deployment.production_deployment.app.schemas.forecast import ForecastRequest #ForecastResponse
from src_production_deployment.production_deployment.app.services.forecasting_service import ForecastingService
from src_production_deployment.configs.config import API_VERSION , MODEL_VERSION
from src_production_deployment.logger.logging import setup_logging
from io import BytesIO
from fastapi.responses import StreamingResponse, Response
from prometheus_client import Counter, Histogram, generate_latest, Gauge # "I want to create a metric whose value represents something that only increases."
import time


log = setup_logging()

app = FastAPI(title = "Demand Forecasting API", version = "1.0.0")

forecast_requests_total = Counter("forecast_requests_total", "Total number of forecast requests",["status"])
forecast_request_duration = Histogram("forecast_request_duration_seconds", "Time spent processing forecast requests", buckets=[5, 10, 30, 60, 90, 120, 180, 300, 600])
api_health = Gauge("api_health", "API health status")
# The first string inside Counter() / Histogram() is the Prometheus metric name


forecasting_service = ForecastingService()

@app.get("/")
def root():
    return {
        "service": "Demand Forecasting API",
        "version": API_VERSION,
        "status": "running"
    }

@app.get("/health")
def health():
    
    if forecasting_service is None:
        raise HTTPException(status_code=503, detail="Forecasting service unavailable")

    api_health.set(1)

    return {
                        "status": "healthy",
                        "service": "Demand Forecasting API",
                        "version": API_VERSION,
                        "model_version": MODEL_VERSION
    }


@app.get("/ready")
def ready():

    if forecasting_service is None:
        raise HTTPException(status_code=503, detail="Forecasting service not ready")

    return {
        "status": "ready"
          }


@app.post("/forecast") #response_model = ForecastResponse)
def forecast(request:ForecastRequest):

    # forecast_requests_total.inc() # increase counter by 1

    start_time = time.perf_counter()

    time.sleep(2)

    request_id = str(uuid.uuid4())

    log.info("Forecast API request started: request_id=%s, forecast_days=%s", request_id, request.forecast_days)

    try:

        final_result = forecasting_service.forecast(request.forecast_days)

        #final_result["request_id"] = request_id

        #final_result["model_version"] = MODEL_VERSION

        result = final_result["predictions"]

        result["request_id"] = request_id

        result["model_version"] = MODEL_VERSION

        buffer = BytesIO()

        result.to_csv(buffer,index=False)

        buffer.seek(0)

        log.info("Forecast completed: request_id=%s, forecast_days=%s, predictions=%s",
                request_id,
                request.forecast_days,
                len(final_result["predictions"])
            )

        log.info("Final result%s" , final_result)

        forecast_requests_total.labels(status="success").inc()

        return StreamingResponse( buffer, media_type="text/csv",headers={
                    "Content-Disposition":
                    f'attachment; filename="forecast_{request.forecast_days}_days.csv"'
            })

    except ValueError as exc:
        log.exception("Forecast API request failed: request_id=%s", request_id)
        forecast_requests_total.labels(status = "error").inc()
        raise HTTPException(status_code=400, detail=str(exc))

    except Exception:
        log.exception("Unexpected forecast API failure: request_id=%s", request_id)
        forecast_requests_total.labels(status = "error").inc()
        raise HTTPException(status_code=500, detail="Internal server error while generating forecast")

    finally:
        print(">>> RECORDING FORECAST DURATION <<<")
        duration = time.perf_counter() - start_time
        forecast_request_duration.observe(duration)


@app.get("/metrics")
def metrics():
    return Response(content = generate_latest(), media_type="text/plain")





# generate_latest() - This asks the Prometheus Python client: "Give me all the metrics currently maintained by this application."
# HELP forecast_requests_total Total number of forecast requests
# TYPE forecast_requests_total counter
# forecast_requests_total 3.0
