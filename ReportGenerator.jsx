import React, { useState } from 'react';
import axios from 'axios';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

function ReportGenerator() {
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [userId, setUserId] = useState('');
  const [eventType, setEventType] = useState('');
  const [location, setLocation] = useState('');
  const [status, setStatus] = useState('');
  const [templateName, setTemplateName] = useState('default');
  const [email, setEmail] = useState('');
  const [scheduleTime, setScheduleTime] = useState(null);
  const [downloadLink, setDownloadLink] = useState('');
  const [message, setMessage] = useState('');

  const handleGenerateReport = async () => {
    try {
      const response = await axios.post('http://localhost:5000/generate_report', {
        start_date: startDate ? startDate.toISOString().split('T')[0] : null,
        end_date: endDate ? endDate.toISOString().split('T')[0] : null,
        user_id: userId,
        event_type: eventType,
        location: location,
        status: status,
      }, {
        responseType: 'blob'
      });

      const url = window.URL.createObjectURL(new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' }));
      setDownloadLink(url);
    } catch (error) {
      console.error('Error generating report:', error);
    }
  };

  const handleScheduleReport = async () => {
    try {
      await axios.post('http://localhost:5000/schedule_report', {
        start_date: startDate ? startDate.toISOString().split('T')[0] : null,
        end_date: endDate ? endDate.toISOString().split('T')[0] : null,
        user_id: userId,
        event_type: eventType,
        email: email,
        schedule_time: scheduleTime ? scheduleTime.toISOString() : null,
      });
      setMessage('Report scheduled successfully');
    } catch (error) {
      console.error('Error scheduling report:', error);
      setMessage('Error scheduling report');
    }
  };

  return (
    <div>
      <h2>Generate Custom Report</h2>
      <DatePicker
        selected={startDate}
        onChange={(date) => setStartDate(date)}
        placeholderText="Start Date"
      />
      <DatePicker
        selected={endDate}
        onChange={(date) => setEndDate(date)}
        placeholderText="End Date"
      />
      <input
        type="text"
        value={userId}
        onChange={(e) => setUserId(e.target.value)}
        placeholder="User ID"
      />
      <input
        type="text"
        value={eventType}
        onChange={(e) => setEventType(e.target.value)}
        placeholder="Event Type"
      />
      <input
        type="text"
        value={location}
        onChange={(e) => setLocation(e.target.value)}
        placeholder="Location"
      />
      <input
        type="text"
        value={status}
        onChange={(e) => setStatus(e.target.value)}
        placeholder="Status"
      />
      <select value={templateName} onChange={(e) => setTemplateName(e.target.value)}>
        <option value="default">Default</option>
        <option value="custom">Custom</option>
      </select>
      <button onClick={handleGenerateReport}>Generate Report</button>
      {downloadLink && (
        <a href={downloadLink} download="custom_report.xlsx">Download Report</a>
      )}
      <h2>Schedule Report</h2>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email Address"
      />
      <DatePicker
        selected={scheduleTime}
        onChange={(date) => setScheduleTime(date)}
        showTimeSelect
        timeIntervals={15}
        dateFormat="Pp"
        placeholderText="Schedule Time"
      />
      <button onClick={handleScheduleReport}>Schedule Report</button>
      {message && <p>{message}</p>}
    </div>
  );
}

export default ReportGenerator;
