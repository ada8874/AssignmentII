# Smart Fitness Session Analyzer

**Selected option:** Option A  
**Student:** Ada Hashemi, 8874

## Description

This project is a continuation of Assignment I.

The Smart Fitness Session Analyzer reads simulated participant and fitness-session data from CSV files. The program validates the data, converts values to suitable Python types, groups observations into workout sessions, connects each session to an existing participant and analyzes the session.

The analysis compares measurements with the participant's personal reference values and classifies the session as:

- resting
- moderate activity
- high activity
- recovering
- insufficient data

The program also handles invalid data by rejecting problematic rows and continuing with the remaining data when possible.

## Modules

- `models.py` contains the main classes and fitness-analysis logic.
- `validation.py` contains identifier validation, sensor validation and custom exceptions.
- `csv_loader.py` reads and validates CSV data and creates the program objects.
- `reports.py` analyzes workout sessions and creates output files.
- `main.py` connects the different parts of the program and handles command-line arguments.
- `tests.py` contains tests for valid, invalid, missing-file and boundary cases.

## Main Classes

### Participant

Represents a participant and stores:

- participant ID
- name
- baseline heart rate
- baseline skin response
- baseline temperature

### Observation

Represents one fitness observation containing:

- timestamp
- heart rate
- skin response
- temperature
- activity level
- signal quality

### WorkoutSession

Represents a workout session containing a participant and multiple observations.

The class calculates statistics such as average, minimum and maximum heart rate, average activity level, skin response and temperature. It also compares measurements with the participant's reference values and determines the session classification.

Recovery is detected by checking whether heart rate and activity level decrease near the end of the session.

### AnalysisResult

Stores the structured result produced after analyzing a workout session. The result can also be returned as a dictionary using `to_dict()`.

## Object-Oriented Design

The program uses composition because a `WorkoutSession` contains a `Participant` and multiple `Observation` objects.

Encapsulation is demonstrated through the protected-style `_observation_list` attribute in `WorkoutSession`. Observations are added through `add_observation()` and accessed through the `observations` property.

The program also uses class methods such as:

```python
Participant.from_dict()
Observation.from_dict()
```

Inheritance is not used because there is no natural inheritance relationship between the main classes. Composition provides a clearer representation of the fitness-session structure.

## Validation

Participant IDs must follow the format:

```text
PXXX
```

Example:

```text
P001
```

Fitness session IDs must follow the format:

```text
FIT-YYYY-NNN
```

Example:

```text
FIT-2026-001
```

The program also validates:

- timestamp
- heart rate
- skin response
- temperature
- activity level
- signal quality

The following rules are used:

- timestamp must be non-negative
- heart rate must be between 35 and 205 bpm
- skin response cannot be negative
- temperature must be between 25 and 42 degrees Celsius
- activity level must be between 0 and 1
- signal quality must be between 0 and 1
- signal quality below 0.60 is treated as poor-quality data

Rejected records include the source file, row number, field and reason for rejection.

## Error Handling

The program uses two custom exception classes:

```python
InvalidIdentifierError
InvalidRecordError
```

Targeted error handling is also used for errors such as:

- `FileNotFoundError`
- `PermissionError`
- `ValueError`
- `KeyError`
- CSV-related errors

Recoverable row errors are recorded and the program continues with the next row when possible.

## Output

The program creates three output files:

```text
analysis_summary.csv
analysis_report.txt
rejected_records.txt
```

`analysis_summary.csv` contains one row for each processed workout session.

`analysis_report.txt` contains a readable explanation of each analysis result.

`rejected_records.txt` contains information about rejected CSV rows and explains why they were rejected.

## Running the Program

Run the program from the repository root:

```bash
python3 main.py
```

The program uses the following files by default:

```text
data/participants.csv
data/fitness_sessions.csv
data/fitness_sessions_invalid.csv
```

The full command can also be used:

```bash
python3 main.py --profiles data/participants.csv --sessions data/fitness_sessions.csv --invalid-sessions data/fitness_sessions_invalid.csv --output output
```

The program prints a short completion summary showing the number of accepted and rejected rows and the report files that were created.

Example:

```text
Fitness analysis completed.
Accepted rows: 25
Rejected rows: 15
Created report files:
- output\analysis_summary.csv
- output\analysis_report.txt
- output\rejected_records.txt
```

## Running the Tests

Run the tests from the repository root:

python3 -m tests.tests

Expected result:

All tests passed

The tests cover:

- valid and invalid participant IDs
- valid and invalid session IDs
- participant loading
- session loading
- invalid CSV records
- missing files
- workout-session analysis
- report generation
- valid boundary values
- invalid boundary values

## Requirements

The project uses only the Python standard library.

No third-party packages are required.

## Limitations

- The supplied fitness data are simulated.
- The classification thresholds are manually defined.
- The program is not intended for medical use.
- Recovery detection compares measurements near the beginning and end of a session.
- Signal quality below 0.60 is rejected according to the chosen data-quality rule.
- The analysis is rule-based and does not use machine learning.
