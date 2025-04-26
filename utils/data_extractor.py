import datetime
import pandas as pd
import ephem


def extract_zodiac_signs(date: datetime):
    """
    Extracts the Thai zodiac sign based on the provided date using the Buddhist calendar.

    The Thai zodiac, or "Naksat" (นักษัตร), is a 12-year cycle similar to the Chinese zodiac
    but calculated using the Buddhist Era year. The cycle is determined by taking the Buddhist 
    year (which is Gregorian year + 543) modulo 12.

    Thai Zodiac Cycle:
    - Remainder 1: Horse (มะเมีย)
    - Remainder 2: Goat (มะแม)
    - Remainder 3: Monkey (วอก)
    - Remainder 4: Rooster (ระกา)
    - Remainder 5: Dog (จอ)
    - Remainder 6: Pig (กุน)
    - Remainder 7: Rat (ชวด) 
    - Remainder 8: Ox (ฉลู)
    - Remainder 9: Tiger (ขาล)
    - Remainder 10: Rabbit (เถาะ)
    - Remainder 11: Dragon (มะโรง)
    - Remainder 0: Snake (มะเส็ง)

    Args:
        date (datetime): The date to determine the zodiac sign for.
                         Only the year component is used in the calculation.

    Returns:
        str: The Thai zodiac sign in English.

    Example:
        >>> extract_zodiac_signs(datetime.datetime(1990, 1, 1))
        'Horse'
    """
    # Calculate Thai zodiac using the formula: (Buddhist year % 12)
    # 1. Convert to Buddhist year (AD + 543)
    # 2. Calculate remainder when divided by 12
    buddhist_year = date.year + 543
    remainder = buddhist_year % 12

    # Map the remainder to the corresponding Thai zodiac
    thai_zodiac = None
    if remainder == 1:
        thai_zodiac = "Horse"  # มะเมีย
    elif remainder == 2:
        thai_zodiac = "Goat"   # มะแม
    elif remainder == 3:
        thai_zodiac = "Monkey"  # วอก
    elif remainder == 4:
        thai_zodiac = "Rooster"  # ระกา
    elif remainder == 5:
        thai_zodiac = "Dog"    # จอ
    elif remainder == 6:
        thai_zodiac = "Pig"    # กุน
    elif remainder == 7:
        thai_zodiac = "Rat"    # ชวด
    elif remainder == 8:
        thai_zodiac = "Ox"     # ฉลู
    elif remainder == 9:
        thai_zodiac = "Tiger"  # ขาล
    elif remainder == 10:
        thai_zodiac = "Rabbit"  # เถาะ
    elif remainder == 11:
        thai_zodiac = "Dragon"  # มะโรง
    elif remainder == 0:
        thai_zodiac = "Snake"  # มะเส็ง

    return thai_zodiac


# Function to calculate moon phase (0-1 where 0=new moon, 0.5=full moon, 1=new moon again)
def extract_moon_phase(date: datetime) -> float:
    """
    Calculates the moon phase for a given date.

    The moon phase is represented as a value between 0 and 1:
    - 0.0: New Moon (not visible)
    - 0.25: First Quarter
    - 0.5: Full Moon 
    - 0.75: Last Quarter
    - 1.0: New Moon (cycle completes)

    Args:
        date (datetime): The date for which to calculate the moon phase

    Returns:
        float: Moon phase value between 0 and 1

    Example:
        >>> phase = extract_moon_phase(datetime.datetime(2025, 4, 27))
        >>> print(f"Moon phase: {phase:.4f}")
        Moon phase: 0.xxxx
    """
    moon = ephem.Moon()
    # Convert the date to a DateTime object
    date = ephem.Date(date)
    moon.compute(date)
    # Moon phase is a value between 0 and 1
    return moon.phase / 100.0  # Normalized to 0-1 scale


def extract_moon_distance_km(date: datetime) -> float:
    """
    Calculates the distance between Earth and the Moon for a given date.

    Uses the PyEphem library to compute the Earth-Moon distance in kilometers.
    The distance varies throughout the lunar cycle as the Moon follows an 
    elliptical orbit around Earth.

    Args:
        date (datetime): The date for which to calculate the Moon's distance

    Returns:
        float: Distance between Earth and Moon in kilometers

    Example:
        >>> distance = extract_moon_distance_km(datetime.datetime(2025, 4, 27))
        >>> print(f"Moon distance: {distance:.2f} km")
        Moon distance: xxxxxx.xx km
    """
    moon = ephem.Moon()
    date = ephem.Date(date)
    moon.compute(date)
    au = ephem.meters_per_au
    return moon.earth_distance * au / 1000  # Convert to km


if __name__ == "__main__":
    # Test extract_zodiac_signs function with multiple years
    print("===== Thai Zodiac Sign Tests =====")
    test_years = [1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025]
    for year in test_years:
        thai_zodiac = extract_zodiac_signs(datetime.datetime(year, 1, 1))
        buddhist_year = year + 543
        print(f"Year: {year} (BE {buddhist_year}) - Thai Zodiac: {thai_zodiac}")

    # Test moon phase function
    print("\n===== Moon Phase Tests =====")
    test_dates = [
        datetime.datetime(2025, 4, 27),  # Current date
        datetime.datetime(2025, 5, 1),   # Few days later
        datetime.datetime(2025, 5, 15),  # Mid-month
    ]
    for date in test_dates:
        moon_phase = extract_moon_phase(date)
        phase_description = "Full Moon" if 0.45 <= moon_phase <= 0.55 else \
            "New Moon" if moon_phase <= 0.05 or moon_phase >= 0.95 else \
            "Waxing" if 0.05 < moon_phase < 0.45 else "Waning"
        print(
            f"Date: {date.strftime('%Y-%m-%d')} - Moon Phase: {moon_phase:.4f} ({phase_description})")

    # Test moon distance function
    print("\n===== Moon Distance Tests =====")
    for date in test_dates:
        distance = extract_moon_distance_km(date)
        print(
            f"Date: {date.strftime('%Y-%m-%d')} - Moon Distance: {distance:.2f} km")
