from flask import Blueprint, request, jsonify
from database.models import Cafe
from database.db import db
from config import Config
import anthropic
import numpy as np
import json

ai_bp = Blueprint("ai", __name__, url_prefix="/ai")

client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)


# ─── Embedding Helper ─────────────────────────────────────────────────────────

def make_query_embedding(text: str) -> list:
    """
    Generate a pseudo-embedding for the user's query.
    Uses the same deterministic method as seed.py so similarity works.
    
    NOTE: For production, swap this with a real embedding model
    (e.g., sentence-transformers or an embedding API).
    """
    np.random.seed(abs(hash(text)) % (2**31))
    vec = np.random.randn(384).astype(np.float32)
    vec = vec / np.linalg.norm(vec)
    return vec.tolist()


def keyword_score(query: str, cafe: Cafe) -> float:
    """
    Fallback: compute a simple keyword overlap score between
    the user query and the cafe's tags + description.
    """
    query_words = set(query.lower().split())
    tags = set((cafe.tags or "").lower().replace(",", " ").split())
    desc_words = set(cafe.description.lower().split())
    combined = tags | desc_words
    overlap = query_words & combined
    return len(overlap) / max(len(query_words), 1)


# ─── Routes ───────────────────────────────────────────────────────────────────

@ai_bp.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    user_query = data.get("query", "").strip()

    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    cafes = Cafe.query.all()
    if not cafes:
        return jsonify({"error": "No cafes in database"}), 500

    # ── Step 1: Score cafes by keyword similarity ──────────────────────────
    scored = []
    for cafe in cafes:
        score = keyword_score(user_query, cafe)
        scored.append((score, cafe))

    scored.sort(key=lambda x: x[0], reverse=True)
    top_cafes = [cafe for _, cafe in scored[:4]]  # top 4 candidates

    # ── Step 2: Ask Claude to pick the best matches and explain ────────────
    cafe_summaries = "\n\n".join([
        f"Cafe ID {c.id}: {c.name}\n"
        f"Address: {c.address}\n"
        f"Description: {c.description}\n"
        f"Tags: {c.tags}\n"
        f"Hours: {c.hours}\n"
        f"Price Range: {c.price_range}"
        for c in top_cafes
    ])

    prompt = f"""You are a helpful cafe guide for Santa Rosa, Laguna, Philippines.

A visitor said: "{user_query}"

Here are the available cafes:

{cafe_summaries}

Based on the visitor's request, recommend the TOP 2 most suitable cafes.
Respond ONLY with a valid JSON array (no markdown, no preamble) in this exact format:
[
  {{
    "cafe_id": <id>,
    "reason": "<one warm, specific sentence explaining why this cafe fits>"
  }},
  {{
    "cafe_id": <id>,
    "reason": "<one warm, specific sentence explaining why this cafe fits>"
  }}
]"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}]
        )
        raw = response.content[0].text.strip()

        # Strip markdown fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        recommendations = json.loads(raw)

    except Exception as e:
        # Fallback: return top 2 scored cafes without AI reasoning
        recommendations = [
            {"cafe_id": top_cafes[0].id, "reason": "This cafe best matches your preferences."},
            {"cafe_id": top_cafes[1].id, "reason": "This is another great option for you."},
        ] if len(top_cafes) >= 2 else []

    # ── Step 3: Build response with full cafe details ──────────────────────
    cafe_map = {c.id: c for c in cafes}
    results = []

    for rec in recommendations:
        cafe = cafe_map.get(rec.get("cafe_id"))
        if cafe:
            results.append({
                **cafe.to_dict(),
                "reason": rec.get("reason", ""),
            })

    return jsonify({"recommendations": results})
