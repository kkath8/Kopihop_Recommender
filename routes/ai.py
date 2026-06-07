"""
routes/ai.py — Free AI Recommendation Engine

Supports English, Tagalog, and Taglish queries.
"""

from flask import Blueprint, request, jsonify, session
from database.models import Cafe, VoiceLog, UserSession
from database.db import db
from config import Config
import json, uuid, re, urllib.request, urllib.error

ai_bp = Blueprint("ai", __name__, url_prefix="/ai")


# Tagalog → English keyword map
# Used to expand Filipino/Taglish queries so scoring works correctly.

TAGALOG_MAP = {
    # Vibe
    "tahimik":      ["quiet", "peaceful", "calm", "solo"],
    "maingay":      ["lively", "loud", "busy", "social"],
    "maaliwalas":   ["bright", "open", "spacious", "airy"],
    "maluwag":      ["spacious", "roomy", "big"],
    "maganda":      ["beautiful", "aesthetic", "instagram", "pretty"],
    "maayos":       ["nice", "clean", "premium", "neat"],
    "chill":        ["relaxed", "casual", "chill"],
    "komportable":  ["comfortable", "cozy", "relaxed"],

    # People
    "barkada":      ["group", "friends", "hangout", "social"],
    "grupo":        ["group", "friends", "barkada"],
    "pamilya":      ["family", "kids", "friendly"],
    "mag-asawa":    ["couple", "romantic", "date"],
    "date":         ["romantic", "couple", "date"],
    "estudyante":   ["student", "study", "wifi", "affordable"],
    "solo":         ["solo", "quiet", "alone"],

    # Activities
    "pag-aaral":    ["study", "wifi", "quiet", "student"],
    "mag-aral":     ["study", "wifi", "quiet", "student"],
    "kwentuhan":    ["hangout", "chat", "social", "friends"],
    "tambayan":     ["hangout", "chill", "casual", "barkada"],
    "kain":         ["food", "meal", "dining", "eat"],
    "merienda":     ["snacks", "light food", "afternoon"],
    "almusal":      ["breakfast", "brunch", "morning"],

    # Time
    "gabi":         ["night", "evening", "late"],
    "hatinggabi":   ["late-night", "midnight", "open-late"],
    "umaga":        ["morning", "breakfast", "early"],
    "hapon":        ["afternoon"],
    "araw-araw":    ["everyday", "casual", "quick"],
    "palagi":       ["always", "24hours", "open-late"],
    "bukas":        ["open", "available"],

    # Budget
    "mura":         ["affordable", "cheap", "budget"],
    "mahal":        ["expensive", "premium", "upscale"],
    "sulit":        ["value", "affordable", "worth-it"],
    "budget":       ["affordable", "cheap", "budget"],
    "libre":        ["free", "affordable"],

    # Food/Drink
    "kape":         ["coffee", "espresso", "cafe"],
    "matamis":      ["sweet", "dessert", "cake"],
    "pagkain":      ["food", "meal", "rice", "eat"],
    "silog":        ["rice meal", "Filipino food", "breakfast"],
    "goto":         ["Filipino food", "comfort food", "rice"],

    # Features
    "wifi":         ["wifi", "internet", "study"],
    "charging":     ["outlets", "charging", "study"],
    "live-band":    ["live music", "entertainment", "band"],
    "labas":        ["outdoor", "alfresco", "open-air", "garden"],
    "hardin":       ["garden", "outdoor", "nature"],
    "nakatagong":   ["hidden", "tucked", "secret"],

    # Common Taglish filler
    "yung":         [],
    "lang":         [],
    "sana":         ["preferred", "would like"],
    "may":          ["has", "with"],
    "meron":        ["has", "with", "available"],
    "pwede":        ["can", "possible", "available"],
    "gusto":        ["want", "like", "prefer"],
    "para":         ["for"],
    "ngayon":       ["now", "open", "today"],
}

TAGALOG_STOP = {
    "ang","ng","na","sa","at","ay","ko","mo","ba","naman","yung","yong",
    "may","meron","wala","sana","parang","talaga","dito","doon","ito",
    "iyon","lang","din","rin","pa","pala","kaya","pero","kasi","po","ate",
    "kuya","yun","yon","mga","kung","para","si","ni","kay","nag","mag",
}


# Helpers

def detect_language(text: str) -> str:
    words = set(text.lower().split())
    hits = len(words & (set(TAGALOG_MAP.keys()) | TAGALOG_STOP))
    ratio = hits / max(len(words), 1)
    if ratio > 0.4:  return "tl"
    if ratio > 0.15: return "taglish"
    return "en"


def expand_query(query: str) -> str:
    """Append English equivalents of any Tagalog words found in the query."""
    ql = query.lower()
    extras = []
    for tl_word, en_words in TAGALOG_MAP.items():
        if tl_word in ql:
            extras.extend(en_words)
    return f"{query} {' '.join(extras)}" if extras else query


def score_cafe(expanded_query: str, cafe: Cafe) -> float:
    """Keyword overlap score between expanded query and cafe data."""
    q_words = set(expanded_query.lower().split())
    tags      = set((cafe.tags or "").lower().replace(",", " ").split())
    desc      = set(cafe.description.lower().split())
    name      = set(cafe.name.lower().split())
    combined  = tags | desc | name
    overlap   = q_words & combined
    tag_boost = len(q_words & tags) * 0.4
    return len(overlap) / max(len(q_words), 1) + tag_boost


def smart_reason(query: str, cafe: Cafe) -> str:
    """
    Build a natural-sounding reason string without any AI call.
    Used as fallback when Ollama is unavailable.
    """
    q = query.lower()
    tags = (cafe.tags or "").lower().split(",")

    reasons = []
    if any(t in q for t in ["study","mag-aral","pag-aaral","wifi","laptop"]):
        if "wifi" in tags or "study" in tags or "charging" in tags:
            reasons.append("great for studying with WiFi and power outlets")
    if any(t in q for t in ["quiet","tahimik","solo","peaceful"]):
        if "quiet" in tags or "solo" in tags or "calm" in tags:
            reasons.append("offers a quiet and peaceful atmosphere")
    if any(t in q for t in ["barkada","group","friends","grupo"]):
        if "barkada" in tags or "group" in tags or "friends" in tags:
            reasons.append("perfect for barkada hangouts")
    if any(t in q for t in ["date","romantic","couple","mag-asawa"]):
        if "romantic" in tags or "date" in tags or "cozy" in tags:
            reasons.append("has a romantic and cozy ambiance")
    if any(t in q for t in ["mura","cheap","affordable","budget"]):
        if "affordable" in tags or "budget" in tags or "cheap" in tags:
            reasons.append(f"budget-friendly at {cafe.price_range}")
    if any(t in q for t in ["late","gabi","hatinggabi","midnight","24"]):
        if "late-night" in tags or "24hours" in tags or "open-late" in tags:
            reasons.append("open late so you can hang out anytime")
    if any(t in q for t in ["live","band","music"]):
        if "live-band" in tags:
            reasons.append("has live band nights for great entertainment")
    if any(t in q for t in ["outdoor","garden","labas","hardin","fresh"]):
        if "garden" in tags or "outdoor" in tags or "open-air" in tags:
            reasons.append("has a relaxing outdoor garden setting")

    if reasons:
        return f"{cafe.name} is a solid choice — it's {' and '.join(reasons)}."
    return f"{cafe.name} matches what you're looking for in Santa Rosa."


# Free Ollama AI call

def call_ollama(prompt: str) -> str | None:
    """
    Send a prompt to a locally running Ollama instance.
    Returns the response text, or None if Ollama is unavailable.

    To set up Ollama (free):
      1. Download from https://ollama.com
      2. Run: ollama pull llama3   (or mistral, phi3, etc.)
      3. Ollama runs automatically on localhost:11434
    """
    if not Config.USE_OLLAMA:
        return None

    payload = json.dumps({
        "model":  Config.OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.7, "num_predict": 500},
    }).encode("utf-8")

    try:
        req = urllib.request.Request(
            f"{Config.OLLAMA_URL}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("response", "").strip()
    except Exception:
        return None  # Ollama not running → fall through to keyword fallback


def parse_ollama_json(raw: str) -> dict | None:
    """Try to extract a JSON object from Ollama's response."""
    if not raw:
        return None
    # Strip markdown fences
    raw = re.sub(r"^```json?\s*", "", raw.strip())
    raw = re.sub(r"\s*```$", "", raw)
    # Find first {...} block
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except Exception:
            pass
    return None


# Route

@ai_bp.route("/recommend", methods=["POST"])
def recommend():
    """
    POST /ai/recommend
    Body: { "query": "...", "conversation_history": [...] }

    Returns:
    {
      "recommendations": [ { ...cafe fields, "reason": "..." } ],
      "ai_message": "...",
      "detected_lang": "en|tl|taglish",
      "engine": "ollama|keyword"
    }
    """
    data         = request.get_json() or {}
    user_query   = (data.get("query") or "").strip()
    conv_history = data.get("conversation_history", [])
    input_method = data.get("input_method", "voice")

    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    detected_lang  = detect_language(user_query)
    expanded_query = expand_query(user_query)

    # Score all cafes
    cafes = Cafe.query.all()
    if not cafes:
        return jsonify({"error": "No cafes in database"}), 500

    scored    = sorted([(score_cafe(expanded_query, c), c) for c in cafes],
                       key=lambda x: x[0], reverse=True)
    top_cafes = [c for _, c in scored[:5]]

    # Try Ollama first
    engine      = "keyword"
    ai_message  = ""
    results     = []

    if Config.USE_OLLAMA:
        cafe_block = "\n\n".join([
            f"ID {c.id}: {c.name}\n  Tags: {c.tags}\n  Hours: {c.hours}\n  Price: {c.price_range}\n  Description: {c.description}"
            for c in top_cafes
        ])

        # Build conversation context
        history_text = ""
        for turn in conv_history[-4:]:
            role = "User" if turn["role"] == "user" else "Assistant"
            history_text += f"{role}: {turn['content']}\n"

        prompt = f"""You are KopiBot, a friendly cafe guide for Santa Rosa, Laguna, Philippines.
You understand English, Tagalog, and Taglish (mixed Filipino-English).
Reply in the same language the user used.

{history_text}User: {user_query}

Top matching cafes:
{cafe_block}

Pick the best 1-3 cafes from the list above. Respond ONLY with this JSON format (no other text):
{{
  "ai_message": "<short friendly conversational reply, 1-2 sentences>",
  "recommendations": [
    {{"cafe_id": <id>, "reason": "<one warm specific sentence why this fits>"}},
    {{"cafe_id": <id>, "reason": "<one warm specific sentence why this fits>"}}
  ]
}}"""

        raw = call_ollama(prompt)
        parsed = parse_ollama_json(raw)

        if parsed:
            engine     = "ollama"
            ai_message = parsed.get("ai_message", "")
            cafe_map   = {c.id: c for c in cafes}

            for rec in parsed.get("recommendations", []):
                cafe = cafe_map.get(rec.get("cafe_id"))
                if cafe:
                    d = cafe.to_dict()
                    d["reason"] = rec.get("reason", smart_reason(user_query, cafe))
                    results.append(d)

    # Keyword fallback (always works, no AI needed)
    if not results:
        engine = "keyword"
        pick   = top_cafes[:2]

        # Build a friendly message based on query language
        if detected_lang == "tl":
            ai_message = f"Narito ko ang mga cafe na bagay para sa'yo sa Santa Rosa!"
        elif detected_lang == "taglish":
            ai_message = f"Here are some great cafes na pwede mo puntahan!"
        else:
            ai_message = f"Here are the best cafes matching your request in Santa Rosa!"

        for cafe in pick:
            d = cafe.to_dict()
            d["reason"] = smart_reason(user_query, cafe)
            results.append(d)

    # Log the query
    if Config.VOICE_LOG_ENABLED:
        try:
            token = session.get("kopihop_token") or str(uuid.uuid4())
            session["kopihop_token"] = token
            user_sess = UserSession.query.filter_by(session_token=token).first()
            if not user_sess:
                user_sess = UserSession(session_token=token)
                db.session.add(user_sess)
                db.session.flush()

            log = VoiceLog(
                session_id=user_sess.id,
                query_text=user_query,
                detected_lang=detected_lang,
                input_method=input_method,
                recommended_ids=json.dumps([r["id"] for r in results]),
            )
            db.session.add(log)
            db.session.commit()
        except Exception:
            db.session.rollback()

    return jsonify({
        "recommendations": results,
        "ai_message":      ai_message,
        "detected_lang":   detected_lang,
        "engine":          engine,
    })
