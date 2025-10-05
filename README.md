# Festival API

A simple FastAPI-based web service to retrieve holidays (national and regional) for any country using the `holidays` Python library.

## Features

- Fetch all holidays (national + regional) for a given country and year.
- Supports ISO country codes (e.g., 'IN' for India, 'US' for United States).
- Returns data in JSON format, easy to consume from JavaScript or other clients.
- Deployed on Railway for public access.

## API Endpoint

### GET /holidays/{country_code}

- **Parameters**:
  - `country_code` (path): ISO 3166-1 alpha-2 country code (e.g., 'IN', 'US').
  - `year` (query): The year for which to fetch holidays (e.g., 2026).

- **Example Request**:
  ```
  GET https://your-railway-url.up.railway.app/holidays/IN?year=2026
  ```

- **Example Response**:
  ```json
  [
    {"date": "2026-01-01", "name": "New Year's Day"},
    {"date": "2026-01-14", "name": "Pongal"},
    ...
  ]
  ```

- **Error Response** (404):
  ```json
  {"detail": "Country code not found."}
  ```

## Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/festival-api.git
   cd festival-api
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
- **Uvicorn**: ASGI server for FastAPI.

## License

MIT License. See [LICENSE](LICENSE) for details.

## Contributing

Feel free to open issues or submit pull requests!# Festivals-API
