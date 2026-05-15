import pytest
from src.connectors.file_system.parquet_reader import ParquetReader
from src.data_quality.data_quality_validation_library import DataQualityValidator

@pytest.mark.parquet_data
def test_case_to_validate_row_count_of_facility_type_avg_time_spent_per_visit_date(pg_conn):
    pq_path = "../PyTest DQ Framework/parquet_data/facility_type_avg_time_spent_per_visit_date"
    try:
        pq_df = ParquetReader.read_parquet(pq_path)
    except Exception as e:
        pytest.fail(f"Failed to read parquet file at {pq_path}: {e}")

    query = """
        SELECT f.facility_type, DATE(v.visit_timestamp) as visit_date, Round(AVG(v.duration_minutes),2) as avg_time_spent_pg
        FROM visits v
        JOIN facilities f ON v.facility_id = f.id
        GROUP BY f.facility_type, DATE(v.visit_timestamp)
    """
    try:
        pg_df = pg_conn.fetch_query(query)
    except Exception as e:
        pytest.fail(f"Failed to execute query on Postgres: {e}")

    try:
        assert DataQualityValidator.validate_row_count(pg_df, pq_df), \
            f"Row count mismatch: Postgres={len(pg_df)}, Parquet={len(pq_df)}"
    except AssertionError as e:
        pytest.fail(str(e))
    except Exception as e:
        pytest.fail(f"Error during row count validation: {e}")

@pytest.mark.parquet_data
def test_case_to_validate_matching_rows_data_of_facility_type_avg_time_spent_per_visit(pg_conn):
    pq_path = "../PyTest DQ Framework/parquet_data/facility_type_avg_time_spent_per_visit_date"
    try:
        pq_df = ParquetReader.read_parquet(pq_path)
        pq_df = pq_df[['facility_type', 'visit_date', 'avg_time_spent']]
    except Exception as e:
        pytest.fail(f"Failed to read or process parquet file at {pq_path}: {e}")

    query = """
        SELECT f.facility_type, DATE(v.visit_timestamp) as visit_date, Round(AVG(v.duration_minutes),2) as avg_time_spent_pg
        FROM visits v
        JOIN facilities f ON v.facility_id = f.id
        GROUP BY f.facility_type, DATE(v.visit_timestamp)
    """
    try:
        pg_df = pg_conn.fetch_query(query)
    except Exception as e:
        pytest.fail(f"Failed to execute query on Postgres: {e}")

    try:
        assert DataQualityValidator.validate_avg_time_spent(pg_df, pq_df)
    except AssertionError as e:
        pytest.fail(str(e))
    except Exception as e:
        pytest.fail(f"Error during average time spent validation: {e}")