import cv2
import mediapipe as mp
import numpy as np
import pygame
from time import time
import scripts.core as c

class GestureController:
    def __init__(self, game):
        self.game = game
        self.cap = None
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Hand tracking variables
        self.hand_landmarks = None
        self.hand_position = (c.WIN_SIZE[0] // 2, c.WIN_SIZE[1] // 2)
        self.prev_hand_position = self.hand_position
        self.smoothing_factor = 0.7
        
        # Gesture recognition
        self.gesture_history = []
        self.gesture_threshold = 0.8
        self.last_gesture_time = 0
        self.gesture_cooldown = 0.5
        
        # Camera setup
        self.camera_width = 480
        self.camera_height = 360
        self.camera_center = (self.camera_width // 2, self.camera_height // 2)
        
        # Initialize camera
        self.init_camera()
        
    def init_camera(self):
        try:
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.camera_width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.camera_height)
            if not self.cap.isOpened():
                print("Warning: Could not open camera. Falling back to mouse controls.")
                self.cap = None
        except Exception as e:
            print(f"Camera initialization error: {e}")
            self.cap = None
    
    def get_hand_position(self):
        # Use mouse controls when in menu or game over state
        if self.game.menu_active or self.game.game_over:
            return pygame.mouse.get_pos()
        
        # Use hand tracking only during active gameplay
        if self.cap is None or not self.cap.isOpened():
            print("[ERROR] Camera not available or failed to open. Using mouse controls.")
            return pygame.mouse.get_pos()
        
        ret, frame = self.cap.read()
        if not ret:
            return self.hand_position
        
        # Flip frame horizontally for more intuitive control
        frame = cv2.flip(frame, 1)
        
        # Convert to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            self.hand_landmarks = hand_landmarks
            index_tip = hand_landmarks.landmark[8]
            x = int(index_tip.x * self.camera_width)
            y = int(index_tip.y * self.camera_height)
            game_x = int((x / self.camera_width) * c.WIN_SIZE[0])
            game_y = int((y / self.camera_height) * c.WIN_SIZE[1])
            smoothed_x = int(self.smoothing_factor * game_x + (1 - self.smoothing_factor) * self.hand_position[0])
            smoothed_y = int(self.smoothing_factor * game_y + (1 - self.smoothing_factor) * self.hand_position[1])
            self.prev_hand_position = self.hand_position
            self.hand_position = (smoothed_x, smoothed_y)
            self.detect_gestures(hand_landmarks)
            self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
            gesture_text = "No Gesture"
            if self.is_fist_gesture(hand_landmarks):
                gesture_text = "FIST - Repulse"
            elif self.is_peace_gesture(hand_landmarks):
                gesture_text = "PEACE - Shield"
            elif self.is_pointing_gesture(hand_landmarks):
                gesture_text = "POINTING - Move"
            cv2.putText(frame, gesture_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Hand: ({smoothed_x}, {smoothed_y})", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        # Show camera feed in a separate window only during gameplay
        cv2.imshow('Hand Tracking', frame)
        cv2.waitKey(1)
        return self.hand_position
    
    def detect_gestures(self, hand_landmarks):
        # Only detect gestures during active gameplay
        if self.game.menu_active or self.game.game_over:
            return
            
        current_time = time()
        if current_time - self.last_gesture_time < self.gesture_cooldown:
            return
        if self.is_fist_gesture(hand_landmarks):
            self.game.player.repulse()
            self.last_gesture_time = current_time
            print("Fist gesture detected - Repulse activated!")
        elif self.is_peace_gesture(hand_landmarks):
            self.game.player.set_shield(5000)
            self.last_gesture_time = current_time
            print("Peace gesture detected - Shield activated!")
    def is_fist_gesture(self, hand_landmarks):
        finger_tips = [4, 8, 12, 16, 20]
        finger_mids = [3, 6, 10, 14, 18]
        closed_fingers = 0
        for tip, mid in zip(finger_tips, finger_mids):
            if hand_landmarks.landmark[tip].y > hand_landmarks.landmark[mid].y:
                closed_fingers += 1
        return closed_fingers >= 4
    def is_peace_gesture(self, hand_landmarks):
        index_tip = hand_landmarks.landmark[8]
        index_mid = hand_landmarks.landmark[6]
        middle_tip = hand_landmarks.landmark[12]
        middle_mid = hand_landmarks.landmark[10]
        ring_tip = hand_landmarks.landmark[16]
        ring_mid = hand_landmarks.landmark[14]
        pinky_tip = hand_landmarks.landmark[20]
        pinky_mid = hand_landmarks.landmark[18]
        index_up = index_tip.y < index_mid.y
        middle_up = middle_tip.y < middle_mid.y
        ring_down = ring_tip.y > ring_mid.y
        pinky_down = pinky_tip.y > pinky_mid.y
        return index_up and middle_up and ring_down and pinky_down
    def is_pointing_gesture(self, hand_landmarks):
        index_tip = hand_landmarks.landmark[8]
        index_mid = hand_landmarks.landmark[6]
        middle_tip = hand_landmarks.landmark[12]
        middle_mid = hand_landmarks.landmark[10]
        ring_tip = hand_landmarks.landmark[16]
        ring_mid = hand_landmarks.landmark[14]
        pinky_tip = hand_landmarks.landmark[20]
        pinky_mid = hand_landmarks.landmark[18]
        index_up = index_tip.y < index_mid.y
        middle_down = middle_tip.y > middle_mid.y
        ring_down = ring_tip.y > ring_mid.y
        pinky_down = pinky_tip.y > pinky_mid.y
        return index_up and middle_down and ring_down and pinky_down
    def cleanup(self):
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()
        self.hands.close()
    
    def hide_camera_window(self):
        """Hide the camera window when not in gameplay"""
        cv2.destroyWindow('Hand Tracking')
    
    def show_camera_window(self):
        """Show the camera window during gameplay"""
        # The window will be created automatically when get_hand_position is called
        pass 