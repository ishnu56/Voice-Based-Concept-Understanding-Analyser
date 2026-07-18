import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "vbcua_results.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS evaluations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            audio_file TEXT,
            topic TEXT,
            transcript TEXT,
            semantic_similarity REAL,
            filler_ratio REAL,
            filler_count INTEGER,
            pause_ratio REAL,
            rms_energy REAL,
            zero_crossing_rate REAL,
            duration REAL,
            transcription_runtime REAL,
            embedding_runtime REAL,
            audio_feature_runtime REAL,
            report_path TEXT,
            session_id TEXT,
            final_score REAL,
            level TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    for column, column_type in [
        ("user_name", "TEXT"),
        ("audio_file", "TEXT"),
        ("filler_count", "INTEGER"),
        ("zero_crossing_rate", "REAL"),
        ("duration", "REAL"),
        ("transcription_runtime", "REAL"),
        ("embedding_runtime", "REAL"),
        ("audio_feature_runtime", "REAL"),
        ("report_path", "TEXT"),
        ("session_id", "TEXT"),
    ]:
        try:
            cur.execute(f"ALTER TABLE evaluations ADD COLUMN {column} {column_type}")
        except sqlite3.OperationalError:
            pass
    conn.commit()
    conn.close()


def save_result(
    topic,
    transcript,
    similarity,
    filler_ratio,
    pause_ratio,
    rms_energy,
    final_score,
    level,
    user_name="Student",
    audio_file="",
    filler_count=0,
    zero_crossing_rate=0.0,
    duration=0.0,
    transcription_runtime=0.0,
    embedding_runtime=0.0,
    audio_feature_runtime=0.0,
    report_path="",
    session_id="",
):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO evaluations(
            user_name, audio_file, topic, transcript, semantic_similarity,
            filler_ratio, filler_count, pause_ratio, rms_energy, zero_crossing_rate,
            duration, transcription_runtime, embedding_runtime, audio_feature_runtime,
            report_path, session_id, final_score, level
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_name, audio_file, topic, transcript, similarity,
        filler_ratio, filler_count, pause_ratio, rms_energy, zero_crossing_rate,
        duration, transcription_runtime, embedding_runtime, audio_feature_runtime,
        report_path, session_id, final_score, level,
    ))
    conn.commit()
    conn.close()


def get_recent_results(limit=10):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT created_at, topic, final_score, level FROM evaluations ORDER BY id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows
