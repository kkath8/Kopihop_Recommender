"""
Run this once to populate the database with cafe data.
Usage: python database/seed.py
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from database.db import db
from database.models import Cafe, MenuItem
import numpy as np


# ─── Cafe Seed Data ──────────────────────────────────────────────────────────

CAFES = [
    {
        "name": "Caffe Arabica",
        "address": "Brgy. Market Area, Saint Rose Village 1, Block 1 Lot 2, City of Santa Rosa, Laguna",
        "description": (
            "A cozy neighborhood cafe known for serving specilaty coffee alongside hearty meals and desserts."
            " It's a comfortable place for casual dining for catching up over coffee."
        ),
        "image": "CaffeArabica.jpg",
        "tags": "cozy,brunch,casual-dining,solo-dining,quiet,families,group,students",
        "hours": "Mon–Sat: 9:00 AM – 9:00 PM | Sun: 11:00 AM - 9:00 PM",
        "price_range": "₱100–₱2000",
        "menu": [
            {"category": "Coffee", "name": "Caffee Americano", "price": "₱110"},
            {"category": "Coffee", "name": "Caffee Latte", "price": "₱110"},
            {"category": "Coffee", "name": "Roasted Almond Latte", "price": "₱110"},
            {"category": "Coffee", "name": "Spanish Latte", "price": "₱110"},
            {"category": "Coffee", "name": "Biscoff Latte", "price": "₱110"},
            {"category": "Coffee", "name": "Mocha Latte", "price": "₱110"},
            {"category": "Coffee", "name": "Salted Caramel", "price": "₱110"},

            {"category": "Food", "name": "Salad", "price": "₱80"},
            {"category": "Food", "name": "Chicken", "price": "₱80"},
            {"category": "Food", "name": "Pasta", "price": "₱80"},
            {"category": "Food", "name": "Beef", "price": "₱80"},
            {"category": "Food", "name": "French Fries", "price": "₱80"},
            {"category": "Food", "name": "Mojos", "price": "₱80"},
            {"category": "Food", "name": "Mashed Potato", "price": "₱80"},
            {"category": "Food", "name": "Sandwiches", "price": "₱80"},

            {"category": "Drinks", "name": "ButterScotch", "price": "₱150"},
            {"category": "Drinks", "name": "Cookies and Cream", "price": "₱150"},
            {"category": "Drinks", "name": "Wintermelon", "price": "₱150"},
            {"category": "Drinks", "name": "Matcha MilkTea", "price": "₱150"},
            {"category": "Drinks", "name": "Strawberry Cheesecake", "price": "₱150"},
            {"category": "Drinks", "name": "Red Velvet Cheesecake", "price": "₱150"},
        ]
    },
    {
        "name": "Grayscale Coffee Club",
        "address": "8469+FJ3, Bittersweet St., City of Santa Rosa, Laguna",
        "description": (
            "A minimalist coffee shop with a modern aesthetic that appeals to coffee lovers looking"
            "for a laid-back but stylish hangout. Ideal for late-night coffee runs and quiet work sessions."
        ),
        "image": "GrayScale.jpg",
        "tags": "24/7,students,aesthetic,minimalist,instagram,night-cafe",
        "hours": "Daily: 24 Hours",
        "price_range": "₱100–₱300",
        "menu": [
            {"category": "Coffee", "name": "Americano", "price": "₱120"},
            {"category": "Coffee", "name": "Cafe Latte", "price": "₱120"},
            {"category": "Coffee", "name": "Spanish Latte", "price": "₱120"},
            {"category": "Coffee", "name": "White Chocolate Mocha", "price": "₱120"},
            {"category": "Coffee", "name": "Dark Chocolate Mocha", "price": "₱120"},
            {"category": "Coffee", "name": "Chocolate", "price": "₱120"},
            {"category": "Coffee", "name": "Signature GCC", "price": "₱120"},
        ]
    },
    {
        "name": "Cafe De Rosa",
        "address": "P. Vallejo St., Corner Rizal Blvd., Brgy. Kanluran, City of Santa Rosa, Laguna",
        "description": (
            "A local cafe with a social and cozy vibe, offerring coffee and light meals in the city center."
            " Great for casual meetups and relaxed evening hangouts."
        ),
        "image": "CafeDeRosa.jpg",
        "tags": "night-cafe,students,family,snacks,hangout-spot,tablea,cozy,relaxed",
        "hours": "Mon–Sun: 11:00 AM – 11:00 PM",
        "price_range": "₱100–₱250",
        "menu": [
            {"category": "Coffee", "name": "Cafe Latte", "price": "₱120"},
            {"category": "Coffee", "name": "caramel Frappe", "price": "₱90"},
            {"category": "Coffee", "name": "Blue Lemonade", "price": "₱160"},
            
            {"category": "Food", "name": "Carbonara", "price": "₱150"},
            {"category": "Food", "name": "Chicken Sandwich", "price": "₱220"},
            {"category": "Food", "name": "Cheesecakes", "price": "₱180"},
            {"category": "Food", "name": "Fries", "price": "₱75"},

            {"category": "Drinks", "name": "Okinawa", "price": "₱130"},
            {"category": "Drinks", "name": "Taro Milk", "price": "₱80"},
        ]
    },
    {
        "name": "Cafe Maestro",
        "address": "Zavalla St., City of Santa Rosa, Laguna",
        "description": (
            "A cozy and aesthetic cafe in Santa ROsa known for its relaxing ambiance, warm lighting, and chill"
            "tambayan vibe perfect for studying, coffee dates, and lte0night hangouts."
        ),
        "image": "CafeMaestro.jpg",
        "tags": "late-night,tambayan,cozy,lovers,late-night-study,quiet,live-band,offordable,family",
        "hours": "Daily: 3:00 PM - !2:00 AM",
        "price_range": "₱150–400",
        "menu": [
            {"category": "Drinks", "name": "Spanish Latte", "price": "₱160"},
            {"category": "Drinks", "name": "Matcha Latte", "price": "₱160"},
            {"category": "Drinks", "name": "Strawberry Soda", "price": "₱160"},
            {"category": "Drinks", "name": "Oreo Frappe", "price": "₱160"},
            {"category": "Drinks", "name": "Blue Lemonade", "price": "₱160"},

            {"category": "Food", "name": "Brownies", "price": "₱180"},
            {"category": "Food", "name": "Red Velvet", "price": "₱180"},
            {"category": "Food", "name": "Cookies", "price": "₱180"},
            
        ]
    },

    {
        "name": "Evrydycoffee",
        "address": "72 F. Gomez St., Brgy. Kanluran, City of Santa Rosa, Laguna",
        "description": (
            "Everyday Coffee is Santa Rosa's go-to neighborhood spot for your daily caffeine fix. "
            "A trendy neighborhood cafe that focuses on simple everyday coofee experiences with a calm"
            " and welcoming atmosphere."
        ),
        "image": "evrydycoffee.jpg",
        "tags": "casual,affordable,everyday,students,cozy,all-day-breakfast,friendly,quick",
        "hours": "Mon–Fri: 10:00 AM – 12:00 AM | Sat: 1:00 PM - 12:00 AM",
        "price_range": "₱100–₱200",
       "menu": [
        {"category": "Coffee", "name": "Sea Salt Latte", "price": "₱100"},
        {"category": "Coffee", "name": "Cold Brew", "price": "₱100"},
        {"category": "Coffee", "name": "Caramel Macchiato", "price": "₱100"},

        {"category": "Drinks", "name": "Dirty Matcha", "price": "₱100"},
        {"category": "Drinks", "name": "Strawberry Matcha", "price": "₱100"},
        {"category": "Drinks", "name": "Passion Fruit Soda", "price": "₱100"},
    
        {"category": "Food", "name": "Cookies", "price": "₱150"},
        {"category": "Food", "name": "Croffles", "price": "₱150"}
    ]
},

{
    "name": "Kafe Lando",
    "address": "Rizal Blvd, Santa Rosa, Laguna",
    "description": (
        "A casual late-night café and Filipino food spot  that offers a laid-back street-style dining experience perfect for barkada hangouts and comfort food cravings."
    ),
    "image": "KafeLando.jpg",
    "tags": "affordable café-meals,casual student hangout,open-air café,budget-friendly food spot",
    "hours": "Daily: 3:00 PM – 3:00 AM",
    "price_range": "₱200-₱400",
    "menu": [
        {"category": "Coffee", "name": "Barako Coffee", "price": "₱100"},

        {"category": "Drinks", "name": "Hot Chocolate", "price": "₱100"},
        {"category": "Drinks", "name": "Iced Tea", "price": "₱100"},

        {"category": "Food", "name": "Goto Special", "price": "₱150"},
        {"category": "Food", "name": "Tapsilog", "price": "₱150"},
        {"category": "Food", "name": "Sisig Meal", "price": "₱150"}
    ]
},

{
    "name": "Sweet Avenue",
    "address": "1202 F. Gomez St, Brgy. Kanluran, Santa Rosa, Laguna",
    "description": (
        "A cute and modern café that offers a sweet and cozy atmosphere perfect for casual coffee breaks and relaxing catch-ups."
    ),
    "image": "SweetAvenue.jpg",
    "tags": "cute aesthetic café,dessert hangout,instagram-worthy café,chill study spot,limited outlets,wifi",
    "hours": "Daily: 10:00 AM – 12:00 AM",
    "price_range": "₱100-₱250",
    "menu": [
        {"category": "Drinks", "name": "Strawberry Latte", "price": "₱100"},
        {"category": "Drinks", "name": "Matcha Milk Tea", "price": "₱100"},
        {"category": "Drinks", "name": "Choco Frappe", "price": "₱100"},
        {"category": "Drinks", "name": "Blueberry Soda", "price": "₱100"},
        {"category": "Drinks", "name": "Green Apple Soda", "price": "₱100"},
        {"category": "Drinks", "name": "Dark Choco Frappe", "price": "₱100"},

        {"category": "Food", "name": "Waffles", "price": "₱150"},
        {"category": "Food", "name": "Cheesecake", "price": "₱150"},
        {"category": "Food", "name": "Fries", "price": "₱150"},
        {"category": "Food", "name": "Tocilog", "price": "₱150"},
        {"category": "Food", "name": "Mojos", "price": "₱150"}
    ]
},

{
    "name": "Cafe Royal",
    "address": "30 F. Gomez St, Santa Rosa, Laguna",
    "description": (
        "A cozy alfresco café and late-night hangout spot with live music and relaxing ambiance."
    ),
    "image": "CafeRoyal.jpg",
    "tags": "barkada café,affordable meals,late-night tambayan,student-friendly café,live band",
    "hours": "Daily: 8:00 AM – 12:00 AM",
    "price_range": "₱200-₱400",
    "menu": [
        {"category": "Drinks", "name": "Spanish Latte", "price": "₱100"},
        {"category": "Drinks", "name": "Cookies & Cream Frappe", "price": "₱100"},

        {"category": "Food", "name": "Wings", "price": "₱150"},
        {"category": "Food", "name": "Sisig Rice", "price": "₱150"},
        {"category": "Food", "name": "Burgers", "price": "₱150"},
        {"category": "Food", "name": "Carbonara", "price": "₱150"},
        {"category": "Food", "name": "Fries", "price": "₱150"}
    ]
},

{
    "name": "Camila’s Maison",
    "address": "1000 P. Vallejo St, Brgy. Malusak, Santa Rosa, Laguna",
    "description": (
        "A cozy café and bakery that offers a homey and relaxing atmosphere perfect for late-night coffee dates, quiet tambayan sessions, and casual dining."
    ),
    "image": "CamilasMaison.jpg",
    "tags": "cozy study café,dessert café,relaxing coffee shop,aesthetic tambayan,free wi-fi,charging outlets",
    "hours": "Daily: 6:00 PM – 3:00 AM",
    "price_range": "₱150-500",
    "menu": [
        {"category": "Drinks", "name": "Tiramisu Latte", "price": "₱100"},
        {"category": "Drinks", "name": "Matcha Latte", "price": "₱100"},
        {"category": "Drinks", "name": "Strawberry Milk", "price": "₱100"},
        {"category": "Drinks", "name": "Fruit Soda", "price": "₱100"},

        {"category": "Food", "name": "Red Velvet Cake", "price": "₱150"},
        {"category": "Food", "name": "Truffle Pasta", "price": "₱150"},
        {"category": "Food", "name": "Chicken Alfredo", "price": "₱150"}
    ]
},

{
    "name": "Dudin’s",
    "address": "255 A.B.G Zavalla St, Brgy. Kanluran, Santa Rosa, Laguna",
    "description": (
        "A simple and family-friendly café that offers comforting meals and a relaxed dining atmosphere perfect for casual gatherings."
    ),
    "image": "Dudins.jpg",
    "tags": "quiet café,affordable meals,cozy tambayan,student-friendly dining",
    "hours": "",
    "price_range": "₱100-₱300",
    "menu": [
        {"category": "Drinks", "name": "Brewed Coffee", "price": "₱100"},
        {"category": "Drinks", "name": "Chocolate Shake", "price": "₱100"},
        {"category": "Drinks", "name": "Lemon Iced Tea", "price": "₱100"},

        {"category": "Food", "name": "Chicken Silog", "price": "₱150"},
        {"category": "Food", "name": "Clubhouse Sandwich", "price": "₱150"},
        {"category": "Food", "name": "Fries", "price": "₱150"},
        {"category": "Food", "name": "Spaghetti", "price": "₱150"}
    ]
},

{
    "name": "PickUp Coffee (SM Branch)",
    "address": "Ground Floor, Expansion Building, SM City Santa Rosa, National Road, Santa Rosa, Laguna",
    "description": (
        "A trendy grab-and-go coffee shop that offers quick, affordable, and flavorful drinks for busy mall-goers and coffee lovers."
    ),
    "image": "PickUpCoffeeSMBranch.jpg",
    "tags": "budget coffee shop,quick coffee fix,affordable café drinks",
    "hours": "Daily: 10:00 AM - 9:00 PM",
    "price_range": "₱50-₱150",
    "menu": [
        {"category": "Drinks", "name": "Kape Kastila", "price": "₱100"},
        {"category": "Drinks", "name": "White Mocha", "price": "₱100"},
        {"category": "Drinks", "name": "Matcha Latte", "price": "₱100"},
        {"category": "Drinks", "name": "Choco Hazelnut", "price": "₱100"},
        {"category": "Drinks", "name": "Iced Americano", "price": "₱100"},
        {"category": "Drinks", "name": "Milk Tea", "price": "₱100"}
    ]
},

{
    "name": "WDYT (What Do You Think)",
    "address": "Phase 3, B19 L17 Spinal Street, Garden Villas Subdivision, Brgy. Malusak, Santa Rosa, Laguna",
    "description": (
        "A unique toy and gaming café that combines coffee, collectibles, and a fun social hangout experience in one creative space."
    ),
    "image": "WDYTWhatDoYouThink.jpg",
    "tags": "gaming café,barkada tambayan,creative hangout,free wi-fi,charging outlets",
    "hours": "Mon–Fri: 4:00 PM – 12:00 AM | Sat–Sun: 8:00 AM – 12:00 AM",
    "price_range": "₱200-₱400",
    "menu": [
        {"category": "Coffee", "name": "WDYT Signature Coffee", "price": "₱100"},

        {"category": "Drinks", "name": "Matcha Latte", "price": "₱100"},
        {"category": "Drinks", "name": "Blue Lemonade", "price": "₱100"},
        {"category": "Drinks", "name": "Milkshake", "price": "₱100"},

        {"category": "Food", "name": "Nachos", "price": "₱150"},
        {"category": "Food", "name": "Spam Rice Bowl", "price": "₱150"},
        {"category": "Food", "name": "Chicken Pops", "price": "₱150"}
    ]
},

{
    "name": "Zus Coffee",
    "address": "Ground Floor, Paseo Malls 2, Greenfield City, Santa Rosa, Laguna",
    "description": (
        "A modern specialty coffee shop that offers premium café drinks at affordable prices with a fast and trendy coffee experience."
    ),
    "image": "ZusCoffee.jpg",
    "tags": "affordable premium coffee,trendy café,modern study café,free wi-fi,charging outlets",
    "hours": "Daily: 10:00 AM – 9:00 PM",
    "price_range": "₱100-₱200",
    "menu": [
        {"category": "Drinks", "name": "Velvet Crème Latte", "price": "₱100"},
        {"category": "Drinks", "name": "Matcha Latte", "price": "₱100"},
        {"category": "Drinks", "name": "Seasalt Brown Sugar Latte", "price": "₱100"},
        {"category": "Drinks", "name": "Pink Lemonade", "price": "₱100"},
        {"category": "Drinks", "name": "Americano", "price": "₱100"},
        {"category": "Drinks", "name": "Chocolate Drink", "price": "₱100"}
    ]
},

{
    "name": "BrewHilda",
    "address": "Macabling Road, Santa Rosa, Laguna",
    "description": (
        "A stylish and cozy café that blends relaxing coffee culture with a lively social atmosphere perfect for hangouts, study sessions, and casual dining."
    ),
    "image": "BrewHilda.jpg",
    "tags": "cozy study café,cheesecake café,relaxing coffee shop,free wi-fi,charging outlets",
    "hours": "Daily: 10:00 AM – 11:00 PM",
    "price_range": "₱200-₱400",
    "menu": [
        {"category": "Drinks", "name": "Biscoff Latte", "price": "₱100"},
        {"category": "Drinks", "name": "Matcha Latte", "price": "₱100"},
        {"category": "Drinks", "name": "Strawberry Soda", "price": "₱100"},

        {"category": "Food", "name": "Cheesecake", "price": "₱150"},
        {"category": "Food", "name": "Nachos", "price": "₱150"},
        {"category": "Food", "name": "Pasta", "price": "₱150"},
        {"category": "Food", "name": "Chicken Wings", "price": "₱150"}
    ]
},

{
    "name": "Bean Here Cafe",
    "address": "0803 F. Gomez St, Santa Rosa, Laguna",
    "description": (
        "A spacious café that mixes coffee shop vibes with a fun KTV and samgyupsal concept, making it more of an all-in-one hangout place than a typical quiet café."
    ),
    "image": "BeanHereCafe.jpg",
    "tags": "cozy study café,ktv café,late-night tambayan,free wi-fi,spacious seating,aesthetic café,barkada hangout,charging outlets",
    "hours": "Daily: 2:00 PM – 2:00 AM",
    "price_range": "₱200-₱400",
    "menu": [
        {"category": "Coffee", "name": "Spanish Latte", "price": "₱100"},
        {"category": "Coffee", "name": "Salted Caramel Latte", "price": "₱100"},
        {"category": "Coffee", "name": "Cold Brew", "price": "₱100"},
        {"category": "Coffee", "name": "Caramel Macchiato", "price": "₱100"},

        {"category": "Drinks", "name": "Matcha Latte", "price": "₱100"},
        {"category": "Drinks", "name": "Mocha", "price": "₱100"},
        {"category": "Drinks", "name": "Strawberry Lemonade Freeze", "price": "₱100"},
        {"category": "Drinks", "name": "Cookies & Cream Frappe", "price": "₱100"},
        {"category": "Drinks", "name": "Hot Chocolate", "price": "₱100"},
        {"category": "Drinks", "name": "Iced Tea", "price": "₱100"},

        {"category": "Food", "name": "Aglio Olio Pasta", "price": "₱150"},
        {"category": "Food", "name": "Samgyupsal", "price": "₱150"},
        {"category": "Food", "name": "Chicken Meals", "price": "₱150"},
        {"category": "Food", "name": "Panini Sandwiches", "price": "₱150"},
        {"category": "Food", "name": "Cheesecake", "price": "₱150"},
        {"category": "Food", "name": "Fries", "price": "₱150"},
        {"category": "Food", "name": "Rice Meals", "price": "₱150"}
    ]
},

{
    "name": "But First Coffee",
    "address": "Laguna Boulevard, City of Santa Rosa, Laguna",
    "description": (
        "A small but popular specialty coffee shop that focuses on fast, quality coffee with a clean and modern café experience. It’s more of a grab-and-go or quick chill spot rather than a long stay café."
    ),
    "image": "ButFirstCoffee.jpg",
    "tags": "grab-and-go coffee,minimalist café,affordable specialty coffee,quick service,modern coffee shop",
    "hours": "Daily: 8:15 AM – 8:45 PM",
    "price_range": "₱120-₱200",
    "menu": [
        {"category": "Drinks", "name": "Vietnamese Latte", "price": "₱100"},
        {"category": "Drinks", "name": "Dirty Matcha", "price": "₱100"},
        {"category": "Drinks", "name": "Strawberry Latte", "price": "₱100"},
        {"category": "Drinks", "name": "Lemonade", "price": "₱100"},
        {"category": "Drinks", "name": "Iced Americano", "price": "₱100"},

        {"category": "Food", "name": "Croissants", "price": "₱150"}
    ]
},

{
    "name": "Starbucks",
    "address": "Ground Floor, SM City Santa Rosa, Brgy L1 Old National Hwy, Santa Rosa, Laguna",
    "description": (
        "A well-known international coffeehouse that offers a comfortable and modern space for studying, meetings, or relaxing breaks while shopping."
    ),
    "image": "Starbucks.jpg",
    "tags": "premium study café,work-friendly coffee shop,group study spot,free wi-fi,many charging outlets",
    "hours": "Daily: 7:00 AM – 11:30 PM",
    "price_range": "₱150-₱500",
    "menu": [
        {"category": "Drinks", "name": "Caramel Macchiato", "price": "₱100"},
        {"category": "Drinks", "name": "Java Chip Frappuccino", "price": "₱100"},
        {"category": "Drinks", "name": "Pink Drink", "price": "₱100"},
        {"category": "Drinks", "name": "Matcha Latte", "price": "₱100"},
        {"category": "Drinks", "name": "Cold Brew", "price": "₱100"},

        {"category": "Food", "name": "Cinnamon Danish", "price": "₱150"},
        {"category": "Food", "name": "sandwiches", "price": "₱150"},
        {"category": "Food", "name": "pastries", "price": "₱150"}
    ]
},

{
    "name": "Bigbrew",
    "address": "3 Garden Villas Subdivision, City of Santa Rosa, Laguna",
    "description": (
        "A simple and budget-friendly milk tea and coffee kiosk that offers quick drinks perfect for everyday cravings and casual takeout."
    ),
    "image": "Bigbrew.jpg",
    "tags": "cheap coffee drinks,affordable milk tea,quick takeout spot,",
    "hours": "Daily: 1:00 PM – 10:00 PM",
    "price_range": "₱39-₱100",
    "menu": [
        {"category": "Drinks", "name": "Wintermelon Milk Tea", "price": "₱100"},
        {"category": "Drinks", "name": "Dark Choco", "price": "₱100"},
        {"category": "Drinks", "name": "Cookies & Cream Frappe", "price": "₱100"},
        {"category": "Drinks", "name": "Strawberry Fruit Tea", "price": "₱100"},
        {"category": "Drinks", "name": "Caramel Macchiato", "price": "₱100"}
    ]
},

{
    "name": "Bad H",
    "address": "Block 3 Lot 23 and 25, De Lima Subdivision, City of Santa Rosa, Laguna",
    "description": (
        ""
    ),
    "image": "BadH.jpg",
    "tags": "cozy,bar,group,friends",
    "hours": "Daily: 10:00 AM - 1:30 AM",
    "price_range": "₱100-₱599",
    "menu": [
        {"category": "Coffee", "name": "Espresso", "price": "₱100"},

        {"category": "Drinks", "name": "Flat White", "price": "₱100"},
        {"category": "Drinks", "name": "Push Over", "price": "₱100"},
        {"category": "Drinks", "name": "Cold White", "price": "₱100"},
        {"category": "Drinks", "name": "Bad Shake", "price": "₱100"},
        {"category": "Drinks", "name": "Dulche de Leche", "price": "₱100"},
        {"category": "Drinks", "name": "White Velvet", "price": "₱100"},

        {"category": "Food", "name": "Pastries", "price": "₱150"}
    ]
},

{
    "name": "Soho Cafe",
    "address": "Unit 103, Aguirre Building, Dr Zavalla St, City of Santa Rosa, 4026 Laguna",
    "description": (
        "A stylish café that offers a calm, modern coffee experience with a slightly upscale but still relaxed neighborhood feel."
    ),
    "image": "SohoCafe.jpg",
    "tags": "hidden study café,quiet coffee shop,aesthetic tambayan,chill café vibes",
    "hours": "Usually afternoon to midnight (varies per day)",
    "price_range": "₱150-₱300",
    "menu": [
        {"category": "Drinks", "name": "Highpoint Signature Drink", "price": "₱100"},
        {"category": "Drinks", "name": "Matcha Latte", "price": "₱100"},
        {"category": "Drinks", "name": "Blue Lemonade", "price": "₱100"},
        {"category": "Drinks", "name": "Oreo Frappe", "price": "₱100"},

        {"category": "Food", "name": "Croffles", "price": "₱150"},
        {"category": "Food", "name": "Fries", "price": "₱150"}
    ]
},

{
    "name": "Three Monkey Brew & Bites",
    "address": "Mesaland Dr, City of Santa Rosa, Laguna",
    "description": (
        "A cozy garden-style café with a relaxing nature vibe, serving coffee, meals, and desserts in a chill open-air setting."
    ),
    "image": "ThreeMonkeyBrewBites.jpg",
    "tags": "garden study café,cozy barkada spot,relaxing café,nature-inspired hangout",
    "hours": "Daily: 7:30 AM – 9:00 PM",
    "price_range": "₱150-₱400",
    "menu": [
        {"category": "Coffee", "name": "Spanish Latte", "price": "₱100"},

        {"category": "Drinks", "name": "Chocolate Milkshake", "price": "₱100"},
        {"category": "Drinks", "name": "Strawberry Soda", "price": "₱100"},

        {"category": "Food", "name": "Beef Burger", "price": "₱150"},
        {"category": "Food", "name": "Truffle Pasta", "price": "₱150"},
        {"category": "Food", "name": "Breakfast Platter", "price": "₱150"}
    ]
},

{
    "name": "JCO",
    "address": "SM City Santa Rosa, National Highway, Santa Rosa, Laguna",
    "description": (
        "A popular café  known for its soft, freshly made donuts and creamy coffee drinks, offering a sweet and relaxing café experience."
    ),
    "image": "JCO.jpg",
    "tags": "dessert café,sweet coffee spot,mall study café,mall wi-fi,limited outlets",
    "hours": "Daily: 10:00 AM – 9:00 PM",
    "price_range": "₱150-₱300",
    "menu": [
        {"category": "Drinks", "name": "Jcoccino", "price": "₱100"},
        {"category": "Drinks", "name": "Iced Chocolate", "price": "₱100"},
        {"category": "Drinks", "name": "Oreo Frappe", "price": "₱100"},
        {"category": "Drinks", "name": "J.Cool Yogurt Drink", "price": "₱100"},

        {"category": "Food", "name": "Alcapone Donut", "price": "₱150"},
        {"category": "Food", "name": "Avocado Dicaprio", "price": "₱150"}
    ]
},

    
]


# ─── Simple Embedding (no external API needed for seed) ──────────────────────

def make_embedding(text: str) -> list:
    """
    Generate a deterministic pseudo-embedding from text using numpy.
    In production, replace this with a real embedding API call.
    The embedding is reproducible for the same text, allowing similarity comparisons.
    """
    np.random.seed(abs(hash(text)) % (2**31))
    vec = np.random.randn(384).astype(np.float32)
    vec = vec / np.linalg.norm(vec)  # normalize to unit vector
    return vec.tolist()


# ─── Seed Function ────────────────────────────────────────────────────────────

def seed():
    app = create_app()
    with app.app_context():
        # Clear existing data
        MenuItem.query.delete()
        Cafe.query.delete()
        db.session.commit()

        for cafe_data in CAFES:
            menu = cafe_data.pop("menu")

            # Generate embedding from description + tags
            embed_text = f"{cafe_data['name']}. {cafe_data['description']} Tags: {cafe_data['tags']}"
            embedding = make_embedding(embed_text)

            cafe = Cafe(**cafe_data, embedding=embedding)
            db.session.add(cafe)
            db.session.flush()  # get cafe.id

            for item in menu:
                menu_item = MenuItem(cafe_id=cafe.id, **item)
                db.session.add(menu_item)

        db.session.commit()
        print(f"✅ Seeded {len(CAFES)} cafes with menu items.")


if __name__ == "__main__":
    seed()
