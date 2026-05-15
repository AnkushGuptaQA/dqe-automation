import pandas as pd

class DataQualityValidator:
    @staticmethod
    def validate_min_time_spent(pg_df, pq_df):
        try:
            pg_df = pg_df.copy()
            pq_df = pq_df.copy()
            pg_df['visit_date'] = pd.to_datetime(pg_df['visit_date'])
            pq_df['visit_date'] = pd.to_datetime(pq_df['visit_date'])
            merged = pd.merge(pg_df, pq_df, on=['facility_name', 'visit_date'], how='inner')
            return merged['min_time_spent'].equals(merged['min_time_spend'])
        except Exception as e:
            print(f"Error in validate_min_time_spent: {e}")
            return False

    @staticmethod
    def validate_avg_time_spent(pg_df, pq_df):
        try:
            pg_df = pg_df.copy()
            pq_df = pq_df.copy()
            pg_df['visit_date'] = pd.to_datetime(pg_df['visit_date'])
            pq_df['visit_date'] = pd.to_datetime(pq_df['visit_date'])
            merged = pd.merge(pg_df, pq_df, on=['facility_type', 'visit_date'], how='inner')
            return merged['avg_time_spent_pg'].equals(merged['avg_time_spent'])
        except Exception as e:
            print(f"Error in validate_avg_time_spent: {e}")
            return False

    @staticmethod
    def validate_sum_treatment_cost(pg_df, pq_df):
        try:
            merged = pd.merge(pg_df, pq_df, on=['facility_type', 'full_name'], how='inner')
            failed_rows = merged[merged['sum_treatment_cost_pg'] != merged['sum_treatment_cost']]
            return failed_rows
        except Exception as e:
            print(f"Error in validate_sum_treatment_cost: {e}")
            return False

    @staticmethod
    def validate_row_count(pg_df, pq_df):
        try:
            return len(pg_df) == len(pq_df)
        except Exception as e:
            print(f"Error in validate_row_count: {e}")
            return False
