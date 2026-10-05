import argparse
import csv

from fitness_app.csv_loader import load_participants, load_sessions
from fitness_app.reports import (
    write_analysis_summary,
    write_analysis_report,
    write_rejected_records
)
from fitness_app.validation import (
    InvalidIdentifierError,
    InvalidRecordError
)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Smart Fitness Session Analyzer"
    )

    parser.add_argument(
        "--profiles",
        default="data/participants.csv",
        help="Path to participant profile CSV file"
    )

    parser.add_argument(
        "--sessions",
        default="data/fitness_sessions.csv",
        help="Path to valid fitness session CSV file"
    )

    parser.add_argument(
        "--invalid-sessions",
        default="data/fitness_sessions_invalid.csv",
        help="Path to intentionally invalid fitness session CSV file"
    )

    parser.add_argument(
        "--output",
        default="output",
        help="Directory where reports will be saved"
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    try:
        participants = load_participants(args.profiles)

        valid_sessions, valid_rejected = load_sessions(
            args.sessions,
            participants
        )

        invalid_sessions, invalid_rejected = load_sessions(
            args.invalid_sessions,
            participants
        )

        all_sessions = valid_sessions.copy()

        for session_id, session in invalid_sessions.items():
            if session_id not in all_sessions:
                all_sessions[session_id] = session

        rejected_records = valid_rejected + invalid_rejected

        summary_file = write_analysis_summary(
            all_sessions,
            args.output
        )

        report_file = write_analysis_report(
            all_sessions,
            args.output
        )

        rejected_file = write_rejected_records(
            rejected_records,
            args.output
        )

        accepted_rows = 0

        for session in all_sessions.values():
            accepted_rows += len(session.observations)

        rejected_rows = set()

        for record in rejected_records:
            rejected_rows.add(
                (record["source"], record["row"])
            )

        print("Fitness analysis completed.")
        print(f"Accepted rows: {accepted_rows}")
        print(f"Rejected rows: {len(rejected_rows)}")
        print("Created report files:")
        print(f"- {summary_file}")
        print(f"- {report_file}")
        print(f"- {rejected_file}")

    except FileNotFoundError as error:
        print(f"File error: {error}")

    except PermissionError as error:
        print(f"Permission error: {error}")

    except InvalidIdentifierError as error:
        print(f"Identifier error: {error}")

    except InvalidRecordError as error:
        print(f"Record error: {error}")

    except csv.Error as error:
        print(f"CSV error: {error}")


if __name__ == "__main__":
    main()