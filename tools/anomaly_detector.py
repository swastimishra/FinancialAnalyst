class AnomalyDetectorAgent:
    @staticmethod
    def detect(df):
        """Mock anomaly detection: returns rows where any numeric value is negative as anomalies."""
        numeric_df = df.select_dtypes(include='number')
        anomalies = df[(numeric_df < 0).any(axis=1)]
        return anomalies.to_dict(orient='records') 