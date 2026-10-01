"""
e-RAPHA NADI — Protocol Engine

Maps the prototype digital Nadi state to an intervention protocol.

The protocol contains:
    1. Acupressure point(s)
    2. Induced-pressure method
    3. Pressure-control parameters
    4. Tai Chi Chuan protocol

All values are prototype/demo parameters and are NOT clinical
treatment prescriptions.
"""

from dataclasses import dataclass, asdict
from typing import List


@dataclass
class AcupressurePoint:
    point_id: str
    name: str
    location: str
    body_region: str


@dataclass
class PressureProtocol:
    mode: str
    ramp_seconds: int
    active_seconds: int
    release_seconds: int
    profile: str
    safety_release: bool = True


@dataclass
class TaiChiChuanProtocol:
    protocol_id: str
    name: str
    description: str
    sequence: List[str]


@dataclass
class InterventionProtocol:
    protocol_id: str
    name: str
    state: str
    points: List[AcupressurePoint]
    pressure: PressureProtocol
    tai_chi_chuan: TaiChiChuanProtocol


# ---------------------------------------------------------------------
# ACUPRESSURE POINT DATABASE
# ---------------------------------------------------------------------

POINTS = {
    "PC6": AcupressurePoint(
        point_id="PC6",
        name="Nei Guan",
        location="Inner forearm, proximal to the wrist",
        body_region="wrist",
    ),

    "LV3": AcupressurePoint(
        point_id="LV3",
        name="Tai Chong",
        location="Dorsum of the foot",
        body_region="foot",
    ),

    "ST36": AcupressurePoint(
        point_id="ST36",
        name="Zu San Li",
        location="Lower leg below the knee region",
        body_region="leg",
    ),
}


# ---------------------------------------------------------------------
# TAI CHI CHUAN PROTOCOLS
# ---------------------------------------------------------------------

TAI_CHI_PROTOCOLS = {
    "TCC_001": TaiChiChuanProtocol(
        protocol_id="TCC_001",
        name="Tai Chi Chuan — Calm Sequence",
        description=(
            "Prototype Tai Chi Chuan sequence associated with "
            "the selected acupressure protocol."
        ),
        sequence=[
            "Preparation",
            "Opening",
            "Slow weight transfer",
            "Controlled arm sequence",
            "Closing",
        ],
    ),

    "TCC_002": TaiChiChuanProtocol(
        protocol_id="TCC_002",
        name="Tai Chi Chuan — Balance Sequence",
        description=(
            "Prototype Tai Chi Chuan sequence for a balanced "
            "intervention protocol."
        ),
        sequence=[
            "Preparation",
            "Opening",
            "Weight transfer",
            "Coordinated arm sequence",
            "Closing",
        ],
    ),

    "TCC_003": TaiChiChuanProtocol(
        protocol_id="TCC_003",
        name="Tai Chi Chuan — Activation Sequence",
        description=(
            "Prototype Tai Chi Chuan sequence associated with "
            "an activation-oriented protocol."
        ),
        sequence=[
            "Preparation",
            "Opening",
            "Dynamic weight transfer",
            "Coordinated arm sequence",
            "Closing",
        ],
    ),
}


# ---------------------------------------------------------------------
# PRESSURE PROTOCOLS
# ---------------------------------------------------------------------

PRESSURE_PROFILES = {
    "CALM": PressureProtocol(
        mode="controlled_pressure",
        ramp_seconds=10,
        active_seconds=60,
        release_seconds=10,
        profile="CALM",
    ),

    "BALANCE": PressureProtocol(
        mode="controlled_pressure",
        ramp_seconds=10,
        active_seconds=60,
        release_seconds=10,
        profile="BALANCE",
    ),

    "ACTIVATE": PressureProtocol(
        mode="intermittent_stimulation",
        ramp_seconds=5,
        active_seconds=30,
        release_seconds=5,
        profile="ACTIVATE",
    ),
}


# ---------------------------------------------------------------------
# INTERVENTION SELECTION
# ---------------------------------------------------------------------

def select_intervention(nadi_state) -> InterventionProtocol:
    """
    Select a prototype intervention based on the calculated
    digital Nadi state.

    This is a demonstration rule engine. It does not establish
    a medical relationship between physiological measurements
    and a disease or treatment.
    """

    vata = nadi_state.vata
    pitta = nadi_state.pitta
    kapha = nadi_state.kapha

    # Highest prototype component determines the demonstration
    # protocol.

    if vata >= pitta and vata >= kapha:

        return InterventionProtocol(
            protocol_id="TC_ACU_001",
            name="Nadi Calm Protocol",
            state="VATA_DOMINANT",
            points=[
                POINTS["PC6"],
            ],
            pressure=PRESSURE_PROFILES["CALM"],
            tai_chi_chuan=TAI_CHI_PROTOCOLS["TCC_001"],
        )

    if pitta >= vata and pitta >= kapha:

        return InterventionProtocol(
            protocol_id="TC_ACU_002",
            name="Nadi Balance Protocol",
            state="PITTA_DOMINANT",
            points=[
                POINTS["LV3"],
            ],
            pressure=PRESSURE_PROFILES["BALANCE"],
            tai_chi_chuan=TAI_CHI_PROTOCOLS["TCC_002"],
        )

    return InterventionProtocol(
        protocol_id="TC_ACU_003",
        name="Nadi Activation Protocol",
        state="KAPHA_DOMINANT",
        points=[
            POINTS["ST36"],
        ],
        pressure=PRESSURE_PROFILES["ACTIVATE"],
        tai_chi_chuan=TAI_CHI_PROTOCOLS["TCC_003"],
    )


# ---------------------------------------------------------------------
# SERIALIZATION
# ---------------------------------------------------------------------

def protocol_to_dict(protocol: InterventionProtocol):
    """
    Convert the protocol into JSON-compatible data for the API.
    """

    return {
        "protocol_id": protocol.protocol_id,
        "name": protocol.name,
        "state": protocol.state,

        "points": [
            asdict(point)
            for point in protocol.points
        ],

        "pressure": asdict(protocol.pressure),

        "tai_chi_chuan": asdict(
            protocol.tai_chi_chuan
        ),
    }
