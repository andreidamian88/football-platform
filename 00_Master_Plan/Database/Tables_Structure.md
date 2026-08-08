# FootballPlatform Database Tables Structure

## Overview

This document describes the structure of the main database tables used in the FootballPlatform MVP.

Each table represents a specific football-related entity and contains attributes required for storing and analysing data.

---

# 1. Players Table

## Purpose

| Column          | Type               | Description              |
| --------------- | ------------------ | ------------------------ |
| player_id       | SERIAL PRIMARY KEY | Unique player identifier |
| first_name      | VARCHAR(50)        | Player first name        |
| last_name       | VARCHAR(50)        | Player surname           |
| date_of_birth   | DATE               | Date of birth            |
| nationality     | VARCHAR(50)        | Player nationality       |
| preferred_foot  | VARCHAR(10)        | Left / Right / Both      |
| club_id         | INTEGER FK         | Current club reference   |
## Structure

| Column | Type | Description |
|---|---|---|
| player_id | SERIAL PRIMARY KEY | Unique player identifier |
| first_name | VARCHAR(50) | Player first name |
| last_name | VARCHAR(50) | Player surname |
| date_of_birth | DATE | Date of birth |
| nationality | VARCHAR(50) | Player nationality |
| height | INTEGER | Player height in cm |
| preferred_foot | VARCHAR(10) | Left / Right |
| club_id | INTEGER FK | Current club |

---

# 2. Clubs Table

## Purpose

Stores football club information.

## Structure

| Column | Type | Description |
|---|---|---|
| club_id | SERIAL PRIMARY KEY | Unique club identifier |
| name | VARCHAR(100) | Club name |
| country | VARCHAR(50) | Country |
| city | VARCHAR(50) | City |
| founded_year | INTEGER | Year founded |

---

# 3. Competitions Table

## Purpose

Stores football competitions.

## Structure

| Column | Type | Description |
|---|---|---|
| competition_id | SERIAL PRIMARY KEY | Unique competition identifier |
| name | VARCHAR(100) | Competition name |
| country | VARCHAR(50) | Country |
| competition_type | VARCHAR(50) | League / Cup / International |
| level | VARCHAR(50) | Competition level |

---

# 4. Player Statistics Table

## Purpose

Stores player performance data by season.

## Structure

| Column | Type | Description |
|---|---|---|
| stat_id | SERIAL PRIMARY KEY | Unique statistic identifier |
| player_id | INTEGER FK | Player reference |
| season | VARCHAR(20) | Football season |
| appearances | INTEGER | Matches played |
| minutes_played | INTEGER | Total minutes |
| goals | INTEGER | Goals scored |
| assists | INTEGER | Assists |

---

# 5. Matches Table

## Purpose

Stores football match information.

## Structure

| Column | Type | Description |
|---|---|---|
| match_id | SPlayer reference |
| club_id | INTEGER FK | Club reference |
| start_date | DATE | Contra
ERIAL PRIMARY KEY | Unique match identifier |
| competition_id | INTEGER FK | Competition reference |
| home_team_id | INTEGER FK | Home club |
| away_team_id | INTEGER FK | Away club |
| match_date | DATE | Match date |
| home_score | INTEGER | Home goals |
| away_score | INTEGER | Away goals |

---

# 6. Contracts Table

## Purpose

Stores player contract information.

## Structure

| Column            | Type               | Description                    |
| ----------------- | ------------------ | ------------------------------ |
| contract_id       | SERIAL PRIMARY KEY | Unique contract identifier     |
| player_id         | INTEGER FK         | Player reference               |
| start_date        | DATE               | Contract start date            |
| end_date          | DATE               | Contract expiry date           |
| contract_type     | VARCHAR(20)        | Professional / Youth / Loan    |
| loan_from         | VARCHAR(100)       | Parent club if player is loaned|
| salary_per_week   | INTEGER            | Weekly salary, if available    |
| release_clause    | INTEGER            | Release clause, if available   |

# 7. Injuries Table

## Purpose

Stores player injury history.

## Structure

| Column | Type | Description |
|---|---|---|
| injury_id | SERIAL PRIMARY KEY | Unique injury identifier |
| player_id | INTEGER FK | Player reference |
| injury_type | VARCHAR(100) | Injury description |
| body_part | VARCHAR(50) | Affected area |
| start_date | DATE | Injury start |
| end_date | DATE | Recovery date |
| days_missed | INTEGER | Days unavailable |

---

# 8. Scouting Reports Table

## Purpose

Stores scouting analysis about players.

## Structure

| Column | Type | Description |
|---|---|---|
| report_id | SERIAL PRIMARY KEY | Unique report identifier |
| player_id | INTEGER FK | Player reference |
| scout_name | VARCHAR(100) | Scout name |
| rating | INTEGER | Player rating |
| strengths | TEXT | Strengths |
| weaknesses | TEXT | Weaknesses |
| potential | INTEGER | Potential score |
| notes | TEXT | Additional comments |

---

# 9. Positions Table

## Purpose

Stores available football positions.

## Structure

| Column | Type | Description |
|---|---|---|
| position_id | SERIAL PRIMARY KEY | Unique identifier |
| name | VARCHAR(20) | Position name |

Examples:

- CM
- CDM
- CAM
- RW
- ST

---

# 10. Player Positions Table

## Purpose

Creates a many-to-many relationship between players and positions.

## Structure

| Column | Type | Description |
|---|---|---|
| player_position_id | SERIAL PRIMARY KEY | Unique identifier |
| player_id | INTEGER FK | Player reference |
| position_id | INTEGER FK | Position reference |
| is_primary | BOOLEAN | Main position |

---

# Future Tables

Possible future additions:

- Transfers
- Agents
- Stadiums
- Club History
- Player Development Timeline
- Betting Analysis
- AI Recommendations
