import datetime
import pandas as pd
import ephem


def extract_zodiac_signs(date: datetime):
    """
    Extracts the Thai and Chinese zodiac signs based on the year of birth.

    Args:
        date (datetime): date

    Returns:
        tuple: A tuple containing the Thai zodiac sign and Chinese zodiac sign.
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
    moon = ephem.Moon()
    # Convert the date to a DateTime object
    date = ephem.Date(date)
    moon.compute(date)
    # Moon phase is a value between 0 and 1
    return moon.phase / 100.0  # Normalized to 0-1 scale


def extract_moon_distance_km(date: datetime) -> float:
    moon = ephem.Moon()
    date = ephem.Date(date)
    moon.compute(date)
    au = ephem.meters_per_au
    return moon.earth_distance * au / 1000  # Convert to km


if __name__ == "__main__":

    year_of_birth = 1990
    thai_zodiac = extract_zodiac_signs(datetime.datetime(year_of_birth, 1, 1))
    print(
        f"Year of Birth: {year_of_birth}, Thai Zodiac: {thai_zodiac}")
