import cv2
import numpy as np
import os
import pickle
from typing import List, Tuple, Dict

class SimpleFaceRecognitionSystem:
    """
    Simplified face recognition system using OpenCV's built-in face detection
    and LBPH (Local Binary Patterns Histograms) face recognizer
    """
    
    def __init__(self, encodings_dir: str = "data/encodings", models_dir: str = "data/models"):
        self.encodings_dir = encodings_dir
        self.models_dir = models_dir
        self.known_face_names = []
        self.face_samples = {}  # Store multiple samples per user
        
        # Create directories
        os.makedirs(encodings_dir, exist_ok=True)
        os.makedirs(models_dir, exist_ok=True)
        
        # Initialize face detector and recognizer
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        
        # Load existing data
        self.load_encodings()
    
    def detect_faces(self, frame):
        """Detect faces in the frame"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(100, 100)
        )
        return faces, gray
    
    def register_face(self, name: str, image_path: str = None, frame=None) -> Tuple[bool, str]:
        """
        Register a new face with the given name
        
        Args:
            name: User's name/ID
            image_path: Path to image file (optional)
            frame: Image frame from webcam (optional)
        
        Returns:
            Tuple of (success, message)
        """
        # Load image
        if image_path:
            image = cv2.imread(image_path)
        elif frame is not None:
            image = frame.copy()
        else:
            return False, "No image provided"
        
        # Detect faces
        faces, gray = self.detect_faces(image)
        
        if len(faces) == 0:
            return False, "No face detected in the image"
        
        if len(faces) > 1:
            return False, "Multiple faces detected. Please ensure only one face is visible"
        
        # Get the face region
        (x, y, w, h) = faces[0]
        face_roi = gray[y:y+h, x:x+w]
        
        # Resize to standard size
        face_roi = cv2.resize(face_roi, (200, 200))
        
        # Check if user already exists
        if name in self.known_face_names:
            return False, f"User '{name}' already registered"
        
        # Add to known faces
        self.known_face_names.append(name)
        
        # Store face sample
        if name not in self.face_samples:
            self.face_samples[name] = []
        self.face_samples[name].append(face_roi)
        
        # Save data
        self._save_data()
        
        # Retrain recognizer
        self._train_recognizer()
        
        return True, f"Successfully registered {name}"
    
    def recognize_faces(self, frame) -> List[Dict]:
        """
        Recognize all faces in the given frame
        
        Args:
            frame: Image frame from webcam
        
        Returns:
            List of dictionaries containing face information
        """
        # Detect faces
        faces, gray = self.detect_faces(frame)
        
        recognized_faces = []
        
        for (x, y, w, h) in faces:
            # Extract face region
            face_roi = gray[y:y+h, x:x+w]
            face_roi = cv2.resize(face_roi, (200, 200))
            
            name = "Unknown"
            confidence = 0.0
            
            # Recognize face if we have trained data
            if len(self.known_face_names) > 0 and hasattr(self.recognizer, 'predict'):
                try:
                    label, conf = self.recognizer.predict(face_roi)
                    
                    # Lower confidence value means better match
                    # Threshold: accept if confidence < 45 (VERY STRICT for security)
                    if conf < 45 and label < len(self.known_face_names):
                        name = self.known_face_names[label]
                        # Convert confidence to percentage (inverse)
                        confidence = max(0, (100 - conf) / 100)
                    
                except Exception as e:
                    print(f"Recognition error: {e}")
            
            recognized_faces.append({
                "name": name,
                "confidence": confidence,
                "location": (y, x+w, y+h, x)  # top, right, bottom, left
            })
        
        return recognized_faces
    
    def _train_recognizer(self):
        """Train the face recognizer with all stored samples"""
        if not self.face_samples:
            return
        
        faces = []
        labels = []
        
        for idx, name in enumerate(self.known_face_names):
            if name in self.face_samples:
                for face_sample in self.face_samples[name]:
                    faces.append(face_sample)
                    labels.append(idx)
        
        if faces:
            self.recognizer.train(faces, np.array(labels))
            # Save trained model
            model_path = os.path.join(self.models_dir, "face_recognizer.yml")
            self.recognizer.save(model_path)
    
    def _save_data(self):
        """Save face samples and names"""
        # Save names
        names_file = os.path.join(self.encodings_dir, "names.pkl")
        with open(names_file, 'wb') as f:
            pickle.dump(self.known_face_names, f)
        
        # Save face samples
        samples_file = os.path.join(self.encodings_dir, "samples.pkl")
        with open(samples_file, 'wb') as f:
            pickle.dump(self.face_samples, f)
    
    def load_encodings(self):
        """Load all saved face data"""
        self.known_face_names = []
        self.face_samples = {}
        
        # Load names
        names_file = os.path.join(self.encodings_dir, "names.pkl")
        if os.path.exists(names_file):
            try:
                with open(names_file, 'rb') as f:
                    self.known_face_names = pickle.load(f)
            except Exception as e:
                print(f"Error loading names: {e}")
        
        # Load samples
        samples_file = os.path.join(self.encodings_dir, "samples.pkl")
        if os.path.exists(samples_file):
            try:
                with open(samples_file, 'rb') as f:
                    self.face_samples = pickle.load(f)
            except Exception as e:
                print(f"Error loading samples: {e}")
        
        # Load trained model if exists
        model_path = os.path.join(self.models_dir, "face_recognizer.yml")
        if os.path.exists(model_path):
            try:
                self.recognizer.read(model_path)
            except Exception as e:
                print(f"Error loading model: {e}")
                # Retrain if model loading fails
                self._train_recognizer()
    
    def delete_user(self, name: str) -> bool:
        """Delete a registered user"""
        if name in self.known_face_names:
            self.known_face_names.remove(name)
            if name in self.face_samples:
                del self.face_samples[name]
            
            self._save_data()
            self._train_recognizer()
            
            return True
        return False
    
    def get_registered_users(self) -> List[str]:
        """Get list of all registered users"""
        return self.known_face_names.copy()
