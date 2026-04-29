import psycopg2
from config import DB_CONFIG

conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()





def get_or_create_player(username):
    cur.execute("SELECT id FROM players WHERE username=%s", (username,))
    r = cur.fetchone()
    if r:
        return r[0]

    cur.execute(
        "INSERT INTO players (username) VALUES (%s) RETURNING id",
        (username,)
    )
    conn.commit()
    return cur.fetchone()[0]


def save_score(player_id, score, level):
    cur.execute("""
        INSERT INTO game_sessions (player_id, score, level_reached)
        VALUES (%s, %s, %s)
    """, (player_id, score, level))
    conn.commit()


def get_best_score(player_id):
    cur.execute("""
        SELECT MAX(score) FROM game_sessions
        WHERE player_id=%s
    """, (player_id,))
    r = cur.fetchone()[0]
    return r if r else 0


def get_leaderboard():
    cur.execute("""
        SELECT p.username, g.score, g.level_reached, g.played_at
        FROM game_sessions g
        JOIN players p ON g.player_id = p.id
        ORDER BY g.score DESC
        LIMIT 10
    """)
    return cur.fetchall()