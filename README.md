# My Flight Manager

A simple FastAPI project to manage flight registrations and queries.

## Features

- Register new flights with validation for flight number, gate, and status.

## Setup

1. Install dependencies:

   ```bash
   pip install fastapi uvicorn
   ```

2. Run the API server:

   ```bash
   uvicorn app.main:app --reload
   ```

3. Access the interactive docs at [http://localhost:8000/docs](http://localhost:8000/docs).

## Testing

Run tests with pytest:

```bash
pip install pytest
pytest
```

## Endpoints

- `POST /flights/` - Register a new flight

## License

MIT
