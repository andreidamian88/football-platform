
import json
import os
import psycopg2

from pathlib import Path
from dotenv import load_dotenv


# ==========================================
# 1. PROJECT CONFIGURATION
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = (
    PROJECT_ROOT
    / "05_Data"
    / "openfootball"
    / "premier_league_2026_27.json"
)

# Load environment variables from .env
load_dotenv(PROJECT_ROOT / ".env")


# ==========================================
# 2. CHECK CONFIGURATION
# ==========================================

required_variables = [
    "DB_HOST",
    "DB_NAME",
    "DB_USER",
    "DB_PASSWORD"
]

missing_variables = [
    variable
    for variable in required_variables
    if not os.getenv(variable)
]

if missing_variables:
    raise SystemExit(
        f"Missing environment variables: {missing_variables}"
    )

if not DATA_FILE.exists():
    raise SystemExit(f"JSON file not found: {DATA_FILE}")


# ==========================================
# 3. LOAD JSON DATA
# ==========================================

with open(DATA_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)

matches = data["matches"]

print("===================================")
print("GOALLENS - MATCH IMPORTER")
print("===================================")
print("Competition:", data.get("name", "Unknown"))
print("Number of matches:", len(matches))
print()


# ==========================================
# 4. IMPORT STATISTICS
# ==========================================

inserted_count = 0
updated_count = 0
unchanged_count = 0
error_count = 0


# ==========================================
# 5. DATABASE CONNECTION
# ==========================================

connection = None

try:

    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    cursor = connection.cursor()

    print("Connected to PostgreSQL successfully.")
    print()


    # ======================================
    # 6. PROCESS MATCHES
    # ======================================

    for match in matches:

        try:

            matchday = match.get("round")
            match_date = match.get("date")
            match_time = match.get("time")

            home_team = match.get("team1")
            away_team = match.get("team2")

            if not all([
                matchday,
                match_date,
                home_team,
                away_team
            ]):
                print("Invalid match record - skipped.")
                error_count += 1
                continue


            # Find home club
            cursor.execute(
                """
                SELECT club_id
                FROM clubs
                WHERE club_name = %s
                """,
                (home_team,)
            )

            home_result = cursor.fetchone()

            if home_result is None:
                print("Home club not found:", home_team)
                error_count += 1
                continue

            home_club_id = home_result[0]


            # Find away club
            cursor.execute(
                """
                SELECT club_id
                FROM clubs
                WHERE club_name = %s
                """,
                (away_team,)
            )

            away_result = cursor.fetchone()

            if away_result is None:
                print("Away club not found:", away_team)
                error_count += 1
                continue

            away_club_id = away_result[0]


            # Avoid a team playing against itself
            if home_club_id == away_club_id:
                print("Invalid fixture: same home and away club.")
                error_count += 1
                continue


            # ==================================
            # 7. READ MATCH SCORES
            # ==================================

            score = match.get("score")

            home_ht_goals = None
            away_ht_goals = None
            home_goals = None
            away_goals = None

            if isinstance(score, list):

                # Simple full-time score
                if len(score) != 2:
                    raise ValueError("Invalid full-time score format.")

                home_goals, away_goals = score


            elif isinstance(score, dict):

                # Detailed half-time and full-time scores
                ht_score = score.get("ht")
                ft_score = score.get("ft")

                if ht_score is not None:

                    if len(ht_score) != 2:
                        raise ValueError("Invalid half-time score.")

                    home_ht_goals, away_ht_goals = ht_score

                if ft_score is not None:

                    if len(ft_score) != 2:
                        raise ValueError("Invalid full-time score.")

                    home_goals, away_goals = ft_score


            elif score is not None:

                raise ValueError("Unknown score format.")


            # Validate score values
            score_values = [
                home_ht_goals,
                away_ht_goals,
                home_goals,
                away_goals
            ]

            for value in score_values:
                if value is not None:
                    if not isinstance(value, int) or isinstance(value, bool):
                        raise ValueError("Score must be an integer.")

                    if value < 0:
                        raise ValueError("Score cannot be negative.")


            # ==================================
            # 8. CHECK EXISTING MATCH
            # ==================================

            cursor.execute(
                """
                SELECT
                    home_ht_goals,
                    away_ht_goals,
                    home_goals,
                    away_goals
                FROM matches
                WHERE competition_id = 1
                  AND season = '2026/27'
                  AND match_date = %s
                  AND home_club_id = %s
                  AND away_club_id = %s
                """,
                (
                    match_date,
                    home_club_id,
                    away_club_id
                )
            )

            existing_match = cursor.fetchone()


            # ==================================
            # 9. INSERT OR UPDATE MATCH
            # ==================================

            cursor.execute(
                """
                INSERT INTO matches (
                    competition_id,
                    season,
                    match_date,
                    match_time,
                    matchday,
                    home_club_id,
                    away_club_id,
                    home_ht_goals,
                    away_ht_goals,
                    home_goals,
                    away_goals
                )

                VALUES (
                    %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s
                )

                ON CONFLICT ON CONSTRAINT unique_match

                DO UPDATE SET

                    home_ht_goals = COALESCE(
                        EXCLUDED.home_ht_goals,
                        matches.home_ht_goals
                    ),

                    away_ht_goals = COALESCE(
                        EXCLUDED.away_ht_goals,
                        matches.away_ht_goals
                    ),

                    home_goals = COALESCE(
                        EXCLUDED.home_goals,
                        matches.home_goals
                    ),

                    away_goals = COALESCE(
                        EXCLUDED.away_goals,
                        matches.away_goals
                    )
                """,
                (
                    1,
                    "2026/27",
                    match_date,
                    match_time,
                    matchday,
                    home_club_id,
                    away_club_id,
                    home_ht_goals,
                    away_ht_goals,
                    home_goals,
                    away_goals
                )
            )


            # ==================================
            # 10. COUNT CHANGES
            # ==================================

            if existing_match is None:

                inserted_count += 1

            else:

                old_scores = existing_match

                new_scores = (
                    home_ht_goals if home_ht_goals is not None else old_scores[0],
                    away_ht_goals if away_ht_goals is not None else old_scores[1],
                    home_goals if home_goals is not None else old_scores[2],
                    away_goals if away_goals is not None else old_scores[3]
                )

                if new_scores != old_scores:
                    updated_count += 1
                else:
                    unchanged_count += 1


        except (ValueError, TypeError, KeyError) as error:

            print(
                "Invalid match:",
                match.get("team1"),
                "vs",
                match.get("team2"),
                "|",
                error
            )

            error_count += 1


        except psycopg2.Error:

            # Roll back the failed transaction before continuing
            connection.rollback()

            print(
                "Database error:",
                match.get("team1"),
                "vs",
                match.get("team2")
            )

            error_count += 1


    # ======================================
    # 11. COMMIT CHANGES
    # ======================================

    connection.commit()

    print()
    print("===================================")
    print("IMPORT SUMMARY")
    print("===================================")

    print("Inserted:", inserted_count)
    print("Updated:", updated_count)
    print("Unchanged:", unchanged_count)
    print("Errors:", error_count)

    print("Import completed.")


except psycopg2.Error as error:

    if connection is not None:
        connection.rollback()

    print("Database connection or transaction failed:", error)


finally:

    if connection is not None:
        connection.close()
        print("Database connection closed.")
