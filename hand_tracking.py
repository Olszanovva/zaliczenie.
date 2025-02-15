import cv2
import mediapipe as mp
import numpy as np

class HandTracking:
    def __init__(self, max_hands=2):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=max_hands, min_detection_confidence=0.7)
        self.mp_draw = mp.solutions.drawing_utils

    def detect_hands(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        return results

    def draw_hands(self, frame, results):
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        return frame

    def calculate_angle(self, point1, point2, point3):
        """Oblicza kąt między trzema punktami"""
        a = np.array(point1)
        b = np.array(point2)
        c = np.array(point3)

        ab = a - b
        cb = c - b

        cosine_angle = np.dot(ab, cb) / (np.linalg.norm(ab) * np.linalg.norm(cb))
        angle = np.arccos(cosine_angle)

        return np.degrees(angle)

    def count_fingers(self, results):
        """Zlicza wyprostowane palce, teraz poprawiona detekcja kciuka"""
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                fingers = []
                finger_tips = [8, 12, 16, 20]  
                for tip in finger_tips:
                    if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
                        fingers.append(1)
                    else:
                        fingers.append(0)

               
                thumb_tip = np.array([hand_landmarks.landmark[4].x, hand_landmarks.landmark[4].y])
                thumb_ip = np.array([hand_landmarks.landmark[3].x, hand_landmarks.landmark[3].y])  
                thumb_mcp = np.array([hand_landmarks.landmark[2].x, hand_landmarks.landmark[2].y])  
                wrist = np.array([hand_landmarks.landmark[0].x, hand_landmarks.landmark[0].y])  
               
                thumb_angle = self.calculate_angle(wrist, thumb_mcp, thumb_tip)

               
                if thumb_angle > 35:
                    fingers.append(1)  
                else:
                    fingers.append(0)  

                return sum(fingers)  

        return 0  
def main():
    cap = cv2.VideoCapture(0)
    tracker = HandTracking()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = tracker.detect_hands(frame)
        frame = tracker.draw_hands(frame, results)
        fingers = tracker.count_fingers(results)

        cv2.putText(frame, f'Wyprostowane palce: {fingers}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Hand Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()