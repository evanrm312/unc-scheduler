from backend.scheduler import conflicts

def test_overlapping_same_day():
    a = {
        "days": ["M", "W", "F"],
        "start": 600,
        "end": 660
    }

    b = {
        "days": ["M", "W", "F"],
        "start": 630,
        "end": 690
    }

    assert conflicts(a, b) is True

def test_nonoverlapping_same_day():
    a = {
        "days": ["M"],
        "start": 600,
        "end": 660
    }

    b = {
        "days": ["M"],
        "start": 720,
        "end": 780
    }

    assert conflicts(a, b) is False


def test_same_time_different_days():
    a = {
        "days": ["M", "W"],
        "start": 600,
        "end": 660
    }

    b = {
        "days": ["T", "R"],
        "start": 600,
        "end": 660
    }

    assert conflicts(a, b) is False


def test_touching_intervals():
    a = {
        "days": ["M"],
        "start": 600,
        "end": 660
    }

    b = {
        "days": ["M"],
        "start": 660,
        "end": 720
    }

    assert conflicts(a, b) is False

def test_partial_day_overlap():
    a = {
        "days": ["M", "W", "F"],
        "start": 600,
        "end": 660
    }

    b = {
        "days": ["W"],
        "start": 630,
        "end": 690
    }

    assert conflicts(a, b) is True