import math
from typing import Callable


class DeliveryMode:
    NORMAL = 1
    TURBO = 2
    HYPERJUMP = 3


MODE_SPEED = {
    DeliveryMode.NORMAL: 10,     # light-minutes per hour
    DeliveryMode.TURBO: 25,
    DeliveryMode.HYPERJUMP: 100,
}

# Planet distances from “Galactic Pizza Hub” in light-minutes
PLANET_DISTANCE = {
    "Mercury": 3,
    "Venus": 2,
    "Earth": 0.5,
    "Mars": 4,
    "Jupiter": 25,
    "Saturn": 50,
    "Neptune": 200,
}


def estimate_delivery_time(
    planet: str,
    mode: int = DeliveryMode.NORMAL,
    surge_load: float = 1.0,
    weather_delay_fn: Callable[[], float] = lambda: 0.0,
) -> float:
    """
    Estimate total delivery time in hours.

    - `planet`: destination planet name
    - `mode`: delivery mode speed multiplier
    - `surge_load`: factor (>=1); simulates high-order load
    - `weather_delay_fn`: returns number of hours to add (stochastic)
    """

    if planet not in PLANET_DISTANCE:
        raise ValueError(f"Unknown destination: {planet}")

    if surge_load < 1:
        raise ValueError("surge_load must be >= 1")

    if mode not in MODE_SPEED:
        raise ValueError("Invalid delivery mode")

    distance = PLANET_DISTANCE[planet]  # light-minutes

    # Base time
    speed = MODE_SPEED[mode]
    travel_time = distance / speed

    # If distance is extremely large, apply nonlinear fatigue penalty
    if distance > 100:
        travel_time *= 1.2  # 20% fatigue penalty

    # Weather delay (provided by injected function)
    weather_delay = weather_delay_fn()
    if weather_delay < 0:
        raise ValueError("weather_delay_fn returned negative delay")

    total_time = (travel_time * surge_load) + weather_delay
    return round(total_time, 2)
