# Festival API

A FastAPI-based web service to retrieve national and regional holidays dynamically for any country using the `holidays` Python library and `pycountry` for ISO 3166-2 subdivision codes.

## Features

- Fetch all holidays (national + regional) for a given country and year.
- Dynamically fetch regional holidays using ISO 3166-2 subdivision codes.
- Supports ISO country codes (e.g., 'IN' for India, 'US' for United States).
- Returns data in JSON format, easy to consume from JavaScript or other clients.
- Deployed on Railway for public access.

## API Endpoint

### GET /holidays/{country_code}

- **Parameters**:
  - `country_code` (path): ISO 3166-1 alpha-2 country code (e.g., 'IN', 'US').
  - `year` (query, required): The year for which to fetch holidays (e.g., 2026).
  - `type` (query, optional): Filter by holiday type - 'national', 'regional', or 'both' (default).
  - `date` (query, optional): Filter to holidays on a specific date (YYYY-MM-DD). If provided, returns holidays for that date only.

- **Example Requests**:
  ```
  # All holidays for India in 2026
  GET https://festivalsapi.up.railway.app/holidays/IN?year=2026

  # Only national holidays for India in 2026
  GET https://festivalsapi.up.railway.app/holidays/IN?year=2026&type=national

  # Only regional holidays for India in 2026
  GET https://festivalsapi.up.railway.app/holidays/IN?year=2026&type=regional

  # All holidays on a specific date (e.g., Pongal)
  GET https://festivalsapi.up.railway.app/holidays/IN?year=2026&date=2026-01-14

  # Regional holidays on a specific date
  GET https://festivalsapi.up.railway.app/holidays/IN?year=2026&date=2026-01-14&type=regional
  ```

- **Example Response**:
  ```json
  [
    {"date": "2026-01-01", "name": "New Year's Day", "type": "national"},
    {"date": "2026-01-14", "name": "Pongal", "type": "regional"},
    ...
  ]
  ```

- **Error Responses**:
  - 404: Country code not found.
  - 400: Invalid date format (use YYYY-MM-DD).

- **Error Response** (404):
  ```json
  {"detail": "Country code not found."}
  ```

## Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/saikumar2304/Festivals-API.git
   cd Festivals-API
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

4. Visit `http://127.0.0.1:8000/docs` for interactive API documentation (Swagger UI).

## Deployment

This project is configured for deployment on Railway:

- **Procfile**: Defines the web process.
- **requirements.txt**: Lists Python dependencies.
- Push to GitHub and connect to Railway for automatic deployment.

## Technologies Used

- **FastAPI**: Modern Python web framework.
- **holidays**: Library for generating holiday data.
- **pycountry**: Library for ISO 3166-2 subdivision codes.
- **Uvicorn**: ASGI server for FastAPI.

## License

MIT License. See [LICENSE](LICENSE) for details.

## Contributing

Feel free to open issues or submit pull requests!
