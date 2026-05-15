import pandas as pd
import os
import pytest

class ParquetReader:
    @staticmethod
    def read_parquet(file_path):
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Parquet file not found: {file_path}")
            return pd.read_parquet(file_path)
        except FileNotFoundError as fnf_error:
            print(f"Error: {fnf_error}")
        except pd.errors.EmptyDataError as ede:
            print(f"Error: Parquet file is empty or corrupt: {ede}")
        except Exception as e:
            print(f"An unexpected error occurred while reading the parquet file: {e}")
