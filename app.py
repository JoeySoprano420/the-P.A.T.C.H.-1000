from flask import Flask, request, jsonify, send_file
from flask_jwt_extended import jwt_required
import pandas as pd
from io import BytesIO
from mongoengine import Q
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
scheduler = BackgroundScheduler()

@app.route('/generate_report', methods=['POST'])
@jwt_required()
def generate_report():
    data = request.json
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    user_id = data.get('user_id')
    event_type = data.get('event_type')
    location = data.get('location')  # Additional filter
    status = data.get('status')      # Additional filter

    query = Q()
    if start_date:
        query &= Q(timestamp__gte=pd.to_datetime(start_date))
    if end_date:
        query &= Q(timestamp__lte=pd.to_datetime(end_date))
    if user_id:
        query &= Q(user_id=user_id)
    if event_type:
        query &= Q(event_type=event_type)
    if location:
        query &= Q(location=location)
    if status:
        query &= Q(status=status)

    analytics_data = Analytics.objects(__raw__=query).all()
    df = pd.DataFrame(list(analytics_data))

    if df.empty:
        return jsonify({'msg': 'No data available for the given filters'}), 404

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Report')

    output.seek(0)
    return send_file(output, as_attachment=True, attachment_filename='custom_report.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route('/schedule_report', methods=['POST'])
@jwt_required()
def schedule_report_endpoint():
    data = request.json
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    user_id = data.get('user_id')
    event_type = data.get('event_type')
    email = data.get('email')
    schedule_time = data.get('schedule_time')

    if not schedule_time:
        return jsonify({'msg': 'Schedule time is required'}), 400

    schedule_time = pd.to_datetime(schedule_time)
    scheduler.add_job(schedule_report, 'date', run_date=schedule_time, args=[start_date, end_date, user_id, event_type, email])
    scheduler.start()

    return jsonify({'msg': 'Report scheduled successfully'}), 200

def schedule_report(start_date, end_date, user_id, event_type, email):
    # Generate the report
    report_data = generate_report_data(start_date, end_date, user_id, event_type)
    send_email_with_report(email, report_data)

def generate_report_data(start_date, end_date, user_id, event_type):
    query = Q()
    if start_date:
        query &= Q(timestamp__gte=pd.to_datetime(start_date))
    if end_date:
        query &= Q(timestamp__lte=pd.to_datetime(end_date))
    if user_id:
        query &= Q(user_id=user_id)
    if event_type:
        query &= Q(event_type=event_type)

    analytics_data = Analytics.objects(__raw__=query).all()
    df = pd.DataFrame(list(analytics_data))
    return df

def send_email_with_report(email, df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Report')

    output.seek(0)
    # Placeholder for email functionality
    # Email sending code here

def load_template(name):
    # Load the template from file or database
    templates = {
        'default': '<Your default template>',
        'custom': '<Your custom template>',
    }
    return templates.get(name, templates['default'])
