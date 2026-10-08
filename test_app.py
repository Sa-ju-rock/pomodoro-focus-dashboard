"""Unit tests for Personal Pomodoro & Focus Dashboard timer logic."""

import pytest
from app import (
    DEFAULT_POMODORO_SECONDS,
    AMBIENT_SOUNDS,
    format_time,
    calculate_progress,
    get_timer_status,
)


def test_default_pomodoro_duration():
    """Verify default Pomodoro is set to 25 minutes (1500 seconds)."""
    assert DEFAULT_POMODORO_SECONDS == 25 * 60
    assert DEFAULT_POMODORO_SECONDS == 1500


@pytest.mark.parametrize(
    "seconds,expected",
    [
        (1500, "25:00"),
        (0, "00:00"),
        (59, "00:59"),
        (60, "01:00"),
        (65, "01:05"),
        (300, "05:00"),
        (-5, "00:00"),
    ],
)
def test_format_time(seconds, expected):
    """Test format_time conversion into MM:SS format."""
    assert format_time(seconds) == expected


def test_calculate_progress_boundary_values():
    """Test progress calculation at start, midpoint, and completion."""
    total = 1500
    # At start: 0% elapsed
    assert calculate_progress(remaining_seconds=1500, total_seconds=total) == 0.0
    # Halfway: 50% elapsed
    assert pytest.approx(calculate_progress(remaining_seconds=750, total_seconds=total), 0.001) == 0.5
    # Finished: 100% elapsed
    assert calculate_progress(remaining_seconds=0, total_seconds=total) == 1.0


def test_calculate_progress_edge_cases():
    """Test edge cases such as zero duration, negative remaining, or overflow."""
    # Zero total duration should not raise ZeroDivisionError
    assert calculate_progress(remaining_seconds=100, total_seconds=0) == 0.0
    assert calculate_progress(remaining_seconds=0, total_seconds=-10) == 0.0

    # Negative remaining should cap at 1.0
    assert calculate_progress(remaining_seconds=-20, total_seconds=100) == 1.0

    # Remaining larger than total should cap at 0.0
    assert calculate_progress(remaining_seconds=200, total_seconds=100) == 0.0


def test_timer_status_states():
    """Test timer status descriptions across different states."""
    # Completed state
    status_done = get_timer_status(remaining_seconds=0, is_running=False)
    assert "Complete" in status_done

    status_done_running_flag = get_timer_status(remaining_seconds=-5, is_running=True)
    assert "Complete" in status_done_running_flag

    # Active focus state
    status_active = get_timer_status(remaining_seconds=1200, is_running=True)
    assert "Focus" in status_active or "Active" in status_active

    # Paused / ready state
    status_paused = get_timer_status(remaining_seconds=1200, is_running=False)
    assert "Paused" in status_paused or "Ready" in status_paused


def test_ambient_sounds_catalog():
    """Test that ambient sounds catalog includes required sound environments."""
    required_keys = ["🌧️ Rain", "☕ Café", "🌲 Forest", "📻 White Noise", "🔇 Silence (Mute)"]
    for key in required_keys:
        assert key in AMBIENT_SOUNDS
        assert "description" in AMBIENT_SOUNDS[key]
        assert len(AMBIENT_SOUNDS[key]["description"]) > 0

    # Verify audio url present for rain, cafe, and forest
    assert AMBIENT_SOUNDS["🌧️ Rain"]["url"] is not None
    assert AMBIENT_SOUNDS["☕ Café"]["url"] is not None
    assert AMBIENT_SOUNDS["🌲 Forest"]["url"] is not None
