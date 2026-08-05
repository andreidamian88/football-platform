# System Architecture

## Overview

Football Intelligence Platform will be developed as a modular application.

The initial goal is to create a scalable foundation for football scouting analytics.

## Main Components

### Frontend
Responsible for user interaction and visualisation.

Future technology:
- React / Next.js


### Backend

Responsible for:
- Business logic
- Data processing
- API communication

Technology:
- Python
- FastAPI


### Database

Responsible for storing:

- Players
- Clubs
- Scouting information
- Statistics

Technology:
- PostgreSQL


### Infrastructure

Deployment environment:

- Linux VPS
- Cloudflare
- HTTPS
- Firewall


## Initial Database Design

Entities:

Players

Clubs

Player Ratings

Scouting Notes

## Scout Radar v1 Decisions

Initial focus position:
- Central Midfielder (CM)

Primary scouting factors:
- Minutes played
- Market value
- Contract situation

Initial database focus:
- Players
- Clubs
- Player statistics
- Market information
- Scouting reports

The first MVP will focus on identifying young midfielders with high potential and good opportunity value.