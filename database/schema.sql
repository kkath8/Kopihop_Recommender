-- =====================================================
-- KopiHop — PostgreSQL Schema Setup
-- =====================================================
-- Run once to set up the database:
--   psql -U postgres -c "CREATE DATABASE kopihop;"
--   psql -U postgres -d kopihop -f database/schema.sql
-- =====================================================

-- Enable pgvector (install from https://github.com/pgvector/pgvector if missing)
CREATE EXTENSION IF NOT EXISTS vector;

-- Drop existing tables (clean slate)
DROP TABLE IF EXISTS favorites     CASCADE;
DROP TABLE IF EXISTS voice_logs    CASCADE;
DROP TABLE IF EXISTS menu_items    CASCADE;
DROP TABLE IF EXISTS cafes         CASCADE;
DROP TABLE IF EXISTS user_sessions CASCADE;

-- ── cafes ──────────────────────────────────────────────
CREATE TABLE cafes (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(200)  NOT NULL,
    address     VARCHAR(500)  NOT NULL,
    description TEXT          NOT NULL,
    image       VARCHAR(300)  NOT NULL,
    tags        VARCHAR(600),
    hours       VARCHAR(200),
    price_range VARCHAR(50),
    embedding   vector(384)
);

-- ── menu_items ─────────────────────────────────────────
CREATE TABLE menu_items (
    id          SERIAL PRIMARY KEY,
    cafe_id     INTEGER NOT NULL REFERENCES cafes(id) ON DELETE CASCADE,
    category    VARCHAR(100) NOT NULL,
    name        VARCHAR(200) NOT NULL,
    description TEXT,
    price       VARCHAR(50)
);

-- ── user_sessions ──────────────────────────────────────
CREATE TABLE user_sessions (
    id             SERIAL PRIMARY KEY,
    session_token  VARCHAR(64) NOT NULL UNIQUE,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_seen      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ── voice_logs ─────────────────────────────────────────
CREATE TABLE voice_logs (
    id               SERIAL PRIMARY KEY,
    session_id       INTEGER REFERENCES user_sessions(id) ON DELETE SET NULL,
    query_text       TEXT        NOT NULL,
    detected_lang    VARCHAR(20) DEFAULT 'en',
    input_method     VARCHAR(10) DEFAULT 'voice',
    recommended_ids  TEXT,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ── favorites ──────────────────────────────────────────
CREATE TABLE favorites (
    id         SERIAL PRIMARY KEY,
    session_id INTEGER NOT NULL REFERENCES user_sessions(id) ON DELETE CASCADE,
    cafe_id    INTEGER NOT NULL REFERENCES cafes(id) ON DELETE CASCADE,
    saved_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_session_cafe UNIQUE (session_id, cafe_id)
);

-- ── indexes ────────────────────────────────────────────
CREATE INDEX idx_menu_items_cafe     ON menu_items(cafe_id);
CREATE INDEX idx_sessions_token      ON user_sessions(session_token);
CREATE INDEX idx_voice_logs_session  ON voice_logs(session_id);
CREATE INDEX idx_favorites_session   ON favorites(session_id);

SELECT '✅ KopiHop schema created successfully!' AS status;
