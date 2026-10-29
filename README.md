# 🌱 FreshRoute AI — Smart Surplus Food Rescue System

**Less Waste. More Good.**

FreshRoute AI is a smart food rescue platform that connects food donors, such as restaurants, bakeries, supermarkets, and hostels, with NGOs and community organizations. It helps reduce food waste through urgency-based prioritization, smart partner matching, and impact tracking.

## 🎯 Problem Statement

Large amounts of surplus food are wasted every day, while many communities need food assistance. Traditional donation processes often lack efficient coordination, timely pickups, and visibility into available food.

## 💡 Our Solution

FreshRoute AI provides a centralized platform to list surplus food, suggest suitable community partners, prioritize urgent pickups, and track food redistribution.

## ✨ Key Features

- **Food Donation Listings:** Add surplus food details, quantity, location, and pickup time.
- **Urgency-Based Prioritization:** Calculate a demo priority score using food category, quantity, and remaining usable time.
- **NGO Matching:** Suggest community partners based on location and food category.
- **Impact Dashboard:** View active listings, total food units listed, rescued food units, and partner counts.
- **Database Integration:** Store food listings and partner information using SQLite.
- **Responsive Interface:** Access the platform through a modern, user-friendly website.

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| Database | SQLite |
| API Documentation | FastAPI Swagger UI |

## 🔄 How It Works

1. A donor lists available surplus food.
2. FreshRoute AI calculates a demo urgency score.
3. The system suggests suitable NGO or community partners.
4. Partners can review the listing and coordinate pickup.
5. The dashboard displays food-rescue activity.

## 📂 Project Structure

```text
FreshRoute-AI/
├── backend/
│   ├── __init__.py
│   └── main.py
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── requirements.txt
├── .env.example
└── README.md
```

## ⚙️ Installation and Setup

### Prerequisites
- Python 3.10 or newer
- A web browser
- VS Code (recommended)

### Step 1: Extract the project

Extract the downloaded ZIP file and open the `FreshRoute-AI` folder in VS Code.

### Step 2: Open the terminal

Run these commands from the project folder.

### Step 3: Create a virtual environment

```bash
python -m venv .venv
```

### Step 4: Activate the environment

For Windows:

```bash
.venv\Scripts\activate
```

### Step 5: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Start the application

```bash
uvicorn backend.main:app --reload
```

### Step 7: Open the website

- **Website:** http://127.0.0.1:8000
- **API documentation:** http://127.0.0.1:8000/docs

No paid API keys are required for this demo.

## 🔌 API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | Check server status |
| GET | `/api/listings` | Retrieve food listings |
| POST | `/api/listings` | Create a food listing |
| GET | `/api/partners` | Retrieve community partners |
| GET | `/api/matches/{listing_id}` | Suggest matching partners |
| GET | `/api/impact` | Retrieve impact metrics |

## 🌍 Real-World Applications

- Restaurants and hotels managing surplus meals
- Bakeries and supermarkets redistributing unsold food
- College hostels coordinating excess food donations
- NGOs organizing community food distribution
- Local food-rescue initiatives

## 🚀 Future Enhancements

- Machine-learning-based food surplus prediction
- Interactive maps and optimized pickup routes
- SMS or WhatsApp notifications
- Secure donor and NGO login
- Multilingual support
- Food-safety checklists and pickup confirmation
- Live analytics and verified impact reports

## ⚠️ Limitations

This version is a student-project prototype. The urgency score uses a transparent, rule-based demo calculation rather than a trained AI model. Partner matches and sample dashboard data are illustrative and do not represent a live food-rescue network. Food quality and safety must be verified before redistribution.

## 🎯 Project Objective

To reduce avoidable food waste by improving coordination between food donors and community organizations through an accessible, data-driven platform.

## 💚 Our Vision

**A future where surplus food becomes an opportunity to nourish communities instead of going to waste.**

---

*FreshRoute AI — Connecting surplus food to communities that need it.*
