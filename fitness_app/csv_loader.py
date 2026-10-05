import csv

from fitness_app.models import Participant, Observation, WorkoutSession
from fitness_app.validation import (
    validate_participant_id,
    validate_session_id,
    validate_observation,
    InvalidRecordError,
    InvalidIdentifierError
)


def load_participants(file_path):
    participants = {}

    try:
        with open(file_path, encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                try:
                    participant_id = row["participant_id"]

                    validate_participant_id(participant_id)

                    participant_data = {
                        "participant_id": participant_id,
                        "name": row["name"],
                        "baseline_heart_rate": int(row["baseline_heart_rate"]),
                        "baseline_temperature": float(row["baseline_temperature"]),
                        "baseline_skin_response": float(row["baseline_skin_response"])
                    }

                    participant = Participant.from_dict(participant_data)
                    participants[participant_id] = participant


                except KeyError as error:
                    raise InvalidRecordError(
                        f"Missing participant field '{error.args[0]}' "
                        f"in row {reader.line_num}"
                    ) from error

                except InvalidIdentifierError as error:
                    raise InvalidIdentifierError(
                        f"Invalid participant identifier in row {reader.line_num}: {error}"
                    ) from error
                
                except ValueError as error:
                    raise InvalidRecordError(
                        f"Invalid participant data in row {reader.line_num}: {error}"
                    ) from error

    except FileNotFoundError as error:
        raise FileNotFoundError(
            f"Participant file not found: {file_path}"
        ) from error

    except PermissionError as error:
        raise PermissionError(
            f"Permission denied when reading participant file: {file_path}"
        ) from error

    except csv.Error as error:
        raise csv.Error(
            f"Could not read participant CSV file {file_path}: {error}"
        ) from error

    return participants


def load_sessions(file_path, participants):
    sessions = {}
    rejected_records = []

    required_fields = [
        "session_id",
        "participant_id",
        "timestamp",
        "heart_rate",
        "skin_response",
        "temperature",
        "activity_level",
        "signal_quality"
    ]

    with open(file_path, encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:

            # Check for an unexpected number of columns
            if None in row or any(row.get(field) is None for field in required_fields):
                rejected_records.append({
                    "source": file_path,
                    "row": reader.line_num,
                    "field": "row",
                    "reason": "Unexpected number of columns"
                })
                continue

            # Check for empty required fields
            missing_fields = [
                field for field in required_fields
                if row[field].strip() == ""
            ]

            if missing_fields:
                for field in missing_fields:
                    rejected_records.append({
                        "source": file_path,
                        "row": reader.line_num,
                        "field": field,
                        "reason": "Missing required value"
                    })

                continue

            session_id = row["session_id"]
            participant_id = row["participant_id"]

            # Validate session ID
            try:
                validate_session_id(session_id)

            except InvalidIdentifierError as error:
                rejected_records.append({
                    "source": file_path,
                    "row": reader.line_num,
                    "field": "session_id",
                    "reason": str(error)
                })
                continue

            # Validate participant ID
            try:
                validate_participant_id(participant_id)

            except InvalidIdentifierError as error:
                rejected_records.append({
                    "source": file_path,
                    "row": reader.line_num,
                    "field": "participant_id",
                    "reason": str(error)
                })
                continue

            # Check that the participant actually exists
            try:
                if participant_id not in participants:
                    raise InvalidRecordError(
                        f"Unknown participant ID: {participant_id}"
                    )

            except InvalidRecordError as error:
                rejected_records.append({
                    "source": file_path,
                    "row": reader.line_num,
                    "field": "participant_id",
                    "reason": str(error)
                })
                continue

            # Create the session if this is the first row for it
            if session_id not in sessions:
                participant = participants[participant_id]

                sessions[session_id] = WorkoutSession(
                    session_id,
                    participant
                )

            # Convert CSV strings into numbers
            converters = {
                "timestamp": int,
                "heart_rate": int,
                "skin_response": float,
                "temperature": float,
                "activity_level": float,
                "signal_quality": float
            }

            observation_data = {}
            conversion_failed = False

            for field, converter in converters.items():
                try:
                    observation_data[field] = converter(row[field])

                except ValueError:
                    rejected_records.append({
                        "source": file_path,
                        "row": reader.line_num,
                        "field": field,
                        "reason": f"Invalid numerical value: {row[field]}"
                    })

                    conversion_failed = True
                    break

            if conversion_failed:
                continue

            # Validate numerical ranges and signal quality
            errors = validate_observation(observation_data)

            if errors:
                for error in errors:
                    rejected_records.append({
                        "source": file_path,
                        "row": reader.line_num,
                        "field": error["field"],
                        "reason": error["reason"]
                    })

                continue

            # Only valid observations reach this point
            observation = Observation.from_dict(observation_data)
            sessions[session_id].add_observation(observation)

    return sessions, rejected_records