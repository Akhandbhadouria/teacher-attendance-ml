#!/usr/bin/env python
"""
Migrate data from JSON files to SQLite database
"""
import os
import sys
import django
import json
from datetime import datetime

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_web.settings')
django.setup()

from attendance.models import User, Attendance

def migrate_data():
    print("=" * 60)
    print("MIGRATING DATA FROM JSON TO SQLITE")
    print("=" * 60)
    
    # Load JSON data
    users_file = "data/users.json"
    attendance_file = "data/attendance.json"
    
    if not os.path.exists(users_file):
        print("❌ users.json not found!")
        return
    
    if not os.path.exists(attendance_file):
        print("❌ attendance.json not found!")
        return
    
    # Load users
    print("\n1. Loading users from JSON...")
    with open(users_file, 'r') as f:
        users_data = json.load(f)
    
    print(f"   Found {len(users_data)} users")
    
    # Load attendance
    print("\n2. Loading attendance from JSON...")
    with open(attendance_file, 'r') as f:
        attendance_data = json.load(f)
    
    print(f"   Found {len(attendance_data)} attendance records")
    
    # Migrate users
    print("\n3. Migrating users to SQLite...")
    users_created = 0
    users_updated = 0
    
    for user_id, user_info in users_data.items():
        try:
            user, created = User.objects.update_or_create(
                user_id=user_id,
                defaults={
                    'name': user_info['name'],
                    'email': user_info.get('email', ''),
                    'phone': user_info.get('phone', ''),
                    'registered_at': datetime.strptime(
                        user_info['registered_at'], 
                        "%Y-%m-%d %H:%M:%S"
                    )
                }
            )
            if created:
                users_created += 1
                print(f"   ✅ Created: {user.name} ({user_id})")
            else:
                users_updated += 1
                print(f"   ♻️  Updated: {user.name} ({user_id})")
        except Exception as e:
            print(f"   ❌ Error with {user_id}: {e}")
    
    print(f"\n   Created: {users_created}, Updated: {users_updated}")
    
    # Migrate attendance
    print("\n4. Migrating attendance to SQLite...")
    attendance_created = 0
    attendance_skipped = 0
    
    for record in attendance_data:
        try:
            user_id = record['user_id']
            
            # Get user
            try:
                user = User.objects.get(user_id=user_id)
            except User.DoesNotExist:
                print(f"   ⚠️  User {user_id} not found, skipping record")
                attendance_skipped += 1
                continue
            
            # Parse date and time
            date = datetime.strptime(record['date'], "%Y-%m-%d").date()
            time = datetime.strptime(record['time'], "%H:%M:%S").time()
            timestamp = datetime.strptime(record['timestamp'], "%Y-%m-%d %H:%M:%S")
            
            # Create or get attendance
            attendance, created = Attendance.objects.get_or_create(
                user=user,
                date=date,
                defaults={
                    'time': time,
                    'timestamp': timestamp
                }
            )
            
            if created:
                attendance_created += 1
                print(f"   ✅ Created: {user.name} on {date}")
            else:
                attendance_skipped += 1
                print(f"   ⏭️  Skipped: {user.name} on {date} (already exists)")
                
        except Exception as e:
            print(f"   ❌ Error with record: {e}")
            attendance_skipped += 1
    
    print(f"\n   Created: {attendance_created}, Skipped: {attendance_skipped}")
    
    # Summary
    print("\n" + "=" * 60)
    print("MIGRATION COMPLETE!")
    print("=" * 60)
    print(f"✅ Users in database: {User.objects.count()}")
    print(f"✅ Attendance records in database: {Attendance.objects.count()}")
    print("\n💡 You can now delete the JSON files if you want:")
    print("   - data/users.json")
    print("   - data/attendance.json")
    print("\n   Or keep them as backup!")

if __name__ == "__main__":
    migrate_data()
