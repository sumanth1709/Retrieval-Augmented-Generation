import subprocess
import sys
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


def run_step(script_name):
    script_path = os.path.join(
        BASE_DIR,
        "ingestion",
        script_name
    )

    print()
    print("=" * 50)
    print("Running:", script_name)
    print("=" * 50)

    result = subprocess.run(
        [sys.executable, script_path]
    )

    if result.returncode != 0:
        print()
        print("ERROR:", script_name, "failed.")
        sys.exit(1)

    print()
    print("Completed:", script_name)


def main():

    print("=" * 50)
    print("       RAG INGESTION PIPELINE")
    print("=" * 50)

    run_step("ingest.py")

    run_step("chunk.py")

    run_step("embedding.py")

    run_step("vector_db.py")

    print()
    print("=" * 50)
    print("INGESTION PIPELINE COMPLETED")
    print("=" * 50)


if __name__ == "__main__":
    main()