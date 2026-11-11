from pathlib import Path
 
# Pfade
BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR / "dataset"
FEATURE_DIR = BASE_DIR / "features"
MODEL_DIR = BASE_DIR / "trained_models"
TEMP_DIR = BASE_DIR / "temp"
TEST_VIDEOS = BASE_DIR / "testvideos"
TEST_FEATURE_DIR = BASE_DIR / "test_features"
 
# MediaPipe Konfiguration
POSE_LANDMARKS = 33
HAND_LANDMARKS = 21
MIN_DETECTION_CONFIDENCE = 0.6
MIN_TRACKING_CONFIDENCE = 0.6
 
# Sequenz- & Feature-Dimensionen
# 21 Hand * 3 + 7 Pose * 3 + 7 Face * 3 = 105 Features
HAND_FEATURE_DIMS = 63
POSE_FEATURE_DIMS = 21
FACE_FEATURE_DIMS = 21

TARGET_FRAMES = 90
FEATURES_PER_FRAME = HAND_FEATURE_DIMS + POSE_FEATURE_DIMS + FACE_FEATURE_DIMS  # 105
INVARIANT_FEATURE_DIMS = 139  # 63 Hand + 10 Finger-Metriken + 3 Kopfvektor + 63 Dynamik

# Training Hyperparameter
MAX_EPOCHS = 150
PATIENCE_EARLY_STOPPING = 30
PATIENCE_REDUCE_LR = 6
BATCH_SIZE = 8
LEARNING_RATE = 0.001
TEST_SIZE = 0.20
VALIDATION_SPLIT = 0.20
 
# Normalisierung
MIN_SHOULDER_WIDTH = 0.05
MAX_ABS_FEATURE = 5.0