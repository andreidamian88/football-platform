
# HALF-TIME DNA — Automated Testing

## 1. Purpose

This document describes the automated tests developed for the HALF-TIME DNA analysis functions.

The objective is to verify that the Python calculations produce the expected results and handle edge cases safely.

## 2. Testing Framework

GoalLens uses Python's built-in `unittest` framework.

The tests are located in:

`08_Tests/test_club_behaviour_fingerprint.py`

The tests import and verify the actual calculation functions from:

`06_Scripts/club_behaviour_fingerprint.py`

## 3. Functions Tested

### Lead Protection

Tests the percentage of half-time leads successfully converted into full-time wins.

### Comeback Win Rate

Tests the percentage of comeback opportunities that result in a full-time win.

## 4. Test Scenarios

| Test scenario | Expected result |
|---|---|
| 3 protected leads from 4 opportunities | 75.00% |
| Zero lead opportunities | None |
| 2 comeback wins from 4 opportunities | 50.00% |
| Zero comeback opportunities | None |
| 2 protected leads from 3 opportunities | 66.67% |
| Zero successful leads from 10 opportunities | 0.00% |

## 5. Running the Tests

From the project root, execute:

```powershell
python -m unittest discover -s 08_Tests -v
```

The `-v` option displays the individual test names and results.

## 6. Initial Test Results

- Total tests: 6
- Passed: 6
- Failed: 0

All six tests passed successfully.

## 7. Important Testing Principles

- Zero opportunities must return `None`.
- Zero successful outcomes with valid opportunities must return `0.00%`.
- Percentage calculations must use the expected rounding.
- Tests verify calculation behaviour, not the accuracy of the underlying football dataset.

## 8. Future Improvements

- Add tests for additional edge cases.
- Expand testing to other HALF-TIME DNA calculations.
- Introduce tests for database data validation.
- Measure automated test coverage as the project grows.
