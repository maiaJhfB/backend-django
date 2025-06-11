import cv2
import mediapipe as mp
import numpy as np
import math
from collections import deque
from scipy.spatial.distance import euclidean
from scipy.interpolate import interp1d

def rotate_image(image, angle):
    """Rotates a BGRA image around its center without clipping."""
    if angle == 0:
        return image

    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    # Get the rotation matrix, then the sine and cosine
    M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # Compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # Adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    # Perform the actual rotation and return the image
    rotated_img = cv2.warpAffine(image, M, (nW, nH), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    return rotated_img

class ImprovedTattooAugmenter:
    def __init__(self, tattoo_image_path, target_body_part="forearm", bg_color_threshold=10,
                 smoothing_window=5, blur_kernel_size=7, rotation_angle=0, use_gpu=False):
        """Initializes the ImprovedTattooAugmenter with enhanced stability features.

        Args:
            tattoo_image_path (str): Path to the tattoo image.
            target_body_part (str): Target body part (currently "forearm").
            bg_color_threshold (int): Tolerance for background removal.
            smoothing_window (int): Number of frames for smoothing (increased default).
            blur_kernel_size (int): Odd integer for Gaussian blur kernel size.
            rotation_angle (float): Angle in degrees to rotate the tattoo image.
            use_gpu (bool): Attempt GPU usage for MediaPipe.
        """
        self.target_body_part = target_body_part
        self.bg_color_threshold = bg_color_threshold
        self.smoothing_window = max(3, smoothing_window)  # Minimum 3 frames
        self.blur_kernel_size = blur_kernel_size if blur_kernel_size % 2 != 0 else blur_kernel_size + 1
        self.rotation_angle = rotation_angle

        # Load and preprocess tattoo
        tattoo_image_raw = cv2.imread(tattoo_image_path, cv2.IMREAD_UNCHANGED)
        if tattoo_image_raw is None:
            raise FileNotFoundError(f"Tattoo image not found at: {tattoo_image_path}")

        tattoo_no_bg = self._preprocess_remove_background(tattoo_image_raw)
        self.tattoo_image_processed = rotate_image(tattoo_no_bg, self.rotation_angle)

        # MediaPipe setup with higher confidence
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.7,  # Increased confidence
            min_tracking_confidence=0.7,   # Increased confidence
            model_complexity=2,             # Higher complexity for better accuracy
            smooth_landmarks=True           # Enable built-in smoothing
        )

        # Enhanced tracking variables
        self.dest_pts_history = deque(maxlen=self.smoothing_window)
        self.landmark_history = deque(maxlen=self.smoothing_window)
        self.visibility_history = deque(maxlen=self.smoothing_window)
        
        # Kalman filter components for each landmark point
        self.kalman_filters = {}
        self.last_valid_roi = None
        self.frames_without_detection = 0
        self.max_frames_without_detection = 10
        
        # Stability thresholds
        self.movement_threshold = 0.02  # 2% of image width/height
        self.angle_stability_threshold = 5.0  # degrees
        self.size_stability_threshold = 0.1   # 10% size change
        
        print(f"ImprovedTattooAugmenter initialized for target: {self.target_body_part}")
        print(f"Enhanced stability features: Kalman filtering, movement prediction, adaptive smoothing")

    def _create_kalman_filter(self):
        """Creates a Kalman filter for landmark tracking."""
        kalman = cv2.KalmanFilter(4, 2)  # 4 state variables (x, y, vx, vy), 2 measurements (x, y)
        kalman.measurementMatrix = np.array([[1, 0, 0, 0],
                                           [0, 1, 0, 0]], np.float32)
        kalman.transitionMatrix = np.array([[1, 0, 1, 0],
                                          [0, 1, 0, 1],
                                          [0, 0, 1, 0],
                                          [0, 0, 0, 1]], np.float32)
        kalman.processNoiseCov = 0.03 * np.eye(4, dtype=np.float32)
        kalman.measurementNoiseCov = 0.1 * np.eye(2, dtype=np.float32)
        kalman.errorCovPost = 0.1 * np.eye(4, dtype=np.float32)
        return kalman

    def _get_smoothed_landmarks(self, landmarks, image_shape):
        """Apply multiple levels of smoothing to landmarks."""
        h, w = image_shape[:2]
        lm = landmarks.landmark
        
        # Get key landmark indices
        elbow_idx = self.mp_pose.PoseLandmark.RIGHT_ELBOW.value
        wrist_idx = self.mp_pose.PoseLandmark.RIGHT_WRIST.value
        
        # Check for left arm if right arm is not visible enough
        left_elbow_idx = self.mp_pose.PoseLandmark.LEFT_ELBOW.value
        left_wrist_idx = self.mp_pose.PoseLandmark.LEFT_WRIST.value
        
        # Determine which arm to use based on visibility
        if (lm[left_elbow_idx].visibility > lm[elbow_idx].visibility and 
            lm[left_wrist_idx].visibility > lm[wrist_idx].visibility):
            elbow_idx, wrist_idx = left_elbow_idx, left_wrist_idx
        
        # Extract current landmarks
        elbow_pt = np.array([lm[elbow_idx].x * w, lm[elbow_idx].y * h], dtype=np.float32)
        wrist_pt = np.array([lm[wrist_idx].x * w, lm[wrist_idx].y * h], dtype=np.float32)
        visibility = min(lm[elbow_idx].visibility, lm[wrist_idx].visibility)
        
        # Initialize Kalman filters if needed
        if 'elbow' not in self.kalman_filters:
            self.kalman_filters['elbow'] = self._create_kalman_filter()
            self.kalman_filters['wrist'] = self._create_kalman_filter()
            # Initialize with current position - fix dimensions
            self.kalman_filters['elbow'].statePre = np.array([[elbow_pt[0]], [elbow_pt[1]], [0], [0]], dtype=np.float32)
            self.kalman_filters['wrist'].statePre = np.array([[wrist_pt[0]], [wrist_pt[1]], [0], [0]], dtype=np.float32)
            self.kalman_filters['elbow'].statePost = self.kalman_filters['elbow'].statePre.copy()
            self.kalman_filters['wrist'].statePost = self.kalman_filters['wrist'].statePre.copy()
        
        # Apply Kalman filtering
        if visibility > 0.5:
            # Predict
            elbow_pred = self.kalman_filters['elbow'].predict()
            wrist_pred = self.kalman_filters['wrist'].predict()
            
            # Update with measurements - fix dimensions
            elbow_measurement = np.array([[elbow_pt[0]], [elbow_pt[1]]], dtype=np.float32)
            wrist_measurement = np.array([[wrist_pt[0]], [wrist_pt[1]]], dtype=np.float32)
            
            self.kalman_filters['elbow'].correct(elbow_measurement)
            self.kalman_filters['wrist'].correct(wrist_measurement)
            
            # Use corrected state - extract x,y coordinates
            elbow_filtered = np.array([self.kalman_filters['elbow'].statePost[0, 0], 
                                     self.kalman_filters['elbow'].statePost[1, 0]], dtype=np.float32)
            wrist_filtered = np.array([self.kalman_filters['wrist'].statePost[0, 0], 
                                     self.kalman_filters['wrist'].statePost[1, 0]], dtype=np.float32)
        else:
            # Use prediction only when visibility is low
            elbow_pred = self.kalman_filters['elbow'].predict()
            wrist_pred = self.kalman_filters['wrist'].predict()
            elbow_filtered = np.array([elbow_pred[0, 0], elbow_pred[1, 0]], dtype=np.float32)
            wrist_filtered = np.array([wrist_pred[0, 0], wrist_pred[1, 0]], dtype=np.float32)
        
        return elbow_filtered, wrist_filtered, visibility

    def _get_simple_smoothed_landmarks(self, landmarks, image_shape):
        """Simple smoothing fallback method."""
        h, w = image_shape[:2]
        lm = landmarks.landmark
        
        # Get key landmark indices
        elbow_idx = self.mp_pose.PoseLandmark.RIGHT_ELBOW.value
        wrist_idx = self.mp_pose.PoseLandmark.RIGHT_WRIST.value
        
        # Check for left arm if right arm is not visible enough
        left_elbow_idx = self.mp_pose.PoseLandmark.LEFT_ELBOW.value
        left_wrist_idx = self.mp_pose.PoseLandmark.LEFT_WRIST.value
        
        # Determine which arm to use based on visibility
        if (lm[left_elbow_idx].visibility > lm[elbow_idx].visibility and 
            lm[left_wrist_idx].visibility > lm[wrist_idx].visibility):
            elbow_idx, wrist_idx = left_elbow_idx, left_wrist_idx
        
        # Extract current landmarks
        elbow_pt = np.array([lm[elbow_idx].x * w, lm[elbow_idx].y * h], dtype=np.float32)
        wrist_pt = np.array([lm[wrist_idx].x * w, lm[wrist_idx].y * h], dtype=np.float32)
        visibility = min(lm[elbow_idx].visibility, lm[wrist_idx].visibility)
        
        # Simple exponential moving average
        if hasattr(self, 'prev_elbow') and hasattr(self, 'prev_wrist'):
            alpha = 0.7  # Smoothing factor
            elbow_pt = alpha * self.prev_elbow + (1 - alpha) * elbow_pt
            wrist_pt = alpha * self.prev_wrist + (1 - alpha) * wrist_pt
        
        self.prev_elbow = elbow_pt.copy()
        self.prev_wrist = wrist_pt.copy()
        
        return elbow_pt, wrist_pt, visibility

    def _preprocess_remove_background(self, img):
        """Converts the image to BGRA and makes the white background transparent."""
        # Ensure image is BGRA
        if img.ndim == 2:
            img_bgra = cv2.cvtColor(img, cv2.COLOR_GRAY2BGRA)
            img_bgra[:, :, 3] = 255
        elif img.shape[2] == 3:
            img_bgra = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
            img_bgra[:, :, 3] = 255
        elif img.shape[2] == 4:
            img_bgra = img.copy()
        else:
            return img

        # Background Removal Logic
        lower_white = np.array([255 - self.bg_color_threshold] * 3, dtype=np.uint8)
        upper_white = np.array([255] * 3, dtype=np.uint8)
        opaque_mask = (img_bgra[:, :, 3] > 200).astype(np.uint8) * 255
        bgr_channels = img_bgra[:, :, :3]
        white_mask = cv2.inRange(bgr_channels, lower_white, upper_white)
        background_mask = cv2.bitwise_and(white_mask, white_mask, mask=opaque_mask)
        alpha_channel = img_bgra[:, :, 3]
        num_transparent = np.sum(background_mask == 255)
        if num_transparent > 0:
            alpha_channel[background_mask == 255] = 0
            img_bgra[:, :, 3] = alpha_channel
        
        return img_bgra

    def _get_body_part_roi_enhanced(self, landmarks, image_shape):
        """Enhanced ROI detection with stability improvements."""
        h, w = image_shape[:2]
        
        try:
            # Get smoothed landmarks using Kalman filtering
            try:
                elbow_pt, wrist_pt, visibility = self._get_smoothed_landmarks(landmarks, image_shape)
            except Exception as kalman_error:
                print(f"Kalman filter error, using simple smoothing: {kalman_error}")
                # Fallback to simple smoothing
                elbow_pt, wrist_pt, visibility = self._get_simple_smoothed_landmarks(landmarks, image_shape)
            
            if visibility < 0.3:
                self.frames_without_detection += 1
                if (self.last_valid_roi is not None and 
                    self.frames_without_detection < self.max_frames_without_detection):
                    # Use last valid ROI with slight degradation
                    return self.last_valid_roi
                return None
            else:
                self.frames_without_detection = 0
            
            # Calculate forearm vector and properties
            v_forearm = wrist_pt - elbow_pt
            forearm_length = np.linalg.norm(v_forearm)
            
            if forearm_length < 30:  # Minimum realistic forearm length
                return None
            
            # Adaptive width based on distance from camera (forearm length)
            base_width_factor = 0.35
            width_adjustment = max(0.8, min(1.2, 100.0 / forearm_length))
            forearm_width_factor = base_width_factor * width_adjustment
            forearm_width = forearm_length * forearm_width_factor
            
            # Create ROI corners
            unit_v_forearm = v_forearm / forearm_length
            v_perp = np.array([-unit_v_forearm[1], unit_v_forearm[0]]) * (forearm_width / 2)
            
            corner1 = elbow_pt + v_perp
            corner2 = elbow_pt - v_perp
            corner3 = wrist_pt - v_perp
            corner4 = wrist_pt + v_perp
            
            dest_pts = np.array([corner1, corner2, corner3, corner4], dtype="float32")
            
            # Stability check against previous frame
            if self.last_valid_roi is not None:
                movement = np.mean(np.linalg.norm(dest_pts - self.last_valid_roi, axis=1))
                movement_ratio = movement / min(w, h)
                
                if movement_ratio > self.movement_threshold:
                    # Large movement detected, blend with previous position
                    blend_factor = 0.7  # Favor previous position
                    dest_pts = blend_factor * self.last_valid_roi + (1 - blend_factor) * dest_pts
            
            self.last_valid_roi = dest_pts.copy()
            return dest_pts
            
        except Exception as e:
            print(f"Error in ROI detection: {e}")
            return None

    def _adaptive_smoothing(self, current_pts):
        """Apply adaptive smoothing based on movement speed."""
        self.dest_pts_history.append(current_pts)
        
        if len(self.dest_pts_history) < 2:
            return current_pts
        
        # Calculate movement speed
        prev_pts = self.dest_pts_history[-2]
        movement_speed = np.mean(np.linalg.norm(current_pts - prev_pts, axis=1))
        
        # Adaptive smoothing factor based on movement
        if movement_speed < 5:  # Slow movement
            alpha = 0.8  # Heavy smoothing
        elif movement_speed < 15:  # Medium movement
            alpha = 0.6  # Medium smoothing
        else:  # Fast movement
            alpha = 0.3  # Light smoothing
        
        # Exponential moving average with adaptive alpha
        if len(self.dest_pts_history) >= 2:
            smoothed_pts = alpha * prev_pts + (1 - alpha) * current_pts
        else:
            smoothed_pts = current_pts
        
        return smoothed_pts

    def _insert_tattoo_geometric_enhanced(self, frame, current_dest_pts):
        """Enhanced tattoo insertion with improved blending and stability."""
        
        # Apply adaptive smoothing
        smoothed_dest_pts = self._adaptive_smoothing(current_dest_pts)
        
        tattoo_to_warp = self.tattoo_image_processed
        tattoo_h, tattoo_w = tattoo_to_warp.shape[:2]
        src_pts = np.array([[0, 0], [tattoo_w - 1, 0], [tattoo_w - 1, tattoo_h - 1], [0, tattoo_h - 1]], dtype="float32")

        try:
            # Get perspective transform with error handling
            M = cv2.getPerspectiveTransform(src_pts, smoothed_dest_pts)
            
            # Check for degenerate transformation
            det = cv2.determinant(M[:2, :2])
            if abs(det) < 1e-6:
                return frame
            
            warped_tattoo = cv2.warpPerspective(
                tattoo_to_warp, M, (frame.shape[1], frame.shape[0]), 
                flags=cv2.INTER_LINEAR,
                borderMode=cv2.BORDER_CONSTANT,
                borderValue=(0, 0, 0, 0)
            )
            
        except Exception as e:
            print(f"Error in perspective transform: {e}")
            return frame

        if warped_tattoo.shape[2] != 4:
            return frame

        # Enhanced alpha blending with feathering
        alpha_channel = warped_tattoo[:, :, 3].astype(np.float32) / 255.0
        
        # Create distance transform for better edge blending
        alpha_binary = (alpha_channel > 0.1).astype(np.uint8)
        dist_transform = cv2.distanceTransform(alpha_binary, cv2.DIST_L2, 5)
        feather_radius = min(10, self.blur_kernel_size)
        feathered_alpha = np.minimum(alpha_channel, dist_transform / feather_radius)
        
        # Apply Gaussian blur for soft edges
        blurred_alpha = cv2.GaussianBlur(feathered_alpha, (self.blur_kernel_size, self.blur_kernel_size), 0)
        alpha_mask_3d = blurred_alpha[:, :, np.newaxis]
        
        # Perform alpha blending
        frame_float = frame.astype(np.float32)
        warped_bgr = warped_tattoo[:, :, :3].astype(np.float32)
        blended_float = frame_float * (1 - alpha_mask_3d) + warped_bgr * alpha_mask_3d
        
        # Apply result only where alpha > threshold
        mask_alpha_gt_0 = blurred_alpha > 0.01
        output_frame = frame.copy()
        output_frame[mask_alpha_gt_0] = blended_float[mask_alpha_gt_0].astype(np.uint8)

        return output_frame

    def process_frame(self, frame):
        """Processes a single frame with enhanced stability."""
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False
        results = self.pose.process(image_rgb)
        image_bgr = frame.copy()
        image_bgr.flags.writeable = True

        output_frame = image_bgr
        
        if results.pose_landmarks:
            current_dest_pts = self._get_body_part_roi_enhanced(results.pose_landmarks, frame.shape)
            
            if current_dest_pts is not None:
                output_frame = self._insert_tattoo_geometric_enhanced(output_frame, current_dest_pts)
        else:
            # No landmarks detected, increment counter
            self.frames_without_detection += 1
            if (self.last_valid_roi is not None and 
                self.frames_without_detection < self.max_frames_without_detection):
                # Use last known position
                output_frame = self._insert_tattoo_geometric_enhanced(output_frame, self.last_valid_roi)

        return output_frame

    def run_on_webcam(self):
        """Runs the enhanced tattoo augmentation on webcam."""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Cannot open webcam.")
            return
            
        # Set camera properties for better performance
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        print("Starting enhanced webcam feed. Press 'q' to quit.")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Cannot read frame from webcam.")
                break
                
            processed_frame = self.process_frame(frame)
            cv2.imshow("Enhanced Tattoo Augmentation - Press Q to Quit", processed_frame)
            
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
                
        cap.release()
        cv2.destroyAllWindows()
        print("Webcam feed stopped.")

    def run_on_image(self, input_image_path, output_image_path):
        """Runs the enhanced tattoo augmentation on a single image."""
        frame = cv2.imread(input_image_path)
        if frame is None:
            print(f"Error: Cannot read image file: {input_image_path}")
            return
            
        print(f"Processing image: {input_image_path}")
        # Reset tracking for single image
        self.dest_pts_history.clear()
        self.landmark_history.clear()
        self.kalman_filters.clear()
        self.last_valid_roi = None
        
        processed_frame = self.process_frame(frame)
        cv2.imwrite(output_image_path, processed_frame)
        print(f"Processed image saved to: {output_image_path}")

    def close(self):
        """Releases resources."""
        self.pose.close()
        print("Enhanced MediaPipe Pose resources released.")

# Alias for backward compatibility
TattooAugmenter = ImprovedTattooAugmenter