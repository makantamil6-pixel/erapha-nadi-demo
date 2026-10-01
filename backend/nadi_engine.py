"""
e-RAPHA NADI — Prototype Nadi State Engine

This module provides simulated physiological inputs and converts them
into a prototype digital Nadi state.

IMPORTANT:
This is demonstration software. The Vata/Pitta/Kapha values are
prototype classification variables and are not medical diagnoses.
"""

from dataclasses import dataclass


@dataclass
class PhysiologicalInput:
    heart_rate: float
    hrv: float
    pulse_amplitude: float
    temperature: float
    motion_level: float = 0.0
    signal_quality: float = 1.0


@dataclass
class NadiState:
    vata: float
    pitta: float
    kapha: float
    arousal: float
    recovery: float
    signal_quality: float

    def as_dict(self):
        return {
            "vata": round(self.vata, 3),
            "pitta": round(self.pitta, 3),
            "kapha": round(self.kapha, 3),
            "arousal": round(self.arousal, 3),
            "recovery": round(self.recovery, 3),
            "signal_quality": round(self.signal_quality, 3),
        }


def clamp(value: float, minimum: float = 0.0, maximum: float = 1.0):
    return max(minimum, min(maximum, value))


def normalize(value, minimum, maximum):
    if maximum == minimum:
        return 0.0

    return clamp((value - minimum) / (maximum - minimum))


def calculate_arousal(data: PhysiologicalInput):
    """
    Prototype arousal calculation.

    Higher heart rate and lower HRV increase the simulated
    arousal value.
    """

    hr_component = normalize(
        data.heart_rate,
        50.0,
        110.0,
    )

    hrv_component = 1.0 - normalize(
        data.hrv,
        20.0,
        100.0,
    )

    arousal = (
        0.60 * hr_component
        + 0.40 * hrv_component
    )

    return clamp(arousal)


def calculate_recovery(data: PhysiologicalInput):
    """
    Prototype recovery indicator.

    Higher HRV and lower resting heart rate contribute to
    the simulated recovery value.
    """

    hrv_component = normalize(
        data.hrv,
        20.0,
        100.0,
    )

    hr_component = 1.0 - normalize(
        data.heart_rate,
        50.0,
        110.0,
    )

    recovery = (
        0.65 * hrv_component
        + 0.35 * hr_component
    )

    return clamp(recovery)


def classify_nadi(data: PhysiologicalInput) -> NadiState:
    """
    Generate a prototype Nadi state.

    This is intentionally a simple demonstration model.
    It should later be replaced by the validated Nadi-analysis
    model used by the project.
    """

    arousal = calculate_arousal(data)
    recovery = calculate_recovery(data)

    # Prototype feature relationships.
    #
    # These values are software demonstration parameters,
    # not clinical definitions of Vata, Pitta or Kapha.

    vata = (
        0.55 * arousal
        + 0.25 * (1.0 - data.signal_quality)
        + 0.20 * normalize(data.motion_level, 0.0, 1.0)
    )

    pitta = (
        0.70 * normalize(data.heart_rate, 60.0, 105.0)
        + 0.30 * (1.0 - recovery)
    )

    kapha = (
        0.65 * (1.0 - arousal)
        + 0.35 * recovery
    )

    # Normalize the three prototype components.
    total = vata + pitta + kapha

    if total > 0:
        vata /= total
        pitta /= total
        kapha /= total

    return NadiState(
        vata=clamp(vata),
        pitta=clamp(pitta),
        kapha=clamp(kapha),
        arousal=arousal,
        recovery=recovery,
        signal_quality=clamp(data.signal_quality),
    )


def simulate_reading():
    """
    Generate a repeatable demonstration reading.
    """

    return PhysiologicalInput(
        heart_rate=78,
        hrv=42,
        pulse_amplitude=0.72,
        temperature=36.5,
        motion_level=0.08,
        signal_quality=0.94,
    )


if __name__ == "__main__":
    reading = simulate_reading()
    state = classify_nadi(reading)

    print("Physiological input:")
    print(reading)

    print("\nPrototype Nadi state:")
    print(state.as_dict())
