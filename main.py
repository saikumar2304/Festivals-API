from fastapi import FastAPI, HTTPException
import holidays
from datetime import datetime
import pycountry

# Create the FastAPI application
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Festivals API is running! Use /holidays/{country_code}?year={year} to get holidays."}

# Define an API endpoint
@app.get("/holidays/{country_code}")
def get_country_holidays(country_code: str, year: int, type: str = "both", date: str = None):
    """
    Gets holidays for a specific country and year.
    Filters: type='national', 'regional', or 'both' (default).
    Optional: date='YYYY-MM-DD' to get holidays on a specific date.
    """
    try:
        holiday_list = []
        
        # Get national holidays
        national_holidays = holidays.country_holidays(country_code.upper(), years=year)
        for date_obj, name in national_holidays.items():
            holiday_list.append({"date": date_obj.isoformat(), "name": name, "type": "national"})
        
        # Get regional holidays from all subdivisions
        # Fetch subdivisions dynamically using pycountry
        try:
            country = pycountry.countries.get(alpha_2=country_code.upper())
            if country:
                subdivs = [subdivision.code.split('-')[-1] for subdivision in pycountry.subdivisions.get(country_code=country.alpha_2)]
            else:
                subdivs = []
            print("\nRegional Holidays:")
            for subdiv in subdivs:
                try:
                    regional_holidays = holidays.country_holidays(country_code.upper(), subdiv=subdiv, years=year)
                    for date_obj, name in regional_holidays.items():
                        print(f"{date_obj} ({subdiv}): {name}")
                        # Add only if date not already in list (avoid duplicates)
                        existing_dates = {h['date'] for h in holiday_list}
                        if date_obj.isoformat() not in existing_dates:
                            holiday_list.append({"date": date_obj.isoformat(), "name": name, "type": "regional"})
                except (KeyError, NotImplementedError):
                    pass
        except Exception as e:
            print(f"Error fetching subdivisions dynamically: {e}")
        
        # Sort by date
        holiday_list.sort(key=lambda x: x['date'])
        
        # Filter by date if provided
        if date:
            try:
                target_date = datetime.fromisoformat(date).date().isoformat()
                holiday_list = [h for h in holiday_list if h['date'] == target_date]
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
        
        # Filter by type
        if type == "national":
            holiday_list = [h for h in holiday_list if h['type'] == "national"]
        elif type == "regional":
            holiday_list = [h for h in holiday_list if h['type'] == "regional"]
        # else 'both', keep all
        
        return holiday_list

    except KeyError:
        # If the country code is invalid, return a 404 error
        raise HTTPException(status_code=404, detail="Country code not found.")