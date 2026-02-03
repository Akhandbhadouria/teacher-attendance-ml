#!/usr/bin/env python3
"""
Face Attendance System - Main Menu
"""

import os
import sys

def clear_screen():
    """Clear the terminal screen"""
    os.system('clear' if os.name != 'nt' else 'cls')

def print_banner():
    """Print the application banner"""
    print("\n" + "="*60)
    print("          🎯 FACE ATTENDANCE SYSTEM 🎯")
    print("="*60)
    print("\n  Real-time face recognition for attendance tracking")
    print("  Supports multiple simultaneous face detection\n")
    print("="*60 + "\n")

def main_menu():
    """Display main menu and handle user choices"""
    
    while True:
        clear_screen()
        print_banner()
        
        print("MAIN MENU:")
        print("-" * 60)
        print("1. 📝 Register New User")
        print("2. ✅ Mark Attendance (Face Recognition)")
        print("3. 📊 View Attendance Records")
        print("4. 👥 View Registered Users")
        print("5. ❌ Exit")
        print("-" * 60)
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            # Register new user
            from register_user_simple import register_user
            clear_screen()
            register_user()
            input("\nPress Enter to continue...")
        
        elif choice == "2":
            # Mark attendance
            from mark_attendance_simple import mark_attendance
            clear_screen()
            mark_attendance()
            input("\nPress Enter to continue...")
        
        elif choice == "3":
            # View attendance
            from view_attendance import view_attendance
            clear_screen()
            view_attendance()
            input("\nPress Enter to continue...")
        
        elif choice == "4":
            # View registered users
            from database import Database
            clear_screen()
            db = Database()
            users = db.get_all_users()
            
            print("\n" + "="*60)
            print("REGISTERED USERS")
            print("="*60)
            
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
            
            print("="*60)
            input("\nPress Enter to continue...")
        
        elif choice == "5":
            # Exit
            clear_screen()
            print("\n" + "="*60)
            print("Thank you for using Face Attendance System!")
            print("="*60 + "\n")
            sys.exit(0)
        
        else:
            print("\n❌ Invalid choice! Please enter 1-5")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        clear_screen()
        print("\n\n" + "="*60)
        print("Application terminated by user")
        print("="*60 + "\n")
        sys.exit(0)
