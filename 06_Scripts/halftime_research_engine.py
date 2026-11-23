
import os
import psycopg2

from dotenv import load_dotenv
from pathlib import Path

from club_behaviour_fingerprint import classify_evidence


# ==================================================
# 1. PROJECT CONFIGURATION
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env")


# ==================================================
# 2. DATABASE CONNECTION
# ==================================================

def connect_to_database():

    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )

        print("Successfully connected to PostgreSQL!")

        return connection

    except psycopg2.Error as error:

        print("Database connection failed:", error)

        return None


# ==================================================
# 3. RETRIEVE COMPETITION OVERVIEW
# ==================================================

def get_competition_overview(connection):

    try:

        cursor = connection.cursor()

        query = """
            SELECT *
            FROM vw_halftime_dna_overview;
        """

        cursor.execute(query)

        results = cursor.fetchall()

        cursor.close()

        return results

    except psycopg2.Error as error:

        print("Error retrieving competition overview:", error)

        return None


# ==================================================
# 4. RETRIEVE CLUB BEHAVIOUR
# ==================================================

def get_club_behaviour(connection):

    try:

        cursor = connection.cursor()

        query = """
            SELECT
                club_name,
                venue,
                completed_matches,
                halftime_leads,
                leads_protected,
                leads_drawn,
                leads_lost,
                points_dropped,
                comeback_opportunities,
                comeback_wins,
                avoided_defeats,
                lead_protection_pct,
                comeback_win_pct,
                avoided_defeat_pct
            FROM vw_halftime_dna_team_behaviour
            ORDER BY club_name, venue;
        """

        cursor.execute(query)

        results = cursor.fetchall()

        cursor.close()

        return results

    except psycopg2.Error as error:

        print("Error retrieving club behaviour:", error)

        return None


# ==================================================
# 5. DISPLAY COMPETITION OVERVIEW
# ==================================================

def display_competition_overview(results):

    for row in results:

        print("\n========== COMPETITION OVERVIEW ==========\n")

        print(f"Competition: {row[0]}")
        print(f"Season: {row[1]}")
        print(f"Total fixtures: {row[2]}")
        print(f"Completed matches: {row[3]}")

        print("\n--- HALF-TIME SITUATIONS ---")

        print(f"Home teams leading: {row[4]}")
        print(f"Away teams leading: {row[5]}")
        print(f"Level at half-time: {row[6]}")

        print("\n--- LEAD PROTECTION ---")

        print(f"Home leads protected: {row[7]}")
        print(f"Away leads protected: {row[8]}")
        print(f"Home protection rate: {row[9]}%")
        print(f"Away protection rate: {row[10]}%")

        print("\n--- POINTS DROPPED ---")

        print(f"Home teams: {row[11]}")
        print(f"Away teams: {row[12]}")

        print("\n--- COMEBACK WINS ---")

        print(f"Home teams: {row[13]}")
        print(f"Away teams: {row[14]}")

        print("\n==========================================")


# ==================================================
# 6. DISPLAY CLUB BEHAVIOUR
# ==================================================

def display_club_behaviour(results):

    print("\n========== CLUB BEHAVIOUR ANALYSIS ==========\n")

    print(
        f"{'Club':<30} "
        f"{'Venue':<7} "
        f"{'Matches':>7} "
        f"{'Leads':>6} "
        f"{'Protected':>10} "
        f"{'Points':>7} "
        f"{'Comebacks':>10} "
        f"{'Wins':>5} "
        f"{'Avoided':>8} "
        f"{'Protection %':>13} "
        f"{'Comeback %':>11} "
        f"{'Avoided %':>10}"
        f"{'Lead Evidence':>18} "
        f"{'Comeback Evidence':>20}"
    )

    print("-" * 180)

    for row in results:

        club_name = row[0]
        venue = row[1]
        matches = row[2]
        leads = row[3]
        protected = row[4]
        points = row[7]
        lead_evidence = classify_evidence(row[3])
        comeback_evidence = classify_evidence(row[8])
        comeback_wins = row[9]
        avoided_defeats = row[10]
        comeback_opportunities = row[8]
        protection_rate = row[11]
        comeback_rate = row[12]
        avoided_rate = row[13]

        if protection_rate is None:
            protection_display = "N/A"
        else:
            protection_display = f"{protection_rate:.2f}%"

        if comeback_rate is None:
            comeback_display = "N/A"
        else:
            comeback_display = f"{comeback_rate:.2f}%"

        if avoided_rate is None:
            avoided_display = "N/A"
        else:
            avoided_display = f"{avoided_rate:.2f}%"

        print(
            f"{club_name:<30} "
            f"{venue:<7} "
            f"{matches:>7} "
            f"{leads:>6} "
            f"{protected:>10} "
            f"{points:>7} "
            f"{comeback_opportunities:>10} "
            f"{comeback_wins:>5} "
            f"{avoided_defeats:>8} "
            f"{protection_display:>13} "
            f"{comeback_display:>11} "
            f"{avoided_display:>10} "
            f"{lead_evidence:>18} "
            f"{comeback_evidence:>20}"
        )
        print("\n" + "=" * 180)

# ==================================================
# 7. MAIN RESEARCH ENGINE
# ==================================================

# ==================================================
# 7. VALIDATE CLUB BEHAVIOUR TOTALS
# ==================================================

def validate_club_behaviour(club_results, overview_results):

    print("\n========== DATA VALIDATION ==========\n")

    if not club_results or not overview_results:
        print("Validation could not be completed.")
        return

    total_leads = sum(row[3] for row in club_results)
    total_protected = sum(row[4] for row in club_results)
    total_points_dropped = sum(row[7] for row in club_results)

    total_comeback_opportunities = sum(row[8] for row in club_results)
    total_comeback_wins = sum(row[9] for row in club_results)
    total_avoided_defeats = sum(row[10] for row in club_results)

    print(f"Lead opportunities: {total_leads}")
    print(f"Leads protected: {total_protected}")
    print(f"Points dropped: {total_points_dropped}")
    print(f"Comeback opportunities: {total_comeback_opportunities}")
    print(f"Comeback wins: {total_comeback_wins}")
    print(f"Avoided defeats: {total_avoided_defeats}")
        # Expected totals from the competition overview
    expected_leads = overview_results[0][4] + overview_results[0][5]
    expected_protected = overview_results[0][7] + overview_results[0][8]
    expected_points_dropped = overview_results[0][11] + overview_results[0][12]
    expected_comeback_opportunities = expected_leads
    expected_comeback_wins = overview_results[0][13] + overview_results[0][14]

    # Compare calculated totals with expected totals
    checks = [
        ("Lead opportunities", total_leads, expected_leads),
        ("Leads protected", total_protected, expected_protected),
        ("Points dropped", total_points_dropped, expected_points_dropped),
        ("Comeback opportunities", total_comeback_opportunities, expected_comeback_opportunities),
        ("Comeback wins", total_comeback_wins, expected_comeback_wins)
    ]

    print("\n========== VALIDATION RESULTS ==========\n")

    passed = 0
    failed = 0

    for name, actual, expected in checks:
        if actual == expected:
            print(f"{name:<30} PASS")
            passed += 1
        else:
            print(f"{name:<30} FAIL (Actual: {actual}, Expected: {expected})")
            failed += 1

    print("\n----------------------------------------")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Overall: {passed}/{len(checks)} checks passed")

    print("\nValidation calculations completed.")

# ==================================================
     # Test evidence classification

def main():

    print("\n========== HALF-TIME DNA RESEARCH ENGINE ==========\n")

    connection = connect_to_database()

    if connection is None:
        return

    try:

        # Retrieve competition overview
        results = get_competition_overview(connection)

        # Retrieve club behaviour
        club_results = get_club_behaviour(connection)

        # Validate club behaviour totals
        if club_results is not None and results is not None:
         validate_club_behaviour(club_results, results)
        # Display club behaviour
        if club_results is not None:

            print("\nClub behaviour data retrieved successfully!")
            print(f"Total records: {len(club_results)}")

            display_club_behaviour(club_results)

        else:

            print("Unable to retrieve club behaviour data.")

        # Display competition overview
        if results is not None:

            print("\nCompetition overview retrieved successfully!")

            display_competition_overview(results)

        else:

            print("Unable to retrieve competition overview.")

    finally:

        connection.close()

        print("\nDatabase connection closed.")


# ==================================================
# 8. PROGRAM ENTRY POINT
# ==================================================

if __name__ == "__main__":

    main()
