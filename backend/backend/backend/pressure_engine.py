"""
e-RAPHA NADI — Induced Pressure Engine

Prototype simulation of an electronically controlled
acupressure actuator.

State machine:

    IDLE
      ↓
    RAMPING
      ↓
    ACTIVE
      ↓
    RELEASING
      ↓
    COMPLETE

At any stage:

    SAFETY EVENT
          ↓
    EMERGENCY_RELEASE
"""

from dataclasses import dataclass
from enum import Enum
import time


class PressureState(str, Enum):
    IDLE = "IDLE"
    RAMPING = "RAMPING"
    ACTIVE = "ACTIVE"
    RELEASING = "RELEASING"
    COMPLETE = "COMPLETE"
    EMERGENCY_RELEASE = "EMERGENCY_RELEASE"


@dataclass
class PressureConfig:
    ramp_seconds: int = 10
    active_seconds: int = 60
    release_seconds: int = 10

    # Prototype device units.
    # This is deliberately NOT represented as a clinical
    # pressure prescription.
    target_level: float = 0.50

    maximum_level: float = 0.70


@dataclass
class PressureStatus:
    state: PressureState
    current_level: float
    target_level: float
    elapsed_seconds: float
    safety_ok: bool
    emergency_release: bool

    def as_dict(self):
        return {
            "state": self.state.value,
            "current_level": round(self.current_level, 3),
            "target_level": round(self.target_level, 3),
            "elapsed_seconds": round(self.elapsed_seconds, 1),
            "safety_ok": self.safety_ok,
            "emergency_release": self.emergency_release,
        }


class PressureController:

    def __init__(self, config: PressureConfig | None = None):
        self.config = config or PressureConfig()

        self.state = PressureState.IDLE
        self.current_level = 0.0
        self.start_time = None
        self.safety_ok = True
        self.emergency_release = False

    # ---------------------------------------------------------------
    # START
    # ---------------------------------------------------------------

    def start(self):

        if self.state not in (
            PressureState.IDLE,
            PressureState.COMPLETE,
        ):
            raise RuntimeError(
                f"Cannot start pressure from state {self.state}"
            )

        self.state = PressureState.RAMPING
        self.current_level = 0.0
        self.start_time = time.monotonic()
        self.safety_ok = True
        self.emergency_release = False

    # ---------------------------------------------------------------
    # UPDATE
    # ---------------------------------------------------------------

    def update(self):

        if self.start_time is None:
            return self.status()

        elapsed = time.monotonic() - self.start_time

        # Safety check happens before normal control.
        if not self.safety_ok:
            self.emergency_release_now()
            return self.status()

        # -----------------------------------------------------------
        # RAMP
        # -----------------------------------------------------------

        if self.state == PressureState.RAMPING:

            ramp = max(self.config.ramp_seconds, 1)

            progress = min(
                elapsed / ramp,
                1.0,
            )

            self.current_level = (
                self.config.target_level * progress
            )

            if progress >= 1.0:
                self.state = PressureState.ACTIVE
                self.start_time = time.monotonic()

        # -----------------------------------------------------------
        # ACTIVE
        # -----------------------------------------------------------

        elif self.state == PressureState.ACTIVE:

            self.current_level = self.config.target_level

            active_elapsed = elapsed

            if active_elapsed >= self.config.active_seconds:

                self.state = PressureState.RELEASING
                self.start_time = time.monotonic()

        # -----------------------------------------------------------
        # RELEASE
        # -----------------------------------------------------------

        elif self.state == PressureState.RELEASING:

            release = max(
                self.config.release_seconds,
                1,
            )

            progress = min(
                elapsed / release,
                1.0,
            )

            self.current_level = (
                self.config.target_level
                * (1.0 - progress)
            )

            if progress >= 1.0:

                self.current_level = 0.0
                self.state = PressureState.COMPLETE

        return self.status()

    # ---------------------------------------------------------------
    # SAFETY
    # ---------------------------------------------------------------

    def safety_fault(self):

        self.safety_ok = False

        self.emergency_release_now()

    def emergency_release_now(self):

        self.current_level = 0.0
        self.state = PressureState.EMERGENCY_RELEASE
        self.emergency_release = True

    # ---------------------------------------------------------------
    # MANUAL RELEASE
    # ---------------------------------------------------------------

    def manual_release(self):

        self.current_level = 0.0
        self.state = PressureState.RELEASING
        self.start_time = time.monotonic()

    # ---------------------------------------------------------------
    # RESET
    # ---------------------------------------------------------------

    def reset(self):

        self.state = PressureState.IDLE
        self.current_level = 0.0
        self.start_time = None
        self.safety_ok = True
        self.emergency_release = False

    # ---------------------------------------------------------------
    # STATUS
    # ---------------------------------------------------------------

    def status(self):

        elapsed = 0.0

        if self.start_time is not None:
            elapsed = time.monotonic() - self.start_time

        return PressureStatus(
            state=self.state,
            current_level=self.current_level,
            target_level=self.config.target_level,
            elapsed_seconds=elapsed,
            safety_ok=self.safety_ok,
            emergency_release=self.emergency_release,
        )
