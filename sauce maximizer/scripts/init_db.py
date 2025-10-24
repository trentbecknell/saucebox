#!/usr/bin/env python3
"""
Database initialization script for Sauce Maximizer.
Sets up initial ingredient database and sample recipes.
"""

import sqlite3
import json
from pathlib import Path

def create_database(db_path: str = "data/sauce_maximizer.db"):
    """Create and initialize the sauce maximizer database."""
    
    # Ensure data directory exists
    Path(db_path).parent.mkdir(exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create ingredients table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            flavor_sweet REAL DEFAULT 0,
            flavor_salty REAL DEFAULT 0,
            flavor_umami REAL DEFAULT 0,
            flavor_sour REAL DEFAULT 0,
            flavor_spicy REAL DEFAULT 0,
            cost_per_unit REAL NOT NULL,
            availability REAL DEFAULT 1.0,
            calories_per_100g REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create recipes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            ingredients TEXT NOT NULL, -- JSON string
            flavor_profile TEXT, -- JSON string
            rating REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert sample ingredients
    sample_ingredients = [
        ("tomato", 0.3, 0.1, 0.6, 0.2, 0.0, 0.50, 1.0, 18),
        ("garlic", 0.1, 0.2, 0.8, 0.1, 0.1, 1.20, 0.9, 149),
        ("olive_oil", 0.0, 0.0, 0.0, 0.0, 0.0, 3.00, 1.0, 884),
        ("basil", 0.2, 0.0, 0.1, 0.0, 0.0, 2.50, 0.7, 22),
        ("onion", 0.4, 0.1, 0.3, 0.1, 0.0, 0.80, 1.0, 40),
        ("salt", 0.0, 1.0, 0.0, 0.0, 0.0, 0.30, 1.0, 0),
        ("black_pepper", 0.0, 0.0, 0.1, 0.0, 0.8, 5.00, 0.8, 251)
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO ingredients 
        (name, flavor_sweet, flavor_salty, flavor_umami, flavor_sour, flavor_spicy, 
         cost_per_unit, availability, calories_per_100g)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', sample_ingredients)
    
    # Insert sample recipes
    sample_recipes = [
        (
            "classic_marinara",
            "Traditional Italian tomato sauce",
            json.dumps({"tomato": 0.7, "garlic": 0.1, "olive_oil": 0.1, "basil": 0.05, "salt": 0.05}),
            json.dumps({"sweet": 0.3, "salty": 0.3, "umami": 0.6, "sour": 0.2, "spicy": 0.0}),
            4.2
        ),
        (
            "garlic_oil",
            "Simple garlic-infused oil sauce",
            json.dumps({"olive_oil": 0.8, "garlic": 0.15, "salt": 0.03, "black_pepper": 0.02}),
            json.dumps({"sweet": 0.1, "salty": 0.4, "umami": 0.7, "sour": 0.0, "spicy": 0.2}),
            3.8
        )
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO recipes 
        (name, description, ingredients, flavor_profile, rating)
        VALUES (?, ?, ?, ?, ?)
    ''', sample_recipes)
    
    conn.commit()
    conn.close()
    
    print(f"Database initialized successfully at {db_path}")
    print(f"Added {len(sample_ingredients)} ingredients and {len(sample_recipes)} recipes")

if __name__ == "__main__":
    create_database()