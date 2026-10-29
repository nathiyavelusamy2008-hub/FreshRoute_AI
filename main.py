
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
import sqlite3
import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = os.getenv("DATABASE_PATH", str(ROOT / "freshroute.db"))
FRONTEND = ROOT / "frontend"

def connect():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db

def priority_score(quantity: int, hours_left: float, category: str) -> int:
    """Transparent demo heuristic; not a food-safety determination."""
    urgency = max(0, min(60, int((12 - max(0, hours_left)) * 5)))
    volume = min(25, max(0, quantity // 2))
    perishability = 15 if category.lower() in {"cooked meal", "dairy", "bakery"} else 8
    return min(100, urgency + volume + perishability)

def init_db():
    with connect() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            donor TEXT NOT NULL, food_name TEXT NOT NULL, category TEXT NOT NULL,
            quantity INTEGER NOT NULL, unit TEXT NOT NULL, location TEXT NOT NULL,
            hours_left REAL NOT NULL, notes TEXT DEFAULT '',
            status TEXT NOT NULL DEFAULT 'Available',
            created_at TEXT NOT NULL
        )""")
        db.execute("""CREATE TABLE IF NOT EXISTS partners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, location TEXT NOT NULL, categories TEXT NOT NULL,
            capacity INTEGER NOT NULL, contact TEXT NOT NULL
        )""")
        if db.execute("SELECT COUNT(*) FROM listings").fetchone()[0] == 0:
            now = datetime.now(timezone.utc).isoformat()
            demo = [
                ("Sunrise Bakery", "Bread & buns", "Bakery", 40, "packs", "Karur", 5, "Packed this morning", "Available", now),
                ("Green Leaf Hostel", "Lunch meals", "Cooked meal", 25, "meals", "Karur", 3, "Vegetarian meals; pickup soon", "Available", now),
                ("Daily Fresh Store", "Milk packets", "Dairy", 18, "packets", "Namakkal", 7, "Refrigerated; check before pickup", "Available", now),
            ]
            db.executemany("""INSERT INTO listings
                (donor,food_name,category,quantity,unit,location,hours_left,notes,status,created_at)
                VALUES (?,?,?,?,?,?,?,?,?,?)""", demo)
        if db.execute("SELECT COUNT(*) FROM partners").fetchone()[0] == 0:
            db.executemany("""INSERT INTO partners (name,location,categories,capacity,contact)
                VALUES (?,?,?,?,?)""", [
                ("Hope Community Kitchen", "Karur", "Bakery,Cooked meal,Dairy,Produce", 100, "hope@example.org"),
                ("Anbu Relief Network", "Namakkal", "Cooked meal,Dairy,Produce", 60, "anbu@example.org"),
                ("Neighbourhood Care Centre", "Karur", "Bakery,Produce", 35, "care@example.org"),
            ])

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="FreshRoute AI API", version="1.0.0", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=FRONTEND), name="static")

@app.get("/")
def home():
    return FileResponse(FRONTEND / "index.html")

@app.get("/api/health")
def health():
    return {"status": "ok", "app": "FreshRoute AI"}

@app.get("/api/listings")
def get_listings():
    with connect() as db:
        rows = db.execute("SELECT * FROM listings ORDER BY id DESC").fetchall()
    result = []
    for row in rows:
        item = dict(row)
        item["priority"] = priority_score(item["quantity"], item["hours_left"], item["category"])
        item["priority_label"] = "Urgent" if item["priority"] >= 75 else "High" if item["priority"] >= 50 else "Normal"
        result.append(item)
    return result

class ListingIn(BaseModel):
    donor: str = Field(min_length=2, max_length=100)
    food_name: str = Field(min_length=2, max_length=120)
    category: str = Field(min_length=2, max_length=50)
    quantity: int = Field(gt=0, le=100000)
    unit: str = Field(min_length=1, max_length=30)
    location: str = Field(min_length=2, max_length=100)
    hours_left: float = Field(gt=0, le=168)
    notes: str = Field(default="", max_length=500)

@app.post("/api/listings", status_code=201)
def create_listing(payload: ListingIn):
    with connect() as db:
        cur = db.execute("""INSERT INTO listings
            (donor,food_name,category,quantity,unit,location,hours_left,notes,status,created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (payload.donor, payload.food_name, payload.category, payload.quantity,
             payload.unit, payload.location, payload.hours_left, payload.notes,
             "Available", datetime.now(timezone.utc).isoformat()))
        listing_id = cur.lastrowid
    return {"message": "Food listing created", "id": listing_id}

@app.get("/api/partners")
def get_partners():
    with connect() as db:
        return [dict(r) for r in db.execute("SELECT * FROM partners ORDER BY name").fetchall()]

@app.get("/api/matches/{listing_id}")
def matches(listing_id: int):
    with connect() as db:
        row = db.execute("SELECT * FROM listings WHERE id=?", (listing_id,)).fetchone()
        partners = db.execute("SELECT * FROM partners").fetchall()
    if not row:
        raise HTTPException(status_code=404, detail="Listing not found")
    listing = dict(row)
    matches = []
    for p in partners:
        partner = dict(p)
        category_match = listing["category"].lower() in partner["categories"].lower()
        same_location = listing["location"].lower() == partner["location"].lower()
        if category_match or same_location:
            score = (60 if same_location else 0) + (40 if category_match else 0)
            matches.append({**partner, "match_score": score})
    return sorted(matches, key=lambda x: x["match_score"], reverse=True)

@app.get("/api/impact")
def impact():
    with connect() as db:
        rows = db.execute("SELECT quantity, status FROM listings").fetchall()
    total = sum(r["quantity"] for r in rows)
    rescued = sum(r["quantity"] for r in rows if r["status"] == "Rescued")
    return {
        "active_listings": sum(1 for r in rows if r["status"] == "Available"),
        "food_units_listed": total,
        "food_units_rescued": rescued,
        "partner_network": 3,
        "note": "Illustrative demo data; units may represent meals, packs, or packets."
    }
