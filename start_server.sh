#!/bin/bash

echo "🎯 Face Attendance System - Starting Web Server"
echo "================================================"
echo ""
echo "Starting Django development server..."
echo "Access the web interface at: http://127.0.0.1:8000/"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd "$(dirname "$0")"
python manage.py runserver
