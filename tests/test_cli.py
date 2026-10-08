import pytest

from backend import cli, models


@pytest.mark.parametrize(
    ("minutes", "expected"),
    [
        (0, "00:00"),
        (8 * 60 + 5, "08:05"),
        (13 * 60 + 30, "13:30"),
        (23 * 60 + 59, "23:59"),
    ],
)
def test_conv_time(minutes, expected):
    assert cli.conv_time(minutes) == expected


def test_ask_time_reprompts_after_invalid_input(monkeypatch, capsys):
    answers = iter(["25:00", "nine", "09:30"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    assert cli.ask_time("Time: ") == 570
    assert capsys.readouterr().out.count("Enter time in HH:MM format.") == 2


def test_ask_weight_reprompts_after_invalid_input(monkeypatch, capsys):
    answers = iter(["high", "6", "2.5"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    assert cli.ask_weight("Weight: ") == 2.5
    output = capsys.readouterr().out
    assert "Enter a numeric value." in output
    assert "Enter a value between 0 and 5." in output


def test_get_preferences_builds_complete_preferences(monkeypatch):
    times = iter([9 * 60, 17 * 60, 12 * 60, 14 * 60])
    weights = iter([4.0, 3.0, 2.0, 5.0])

    monkeypatch.setattr(cli, "ask_time", lambda _prompt: next(times))
    monkeypatch.setattr(cli, "ask_weight", lambda _prompt: next(weights))
    monkeypatch.setattr("builtins.input", lambda _prompt: "30")

    preferences = cli.get_preferences()

    assert preferences == models.Preferences(
        preferred_start=9 * 60,
        preferred_end=17 * 60,
        start_weight=4.0,
        end_weight=3.0,
        gap_weight=2.0,
        lunch_length=30,
        lunch_weight=5.0,
        lunch_start=12 * 60,
        lunch_end=14 * 60,
    )
