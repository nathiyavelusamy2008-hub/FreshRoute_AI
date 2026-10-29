# FreshRoute AI — Smart Surplus Food Rescue System

FreshRoute AI is a full-stack demo platform that helps food donors list surplus food, connects listings with nearby NGO/relief partners, prioritizes pickups by freshness and urgency, and tracks food-rescue impact.

## Features...
- Responsive dashboard with demo impact metrics
- Create and browse surplus-food listings
- Rule-based freshness/urgency priority score (demo, not a trained AI model)
- Simple NGO matching by location and food category
- SQLite persistence
- FastAPI REST API and interactive API docs
- Sample records created automatically
- No paid API keys required

## Tech stack
- Frontend: HTML, CSS, vanilla JavaScript
- Backend: Python, FastAPI, Uvicorn
- Database: SQLite

## Run on Windows
1. Install Python 3.10 or newer.
2. Extract this ZIP.
3. Open Command Prompt/Terminal inside the extracted `FreshRoute-AI` folder.
4. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
5. Activate it:
   ```bash
   .venv\Scripts\activate
   ```
6. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
7. Start the server:
   ```bash
   uvicorn backend.main:app --reload
   ```
8. Open http://127.0.0.1:8000 in your browser.
9. API documentation: http://127.0.0.1:8000/docs

## API endpoints
- `GET /api/health` — health check
- `GET /api/listings` — list food listings
- `POST /api/listings` — create a food listing
- `GET /api/partners` — list NGO/relief partners
- `GET /api/matches/{listing_id}` — matching partner suggestions
- `GET /api/impact` — demo impact metrics

## Notes and limitations
- The priority score is an explainable rule-based demo, not a validated food-safety assessment or trained AI model.
- Demo records and impact metrics are illustrative, not live operational data.
- Always follow local food-safety rules and verify food quality, storage, allergens, and pickup arrangements before redistribution.
- Authentication, maps, notifications, and production deployment are future enhancements.

## Future enhancements
- Train a surplus prediction model from historical kitchen/store data
- Map-based pickup routing
- SMS/WhatsApp notifications
- Role-based donor and NGO accounts
- Food-safety checklist and cold-chain tracking
- Multi-language interface
