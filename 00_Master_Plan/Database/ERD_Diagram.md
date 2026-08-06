# FootballPlatform Entity Relationship Diagram (ERD)

## Overview

This document describes the relationships between the main database entities of the FootballPlatform MVP.

The database is designed using a relational model where entities are connected through primary keys and foreign keys.

---

# Main Entities

## Players

Central entity of the platform.

A player can have:

- multiple statistics records;
- multiple contracts;
- multiple injuries;
- multiple scouting reports;
- multiple positions.

---

## Clubs

Stores football club information.

A club can contain multiple players.

---

## Competitions

Stores football competitions.

Examples:

- Premier League
- UEFA Champions League
- FIFA World Cup

A competition contains multiple matches.

---

# Entity Relationships

            COMPETITIONS
                  |
                  |
                  | 1:M
                  |
                MATCHES
                  
                  
                  
              CLUBS
                |
                |
                | 1:M
                |
              PLAYERS
                |
  --------------------------------
  |              |               |
  |              |               |
  ↓              ↓               ↓
                  |
                |
                ↓

         SCOUTING_REPORTS
         

---

# Relationship Details

## Club → Players

Relationship:

One-to-Many

Explanation:

One club can have many players, but one player belongs to one current club.

---

## Player → Statistics

Relationship:

One-to-Many

Explanation:

A player can have statistics for multiple seasons.

Example:

Player:

Jude Bellingham

Statistics:

- 2023/24
- 2024/25
- 2025/26

---

## Player → Contracts

Relationship:

One-to-Many

Explanation:

A player can sign multiple contracts during their career.

---

## Player → Injuries

Relationship:

One-to-Many

Explanation:

A player can have multiple injury records.

---

## Player → Scouting Reports

Relationship:

One-to-Many

Explanation:

Different scouts can create reports for the same player.

---

# Future Relationships

Possible future additions:

- Transfers
- Agents
- Stadiums
- Academies
- Player Events
- Club History
