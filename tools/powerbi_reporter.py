class PowerBIReporter:
    @staticmethod
    def report(data, anomalies, forecast):
        print("=== Weekly Financial Summary ===")
        print("\nData Head:\n", data.head())
        print("\nAnomalies Detected:")
        for anomaly in anomalies:
            print(anomaly)
        print("\nForecast for Next 4 Weeks:\n", forecast)
        print("\n[Mock PowerBI Report Sent]") 