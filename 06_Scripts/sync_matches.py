
import json
import os

from datetime import date, time
from pathlib import Path

import psycopg2
from dotenv import load_dotenv


# =====================================================
# 1. PROJECT CONFIGURATION
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = (
    PROJECT_ROOT
    / "05_Data"
    / "openfootball"
    / "premier_league_2026_27.json"
)

COMPETITION_NAME = "Premier League"
COUNTRY = "England"
SEASON = "2026/27"

# False = preview only
# True = allow database changes after confirmation
APPLY_CHANGES = False

load_dotenv(PROJECT_ROOT / ".env")


# =====================================================
# 2. CHECK ENVIRONMENT
# =====================================================

required_variables = [
    "DB_HOST",
    "DB_NAME",
    "DB_USER",
    "DB_PASSWORD"
]

missing_variables = [
    name for name in required_variables
    if not os.getenv(name)
]

if missing_variables:
    raise SystemExit(
        f"Missing environment variables: {missing_variables}"
    )

if not DATA_FILE.exists():
    raise SystemExit(f"Data file not found: {DATA_FILE}")


# =====================================================
# 3. VALIDATE SCORE DATA
# =====================================================

def validate_score_pair(values, label):

    if values is None:
        return None, None

    if not isinstance(values, list) or len(values) != 2:
        raise ValueError(f"Invalid {label} score format")

    for value in values:
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(f"{label} scores must be integers")

        if value < 0:
            raise ValueError(f"{label} scores cannot be negative")

    return values[0], values[1]


def parse_match(match):

    if not isinstance(match, dict):
        raise ValueError("Match record must be a JSON object")

    matchday = match.get("round")
    match_date = match.get("date")
    match_time = match.get("time")
    home_team = match.get("team1")
    away_team = match.get("team2")

    if not all([matchday, match_date, home_team, away_team]):
        raise ValueError("Missing required fixture information")

    if not all(isinstance(value, str) for value in [
        matchday, match_date, home_team, away_team
    ]):
        raise ValueError("Fixture fields must be text")

    parsed_date = date.fromisoformat(match_date)

    parsed_time = (
        time.fromisoformat(match_time)
        if match_time else None
    )

    score = match.get("score")

    home_ht = away_ht = None
    home_ft = away_ft = None

    if isinstance(score, list):
        home_ft, away_ft = validate_score_pair(
            score, "Full-time"
        )

    elif isinstance(score, dict):

        home_ht, away_ht = validate_score_pair(
            score.get("ht"), "Half-time"
        )

        home_ft, away_ft = validate_score_pair(
            score.get("ft"), "Full-time"
        )

    elif score is not None:
        raise ValueError("Unknown score format")

    if home_ht is not None and home_ft is not None:
        if home_ht > home_ft or away_ht > away_ft:
            raise ValueError("Half-time score exceeds full-time score")

    return {
        "matchday": matchday,
        "match_date": parsed_date,
        "match_time": parsed_time,
        "home_team": home_team,
        "away_team": away_team,
        "home_ht": home_ht,
        "away_ht": away_ht,
        "home_ft": home_ft,
        "away_ft": away_ft
    }


# =====================================================
# 4. LOAD AND VALIDATE JSON
# =====================================================

with open(DATA_FILE, "r", encoding="utf-8") as file:
    source_data = json.load(file)

if not isinstance(source_data, dict):
    raise SystemExit("Invalid JSON root structure")

if source_data.get("name") != "English Premier League 2026/27":
    raise SystemExit("Unexpected competition name in JSON")

raw_matches = source_data.get("matches")

if not isinstance(raw_matches, list):
    raise SystemExit("JSON does not contain a valid matches list")

valid_matches = []
validation_errors = []
seen_fixtures = set()

for index, raw_match in enumerate(raw_matches, start=1):

    try:
        match = parse_match(raw_match)

        fixture_key = (
            match["match_date"],
            match["home_team"],
            match["away_team"]
        )

        if fixture_key in seen_fixtures:
            raise ValueError("Duplicate fixture in JSON")

        seen_fixtures.add(fixture_key)
        valid_matches.append(match)

    except (ValueError, TypeError, KeyError) as error:
        validation_errors.append(
            f"Record {index}: {error}"
        )


# =====================================================
# 5. DISPLAY START INFORMATION
# =====================================================

print("\n========================================")
print("GOALLENS - MATCH SYNCHRONISATION")
print("========================================")

print("Competition:", COMPETITION_NAME)
print("Country:", COUNTRY)
print("Season:", SEASON)
print("Source:", DATA_FILE.name)
print("Records in JSON:", len(raw_matches))
print("Valid records:", len(valid_matches))
print("Invalid records:", len(validation_errors))

if validation_errors:
    print("\nVALIDATION ERRORS:")

    for error in validation_errors:
        print("-", error)

if not valid_matches:
    raise SystemExit("No valid fixtures to process")


# =====================================================
# 6. CONNECT TO POSTGRESQL
# =====================================================

connection = None
cursor = None

try:

    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    cursor = connection.cursor()

    print("\nConnected to PostgreSQL.")

    # Find the competition instead of assuming its ID
    cursor.execute(
        """
        SELECT competition_id
        FROM competitions
        WHERE competition_name = %s
          AND country = %s
        """,
        (COMPETITION_NAME, COUNTRY)
    )

    competition_rows = cursor.fetchall()

    if len(competition_rows) != 1:
        raise RuntimeError(
            "Expected exactly one matching competition. "
            f"Found: {len(competition_rows)}"
        )

    competition_id = competition_rows[0][0]

    # Load club IDs
    cursor.execute(
        """
        SELECT club_id, club_name
        FROM clubs
        """
    )

    clubs = {
        club_name: club_id
        for club_id, club_name in cursor.fetchall()
    }


    # =================================================
    # 7. BUILD SYNCHRONISATION PLAN
    # =================================================

    plan = []

    counts = {
        "insert": 0,
        "update": 0,
        "unchanged": 0,
        "conflict": 0,
        "error": 0
    }

    for match in valid_matches:

        home_id = clubs.get(match["home_team"])
        away_id = clubs.get(match["away_team"])

        if home_id is None or away_id is None:
            print(
                "\nUnknown club:",
                match["home_team"],
                "vs",
                match["away_team"]
            )
            counts["error"] += 1
            continue

        if home_id == away_id:
            print("\nInvalid fixture: same home and away club.")
            counts["error"] += 1
            continue

        cursor.execute(
            """
            SELECT
                match_id,
                home_ht_goals,
                away_ht_goals,
                home_goals,
                away_goals
            FROM matches
            WHERE competition_id = %s
              AND season = %s
              AND match_date = %s
              AND home_club_id = %s
              AND away_club_id = %s
            """,
            (
                competition_id,
                SEASON,
                match["match_date"],
                home_id,
                away_id
            )
        )

        existing = cursor.fetchone()

        incoming_scores = (
            match["home_ht"],
            match["away_ht"],
            match["home_ft"],
            match["away_ft"]
        )

        if existing is None:

            plan.append({
                "action": "insert",
                "match": match,
                "home_id": home_id,
                "away_id": away_id
            })

            counts["insert"] += 1
            continue

        old_scores = existing[1:]
        fields_to_fill = []
        conflicts = []

        for index, (old, new) in enumerate(
            zip(old_scores, incoming_scores)
        ):

            if old is None and new is not None:
                fields_to_fill.append(index)

            elif old is not None and new is not None and old != new:
                conflicts.append(index)

        if conflicts:
            counts["conflict"] += 1

            print(
                "\nSCORE CONFLICT:",
                match["home_team"],
                "vs",
                match["away_team"],
                "| Database:",
                old_scores,
                "| Source:",
                incoming_scores
            )

        if fields_to_fill:

            plan.append({
                "action": "update",
                "match": match,
                "match_id": existing[0],
                "fields": fields_to_fill
            })

            counts["update"] += 1

        elif not conflicts:

            counts["unchanged"] += 1

    # =================================================
    # 8. DISPLAY PREVIEW
    # =================================================

    print("\n========================================")
    print("SYNCHRONISATION PREVIEW")
    print("========================================")

    print("New fixtures:", counts["insert"])
    print("Fixtures needing score updates:", counts["update"])
    print("Unchanged fixtures:", counts["unchanged"])
    print("Score conflicts:", counts["conflict"])
    print("Unknown/invalid fixtures:", counts["error"])

    if not APPLY_CHANGES:

        connection.rollback()

        print("\nDRY-RUN COMPLETE.")
        print("No database changes were saved.")

    else:

        print("\nWARNING: DATABASE CHANGES REQUESTED.")

        confirmation = input(
            "Type APPLY to confirm these changes: "
        )

        if confirmation != "APPLY":
            connection.rollback()
            print("Cancelled. No changes were saved.")

        else:

            # =========================================
            # 9. APPLY CHANGES SAFELY
            # =========================================

            applied_insertions = 0
            applied_updates = 0
            failed_operations = 0

            for item in plan:

                cursor.execute("SAVEPOINT fixture_operation")

                try:

                    match = item["match"]

                    if item["action"] == "insert":

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
                                %s, %s, %s, %s, %s,
                                %s, %s, %s, %s, %s, %s
                            )
                            """,
                            (
                                competition_id,
                                SEASON,
                                match["match_date"],
                                match["match_time"],
                                match["matchday"],
                                item["home_id"],
                                item["away_id"],
                                match["home_ht"],
                                match["away_ht"],
                                match["home_ft"],
                                match["away_ft"]
                            )
                        )

                        applied_insertions += 1

                    elif item["action"] == "update":

                        column_names = [
                            "home_ht_goals",
                            "away_ht_goals",
                            "home_goals",
                            "away_goals"
                        ]

                        for field_index in item["fields"]:

                            column = column_names[field_index]

                            value = (
                                match["home_ht"],
                                match["away_ht"],
                                match["home_ft"],
                                match["away_ft"]
                            )[field_index]

                            cursor.execute(
                                f"""
                                UPDATE matches
                                SET {column} = %s
                                WHERE match_id = %s
                                  AND {column} IS NULL
                                """,
                                (value, item["match_id"])
                            )

                        applied_updates += 1

                    cursor.execute("RELEASE SAVEPOINT fixture_operation")

                except psycopg2.Error as error:

                    cursor.execute(
                        "ROLLBACK TO SAVEPOINT fixture_operation"
                    )

                    cursor.execute(
                        "RELEASE SAVEPOINT fixture_operation"
                    )

                    failed_operations += 1

                    print(
                        "\nDatabase error for:",
                        match["home_team"],
                        "vs",
                        match["away_team"],
                        "|",
                        error
                    )

            connection.commit()

            print("\n========================================")
            print("SYNCHRONISATION RESULT")
            print("========================================")

            print("Inserted:", applied_insertions)
            print("Updated:", applied_updates)
            print("Failed operations:", failed_operations)
            print("Conflicts left for review:", counts["conflict"])
            print("Committed successfully.")


except (psycopg2.Error, RuntimeError, OSError, ValueError) as error:

    if connection is not None:
        connection.rollback()

    print("\nSynchronisation failed:", error)


finally:

    if cursor is not None:
        cursor.close()

    if connection is not None:
        connection.close()

    print("\nDatabase connection closed.")
