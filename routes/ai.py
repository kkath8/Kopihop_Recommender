"""
routes/ai.py — Free AI Recommendation Engine
Supports English, Tagalog, and Taglish.
"""

from flask import Blueprint, request, jsonify, session
from database.models import Cafe, VoiceLog, UserSession
from database.db import db
from config import Config
import json, uuid, re, urllib.request

ai_bp = Blueprint("ai", __name__, url_prefix="/ai")


# Tagalog → English keyword map

TAGALOG_MAP = {
    "tahimik":      ["quiet", "peaceful", "calm", "solo", "silent"],
    "maingay":      ["lively", "loud", "busy", "social"],
    "maaliwalas":   ["bright", "open", "spacious", "airy"],
    "maluwag":      ["spacious", "roomy", "big"],
    "maganda":      ["beautiful", "aesthetic", "instagram", "pretty"],
    "maayos":       ["nice", "clean", "premium", "neat"],
    "chill":        ["relaxed", "casual", "chill", "cozy"],
    "komportable":  ["comfortable", "cozy", "relaxed"],
    "barkada":      ["group", "friends", "hangout", "social"],
    "grupo":        ["group", "friends", "barkada"],
    "pamilya":      ["family", "kids", "friendly"],
    "mag-asawa":    ["couple", "romantic", "date"],
    "date":         ["romantic", "couple", "date", "cozy"],
    "estudyante":   ["student", "study", "wifi", "affordable"],
    "solo":         ["solo", "quiet", "alone"],
    "pag-aaral":    ["study", "wifi", "quiet", "student"],
    "mag-aral":     ["study", "wifi", "quiet", "student"],
    "kwentuhan":    ["hangout", "chat", "social", "friends"],
    "tambayan":     ["hangout", "chill", "casual", "barkada"],
    "kain":         ["food", "meal", "dining", "eat"],
    "merienda":     ["snacks", "light", "afternoon"],
    "almusal":      ["breakfast", "brunch", "morning"],
    "gabi":         ["night", "evening", "late", "late-night"],
    "hatinggabi":   ["late-night", "midnight", "open-late", "24hours"],
    "umaga":        ["morning", "breakfast", "early"],
    "hapon":        ["afternoon"],
    "araw-araw":    ["everyday", "casual", "quick"],
    "palagi":       ["always", "24hours", "open-late"],
    "bukas":        ["open", "available"],
    "mura":         ["affordable", "cheap", "budget", "inexpensive"],
    "mahal":        ["expensive", "premium", "upscale"],
    "sulit":        ["value", "affordable", "worth"],
    "budget":       ["affordable", "cheap", "budget"],
    "kape":         ["coffee", "espresso", "cafe"],
    "matamis":      ["sweet", "dessert", "cake"],
    "pagkain":      ["food", "meal", "rice", "eat"],
    "silog":        ["rice", "Filipino", "breakfast"],
    "goto":         ["Filipino", "comfort", "rice"],
    "wifi":         ["wifi", "internet", "study"],
    "charging":     ["outlets", "charging", "study"],
    "live-band":    ["live", "music", "entertainment", "band"],
    "labas":        ["outdoor", "alfresco", "open-air", "garden"],
    "hardin":       ["garden", "outdoor", "nature"],
    "nakatagong":   ["hidden", "tucked", "secret"],
    "yung":         [], "lang": [], "po": [], "ba": [],
    "sana":         ["preferred"],
    "may":          ["has", "with"],
    "meron":        ["has", "with", "available"],
    "pwede":        ["available", "open"],
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

# Synonym map — covers natural English phrases that don't appear in tags
# e.g. "studying" → "study", "cheap" → "affordable", "nighttime" → "night"

SYNONYM_MAP = {
    # Study / work
    "studying":     ["study", "wifi", "student", "quiet"],
    "study":        ["study", "wifi", "student", "quiet"],
    "working":      ["wifi", "study", "charging", "quiet"],
    "work":         ["wifi", "study", "charging"],
    "laptop":       ["wifi", "study", "charging"],
    "school":       ["student", "study", "affordable"],
    "homework":     ["study", "wifi", "quiet"],
    "thesis":       ["study", "wifi", "quiet", "charging"],
    "review":       ["study", "wifi", "quiet"],

    # Friends / social
    "friends":      ["barkada", "friends", "hangout", "group"],
    "friend":       ["barkada", "friends", "hangout"],
    "group":        ["group", "barkada", "friends", "spacious"],
    "hang":         ["hangout", "barkada", "friends"],
    "hangout":      ["hangout", "barkada", "friends"],
    "socialize":    ["social", "friends", "hangout"],
    "gathering":    ["group", "friends", "family"],
    "celebration":  ["group", "friends", "spacious"],

    # Romantic / date
    "romantic":     ["romantic", "date", "cozy"],
    "date":         ["romantic", "date", "cozy"],
    "couple":       ["romantic", "date", "cozy"],
    "anniversary":  ["romantic", "date", "cozy"],
    "valentines":   ["romantic", "date", "cozy"],

    # Quiet / peaceful
    "quiet":        ["quiet", "solo", "calm", "peaceful"],
    "peaceful":     ["quiet", "calm", "solo"],
    "calm":         ["quiet", "calm", "relaxed"],
    "relax":        ["relaxed", "cozy", "calm", "quiet"],
    "relaxing":     ["relaxed", "cozy", "calm"],
    "chill":        ["chill", "relaxed", "cozy"],

    # Budget
    "cheap":        ["affordable", "cheap", "budget"],
    "affordable":   ["affordable", "budget", "cheap"],
    "budget":       ["budget", "affordable", "cheap"],
    "inexpensive":  ["affordable", "budget", "cheap"],
    "low":          ["affordable", "budget"],
    "save":         ["affordable", "budget"],
    "economical":   ["affordable", "budget"],

    # Night / late
    "night":        ["night", "late-night", "open-late"],
    "late":         ["late-night", "open-late", "night"],
    "midnight":     ["late-night", "24hours", "open-late"],
    "evening":      ["night", "evening", "late"],
    "nighttime":    ["night", "late-night"],
    "overnight":    ["24hours", "open-late", "late-night"],
    "24":           ["24hours", "open-late"],
    "always":       ["24hours", "open-late"],

    # Morning / breakfast
    "morning":      ["morning", "breakfast", "early"],
    "breakfast":    ["breakfast", "morning", "brunch"],
    "brunch":       ["brunch", "breakfast", "morning"],
    "early":        ["morning", "early", "breakfast"],

    # Food
    "food":         ["food", "meal", "snacks"],
    "eat":          ["food", "meal", "rice"],
    "meal":         ["food", "meal", "rice"],
    "snack":        ["snacks", "light", "food"],
    "dessert":      ["dessert", "sweet", "cake"],
    "sweets":       ["sweet", "dessert"],
    "cake":         ["cake", "dessert", "sweet"],
    "donut":        ["dessert", "sweet", "donut"],

    # Features
    "wifi":         ["wifi", "internet", "study"],
    "internet":     ["wifi", "internet"],
    "outlet":       ["charging", "outlets"],
    "charger":      ["charging", "outlets"],
    "charging":     ["charging", "outlets"],
    "music":        ["live-band", "music", "entertainment"],
    "band":         ["live-band", "music", "band"],
    "live":         ["live-band", "music"],
    "outdoor":      ["outdoor", "garden", "open-air"],
    "garden":       ["garden", "outdoor", "nature"],
    "outside":      ["outdoor", "open-air", "garden"],
    "alfresco":     ["outdoor", "open-air", "garden"],
    "open":         ["open-air", "outdoor", "spacious"],
    "aircon":       ["air-conditioned", "indoor", "cool"],
    "air":          ["air-conditioned", "indoor"],

    # Vibe
    "aesthetic":    ["aesthetic", "instagram", "pretty"],
    "instagram":    ["instagram", "aesthetic", "pretty"],
    "cozy":         ["cozy", "comfortable", "warm"],
    "comfy":        ["cozy", "comfortable"],
    "nice":         ["nice", "aesthetic", "cozy"],
    "pretty":       ["aesthetic", "instagram", "pretty"],
    "cool":         ["aesthetic", "chill", "unique"],
    "fun":          ["fun", "gaming", "unique", "barkada"],
    "unique":       ["unique", "gaming", "ktv"],
    "hidden":       ["hidden", "tucked", "secret"],
    "secret":       ["hidden", "tucked"],
    "local":        ["local", "cozy", "affordable"],

    # Specific concepts
    "ktv":          ["ktv", "group", "barkada", "fun"],
    "karaoke":      ["ktv", "group", "barkada"],
    "gaming":       ["gaming", "unique", "fun"],
    "samgyup":      ["samgyupsal", "group", "barkada"],
    "barbecue":     ["samgyupsal", "food", "group"],
    "mall":         ["mall", "SM", "convenient"],
    "takeout":      ["takeout", "grab-and-go", "quick"],
    "takeaway":     ["takeout", "grab-and-go", "quick"],
    "grab":         ["grab-and-go", "quick", "takeout"],
    "quick":        ["quick", "fast", "grab-and-go"],
    "fast":         ["quick", "fast", "grab-and-go"],
}


# Helpers 

def detect_language(text: str) -> str:
    words = set(text.lower().split())
    hits = len(words & (set(TAGALOG_MAP.keys()) | TAGALOG_STOP))
    ratio = hits / max(len(words), 1)
    if ratio > 0.4:  return "tl"
    if ratio > 0.15: return "taglish"
    return "en"


def expand_query(query: str) -> list[str]:
    """
    Returns a flat list of search terms from the query.
    Expands Tagalog words AND English synonyms so scoring is much broader.
    Example: "quiet cafe for studying" →
      ["quiet","cafe","for","studying","quiet","solo","calm","peaceful",
       "study","wifi","student","quiet"]
    """
    tokens = re.findall(r"[a-zA-Z\-]+", query.lower())
    all_terms = list(tokens)

    for token in tokens:
        # Tagalog expansion
        if token in TAGALOG_MAP:
            all_terms.extend(TAGALOG_MAP[token])
        # English synonym expansion
        if token in SYNONYM_MAP:
            all_terms.extend(SYNONYM_MAP[token])

    return all_terms


def score_cafe(query_terms: list[str], cafe: Cafe) -> float:
    """
    Score a cafe against expanded query terms.
    Checks tags (weighted 2x), description words, and name.
    Returns a float; higher = better match.
    """
    tags_raw  = (cafe.tags or "").lower().replace(",", " ").replace("-", " ")
    desc_raw  = cafe.description.lower().replace("-", " ")
    name_raw  = cafe.name.lower()

    tags_words = set(tags_raw.split())
    desc_words = set(desc_raw.split())
    name_words = set(name_raw.split())

    score = 0.0
    for term in query_terms:
        t = term.lower().replace("-", " ")
        # Tags count double — they are the most reliable signal
        if t in tags_words or any(t in tag for tag in tags_words):
            score += 2.0
        # Description single weight
        elif t in desc_words:
            score += 1.0
        # Name single weight
        elif t in name_words:
            score += 1.0

    # Normalize by number of unique query terms so short queries aren't penalized
    unique_terms = max(len(set(query_terms)), 1)
    return score / unique_terms


def smart_reason(query: str, cafe: Cafe) -> str:
    """Build a natural reason string without AI. Used as keyword-fallback text."""
    q = query.lower()
    tags = [t.strip() for t in (cafe.tags or "").lower().split(",")]

    reasons = []
    if any(t in q for t in ["study","studying","mag-aral","pag-aaral","wifi","laptop","thesis","review","homework"]):
        if any(t in tags for t in ["wifi","study","charging","student","quiet"]):
            reasons.append("great for studying with WiFi and power outlets")
    if any(t in q for t in ["quiet","tahimik","solo","peaceful","calm","relax","relaxing"]):
        if any(t in tags for t in ["quiet","solo","calm","relaxed","cozy"]):
            reasons.append("offers a quiet and peaceful atmosphere")
    if any(t in q for t in ["barkada","group","friends","grupo","hangout","hang"]):
        if any(t in tags for t in ["barkada","group","friends","hangout","social"]):
            reasons.append("perfect for barkada hangouts")
    if any(t in q for t in ["date","romantic","couple","mag-asawa","anniversary"]):
        if any(t in tags for t in ["romantic","date","cozy"]):
            reasons.append("has a romantic and cozy ambiance")
    if any(t in q for t in ["mura","cheap","affordable","budget","inexpensive","save"]):
        if any(t in tags for t in ["affordable","budget","cheap"]):
            reasons.append(f"budget-friendly at {cafe.price_range}")
    if any(t in q for t in ["late","night","gabi","hatinggabi","midnight","24","overnight"]):
        if any(t in tags for t in ["late-night","24hours","open-late","night"]):
            reasons.append("open late so you can hang out anytime")
    if any(t in q for t in ["live","band","music"]):
        if "live-band" in tags:
            reasons.append("has live band nights for great entertainment")
    if any(t in q for t in ["outdoor","garden","labas","hardin","outside","alfresco"]):
        if any(t in tags for t in ["garden","outdoor","open-air"]):
            reasons.append("has a relaxing outdoor garden setting")
    if any(t in q for t in ["dessert","sweet","matamis","cake","donut"]):
        if any(t in tags for t in ["dessert","sweet","cheesecake","donut"]):
            reasons.append("known for its delicious desserts and sweets")
    if any(t in q for t in ["ktv","karaoke"]):
        if "ktv" in tags:
            reasons.append("has a fun KTV room perfect for groups")
    if any(t in q for t in ["instagram","aesthetic","pretty","nice"]):
        if any(t in tags for t in ["aesthetic","instagram"]):
            reasons.append("very aesthetic and Instagram-worthy")

    if reasons:
        return f"{cafe.name} is a great pick — it's {' and '.join(reasons)}."
    return f"{cafe.name} is a solid match for what you're looking for in Santa Rosa."


# Ollama free AI

def call_ollama(prompt: str) -> str | None:
    if not Config.USE_OLLAMA:
        return None
    payload = json.dumps({
        "model":   Config.OLLAMA_MODEL,
        "prompt":  prompt,
        "stream":  False,
        "options": {"temperature": 0.7, "num_predict": 800},
    }).encode("utf-8")
    try:
        req = urllib.request.Request(
            f"{Config.OLLAMA_URL}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            return json.loads(resp.read().decode()).get("response", "").strip()
    except Exception:
        return None


def parse_ollama_json(raw: str) -> dict | None:
    if not raw:
        return None
    raw = re.sub(r"^```json?\s*", "", raw.strip())
    raw = re.sub(r"\s*```$", "", raw)
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except Exception:
            pass
    return None


# Route

# Minimum score to be included in results (tune this lower = more results)
MIN_SCORE     = 0.3
MAX_RESULTS   = 8


@ai_bp.route("/recommend", methods=["POST"])
def recommend():
    data         = request.get_json() or {}
    user_query   = (data.get("query") or "").strip()
    conv_history = data.get("conversation_history", [])
    input_method = data.get("input_method", "voice")

    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    detected_lang = detect_language(user_query)
    query_terms   = expand_query(user_query)

    cafes = Cafe.query.all()
    if not cafes:
        return jsonify({"error": "No cafes in database"}), 500

    # Score every cafe
    scored = sorted(
        [(score_cafe(query_terms, c), c) for c in cafes],
        key=lambda x: x[0],
        reverse=True,
    )

    # Keep cafes above threshold; always return at least top 3 even if scores are low
    qualifying = [(s, c) for s, c in scored if s >= MIN_SCORE]
    if len(qualifying) < 3:
        qualifying = scored[:3]              # floor: always show at least 3

    top_cafes  = [c for _, c in qualifying]
    cafe_map   = {c.id: c for c in cafes}

    # Try Ollama
    engine     = "keyword"
    ai_message = ""
    results    = []

    if Config.USE_OLLAMA:
        cafe_block = "\n\n".join([
            f"ID {c.id}: {c.name}\n  Tags: {c.tags}\n  Hours: {c.hours}\n  Price: {c.price_range}\n  Desc: {c.description}"
            for c in top_cafes
        ])
        history_text = "".join(
            f"{'User' if t['role']=='user' else 'Assistant'}: {t['content']}\n"
            for t in conv_history[-4:]
        )
        prompt = f"""You are KopiBot, a friendly cafe guide for Santa Rosa, Laguna, Philippines.
Understand English, Tagalog, and Taglish. Reply in the same language the user used.

{history_text}User: {user_query}

Matching cafes:
{cafe_block}

Return ALL cafes from the list that genuinely fit the user's request (can be 1 to {len(top_cafes)}).
Respond ONLY with this JSON (no other text):
{{
  "ai_message": "<short friendly reply, 1-2 sentences>",
  "recommendations": [
    {{"cafe_id": <id>, "reason": "<one specific sentence why this fits>"}},
    ...
  ]
}}"""

        raw    = call_ollama(prompt)
        parsed = parse_ollama_json(raw)

        if parsed:
            engine     = "ollama"
            ai_message = parsed.get("ai_message", "")
            for rec in parsed.get("recommendations", []):
                cafe = cafe_map.get(rec.get("cafe_id"))
                if cafe:
                    d = cafe.to_dict()
                    d["reason"] = rec.get("reason", smart_reason(user_query, cafe))
                    results.append(d)

    # Keyword fallback
    if not results:
        engine = "keyword"
        if detected_lang == "tl":
            ai_message = f"Narito ang mga cafe na bagay para sa'yo sa Santa Rosa — {len(top_cafes)} ang nahanap ko!"
        elif detected_lang == "taglish":
            ai_message = f"Here are {len(top_cafes)} cafes na pwede mong puntahan!"
        else:
            ai_message = f"Found {len(top_cafes)} great cafes matching your request!"

        for cafe in top_cafes:
            d = cafe.to_dict()
            d["reason"] = smart_reason(user_query, cafe)
            results.append(d)

    # Log
    if Config.VOICE_LOG_ENABLED:
        try:
            token     = session.get("kopihop_token") or str(uuid.uuid4())
            session["kopihop_token"] = token
            user_sess = UserSession.query.filter_by(session_token=token).first()
            if not user_sess:
                user_sess = UserSession(session_token=token)
                db.session.add(user_sess)
                db.session.flush()
            db.session.add(VoiceLog(
                session_id=user_sess.id,
                query_text=user_query,
                detected_lang=detected_lang,
                input_method=input_method,
                recommended_ids=json.dumps([r["id"] for r in results]),
            ))
            db.session.commit()
        except Exception:
            db.session.rollback()

    return jsonify({
        "recommendations": results,
        "ai_message":      ai_message,
        "detected_lang":   detected_lang,
        "engine":          engine,
    })
