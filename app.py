from flask import Flask, request, render_template, redirect, url_for, session, send_file, flash
from tools.excel_parser import ExcelParserTool
from tools.anomaly_detector import AnomalyDetectorAgent
from tools.forecaster import TimeSeriesForecaster
from tools.powerbi_reporter import PowerBIReporter
import os
import tempfile
import pandas as pd
import io
import pickle
from flask_session import Session

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB upload limit
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = os.path.join(os.path.dirname(__file__), 'flask_session')
app.secret_key = 'your_secret_key_here'  # Needed for session
Session(app)

def save_temp_obj(obj, prefix):
    fd, path = tempfile.mkstemp(prefix=prefix, dir=app.config['SESSION_FILE_DIR'])
    with os.fdopen(fd, 'wb') as f:
        pickle.dump(obj, f)
    return path

def load_temp_obj(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def get_report_context():
    data_path = session.get('data_path')
    anomalies_path = session.get('anomalies_path')
    forecast_path = session.get('forecast_path')
    if not data_path or not anomalies_path or not forecast_path:
        flash("Session expired or no data found. Please upload a file.")
        return None
    df = load_temp_obj(data_path)
    anomalies = load_temp_obj(anomalies_path)
    forecast = load_temp_obj(forecast_path)
    data_html = df.head().to_html(index=False, classes='table table-striped table-bordered')
    forecast_html = forecast.to_html(classes='table table-striped table-bordered')
    return dict(data_html=data_html, anomalies=anomalies, forecast_html=forecast_html)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.xlsx'):
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
                file.save(tmp.name)
                temp_path = tmp.name
            df = ExcelParserTool.read(temp_path)
            anomalies = AnomalyDetectorAgent.detect(df)
            forecast = TimeSeriesForecaster.forecast(df)
            os.unlink(temp_path)
            # Save objects to temp files and store paths in session
            session['data_path'] = save_temp_obj(df, 'data_')
            session['anomalies_path'] = save_temp_obj(anomalies, 'anoms_')
            session['forecast_path'] = save_temp_obj(forecast, 'fcst_')
            return redirect(url_for('report'))
        else:
            return render_template('upload.html', error='Please upload a valid .xlsx file.')
    return render_template('upload.html')

@app.route('/report', methods=['GET'])
def report():
    ctx = get_report_context()
    if ctx is None:
        return redirect(url_for('upload_file'))
    return render_template('report.html', **ctx)

@app.route('/generate_forecast', methods=['POST'])
def generate_forecast():
    weeks = int(request.form.get('forecast_weeks', 4))
    df = load_temp_obj(session.get('data_path'))
    forecast = TimeSeriesForecaster.forecast(df, weeks=weeks)
    session['forecast_path'] = save_temp_obj(forecast, 'fcst_')
    return redirect(url_for('report'))

@app.route('/download_report')
def download_report():
    df = load_temp_obj(session.get('data_path'))
    anomalies = load_temp_obj(session.get('anomalies_path'))
    forecast = load_temp_obj(session.get('forecast_path'))
    html = render_template('report_download.html', data_html=df.head().to_html(index=False, classes='table table-striped'), anomalies=anomalies, forecast_html=forecast.to_html(classes='table table-striped'))
    try:
        import pdfkit
        pdf = pdfkit.from_string(html, False)
        return send_file(io.BytesIO(pdf), as_attachment=True, download_name='financial_report.pdf', mimetype='application/pdf')
    except Exception:
        return html

@app.route('/export_excel')
def export_excel():
    df = load_temp_obj(session.get('data_path'))
    forecast = load_temp_obj(session.get('forecast_path'))
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
        forecast.to_excel(writer, sheet_name='Forecast')
    output.seek(0)
    return send_file(output, as_attachment=True, download_name='financial_data_export.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == '__main__':
    os.makedirs(app.config['SESSION_FILE_DIR'], exist_ok=True)
    app.run(debug=True) 