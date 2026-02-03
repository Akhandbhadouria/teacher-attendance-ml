import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class Database:
    """Simple JSON-based database for storing user and attendance data"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.users_file = os.path.join(data_dir, "users.json")
        self.attendance_file = os.path.join(data_dir, "attendance.json")
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize files if they don't exist
        if not os.path.exists(self.users_file):
            self._save_json(self.users_file, {})
        if not os.path.exists(self.attendance_file):
            self._save_json(self.attendance_file, [])
    
    def _load_json(self, filepath: str):
        """Load JSON data from file"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {} if filepath == self.users_file else []
    
    def _save_json(self, filepath: str, data):
        """Save JSON data to file"""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
    
    def add_user(self, user_id: str, name: str, email: str = "", phone: str = "") -> bool:
        """Add a new user to the database"""
        users = self._load_json(self.users_file)
        
        if user_id in users:
            return False
        
        users[user_id] = {
            "name": name,
            "email": email,
            "phone": phone,
            "registered_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self._save_json(self.users_file, users)
        return True
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user information by ID"""
        users = self._load_json(self.users_file)
        return users.get(user_id)
    
    def get_all_users(self) -> Dict:
        """Get all registered users"""
        return self._load_json(self.users_file)
    
    def mark_attendance(self, user_id: str, name: str) -> bool:
        """Mark attendance for a user"""
        attendance_records = self._load_json(self.attendance_file)
        
        # Check if already marked today
        today = datetime.now().strftime("%Y-%m-%d")
        for record in attendance_records:
            if record["user_id"] == user_id and record["date"] == today:
                return False  # Already marked today
        
        # Add new attendance record
        record = {
            "user_id": user_id,
            "name": name,
            "date": today,
            "time": datetime.now().strftime("%H:%M:%S"),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        attendance_records.append(record)
        self._save_json(self.attendance_file, attendance_records)
        return True
    
    def get_attendance_by_date(self, date: str = None) -> List[Dict]:
        """Get attendance records for a specific date"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        attendance_records = self._load_json(self.attendance_file)
        return [r for r in attendance_records if r["date"] == date]
    
    def get_user_attendance(self, user_id: str) -> List[Dict]:
        """Get all attendance records for a specific user"""
        attendance_records = self._load_json(self.attendance_file)
        return [r for r in attendance_records if r["user_id"] == user_id]
    
    def delete_user(self, user_id: str) -> bool:
        """Delete a user from the database"""
        users = self._load_json(self.users_file)
        
        if user_id not in users:
            return False
        
        # Remove user
        del users[user_id]
        self._save_json(self.users_file, users)
        
        # Optionally remove attendance records (commented out to keep history)
        # attendance_records = self._load_json(self.attendance_file)
        # attendance_records = [r for r in attendance_records if r["user_id"] != user_id]
        # self._save_json(self.attendance_file, attendance_records)
        
        return True
