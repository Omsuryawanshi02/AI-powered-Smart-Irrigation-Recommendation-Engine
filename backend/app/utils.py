from datetime import date

ACRE_TO_HECTARE = 0.4046856

# Rough, crop-agnostic day ranges since sowing -> growth stage.
# Used only as a sensible default; the stage can always be set/overridden
# explicitly on the Field record.
_STAGE_DAY_RANGES = [
    (0, 20, "Sowing"),
    (20, 60, "Vegetative"),
    (60, 100, "Flowering"),
    (100, 10_000, "Harvest"),
]


def to_hectares(size: float, unit: str) -> float:
    unit = (unit or "hectare").strip().lower()
    if unit in ("acre", "acres"):
        return round(size * ACRE_TO_HECTARE, 4)
    return round(size, 4)


def estimate_growth_stage(sowing_date: date | None, today: date | None = None) -> str:
    if sowing_date is None:
        return "Sowing"
    today = today or date.today()
    days = (today - sowing_date).days
    if days < 0:
        return "Sowing"
    for lo, hi, stage in _STAGE_DAY_RANGES:
        if lo <= days < hi:
            return stage
    return "Harvest"


def estimate_season(today: date | None = None) -> str:
    """India-style cropping season derived from the current month."""
    today = today or date.today()
    month = today.month
    if month in (6, 7, 8, 9, 10):
        return "Kharif"
    if month in (11, 12, 1, 2, 3):
        return "Rabi"
    return "Zaid"  # April, May
