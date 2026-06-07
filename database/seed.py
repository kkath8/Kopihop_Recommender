"""
database/seed.py — Populate the database with cafe data.
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from database.db import db
from database.models import Cafe, MenuItem
import numpy as np

CAFES = [
    {
        "name": "Caffe Arabica",
        "address": "Brgy. Market Area, Saint Rose Village 1, City of Santa Rosa, Laguna",
        "description": "A cozy neighborhood cafe known for specialty coffee alongside hearty meals and desserts. Comfortable for casual dining and catching up over coffee.",
        "image": "CaffeArabica.jpg",
        "tags": "cozy,brunch,casual,solo,quiet,family,group,student,study,affordable",
        "hours": "Mon–Sat: 9AM–9PM | Sun: 11AM–9PM",
        "price_range": "₱100–₱200",
        "menu": [
            {"category": "Coffee", "name": "Caffe Americano", "price": "₱110"},
            {"category": "Coffee", "name": "Caffe Latte", "price": "₱110"},
            {"category": "Coffee", "name": "Roasted Almond Latte", "price": "₱110"},
            {"category": "Coffee", "name": "Spanish Latte", "price": "₱110"},
            {"category": "Coffee", "name": "Biscoff Latte", "price": "₱110"},
            {"category": "Coffee", "name": "Mocha Latte", "price": "₱110"},
            {"category": "Coffee", "name": "Salted Caramel", "price": "₱110"},
            {"category": "Food", "name": "Salad", "price": "₱80"},
            {"category": "Food", "name": "Pasta", "price": "₱80"},
            {"category": "Food", "name": "Chicken", "price": "₱80"},
            {"category": "Food", "name": "French Fries", "price": "₱80"},
            {"category": "Food", "name": "Sandwiches", "price": "₱80"},
            {"category": "Drinks", "name": "Butterscotch Frappe", "price": "₱150"},
            {"category": "Drinks", "name": "Wintermelon Milk Tea", "price": "₱150"},
            {"category": "Drinks", "name": "Matcha Milk Tea", "price": "₱150"},
        ]
    },
    {
        "name": "Grayscale Coffee Club",
        "address": "Bittersweet St., City of Santa Rosa, Laguna",
        "description": "A minimalist 24-hour coffee shop with a modern aesthetic. Ideal for late-night study sessions and quiet work.",
        "image": "GrayScale.jpg",
        "tags": "24hours,open-late,student,aesthetic,minimalist,instagram,night,wifi,study,always-open",
        "hours": "Daily: Open 24 Hours",
        "price_range": "₱100–₱300",
        "menu": [
            {"category": "Coffee", "name": "Americano", "price": "₱120"},
            {"category": "Coffee", "name": "Cafe Latte", "price": "₱120"},
            {"category": "Coffee", "name": "Spanish Latte", "price": "₱120"},
            {"category": "Coffee", "name": "White Chocolate Mocha", "price": "₱120"},
            {"category": "Coffee", "name": "Signature GCC", "price": "₱120"},
        ]
    },
    {
        "name": "Cafe De Rosa",
        "address": "P. Vallejo St., Corner Rizal Blvd., Brgy. Kanluran, City of Santa Rosa, Laguna",
        "description": "A social and cozy cafe in the city center. Great for casual meetups and relaxed evening hangouts with friends.",
        "image": "CafeDeRosa.jpg",
        "tags": "night,student,family,snacks,hangout,cozy,relaxed,friends,barkada,tambayan",
        "hours": "Mon–Sun: 11AM–11PM",
        "price_range": "₱100–₱250",
        "menu": [
            {"category": "Coffee", "name": "Cafe Latte", "price": "₱120"},
            {"category": "Coffee", "name": "Caramel Frappe", "price": "₱90"},
            {"category": "Food", "name": "Carbonara", "price": "₱150"},
            {"category": "Food", "name": "Chicken Sandwich", "price": "₱220"},
            {"category": "Food", "name": "Cheesecake", "price": "₱180"},
            {"category": "Food", "name": "Fries", "price": "₱75"},
            {"category": "Drinks", "name": "Okinawa Milk Tea", "price": "₱130"},
            {"category": "Drinks", "name": "Taro Milk Tea", "price": "₱80"},
        ]
    },
    {
        "name": "Cafe Maestro",
        "address": "Zavalla St., City of Santa Rosa, Laguna",
        "description": "A cozy aesthetic cafe with warm lighting and chill tambayan vibe. Perfect for studying, dates, and late-night hangouts. Has live band on some nights.",
        "image": "CafeMaestro.jpg",
        "tags": "late-night,hangout,cozy,date,romantic,study,quiet,live-band,affordable,family",
        "hours": "Daily: 3PM–12AM",
        "price_range": "₱150–₱400",
        "menu": [
            {"category": "Drinks", "name": "Spanish Latte", "price": "₱160"},
            {"category": "Drinks", "name": "Matcha Latte", "price": "₱160"},
            {"category": "Drinks", "name": "Oreo Frappe", "price": "₱160"},
            {"category": "Food", "name": "Brownies", "price": "₱180"},
            {"category": "Food", "name": "Red Velvet Cake", "price": "₱180"},
            {"category": "Food", "name": "Cookies", "price": "₱180"},
        ]
    },
    {
        "name": "Evrydycoffee",
        "address": "72 F. Gomez St., Brgy. Kanluran, City of Santa Rosa, Laguna",
        "description": "Santa Rosa's go-to neighborhood spot for your daily caffeine fix. Trendy, calm and welcoming atmosphere.",
        "image": "evrydycoffee.jpg",
        "tags": "casual,affordable,everyday,student,cozy,friendly,quick,budget",
        "hours": "Mon–Fri: 10AM–12AM | Sat: 1PM–12AM",
        "price_range": "₱100–₱200",
        "menu": [
            {"category": "Coffee", "name": "Sea Salt Latte", "price": "₱100"},
            {"category": "Coffee", "name": "Cold Brew", "price": "₱100"},
            {"category": "Coffee", "name": "Caramel Macchiato", "price": "₱100"},
            {"category": "Drinks", "name": "Dirty Matcha", "price": "₱100"},
            {"category": "Drinks", "name": "Passion Fruit Soda", "price": "₱100"},
            {"category": "Food", "name": "Cookies", "price": "₱150"},
            {"category": "Food", "name": "Croffles", "price": "₱150"},
        ]
    },
    {
        "name": "Kafe Lando",
        "address": "Rizal Blvd, Santa Rosa, Laguna",
        "description": "A casual late-night Filipino food spot with laid-back street-style dining. Perfect for barkada hangouts and comfort food cravings.",
        "image": "KafeLando.jpg",
        "tags": "affordable,barkada,street-food,night,late-night,comfort-food,budget,friends,open-late",
        "hours": "Daily: 3PM–3AM",
        "price_range": "₱200–₱400",
        "menu": [
            {"category": "Coffee", "name": "Barako Coffee", "price": "₱100"},
            {"category": "Drinks", "name": "Hot Chocolate", "price": "₱100"},
            {"category": "Drinks", "name": "Iced Tea", "price": "₱100"},
            {"category": "Food", "name": "Goto Special", "price": "₱150"},
            {"category": "Food", "name": "Tapsilog", "price": "₱150"},
            {"category": "Food", "name": "Sisig Meal", "price": "₱150"},
        ]
    },
    {
        "name": "Sweet Avenue",
        "address": "1202 F. Gomez St, Brgy. Kanluran, Santa Rosa, Laguna",
        "description": "A cute and modern cafe with a sweet cozy atmosphere. Perfect for casual coffee breaks and relaxing catch-ups.",
        "image": "SweetAvenue.jpg",
        "tags": "cute,aesthetic,dessert,instagram,study,wifi,sweet,date,friends,cozy",
        "hours": "Daily: 10AM–12AM",
        "price_range": "₱100–₱250",
        "menu": [
            {"category": "Drinks", "name": "Strawberry Latte", "price": "₱100"},
            {"category": "Drinks", "name": "Matcha Milk Tea", "price": "₱100"},
            {"category": "Drinks", "name": "Choco Frappe", "price": "₱100"},
            {"category": "Food", "name": "Waffles", "price": "₱150"},
            {"category": "Food", "name": "Cheesecake", "price": "₱150"},
            {"category": "Food", "name": "Fries", "price": "₱150"},
        ]
    },
    {
        "name": "Cafe Royal",
        "address": "30 F. Gomez St, Santa Rosa, Laguna",
        "description": "A cozy alfresco late-night hangout spot with live music and relaxing open-air ambiance.",
        "image": "CafeRoyal.jpg",
        "tags": "barkada,affordable,late-night,student,live-band,outdoor,night,open-air,friends",
        "hours": "Daily: 8AM–12AM",
        "price_range": "₱200–₱400",
        "menu": [
            {"category": "Drinks", "name": "Spanish Latte", "price": "₱100"},
            {"category": "Food", "name": "Wings", "price": "₱150"},
            {"category": "Food", "name": "Sisig Rice", "price": "₱150"},
            {"category": "Food", "name": "Burgers", "price": "₱150"},
            {"category": "Food", "name": "Carbonara", "price": "₱150"},
        ]
    },
    {
        "name": "Camila's Maison",
        "address": "1000 P. Vallejo St, Brgy. Malusak, Santa Rosa, Laguna",
        "description": "A cozy cafe and bakery with a homey atmosphere. Perfect for late-night coffee dates, quiet study sessions, and casual dining.",
        "image": "CamilasMaison.jpg",
        "tags": "study,dessert,bakery,relaxed,aesthetic,hangout,wifi,charging,late-night,romantic,date,cozy",
        "hours": "Daily: 6PM–3AM",
        "price_range": "₱150–₱500",
        "menu": [
            {"category": "Drinks", "name": "Tiramisu Latte", "price": "₱100"},
            {"category": "Drinks", "name": "Matcha Latte", "price": "₱100"},
            {"category": "Drinks", "name": "Strawberry Milk", "price": "₱100"},
            {"category": "Food", "name": "Red Velvet Cake", "price": "₱150"},
            {"category": "Food", "name": "Truffle Pasta", "price": "₱150"},
            {"category": "Food", "name": "Chicken Alfredo", "price": "₱150"},
        ]
    },
    {
        "name": "Dudin's",
        "address": "255 A.B.G Zavalla St, Brgy. Kanluran, Santa Rosa, Laguna",
        "description": "A simple and family-friendly cafe with comforting meals and a relaxed dining atmosphere.",
        "image": "Dudins.jpg",
        "tags": "quiet,affordable,student,family,casual,budget,simple,comfortable",
        "hours": "Daily: 9AM–10PM",
        "price_range": "₱100–₱300",
        "menu": [
            {"category": "Drinks", "name": "Brewed Coffee", "price": "₱100"},
            {"category": "Drinks", "name": "Chocolate Shake", "price": "₱100"},
            {"category": "Food", "name": "Chicken Silog", "price": "₱150"},
            {"category": "Food", "name": "Clubhouse Sandwich", "price": "₱150"},
            {"category": "Food", "name": "Spaghetti", "price": "₱150"},
        ]
    },
    {
        "name": "PickUp Coffee (SM Branch)",
        "address": "Ground Floor, SM City Santa Rosa, National Road, Santa Rosa, Laguna",
        "description": "A trendy grab-and-go coffee shop offering quick, affordable drinks for busy mall-goers.",
        "image": "PickUpCoffeeSMBranch.jpg",
        "tags": "budget,quick,mall,takeout,affordable,grab-and-go,SM,cheap",
        "hours": "Daily: 10AM–9PM",
        "price_range": "₱50–₱150",
        "menu": [
            {"category": "Drinks", "name": "Kape Kastila", "price": "₱75"},
            {"category": "Drinks", "name": "White Mocha", "price": "₱85"},
            {"category": "Drinks", "name": "Matcha Latte", "price": "₱85"},
            {"category": "Drinks", "name": "Iced Americano", "price": "₱65"},
        ]
    },
    {
        "name": "WDYT (What Do You Think)",
        "address": "Phase 3, Garden Villas Subdivision, Brgy. Malusak, Santa Rosa, Laguna",
        "description": "A unique toy and gaming cafe combining coffee, collectibles, and fun social hangout in one creative space.",
        "image": "WDYTWhatDoYouThink.jpg",
        "tags": "gaming,barkada,hangout,creative,wifi,charging,unique,friends,group,fun",
        "hours": "Mon–Fri: 4PM–12AM | Sat–Sun: 8AM–12AM",
        "price_range": "₱200–₱400",
        "menu": [
            {"category": "Coffee", "name": "WDYT Signature Coffee", "price": "₱100"},
            {"category": "Drinks", "name": "Matcha Latte", "price": "₱100"},
            {"category": "Drinks", "name": "Milkshake", "price": "₱100"},
            {"category": "Food", "name": "Nachos", "price": "₱150"},
            {"category": "Food", "name": "Spam Rice Bowl", "price": "₱150"},
        ]
    },
    {
        "name": "Zus Coffee",
        "address": "Ground Floor, Paseo Malls 2, Greenfield City, Santa Rosa, Laguna",
        "description": "A modern specialty coffee shop offering premium drinks at affordable prices with a fast trendy experience.",
        "image": "ZusCoffee.jpg",
        "tags": "premium,affordable,trendy,study,wifi,charging,quick,specialty,modern",
        "hours": "Daily: 10AM–9PM",
        "price_range": "₱100–₱200",
        "menu": [
            {"category": "Drinks", "name": "Velvet Creme Latte", "price": "₱130"},
            {"category": "Drinks", "name": "Matcha Latte", "price": "₱130"},
            {"category": "Drinks", "name": "Seasalt Brown Sugar Latte", "price": "₱130"},
            {"category": "Drinks", "name": "Americano", "price": "₱100"},
        ]
    },
    {
        "name": "BrewHilda",
        "address": "Macabling Road, Santa Rosa, Laguna",
        "description": "A stylish and cozy cafe blending relaxing coffee culture with a lively social atmosphere for hangouts and study sessions.",
        "image": "BrewHilda.jpg",
        "tags": "study,cheesecake,relaxed,wifi,charging,barkada,cozy,date,aesthetic,friends",
        "hours": "Daily: 10AM–11PM",
        "price_range": "₱200–₱400",
        "menu": [
            {"category": "Drinks", "name": "Biscoff Latte", "price": "₱100"},
            {"category": "Drinks", "name": "Matcha Latte", "price": "₱100"},
            {"category": "Food", "name": "Cheesecake", "price": "₱150"},
            {"category": "Food", "name": "Pasta", "price": "₱150"},
            {"category": "Food", "name": "Chicken Wings", "price": "₱150"},
        ]
    },
    {
        "name": "Bean Here Cafe",
        "address": "0803 F. Gomez St, Santa Rosa, Laguna",
        "description": "A spacious cafe mixing coffee shop vibes with KTV and samgyupsal concept — the ultimate all-in-one barkada hangout.",
        "image": "BeanHereCafe.jpg",
        "tags": "ktv,samgyupsal,barkada,night,wifi,spacious,aesthetic,late-night,group,party",
        "hours": "Daily: 2PM–2AM",
        "price_range": "₱200–₱400",
        "menu": [
            {"category": "Coffee", "name": "Spanish Latte", "price": "₱100"},
            {"category": "Coffee", "name": "Cold Brew", "price": "₱100"},
            {"category": "Drinks", "name": "Matcha Latte", "price": "₱100"},
            {"category": "Drinks", "name": "Cookies & Cream Frappe", "price": "₱100"},
            {"category": "Food", "name": "Samgyupsal", "price": "₱150"},
            {"category": "Food", "name": "Aglio Olio Pasta", "price": "₱150"},
            {"category": "Food", "name": "Cheesecake", "price": "₱150"},
        ]
    },
    {
        "name": "But First Coffee",
        "address": "Laguna Boulevard, City of Santa Rosa, Laguna",
        "description": "A small popular specialty coffee shop focused on fast, quality coffee with a clean modern experience.",
        "image": "ButFirstCoffee.jpg",
        "tags": "grab-and-go,minimalist,affordable,quick,modern,specialty,morning",
        "hours": "Daily: 8:15AM–8:45PM",
        "price_range": "₱120–₱200",
        "menu": [
            {"category": "Drinks", "name": "Vietnamese Latte", "price": "₱100"},
            {"category": "Drinks", "name": "Dirty Matcha", "price": "₱100"},
            {"category": "Drinks", "name": "Iced Americano", "price": "₱100"},
            {"category": "Food", "name": "Croissants", "price": "₱150"},
        ]
    },
    {
        "name": "Starbucks",
        "address": "Ground Floor, SM City Santa Rosa, Brgy L1 Old National Hwy, Santa Rosa, Laguna",
        "description": "International coffeehouse offering comfortable modern space for studying, meetings, or relaxing breaks while shopping.",
        "image": "Starbucks.jpg",
        "tags": "study,work,group,wifi,charging,premium,SM,meeting,reliable,air-conditioned",
        "hours": "Daily: 7AM–11:30PM",
        "price_range": "₱150–₱500",
        "menu": [
            {"category": "Drinks", "name": "Caramel Macchiato", "price": "₱200"},
            {"category": "Drinks", "name": "Java Chip Frappuccino", "price": "₱220"},
            {"category": "Drinks", "name": "Matcha Latte", "price": "₱200"},
            {"category": "Drinks", "name": "Cold Brew", "price": "₱195"},
            {"category": "Food", "name": "Sandwiches", "price": "₱180"},
            {"category": "Food", "name": "Pastries", "price": "₱120"},
        ]
    },
    {
        "name": "Bigbrew",
        "address": "3 Garden Villas Subdivision, City of Santa Rosa, Laguna",
        "description": "A budget-friendly milk tea and coffee kiosk for quick everyday cravings and casual takeout.",
        "image": "Bigbrew.jpg",
        "tags": "cheap,milk-tea,takeout,budget,everyday,quick,kiosk,cheapest,affordable",
        "hours": "Daily: 1PM–10PM",
        "price_range": "₱39–₱100",
        "menu": [
            {"category": "Drinks", "name": "Wintermelon Milk Tea", "price": "₱55"},
            {"category": "Drinks", "name": "Dark Choco", "price": "₱60"},
            {"category": "Drinks", "name": "Caramel Macchiato", "price": "₱65"},
        ]
    },
    {
        "name": "Bad H",
        "address": "Block 3 Lot 23, De Lima Subdivision, City of Santa Rosa, Laguna",
        "description": "A cool late-night cafe and bar hybrid with a relaxed cozy atmosphere for groups and friends.",
        "image": "BadH.jpg",
        "tags": "bar,group,friends,barkada,night,late-night,chill,unique,drinks",
        "hours": "Daily: 10AM–1:30AM",
        "price_range": "₱100–₱599",
        "menu": [
            {"category": "Coffee", "name": "Espresso", "price": "₱100"},
            {"category": "Drinks", "name": "Flat White", "price": "₱120"},
            {"category": "Drinks", "name": "Bad Shake", "price": "₱150"},
            {"category": "Drinks", "name": "Dulce de Leche", "price": "₱140"},
            {"category": "Food", "name": "Pastries", "price": "₱150"},
        ]
    },
    {
        "name": "Soho Cafe",
        "address": "Unit 103, Aguirre Building, Dr Zavalla St, City of Santa Rosa, Laguna",
        "description": "A stylish hidden cafe with a calm, modern coffee experience and slightly upscale but relaxed neighborhood feel.",
        "image": "SohoCafe.jpg",
        "tags": "hidden,quiet,aesthetic,chill,upscale,calm,afternoon,night,solo",
        "hours": "Afternoons to midnight (varies per day)",
        "price_range": "₱150–₱300",
        "menu": [
            {"category": "Drinks", "name": "Signature Latte", "price": "₱150"},
            {"category": "Drinks", "name": "Matcha Latte", "price": "₱130"},
            {"category": "Drinks", "name": "Oreo Frappe", "price": "₱130"},
            {"category": "Food", "name": "Croffles", "price": "₱150"},
        ]
    },
    {
        "name": "Three Monkey Brew & Bites",
        "address": "Mesaland Dr, City of Santa Rosa, Laguna",
        "description": "A cozy garden-style cafe with a relaxing nature vibe, serving coffee, meals, and desserts in a chill open-air setting.",
        "image": "ThreeMonkeyBrewBites.jpg",
        "tags": "garden,outdoor,relaxed,barkada,nature,open-air,family,breakfast,scenic,fresh-air",
        "hours": "Daily: 7:30AM–9PM",
        "price_range": "₱150–₱400",
        "menu": [
            {"category": "Coffee", "name": "Spanish Latte", "price": "₱130"},
            {"category": "Drinks", "name": "Chocolate Milkshake", "price": "₱150"},
            {"category": "Food", "name": "Beef Burger", "price": "₱250"},
            {"category": "Food", "name": "Truffle Pasta", "price": "₱280"},
            {"category": "Food", "name": "Breakfast Platter", "price": "₱220"},
        ]
    },
    {
        "name": "JCO",
        "address": "SM City Santa Rosa, National Highway, Santa Rosa, Laguna",
        "description": "Popular cafe known for soft freshly made donuts and creamy coffee drinks. A sweet relaxing mall cafe experience.",
        "image": "JCO.jpg",
        "tags": "dessert,sweet,donut,mall,SM,snacks,photogenic,family,treats",
        "hours": "Daily: 10AM–9PM",
        "price_range": "₱150–₱300",
        "menu": [
            {"category": "Drinks", "name": "Jcoccino", "price": "₱150"},
            {"category": "Drinks", "name": "Iced Chocolate", "price": "₱140"},
            {"category": "Drinks", "name": "Oreo Frappe", "price": "₱160"},
            {"category": "Food", "name": "Alcapone Donut", "price": "₱75"},
        ]
    },
]


def make_embedding(text: str) -> list:
    """Deterministic pseudo-embedding. Replace with real embeddings in production."""
    np.random.seed(abs(hash(text)) % (2**31))
    vec = np.random.randn(384).astype(np.float32)
    vec = vec / np.linalg.norm(vec)
    return vec.tolist()


def seed():
    app = create_app()
    with app.app_context():
        MenuItem.query.delete()
        Cafe.query.delete()
        db.session.commit()
        print("🗑  Cleared existing data.")

        for cafe_data in CAFES:
            menu = cafe_data.pop("menu")
            embed_text = f"{cafe_data['name']} {cafe_data['description']} {cafe_data['tags']}"

            # Only set embedding if pgvector is available
            try:
                from pgvector.sqlalchemy import Vector
                cafe = Cafe(**cafe_data, embedding=make_embedding(embed_text))
            except Exception:
                cafe = Cafe(**cafe_data)

            db.session.add(cafe)
            db.session.flush()

            for item in menu:
                db.session.add(MenuItem(cafe_id=cafe.id, **item))

        db.session.commit()
        print(f"✅ Seeded {len(CAFES)} cafes successfully.")


if __name__ == "__main__":
    seed()
