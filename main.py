from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"

app = FastAPI(
    title="e-RAPHA NADI Demo",
    description=(
        "Prototype digital health platform integrating Nadi-based "
        "physiological assessment, targeted acupressure with induced "
        "pressure, and Tai Chi Chuan protocols in a closed-loop system."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "system": "e-RAPHA NADI",
        "mode": "prototype",
    }


@app.get("/api/nadi")
def get_nadi_state():
    """
    Prototype Nadi state.
    Values are simulated and are NOT a medical diagnosis.
    """
    return {
        "vata": 0.67,
        "pitta": 0.33,
        "kapha": 0.00,
        "arousal": 0.74,
        "recovery": 0.31,
        "signal_quality": 0.94,
    }


@app.get("/api/acupressure")
def get_acupressure_protocol():
    """
    Prototype intervention protocol.
    Pressure values are intentionally represented as protocol
    identifiers rather than clinical pressure prescriptions.
    """
    return {
        "protocol_id": "TC_ACU_001",
        "point": "PC6",
        "point_name": "Nei Guan",
        "stimulation": "controlled_pressure",
        "duration_seconds": 60,
        "tai_chi_chuan_protocol": "TCC_001",
    }


@app.get("/api/pressure")
def get_pressure_state():
    return {
        "state": "READY",
        "pressure": 0,
        "target": 0,
        "safety": "NORMAL",
        "emergency_release": False,
    }


@app.post("/api/pressure/start")
def start_pressure():
    return {
        "state": "RAMPING",
        "message": "Pressure protocol started in simulation mode.",
    }


@app.post("/api/pressure/release")
def release_pressure():
    return {
        "state": "RELEASED",
        "pressure": 0,
        "emergency_release": False,
    }


@app.get("/api/response")
def get_response():
    return {
        "before": {
            "heart_rate": 78,
            "hrv": 42,
        },
        "after": {
            "heart_rate": 72,
            "hrv": 48,
        },
        "response_status": "MEASURED",
        "prototype": True,
    }


# Serve frontend if it exists
if FRONTEND_DIR.exists():
    app.mount(
        "/",
        StaticFiles(directory=FRONTEND_DIR, html=True),
        name="frontend",
    )
