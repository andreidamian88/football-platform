
# HALF-TIME DNA — Research Findings

## 1. Research Objectives

### 1.1 Purpose

The purpose of this research is to investigate football team behaviour around half-time using match-level data.

The research focuses on understanding how teams perform after leading or trailing at half-time and identifying potential behavioural patterns.

### 1.2 Research Questions

This research investigates four main questions:

1. How frequently do teams protect a half-time lead?
2. How frequently do teams lose points after leading at half-time?
3. Which teams win after trailing at half-time?
4. Which teams avoid defeat after trailing at half-time?

### 1.3 Analytical Dimensions

The research is organised into four dimensions:

- Lead Protection
- Lead Vulnerability
- Comeback Ability
- Resilience

These dimensions provide different perspectives on match outcomes following the half-time score.


## 2. Dataset Overview

### 2.1 Competition

- Competition: Premier League
- Season: 2026/27
- Total fixtures: 380
- Completed matches with both half-time and full-time scores: 45

### 2.2 Data Completeness

Out of the 380 fixtures:

- 45 matches contain both half-time and full-time scores.
- 5 matches contain full-time scores only.
- 330 matches have no recorded scores.

Only matches with both half-time and full-time scores are included in the HALF-TIME DNA calculations.

### 2.3 Data Source

The initial fixture dataset was obtained from OpenFootball:

https://github.com/openfootball/football.json/blob/master/2026-27/en.1.json

The local JSON file is stored at:

`05_Data/openfootball/premier_league_2026_27.json`

The file was checked against the corresponding remote source using SHA256 hashing. The hashes matched at the time of verification.

This confirms that the local file was an exact copy of the remote file at that time. It does not independently verify the accuracy of the football results.

### 2.4 Data Limitations

The research currently uses a relatively small sample of 45 completed matches.

The available dataset provides:

- Half-time scores.
- Full-time scores.
- Home and away teams.
- Match-level outcomes.

It does not provide detailed event or tracking information such as:

- Possession.
- Shots and expected goals.
- Pressing intensity.
- Passing networks.
- Player movement.
- Tactical formations.

Consequently, the current research focuses on match outcomes and score-based behaviour rather than detailed tactical analysis.

## 3. Competition-Level Findings

### 3.1 Half-Time Situations

The 45 completed matches produced the following half-time situations:

| Half-time situation | Matches |
|---|---:|
| Home team leading | 15 |
| Away team leading | 12 |
| Level at half-time | 18 |
| Total | 45 |

### 3.2 Lead Protection

There were 27 recorded half-time lead opportunities.

| Outcome | Matches |
|---|---:|
| Leads protected | 18 |
| Leads ending in a draw | 7 |
| Leads ending in defeat | 2 |
| Total | 27 |

The overall lead protection rate was 66.67%.

### 3.3 Lead Vulnerability

Nine of the 27 half-time leads were not converted into full-time victories.

These consisted of:

- 7 matches ending in a draw.
- 2 matches ending in defeat.

The total points dropped by teams leading at half-time were 20.

Points dropped are calculated as:

- 2 points for a draw.
- 3 points for a defeat.

### 3.4 Comeback and Resilience Findings

There were 27 recorded opportunities where a team was losing at half-time.

| Outcome | Matches |
|---|---:|
| Comeback wins | 2 |
| Avoided defeats | 9 |
| Total opportunities | 27 |

The overall comeback win rate was 7.41%.

The overall avoided defeat rate was 33.33%.

Avoided defeats include both draws and comeback wins.


## 4. Individual Club Observations

### 4.1 Lead Protection

Several clubs recorded perfect lead-protection rates in the available sample.

Examples include:

| Club | Protected leads | Opportunities | Rate |
|---|---:|---:|---:|
| Brighton | 3 | 3 | 100% |
| Manchester City | 3 | 3 | 100% |
| Chelsea | 2 | 2 | 100% |
| Everton | 2 | 2 | 100% |
| Bournemouth | 0 | 3 | 0% |

These results describe the available matches only. The small number of opportunities does not support conclusions about long-term team behaviour.

### 4.2 Lead Vulnerability

AFC Bournemouth recorded:

- 3 half-time lead opportunities.
- 0 protected leads.
- 2 matches ending in draws.
- 1 match ending in defeat.
- 7 points dropped.

Fulham recorded one half-time lead opportunity, which ended in defeat.

These observations identify clubs for further investigation but should not be interpreted as established performance characteristics.

### 4.3 Comeback Ability and Resilience

The following observations emerged from the comeback analysis:

**Crystal Palace**
- 4 comeback opportunities.
- 1 comeback win.
- 1 avoided defeat.
- Comeback win rate: 25%.
- Avoided defeat rate: 25%.

**Manchester City**
- 1 comeback opportunity.
- 1 comeback win.
- Avoided defeat rate: 100%.

**Liverpool**
- 2 comeback opportunities.
- 0 comeback wins.
- 2 avoided defeats.
- Avoided defeat rate: 100%.

These examples demonstrate the difference between winning after trailing at half-time and simply avoiding defeat.

### 4.4 Interpretation

The current results suggest that lead protection, comeback ability and resilience should be analysed as separate behavioural dimensions.

However, these are preliminary observations based on a limited dataset. Further completed matches are required before identifying stable team patterns.


## 5. Research Limitations and Reliability

### 5.1 Sample Size

The current analysis includes 45 completed matches.

Although the competition contains 380 scheduled fixtures, only 45 currently have both half-time and full-time scores recorded in the dataset.

The number of opportunities for individual clubs is also limited. Some clubs have no recorded comeback opportunities, while others have only one to four.

Consequently, percentages can change significantly when additional matches are included.

### 5.2 Data Quality and Verification

The local fixture file was compared with the corresponding OpenFootball source using SHA256 hashing.

The matching hashes confirm that the local file was an exact copy of the remote file at the time of verification.

However, this does not independently confirm that every fixture or result is factually accurate.

Further verification against reliable football results sources is required before publishing definitive findings.

### 5.3 Analytical Limitations

The current analysis uses half-time and full-time scorelines.

It cannot explain why a team protected a lead, lost a lead or recovered from a losing position.

For example, the current dataset cannot establish whether a result was influenced by:

- Tactical substitutions.
- Possession and territorial control.
- Pressing intensity.
- Shot quality and expected goals.
- Player performance or injuries.
- Changes in formation.

### 5.4 Interpretation of Results

All percentages and club observations should be treated as exploratory findings.

A high percentage based on one or two opportunities does not provide strong evidence of consistent behaviour.

The research therefore avoids definitive club rankings and conclusions about long-term performance.


## 6. Conclusions and Future Research

### 6.1 Research Conclusions

The initial HALF-TIME DNA analysis demonstrates how half-time and full-time scores can be used to investigate different aspects of football team behaviour.

The competition-level findings show that:

- 18 of 27 half-time leads were protected (66.67%).
- 9 of 27 leads were not converted into victories (33.33%).
- Teams leading at half-time dropped 20 points.
- There were 2 comeback wins from 27 comeback opportunities (7.41%).
- Teams avoided defeat in 9 of 27 comeback opportunities (33.33%).

These findings provide an initial statistical foundation for the HALF-TIME DNA concept.

However, the limited sample size means that the results should be treated as preliminary rather than definitive.

### 6.2 Future Research

The next development stages should focus on:

1. Expanding the dataset with additional completed matches.
2. Verifying match results against reliable football data sources.
3. Comparing team behaviour across multiple seasons.
4. Investigating home and away differences.
5. Analysing first-half and second-half scoring patterns.
6. Exploring event-level data to investigate tactical behaviour.

### 6.3 Future GoalLens Development

The longer-term objective is to develop HALF-TIME DNA into a football intelligence feature.

Future versions could combine match outcomes with additional information such as possession, shots, expected goals, substitutions and tactical events.

This would allow GoalLens to move beyond describing what happened and begin investigating how and why teams behave differently during matches.

### 6.4 Final Research Statement

HALF-TIME DNA is an exploratory football behaviour research project.

Its purpose is not simply to report match statistics, but to identify measurable patterns, test assumptions and develop evidence-based insights into football.
