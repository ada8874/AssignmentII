from fitness_app.models import AnalysisResult
from pathlib import Path
import csv

def analyze_session(session):
    usable_observations = len(session.observations)

    result = AnalysisResult(
        average_heart_rate=session.average_heart_rate(),
        minimum_heart_rate=session.minimum_heart_rate(),
        maximum_heart_rate=session.maximum_heart_rate(),
        average_activity_level=session.average_activity_level(),
        heart_rate_difference=session.heart_rate_difference(),
        total_observations=usable_observations,
        usable_observations=usable_observations,
        rejected_observations=0,
        average_skin_response=session.average_skin_response(),
        skin_response_difference=session.skin_response_difference(),
        average_temperature=session.average_temperature(),
        temperature_difference=session.temperature_difference(),
        classification=session.classify_intensity(),
        explanation=session.classification_explanation()
    )



    return result

def write_rejected_records(rejected_records, output_dir):
    output_path = Path(output_dir)

    # Create the output folder if it does not already exist
    output_path.mkdir(parents=True, exist_ok=True)

    file_path = output_path / "rejected_records.txt"

    with open(file_path, "w", encoding="utf-8") as file:
        if len(rejected_records) == 0:
            file.write("No rejected records.\n")

        else:
            for record in rejected_records:
                file.write(
                    f"Source: {record['source']}, "
                    f"Row: {record['row']}, "
                    f"Field: {record['field']}, "
                    f"Reason: {record['reason']}\n"
                )

    return file_path

def write_analysis_summary(sessions, output_dir):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    file_path = output_path / "analysis_summary.csv"

    fieldnames = [
        "session_id",
        "participant_id",
        "participant_name",
        "usable_observations",
        "average_heart_rate",
        "minimum_heart_rate",
        "maximum_heart_rate",
        "average_activity_level",
        "heart_rate_difference",
        "classification",
        "explanation"
    ]

    with open(file_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for session_id, session in sessions.items():
            result = analyze_session(session)

            writer.writerow({
                "session_id": session_id,
                "participant_id": session.participant.participant_id,
                "participant_name": session.participant.name,
                "usable_observations": result.usable_observations,
                "average_heart_rate": result.average_heart_rate,
                "minimum_heart_rate": result.minimum_heart_rate,
                "maximum_heart_rate": result.maximum_heart_rate,
                "average_activity_level": result.average_activity_level,
                "heart_rate_difference": result.heart_rate_difference,
                "classification": result.classification,
                "explanation": result.explanation
            })

    return file_path

def write_analysis_report(sessions, output_dir):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    file_path = output_path / "analysis_report.txt"

    with open(file_path, "w", encoding="utf-8") as file:
        for session_id, session in sessions.items():
            result = analyze_session(session)

            file.write(f"Session: {session_id}\n")
            file.write(
                f"Participant: {session.participant.name} "
                f"({session.participant.participant_id})\n"
            )
            file.write(
                f"Usable observations: {result.usable_observations}\n"
            )
            file.write(
                f"Classification: {result.classification}\n"
            )
            file.write(
                f"Explanation: {result.explanation}\n"
            )

            file.write(
                f"Average heart rate: {result.average_heart_rate}\n"
            )
            file.write(
                f"Minimum heart rate: {result.minimum_heart_rate}\n"
            )
            file.write(
                f"Maximum heart rate: {result.maximum_heart_rate}\n"
            )
            file.write(
                f"Average activity level: {result.average_activity_level}\n"
            )

            file.write("\n")

    return file_path