import pytest
from src.connectors.file_system.parquet_reader import ParquetReader
from src.data_quality.data_quality_validation_library import DataQualityValidator

@pytest.mark.parquet_data
def test_case_to_validate_row_count_of_patient_sum_treatment_cost_per_facility_type(pg_conn):
    pq_path = "../PyTest DQ Framework/parquet_data/patient_sum_treatment_cost_per_facility_type"
    try:
        pq_df = ParquetReader.read_parquet(pq_path)
    except Exception as e:
        pytest.fail(f"Failed to read parquet file: {pq_path}. Error: {e}")

    query = """
        SELECT f.facility_type, CONCAT(p.first_name, ' ', p.last_name) as full_name, SUM(v.treatment_cost) as sum_treatment_cost_pg
        FROM visits v
        JOIN facilities f ON v.facility_id = f.id
        JOIN patients p ON v.patient_id = p.id
        GROUP BY f.facility_type, full_name
    """
    try:
        pg_df = pg_conn.fetch_query(query)
    except Exception as e:
        pytest.fail(f"Failed to execute Postgres query. Error: {e}")

    try:
        assert DataQualityValidator.validate_row_count(pg_df, pq_df), \
            f"Row count mismatch: Postgres={len(pg_df)}, Parquet={len(pq_df)}"
    except Exception as e:
        pytest.fail(f"Row count validation failed. Error: {e}")

@pytest.mark.parquet_data
def test_case_to_validate_matching_rows_data_of_patient_sum_treatment_cost_per_facility_type(pg_conn):
    pq_path = "../PyTest DQ Framework/parquet_data/patient_sum_treatment_cost_per_facility_type"
    try:
        pq_df = ParquetReader.read_parquet(pq_path)
        pq_df = pq_df[['facility_type', 'full_name', 'sum_treatment_cost']]
    except Exception as e:
        pytest.fail(f"Failed to read or process parquet file: {pq_path}. Error: {e}")

    query = """
        SELECT f.facility_type, CONCAT(p.first_name, ' ', p.last_name) as full_name, SUM(v.treatment_cost) as sum_treatment_cost_pg
        FROM visits v
        JOIN facilities f ON v.facility_id = f.id
        JOIN patients p ON v.patient_id = p.id
        GROUP BY f.facility_type, full_name
    """
    try:
        pg_df = pg_conn.fetch_query(query)
    except Exception as e:
        pytest.fail(f"Failed to execute Postgres query. Error: {e}")

    try:
        failed_rows = DataQualityValidator.validate_sum_treatment_cost(pg_df, pq_df)
        assert failed_rows.empty, f"Validation failed for rows:\n{failed_rows}"
    except Exception as e:
        pytest.fail(f"Sum treatment cost validation failed. Error: {e}")