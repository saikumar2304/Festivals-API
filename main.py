from fastapi import FastAPI, HTTPException
import holidays
from holidays.utils import list_subdivisions

# Create the FastAPI application
app = FastAPI()

# Define an API endpoint
@app.get("/holidays/{country_code}")
def get_country_holidays(country_code: str, year: int):
    """
    Gets a list of all holidays (national and regional) for a specific country and year.
    """
    try:
        holiday_dict = {}
        
        # Get national holidays
        national_holidays = holidays.country_holidays(country_code.upper(), years=year)
        holiday_dict.update(national_holidays)
        
        # Get regional holidays from all subdivisions
        try:
            subdivs = list_subdivisions(country_code.upper())
            for subdiv in subdivs:
                try:
                    regional_holidays = holidays.country_holidays(country_code.upper(), subdiv=subdiv, years=year)
                    holiday_dict.update(regional_holidays)
                except (KeyError, NotImplementedError):
                    pass
        except (AttributeError, KeyError):
            pass  # No subdivisions available
        
        # Convert the data into a sorted list of dictionaries for easy use in JS
        holiday_list = [{"date": date.isoformat(), "name": name} for date, name in sorted(holiday_dict.items())]
        
        return holiday_list

    except KeyError:
        # If the country code is invalid, return a 404 error
        raise HTTPException(status_code=404, detail="Country code not found.")