import pandas as pd

class TimeSeriesForecaster:
    @staticmethod
    def forecast(df, weeks=4):
        """Mock forecast: projects the mean of each numeric column for the next 'weeks' weeks."""
        numeric_df = df.select_dtypes(include='number')
        means = numeric_df.mean()
        forecast = pd.DataFrame([means] * weeks, index=[f'Week {i+1}' for i in range(weeks)])
        return forecast 