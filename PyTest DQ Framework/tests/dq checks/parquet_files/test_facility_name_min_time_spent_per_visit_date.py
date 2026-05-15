import pytest
from src.connectors.file_system.parquet_reader import ParquetReader
from src.data_quality.data_quality_validation_library import DataQualityValidator

@pytest.mark.parquet_data
def test_case_to_validate_row_count_of_facility_name_min_time_spent_per_visit_date(pg_conn):
    pq_path = "../PyTest DQ Framework/parquet_data/facility_name_min_time_spent_per_visit_date"
    try:
        pq_df = ParquetReader.read_parquet(pq_path)
    except Exception as e:
        pytest.fail(f"Failed to read Parquet file: {e}")

    query = """
        SELECT f.facility_name, DATE(v.visit_timestamp) as visit_date, MIN(v.duration_minutes) as min_time_spend
        FROM visits v
        JOIN facilities f ON v.facility_id = f.id
        GROUP BY f.facility_name, DATE(v.visit_timestamp)
    """
    try:
        pg_df = pg_conn.fetch_query(query)
    except Exception as e:
        pytest.fail(f"Failed to execute Postgres query: {e}")

    try:
        assert DataQualityValidator.validate_row_count(pg_df, pq_df), \
            f"Row count mismatch: Postgres={len(pg_df)}, Parquet={len(pq_df)}"
    except Exception as e:
        pytest.fail(f"Row count validation failed: {e}")

@pytest.mark.parquet_data
def test_case_to_validate_matching_rows_data_of_facility_name_min_time_spent_per_visit_date(pg_conn):
    pq_path = "../PyTest DQ Framework/parquet_data/facility_name_min_time_spent_per_visit_date"
    try:
        pq_df = ParquetReader.read_parquet(pq_path)
        pq_df = pq_df[['facility_name', 'visit_date', 'min_time_spent']]
    except Exception as e:
        pytest.fail(f"Failed to read or process Parquet file: {e}")

    query = """
        SELECT f.facility_name, DATE(v.visit_timestamp) as visit_date, MIN(v.duration_minutes) as min_time_spend
        FROM visits v
        JOIN facilities f ON v.facility_id = f.id
        GROUP BY f.facility_name, DATE(v.visit_timestamp)
    """
    try:
        pg_df = pg_conn.fetch_query(query)
    except Exception as e:
        pytest.fail(f"Failed to execute Postgres query: {e}")

    try:
        assert DataQualityValidator.validate_min_time_spent(pg_df, pq_df)
    except Exception as e:
        pytest.fail(f"Min time spent validation failed: {e}")
