import os
from fastapi import FastAPI, HTTPException
import pymysql
from typing import Dict

# Environment variables for DB connection
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = int(os.getenv("DB_PORT", 3306))


def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        port=DB_PORT,
        cursorclass=pymysql.cursors.Cursor,
        autocommit=True
    )


app = FastAPI(title="TeamStats API")

QUERIES = {
    "team_avg_goals_last5": """
        SELECT ROUND(AVG(goals_scored),1)
        FROM (
            SELECT goals_scored
            FROM match_summary
            WHERE teamid = %s
            ORDER BY match_dt DESC
            LIMIT 5
        ) AS A;
    """,
    "team_avg_conceded_last5": """
        SELECT ROUND(AVG(goals_conceded),1)
        FROM (
            SELECT goals_conceded
            FROM match_summary
            WHERE teamid = %s
            ORDER BY match_dt DESC
            LIMIT 5
        ) AS A;
    """,
    "team_home_goals_avg": """
        SELECT ROUND(AVG(goals_scored),1)
        FROM (
            SELECT goals_scored
            FROM match_summary
            WHERE teamid = %s AND ishome=1
        ) AS A;
    """,
    "opponent_away_goals_avg": """
        SELECT ROUND(AVG(goals_scored),1)
        FROM (
            SELECT goals_scored
            FROM match_summary
            WHERE teamid = %s AND ishome=0
        ) AS A;
    """,
    "opponent_avg_conceded_last5": """
        SELECT ROUND(AVG(goals_conceded),1)
        FROM (
            SELECT goals_conceded
            FROM match_summary
            WHERE teamid = %s
            ORDER BY match_dt DESC
            LIMIT 5
        ) AS A;
    """,
    "opponent_avg_goals_last5": """
        SELECT ROUND(AVG(goals_scored),1)
        FROM (
            SELECT goals_scored
            FROM match_summary
            WHERE teamid = %s
            ORDER BY match_dt DESC
            LIMIT 5
        ) AS A;
    """
}


@app.get("/team_stats/{teamid}/{opponentid}")
def get_team_stats(teamid: int, opponentid: int) -> Dict:
    if not (DB_HOST and DB_USER and DB_PASS and DB_NAME):
        raise HTTPException(status_code=500, detail="Database config not set in environment")

    result = {}
    try:
        conn = get_connection()
        cursor = conn.cursor()

        for key, query in QUERIES.items():
            if key.startswith("team_"):
                params = (teamid,)
            else:
                params = (opponentid,)

            cursor.execute(query, params)
            row = cursor.fetchone()
            val = row[0] if row is not None else None
            result[key] = float(val) if val is not None else 0.0

        cursor.close()
        conn.close()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
