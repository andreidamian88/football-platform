# GoalLens — HALF-TIME DNA Methodology


**Version:** 1.0
**Competition:** Premier League
**Season:** 2026/27
**Status:** Initial analytical prototype

## 1. Purpose

HALF-TIME DNA investigates how football teams perform between half-time and the final whistle.

The initial analysis focuses on:
- Protecting half-time leads.
- Losing a half-time lead.
- Recovering from a half-time deficit.
- Differences between home and away behaviour.

The objective is to identify measurable behavioural patterns, not simply rank teams by results.

## 2. Data requirements

A match is considered complete for this analysis when all four score values are available:

- Home half-time goals
- Away half-time goals
- Home full-time goals
- Away full-time goals

Matches with missing score information are excluded from the calculations.

## 3. Metric definitions

### Completed matches
Number of matches with complete half-time and full-time scores.

### Half-time leads
Number of matches in which a team was ahead at half-time.

### Leads protected
Number of half-time leads that resulted in a full-time victory.

### Leads drawn
Number of half-time leads that resulted in a full-time draw.

### Leads lost
Number of half-time leads that resulted in a full-time defeat.

### Points dropped
Points a team failed to collect after leading at half-time:

- Draw: 2 points dropped.
- Defeat: 3 points dropped.
- Victory: 0 points dropped.

### Comeback opportunities
Number of matches in which a team was losing at half-time.

### Comeback wins
Number of matches in which a team was losing at half-time but won at full-time.

### Avoided defeats
Number of matches in which a team was losing at half-time but finished with either a draw or a victory.

## 4. Percentage calculations

**Lead protection percentage**

Leads protected ÷ Half-time leads × 100

**Comeback win percentage**

Comeback wins ÷ Comeback opportunities × 100

**Avoided defeat percentage**

Avoided defeats ÷ Comeback opportunities × 100

If the denominator is zero, the percentage is NULL rather than zero.

This distinction prevents teams without opportunities from being incorrectly treated as having a 0% success rate.

## 5. Initial dataset validation

Current dataset results:

| Metric | Value |
|---|---:|
| Total fixtures | 380 |
| Completed matches | 45 |
| Team-match records | 90 |
| Half-time leads | 27 |
| Leads protected | 18 |
| Points dropped | 20 |
| Comeback wins | 2 |

The 90 team-match records represent two team perspectives for each of the 45 completed matches.

All five consistency checks between the team behaviour view and the previous analytical views passed.

## 6. Home and away analysis

Every completed match contributes:
- One home-team record.
- One away-team record.

This allows GoalLens to compare behavioural patterns at home and away independently.

The analysis currently includes 20 clubs and 40 club/venue combinations.

## 7. Limitations

- The current analysis uses a sample of only 45 completed matches.
- Some club percentages are based on only one or two opportunities.
- Small samples can produce misleadingly high or low percentages.
- Match-level scores cannot reveal detailed tactical behaviour, pressing intensity, possession or territory.
- The dataset has been checked against its OpenFootball source file, but this does not independently verify the real-world accuracy of every fixture or result.

These metrics should be treated as exploratory observations, not definitive descriptions of team identity.

## 8. Analytical principles

GoalLens will follow these principles:

1. Display sample sizes alongside percentages.
2. Never treat NULL as zero.
3. Avoid unsupported conclusions.
4. Keep metric definitions transparent.
5. Recalculate metrics from source data.
6. Separate measured facts from interpretation.
7. Validate data before publishing analysis.

## 9. Future development

Potential extensions include:
- Larger historical samples.
- Season-to-season comparisons.
- Home and away behavioural fingerprints.
- Second-half goal patterns.
- Event-level tactical analysis.
- Statistical confidence and sample-size indicators.

**GoalLens philosophy: Football is more than 90 minutes.**