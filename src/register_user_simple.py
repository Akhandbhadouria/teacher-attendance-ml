import cv2
import os
from simple_face_recognition import SimpleFaceRecognitionSystem
from database import Database

def register_user():
    """Interactive user registration with face capture"""
    
    print("\n" + "="*60)
    print("          FACE ATTENDANCE SYSTEM - USER REGISTRATION")
    print("="*60 + "\n")
    
    # Initialize systems
    face_system = SimpleFaceRecognitionSystem()
    db = Database()
    
    # Get user information
    print("Please enter your details:")
    user_id = input("User ID (unique identifier): ").strip()
    
    if not user_id:
        print("❌ User ID cannot be empty!")
        return
    
    # Check if user already exists
    if db.get_user(user_id):
        print(f"❌ User ID '{user_id}' already exists!")
        return
    
    name = input("Full Name: ").strip()
    email = input("Email (optional): ").strip()
    phone = input("Phone (optional): ").strip()
    
    if not name:
        print("❌ Name cannot be empty!")
        return
    
    print("\n" + "-"*60)
    print("Starting webcam for face capture...")
    print("Instructions:")
    print("  • Position your face in the center of the frame")
    print("  • Ensure good lighting")
    print("  • Look directly at the camera")
    print("  • Press SPACE to capture your face")
    print("  • Press 'q' to cancel")
    print("-"*60 + "\n")
    
    # Open webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Cannot access webcam!")
        return
    
    face_captured = False
    captured_frame = None
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to capture frame")
            break
        
        # Display frame
        display_frame = frame.copy()
        
        # Detect faces for visual feedback
        faces, _ = face_system.detect_faces(frame)
        
        # Draw rectangles around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(display_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(display_frame, "Face Detected", (x, y-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Draw guide rectangle
        height, width = frame.shape[:2]
        rect_width = int(width * 0.4)
        rect_height = int(height * 0.5)
        x1 = (width - rect_width) // 2
        y1 = (height - rect_height) // 2
        x2 = x1 + rect_width
        y2 = y1 + rect_height
        
        cv2.rectangle(display_frame, (x1, y1), (x2, y2), (255, 255, 0), 2)
        cv2.putText(display_frame, "Position face here", (x1, y1 - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.putText(display_frame, "Press SPACE to capture", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(display_frame, "Press Q to cancel", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        cv2.imshow("Face Registration", display_frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord(' '):  # Space key
            captured_frame = frame.copy()
            face_captured = True
            break
        elif key == ord('q'):
            print("\n❌ Registration cancelled")
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    if not face_captured:
        return
    
    print("\n📸 Face captured! Processing...")
    
    # Register face
    success, message = face_system.register_face(user_id, frame=captured_frame)
    
    if success:
        # Save user to database
        db.add_user(user_id, name, email, phone)
        
        # Save captured image
        images_dir = "data/images"
        os.makedirs(images_dir, exist_ok=True)
        image_path = os.path.join(images_dir, f"{user_id}.jpg")
        cv2.imwrite(image_path, captured_frame)
        
        print("\n" + "="*60)
        print("✅ REGISTRATION SUCCESSFUL!")
        print("="*60)
        print(f"User ID: {user_id}")
        print(f"Name: {name}")
        print(f"Email: {email if email else 'N/A'}")
        print(f"Phone: {phone if phone else 'N/A'}")
        print(f"Image saved: {image_path}")
        print("="*60 + "\n")
    else:
        print(f"\n❌ Registration failed: {message}\n")

if __name__ == "__main__":
    register_user()
