import re


# Raised when an identifier does not follow the required format
class InvalidIdentifierError(ValueError):
    pass


# Raised when a CSV record contains invalid data
class InvalidRecordError(ValueError):
    pass


# Checks if the participant ID has the right format PXXX
def validate_participant_id(participant_id):
    pattern = r"^P\d{3}$"

    if re.fullmatch(pattern, participant_id) is None:
        raise InvalidIdentifierError(
            f"Invalid participant ID: {participant_id}"
        )

    return True


# Looks for the format "FIT-YYYY-NNN"
def validate_session_id(session_id):
    pattern = r"^FIT-\d{4}-\d{3}$"

    if re.fullmatch(pattern, session_id) is None:
        raise InvalidIdentifierError(
            f"Invalid session ID: {session_id}"
        )

    return True


# Checks if an observation contains valid sensor values
def validate_observation(data):
    errors = []

    # Check timestamp
    if data["timestamp"] is None or data["timestamp"] < 0:
        errors.append({
            "field": "timestamp",
            "reason": "Invalid timestamp"
        })

    # Check heart rate
    if data["heart_rate"] is None:
        errors.append({
            "field": "heart_rate",
            "reason": "Heart rate is missing"
        })
    elif data["heart_rate"] < 35 or data["heart_rate"] > 205:
        errors.append({
            "field": "heart_rate",
            "reason": "Heart rate is outside the valid range"
        })

    # Check skin response
    if data["skin_response"] is None:
        errors.append({
            "field": "skin_response",
            "reason": "Skin response is missing"
        })
    elif data["skin_response"] < 0:
        errors.append({
            "field": "skin_response",
            "reason": "Skin response can't be negative"
        })

    # Check temperature
    if data["temperature"] is None:
        errors.append({
            "field": "temperature",
            "reason": "Temperature is missing"
        })
    elif data["temperature"] < 25 or data["temperature"] > 42:
        errors.append({
            "field": "temperature",
            "reason": "Temperature is outside the valid range"
        })

    # Check activity level
    if data["activity_level"] is None:
        errors.append({
            "field": "activity_level",
            "reason": "Activity level is missing"
        })
    elif data["activity_level"] < 0 or data["activity_level"] > 1:
        errors.append({
            "field": "activity_level",
            "reason": "Activity level must be between 0 and 1"
        })

    # Check signal quality
    if data["signal_quality"] is None:
        errors.append({
            "field": "signal_quality",
            "reason": "Signal quality is missing"
        })
    elif data["signal_quality"] < 0 or data["signal_quality"] > 1:
        errors.append({
            "field": "signal_quality",
            "reason": "Signal quality must be between 0 and 1"
        })
    elif data["signal_quality"] < 0.60:
        errors.append({
            "field": "signal_quality",
            "reason": "Signal quality is too low"
        })

    return errors