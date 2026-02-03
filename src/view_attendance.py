from database import Database
from datetime import datetime

def view_attendance():
    """View attendance records"""
    
    db = Database()
    
    print("\n" + "="*60)
    print("       FACE ATTENDANCE SYSTEM - VIEW ATTENDANCE")
    print("="*60 + "\n")
    
    print("Options:")
    print("1. View today's attendance")
    print("2. View attendance by date")
    print("3. View user's attendance history")
    print("4. View all registered users")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        # Today's attendance
        today = datetime.now().strftime("%Y-%m-%d")
        records = db.get_attendance_by_date(today)
        
        print("\n" + "-"*60)
        print(f"ATTENDANCE FOR {today}")
        print("-"*60)
        
        if records:
            print(f"\nTotal Present: {len(records)}\n")
            for i, record in enumerate(records, 1):
                print(f"{i}. {record['name']} (ID: {record['user_id']})")
                print(f"   Time: {record['time']}")
                print()
        else:
            print("\n❌ No attendance records for today")
    
    elif choice == "2":
        # Specific date
        date_str = input("\nEnter date (YYYY-MM-DD): ").strip()
        
        try:
            # Validate date format
            datetime.strptime(date_str, "%Y-%m-%d")
            
            records = db.get_attendance_by_date(date_str)
            
            print("\n" + "-"*60)
            print(f"ATTENDANCE FOR {date_str}")
            print("-"*60)
            
            if records:
                print(f"\nTotal Present: {len(records)}\n")
                for i, record in enumerate(records, 1):
                    print(f"{i}. {record['name']} (ID: {record['user_id']})")
                    print(f"   Time: {record['time']}")
                    print()
            else:
                print(f"\n❌ No attendance records for {date_str}")
        
        except ValueError:
            print("\n❌ Invalid date format! Please use YYYY-MM-DD")
    
    elif choice == "3":
        # User's attendance history
        user_id = input("\nEnter User ID: ").strip()
        
        user_info = db.get_user(user_id)
        if not user_info:
            print(f"\n❌ User ID '{user_id}' not found!")
            return
        
        records = db.get_user_attendance(user_id)
        
        print("\n" + "-"*60)
        print(f"ATTENDANCE HISTORY FOR {user_info['name']} (ID: {user_id})")
        print("-"*60)
        
        if records:
            print(f"\nTotal Days Present: {len(records)}\n")
            for i, record in enumerate(records, 1):
                print(f"{i}. Date: {record['date']}")
                print(f"   Time: {record['time']}")
                print()
        else:
            print(f"\n❌ No attendance records for {user_info['name']}")
    
    elif choice == "4":
        # All registered users
        users = db.get_all_users()
        
        print("\n" + "-"*60)
        print("REGISTERED USERS")
        print("-"*60)
        
        if users:
            print(f"\nTotal Users: {len(users)}\n")
            for i, (user_id, user_info) in enumerate(users.items(), 1):
                print(f"{i}. {user_info['name']} (ID: {user_id})")
                print(f"   Email: {user_info.get('email', 'N/A')}")
                print(f"   Phone: {user_info.get('phone', 'N/A')}")
                print(f"   Registered: {user_info['registered_at']}")
                print()
        else:
            print("\n❌ No users registered yet")
    
    else:
        print("\n❌ Invalid choice!")
    
    print("="*60 + "\n")

if __name__ == "__main__":
    view_attendance()
