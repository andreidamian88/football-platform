
import os

import psycopg2
from dotenv import load_dotenv
from pathlib import Path


# ==========================================
# 1. PROJECT CONFIGURATION
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env")


# ==========================================
# 2. DATABASE CONNECTION
# ==========================================

def connect_to_database():

    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )

        print("Successfully connected to GoalLens database!")

        return connection

    except psycopg2.Error as error:

        print("Database connection failed:", error)

        return None


# ==========================================

# ==========================================
# 3. RETRIEVE CLUB BEHAVIOUR DATA
# ==========================================

def get_club_behaviour(connection):

    query = """
        SELECT
            club_name,
            venue,
            completed_matches,
            halftime_leads,
            leads_protected,
            points_dropped,
            comeback_wins,
            comeback_opportunities,
            lead_protection_pct,
            comeback_win_pct

        FROM vw_halftime_dna_team_behaviour

        ORDER BY club_name, venue;
    """

    try:

        cursor = connection.cursor()

        cursor.execute(query)

        results = cursor.fetchall()

        cursor.close()

        return results

    except psycopg2.Error as error:

        print("Error retrieving club statistics:", error)

        return []


# ==========================================
# 4. CALCULATE BEHAVIOUR METRICS
# ==========================================

def calculate_lead_protection(halftime_leads, leads_protected):

    if halftime_leads == 0:
        return None

    percentage = (leads_protected / halftime_leads) * 100

    return round(percentage, 2)

# ==========================================
# 5. CALCULATE COMEBACK BEHAVIOUR
# ==========================================

def calculate_comeback_win_rate(comeback_opportunities, comeback_wins):

    if comeback_opportunities == 0:
        return None

    percentage = (
        comeback_wins / comeback_opportunities
    ) * 100

    return round(percentage, 2)

# ==========================================
# ==========================================
# 6. MAIN PROGRAM
# ==========================================

def main():

    print("\n===================================")
    print("GOALLENS - CLUB BEHAVIOUR FINGERPRINT")
    print("===================================\n")

    connection = connect_to_database()

    if connection is None:
        return

    try:
        results = get_club_behaviour(connection)

        validation_passed = 0
        validation_failed = 0

        print("\nCLUB BEHAVIOUR DATA")
        print("-----------------------------------")

        for row in results:

            protection_rate = calculate_lead_protection(
                row[3],
                row[4]
            )

            comeback_rate = calculate_comeback_win_rate(
                row[7],
                row[6]
            )

            database_protection = row[8]
            database_comeback = row[9]

            protection_match = protection_rate == (
                round(float(database_protection), 2)
                if database_protection is not None else None
            )

            comeback_match = comeback_rate == (
                round(float(database_comeback), 2)
                if database_comeback is not None else None
            )

            if protection_match and comeback_match:
                validation_passed += 1
            else:
                validation_failed += 1
                print(f"VALIDATION FAILED: {row[0]} ({row[1]})")

            if protection_rate is None:
                rate_text = "N/A"
            else:
                rate_text = f"{protection_rate:.2f}%"

            if comeback_rate is None:
                comeback_text = "N/A"
            else:
                comeback_text = f"{comeback_rate:.2f}%"

            print(
                f"{row[0]:30} | "
                f"{row[1]:5} | "
                f"Matches: {row[2]:2} | "
                f"HT Leads: {row[3]:2} | "
                f"Protected: {row[4]:2} | "
                f"Protection: {rate_text} | "
                f"Comeback Rate: {comeback_text}"
            )

        print("\nVALIDATION SUMMARY")
        print("-----------------------------------")
        print("Records checked:", len(results))
        print("Passed:", validation_passed)
        print("Failed:", validation_failed)
        if len(results) > 0:
             validation_rate = (
                 validation_passed / len(results)
             ) * 100
        else:
                validation_rate = 0

        print(f"Validation rate: {validation_rate:.2f}%")
        print("-----------------------------------")
        print("Total records retrieved:", len(results))

    finally:
        connection.close()
        print("\nDatabase connection closed.")


if __name__ == "__main__":
    main()