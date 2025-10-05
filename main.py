from fastapi import FastAPI, HTTPException
import holidays

# Create the FastAPI application
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Festivals API is running! Use /holidays/{country_code}?year={year} to get holidays."}

# Define an API endpoint
@app.get("/holidays/{country_code}")
def get_country_holidays(country_code: str, year: int):
    """
    Gets a list of all holidays (national and regional) for a specific country and year.
    """
    try:
        holiday_list = []
        
        # Get national holidays
        national_holidays = holidays.country_holidays(country_code.upper(), years=year)
        for date, name in national_holidays.items():
            holiday_list.append({"date": date.isoformat(), "name": name, "type": "national"})
        
        # Get regional holidays from all subdivisions
        try:
            country_module = getattr(holidays, country_code.upper())
            subdivs = list(country_module.subdivisions.keys()) if hasattr(country_module, 'subdivisions') else []
            for subdiv in subdivs:
                try:
                    regional_holidays = holidays.country_holidays(country_code.upper(), subdiv=subdiv, years=year)
                    for date, name in regional_holidays.items():
                        # Add only if date not already in list (avoid duplicates)
                        existing_dates = {h['date'] for h in holiday_list}
                        if date.isoformat() not in existing_dates:
                            holiday_list.append({"date": date.isoformat(), "name": name, "type": "regional"})
                except (KeyError, NotImplementedError):
                    pass
        except AttributeError:
            pass  # No subdivisions available
        
        # Sort by date
        holiday_list.sort(key=lambda x: x['date'])
        
        return holiday_list

    except KeyError:
        # If the country code is invalid, return a 404 error
        raise HTTPException(status_code=404, detail="Country code not found.")