from tools.excel_parser import ExcelParserTool
from tools.anomaly_detector import AnomalyDetectorAgent
from tools.forecaster import TimeSeriesForecaster
from tools.powerbi_reporter import PowerBIReporter
from apscheduler.schedulers.blocking import BlockingScheduler
import os

def supervisor_workflow():
    # For demo, use a sample Excel file path
    file_path = os.path.join(os.path.dirname(__file__), 'sample_financial_data.xlsx')
    data = ExcelParserTool.read(file_path)
    anomalies = AnomalyDetectorAgent.detect(data)
    forecast = TimeSeriesForecaster.forecast(data)
    PowerBIReporter.report(data, anomalies, forecast)

def schedule_weekly():
    scheduler = BlockingScheduler()
    scheduler.add_job(supervisor_workflow, 'interval', weeks=1)
    print('Supervisor scheduled to run weekly. Press Ctrl+C to exit.')
    scheduler.start()

if __name__ == '__main__':
    # Run once for demo
    supervisor_workflow()
    # Uncomment below to enable weekly scheduling
    # schedule_weekly() 