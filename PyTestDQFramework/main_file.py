import os
import subprocess

def run_all_tests():
    try:
        test_dir = os.path.join("tests", "dqchecks", "parquet_files")
        report_dir = os.path.join("Test_Reports")
        os.makedirs(report_dir, exist_ok=True)
    except OSError as e:
        print(f"Error creating report directory: {e}")
        return

    report_path = os.path.join(report_dir, "report.html")

    try:
        result = subprocess.run([
            "pytest", test_dir,
            f"--html={report_path}",
            "--self-contained-html"
        ], check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Tests failed with error: {e}")
        print(e.output)
    except FileNotFoundError as e:
        print(f"Pytest not found: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    run_all_tests()