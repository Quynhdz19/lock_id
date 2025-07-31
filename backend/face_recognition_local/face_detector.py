import face_recognition
import cv2
import numpy as np
import os
import pickle
from typing import List, Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FaceDetector:
    def __init__(self, tolerance: float = 0.6):
        """
        Initialize face detector with tolerance for face matching
        :param tolerance: Lower values are more strict (0.6 is default)
        """
        self.tolerance = tolerance
        self.known_face_encodings = []
        self.known_face_names = []
        
    def load_known_faces(self, faces_data: List[Tuple[str, str]]):
        """
        Load known faces from database
        :param faces_data: List of tuples (user_id, face_encoding)
        """
        self.known_face_encodings = []
        self.known_face_names = []
        
        for user_id, face_encoding_str in faces_data:
            try:
                # Convert string back to numpy array
                face_encoding = np.array(eval(face_encoding_str))
                self.known_face_encodings.append(face_encoding)
                self.known_face_names.append(user_id)
                logger.info(f"Loaded face data for user {user_id}")
            except Exception as e:
                logger.error(f"Error loading face data for user {user_id}: {e}")
    
    def encode_face_from_image(self, image_path: str) -> Optional[np.ndarray]:
        """
        Encode a face from an image file
        :param image_path: Path to the image file
        :return: Face encoding as numpy array or None if no face found
        """
        try:
            # Load image
            image = face_recognition.load_image_file(image_path)
            
            # Find face locations
            face_locations = face_recognition.face_locations(image)
            
            if not face_locations:
                logger.warning("No face found in image")
                return None
            
            # Get face encodings
            face_encodings = face_recognition.face_encodings(image, face_locations)
            
            if not face_encodings:
                logger.warning("Could not encode face")
                return None
            
            # Return the first face encoding
            return face_encodings[0]
            
        except Exception as e:
            logger.error(f"Error encoding face from image {image_path}: {e}")
            return None
    
    def encode_face_from_bytes(self, image_bytes: bytes) -> Optional[np.ndarray]:
        """
        Encode a face from image bytes
        :param image_bytes: Image data as bytes
        :return: Face encoding as numpy array or None if no face found
        """
        try:
            # Convert bytes to numpy array
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Convert BGR to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Find face locations
            face_locations = face_recognition.face_locations(image_rgb)
            
            if not face_locations:
                logger.warning("No face found in image")
                return None
            
            # Get face encodings
            face_encodings = face_recognition.face_encodings(image_rgb, face_locations)
            
            if not face_encodings:
                logger.warning("Could not encode face")
                return None
            
            # Return the first face encoding
            return face_encodings[0]
            
        except Exception as e:
            logger.error(f"Error encoding face from bytes: {e}")
            return None
    
    def recognize_face(self, face_encoding: np.ndarray) -> Tuple[Optional[str], float]:
        """
        Recognize a face against known faces
        :param face_encoding: Face encoding to recognize
        :return: Tuple of (user_id, confidence_score) or (None, 0.0) if no match
        """
        if not self.known_face_encodings:
            logger.warning("No known faces loaded")
            return None, 0.0
        
        try:
            # Compare face with known faces
            matches = face_recognition.compare_faces(
                self.known_face_encodings, 
                face_encoding, 
                tolerance=self.tolerance
            )
            
            # Calculate face distances
            face_distances = face_recognition.face_distance(
                self.known_face_encodings, 
                face_encoding
            )
            
            if not matches:
                logger.info("No face matches found")
                return None, 0.0
            
            # Find the best match
            best_match_index = np.argmin(face_distances)
            
            if matches[best_match_index]:
                user_id = self.known_face_names[best_match_index]
                confidence = 1.0 - face_distances[best_match_index]
                confidence_percentage = int(confidence * 100)
                
                logger.info(f"Face recognized as user {user_id} with {confidence_percentage}% confidence")
                return user_id, confidence_percentage
            
            return None, 0.0
            
        except Exception as e:
            logger.error(f"Error recognizing face: {e}")
            return None, 0.0
    
    def detect_faces_in_image(self, image_path: str) -> List[Tuple[int, int, int, int]]:
        """
        Detect all faces in an image
        :param image_path: Path to the image file
        :return: List of face locations (top, right, bottom, left)
        """
        try:
            image = face_recognition.load_image_file(image_path)
            face_locations = face_recognition.face_locations(image)
            return face_locations
        except Exception as e:
            logger.error(f"Error detecting faces in image {image_path}: {e}")
            return []
    
    def save_face_encoding(self, face_encoding: np.ndarray, user_id: str, save_path: str):
        """
        Save face encoding to file
        :param face_encoding: Face encoding to save
        :param user_id: User ID
        :param save_path: Path to save the encoding
        """
        try:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # Convert numpy array to string for storage
            encoding_str = str(face_encoding.tolist())
            
            with open(save_path, 'w') as f:
                f.write(encoding_str)
            
            logger.info(f"Face encoding saved for user {user_id}")
            
        except Exception as e:
            logger.error(f"Error saving face encoding for user {user_id}: {e}")
    
    def load_face_encoding(self, load_path: str) -> Optional[np.ndarray]:
        """
        Load face encoding from file
        :param load_path: Path to the encoding file
        :return: Face encoding as numpy array or None if error
        """
        try:
            with open(load_path, 'r') as f:
                encoding_str = f.read()
            
            # Convert string back to numpy array
            encoding_list = eval(encoding_str)
            return np.array(encoding_list)
            
        except Exception as e:
            logger.error(f"Error loading face encoding from {load_path}: {e}")
            return None 