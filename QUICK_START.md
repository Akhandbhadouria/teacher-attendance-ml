# 🎯 Face Attendance System - Quick Reference

## 🚀 Starting the System

### Option 1: Using the Startup Script
```bash
./start_server.sh
```

### Option 2: Manual Start
```bash
python manage.py runserver
```

Then open your browser to: **http://127.0.0.1:8000/**

## 📱 Main Features

### 1. Dashboard (/)
- View statistics
- Quick access to all features

### 2. Register User (/register/)
- Fill in user details
- Capture face via webcam
- Automatic registration

### 3. Mark Attendance (/mark-attendance/)
- Start camera
- Automatic face detection
- Real-time attendance marking
- **Supports multiple faces simultaneously!**

### 4. View Users (/users/)
- See all registered users
- View user profiles
- Check attendance history

### 5. Attendance Records (/attendance/)
- Filter by date
- View attendance table
- Export data

### 6. Statistics (/statistics/)
- 7-day trends
- Attendance analytics

## 🎯 Current System Status

✅ **Registered Users:** 1
- User ID: 12317691
- Name: irfan

✅ **System Status:** Fully Operational
- Web interface: Ready
- Face recognition: Working
- Database: Initialized
- Camera access: Available

## 💡 Quick Tips

### Registration
1. Click "Register" in menu
2. Fill form (User ID, Name, Email, Phone)
3. Click "Start Camera"
4. Click "Capture Face"
5. Click "Register User"

### Mark Attendance
1. Click "Mark Attendance" in menu
2. Click "Start Attendance System"
3. Stand in front of camera
4. Wait for automatic detection
5. Attendance marked instantly!

### View Records
- Click "Attendance" to see records
- Use date filter to view specific dates
- Click on users to see their history

## 🔧 Troubleshooting

**Camera not working?**
- Allow camera permissions in browser
- Close other apps using camera

**Face not detected?**
- Improve lighting
- Move closer to camera
- Look directly at camera

**Server not starting?**
- Check if port 8000 is free
- Run: `python manage.py runserver`

## 📞 Need Help?

Check the full README.md for detailed documentation.

---

**Made with ❤️ - Enjoy your Face Attendance System!**
