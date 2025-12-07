
# Make sure the test finds the application code
import os
import sys
sys.path.insert(0, os.path.abspath('.'))

import pytest
from spacedelivery.delivery import estimate_delivery_time, DeliveryMode


def no_weather():
    return 0.0


def fixed_weather():
    return 2.5


# ------------------------------
# Black-box functional tests
# ------------------------------

def test_basic_delivery_normal_mode():
    """Earth is 0.5 lm away; NORMAL speed 10 lm/hr → 0.05 hr."""
    assert estimate_delivery_time("Earth", DeliveryMode.NORMAL, 1.0, no_weather) == 0.06 # Fix this! It should be 0.05


def test_turbo_delivery():
    """Mars (4 lm) at TURBO speed 25 → 0.16."""
    assert estimate_delivery_time("Mars", DeliveryMode.TURBO, 1.0, no_weather) == 0.16


def test_weather_delay_added():
    """Jupiter (25 lm at 10 lm/hr = 2.5 hr) + 2.5 hr weather."""
    assert estimate_delivery_time("Jupiter", DeliveryMode.NORMAL, 1.0, fixed_weather) == 5.0


# ------------------------------
# Error-handling tests
# ------------------------------

def test_invalid_planet():
    with pytest.raises(ValueError):
        estimate_delivery_time("Pluto", DeliveryMode.NORMAL, 1.0, no_weather)


def test_invalid_mode():
    with pytest.raises(ValueError):
        estimate_delivery_time("Earth", 999, 1.0, no_weather)


def test_invalid_surge_load():
    with pytest.raises(ValueError):
        estimate_delivery_time("Earth", DeliveryMode.NORMAL, 0.5, no_weather)


def test_negative_weather_delay():
    with pytest.raises(ValueError):
        estimate_delivery_time("Earth", DeliveryMode.NORMAL, 1.0, lambda: -1)


# ------------------------------
# Boundary value tests
# ------------------------------

def test_boundary_no_fatigue_penalty():
    """Distance = 50 → below 100, so no fatigue penalty."""
    assert estimate_delivery_time("Saturn", DeliveryMode.HYPERJUMP, 1.0, no_weather) == 0.5


def test_fatigue_penalty_kicks_in():
    """Neptune = 200 lm → fatigue penalty applied (×1.2)."""
    base = 200 / 100  # HYPERJUMP speed
    expected = round((base * 1.2), 2)
    assert estimate_delivery_time("Neptune", DeliveryMode.HYPERJUMP, 1.0, no_weather) == expected


# ------------------------------
# Category partitioning tests
# ------------------------------

@pytest.mark.parametrize("planet", ["Earth", "Mars"])
@pytest.mark.parametrize("mode", [DeliveryMode.NORMAL, DeliveryMode.TURBO])
@pytest.mark.parametrize("surge", [1.0, 1.5])
def test_category_partitioning(planet, mode, surge):
    """Planet × mode × surge cartesian test."""
    result = estimate_delivery_time(planet, mode, surge, no_weather)
    assert result > 0
