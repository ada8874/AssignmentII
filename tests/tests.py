from fitness_app.reports import (
    analyze_session,
    write_rejected_records,
    write_analysis_summary,
    write_analysis_report
)

from fitness_app.csv_loader import load_participants, load_sessions

from fitness_app.validation import (
    validate_participant_id,
    validate_session_id,
    validate_observation,
    InvalidIdentifierError
)


def test_write_analysis_report():
    participants = load_participants("data/participants.csv")

    sessions, rejected_records = load_sessions(
        "data/fitness_sessions.csv",
        participants
    )

    file_path = write_analysis_report(
        sessions,
        "output"
    )

    assert file_path.exists()


def test_write_analysis_summary():
    participants = load_participants("data/participants.csv")

    sessions, rejected_records = load_sessions(
        "data/fitness_sessions.csv",
        participants
    )

    file_path = write_analysis_summary(
        sessions,
        "output"
    )

    assert file_path.exists()


def test_analyze_session():
    participants = load_participants("data/participants.csv")

    sessions, rejected_records = load_sessions(
        "data/fitness_sessions.csv",
        participants
    )

    session = sessions["FIT-2026-001"]
    result = analyze_session(session)

    assert result.classification is not None
    assert result.usable_observations == len(session.observations)
    assert result.average_heart_rate is not None


def test_load_sessions():
    participants = load_participants("data/participants.csv")

    sessions, rejected_records = load_sessions(
        "data/fitness_sessions.csv",
        participants
    )

    assert len(sessions) > 0

    for session in sessions.values():
        assert session.session_id is not None


def test_load_participants():
    participants = load_participants("data/participants.csv")

    assert "P001" in participants
    assert "P002" in participants
    assert "P003" in participants

    participant = participants["P001"]

    assert participant.name == "Amina Noor"
    assert participant.baseline_heart_rate == 68

    assert isinstance(participant.baseline_heart_rate, int)
    assert isinstance(participant.baseline_skin_response, float)
    assert isinstance(participant.baseline_temperature, float)


def test_valid_participant_id():
    assert validate_participant_id("P001") is True


def test_valid_session_id():
    assert validate_session_id("FIT-2026-001") is True


def test_invalid_participant_id():
    try:
        validate_participant_id("001")
        assert False

    except InvalidIdentifierError as error:
        assert "Invalid participant ID" in str(error)


def test_observation_boundaries():
    valid_low = {
        "timestamp": 0,
        "heart_rate": 35,
        "skin_response": 0.0,
        "temperature": 25.0,
        "activity_level": 0.0,
        "signal_quality": 0.60
    }

    valid_high = {
        "timestamp": 1,
        "heart_rate": 205,
        "skin_response": 1.0,
        "temperature": 42.0,
        "activity_level": 1.0,
        "signal_quality": 1.0
    }

    assert validate_observation(valid_low) == []
    assert validate_observation(valid_high) == []


def test_invalid_session_id():
    try:
        validate_session_id("FIT-26-001")
        assert False

    except InvalidIdentifierError as error:
        assert "Invalid session ID" in str(error)


def test_invalid_session_file():
    participants = load_participants("data/participants.csv")

    sessions, rejected_records = load_sessions(
        "data/fitness_sessions_invalid.csv",
        participants
    )

    # Program should continue even though the file contains bad rows
    assert isinstance(sessions, dict)

    # Invalid file should produce rejected records
    assert len(rejected_records) > 0

    # Each rejection should contain the required information
    for record in rejected_records:
        assert "source" in record
        assert "row" in record
        assert "field" in record
        assert "reason" in record

    fields = []

    for record in rejected_records:
        fields.append(record["field"])

    # Make sure identifier problems were detected
    assert "participant_id" in fields or "session_id" in fields


def test_missing_file():
    try:
        load_participants("data/file_that_does_not_exist.csv")
        assert False

    except FileNotFoundError as error:
        assert "Participant file not found" in str(error)


def test_write_rejected_records():
    participants = load_participants("data/participants.csv")

    sessions, rejected_records = load_sessions(
        "data/fitness_sessions_invalid.csv",
        participants
    )

    file_path = write_rejected_records(
        rejected_records,
        "output"
    )

    assert file_path.exists()


def test_invalid_observation_boundaries():
    invalid = {
        "timestamp": -1,
        "heart_rate": 206,
        "skin_response": -0.1,
        "temperature": 43.0,
        "activity_level": 1.01,
        "signal_quality": 0.59
    }

    errors = validate_observation(invalid)

    assert len(errors) > 0

    fields = []

    for error in errors:
        fields.append(error["field"])

    assert "timestamp" in fields
    assert "heart_rate" in fields
    assert "skin_response" in fields
    assert "temperature" in fields
    assert "activity_level" in fields
    assert "signal_quality" in fields


test_valid_participant_id()
test_valid_session_id()
test_invalid_participant_id()
test_invalid_session_id()
test_load_participants()
test_load_sessions()
test_invalid_session_file()
test_missing_file()
test_analyze_session()
test_write_rejected_records()
test_write_analysis_summary()
test_write_analysis_report()
test_observation_boundaries()
test_invalid_observation_boundaries()

print("All tests passed")