from typing import List, Tuple
from keras.saving import register_keras_serializable
import numpy as np
import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import (
    BatchNormalization,
    Bidirectional,
    Concatenate,
    Dense,
    Dropout,
    GlobalAveragePooling1D,
    GlobalMaxPooling1D,
    Input,
    LSTM,
    Layer,
)
 
 
@register_keras_serializable(package="dgs")
class InvariantFeatureLayer(Layer):
    """Computes biomechanically invariant sign language features."""
 
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
 
    def call(self, inputs: tf.Tensor) -> tf.Tensor:
        # inputs shape: (Batch, 90, 105)
 
        # 1. Wrist-centered Hand Geometry (63 Dims)
        hand = tf.reshape(inputs[:, :, :63], (-1, 90, 21, 3))
        wrist = hand[:, :, 0:1, :]
        wrist_pt = wrist[:, :, 0, :]
 
        hand_rel = hand - wrist
        hand_shape = tf.reshape(hand_rel, (-1, 90, 63))
 
        # 2. Hand Velocity (63 Dims)
        velocity_diff = inputs[:, 1:, :63] - inputs[:, :-1, :63]
        zero_pad = tf.zeros_like(inputs[:, 0:1, :63])
        hand_velocity = tf.concat([zero_pad, velocity_diff], axis=1)
 
        # 3. Handshape & Finger Metrics (14 Dims)
        t_tip = hand[:, :, 4, :]
        i_tip = hand[:, :, 8, :]
        m_tip = hand[:, :, 12, :]
        r_tip = hand[:, :, 16, :]
        p_tip = hand[:, :, 20, :]
 
        i_mcp = hand[:, :, 5, :]
        m_mcp = hand[:, :, 9, :]
        r_mcp = hand[:, :, 13, :]
        p_mcp = hand[:, :, 17, :]
 
        palm_len = tf.norm(m_mcp - wrist_pt, axis=-1, keepdims=True) + 1e-4
 
        ext_i_mcp = tf.norm(i_tip - i_mcp, axis=-1, keepdims=True) / palm_len
        ext_m_mcp = tf.norm(m_tip - m_mcp, axis=-1, keepdims=True) / palm_len
        ext_r_mcp = tf.norm(r_tip - r_mcp, axis=-1, keepdims=True) / palm_len
        ext_p_mcp = tf.norm(p_tip - p_mcp, axis=-1, keepdims=True) / palm_len
 
        flat_hand_score = (
            ext_i_mcp + ext_m_mcp + ext_r_mcp + ext_p_mcp
        ) * 0.25
 
        d_ti = tf.norm(i_tip - t_tip, axis=-1, keepdims=True)
        d_tm = tf.norm(m_tip - t_tip, axis=-1, keepdims=True)
        d_tr = tf.norm(r_tip - t_tip, axis=-1, keepdims=True)
        d_tp = tf.norm(p_tip - t_tip, axis=-1, keepdims=True)
        knospe_score = (d_ti + d_tm + d_tr + d_tp) / (4.0 * palm_len)
        pinch_ratio = d_ti / palm_len
 
        ext_t_w = tf.norm(t_tip - wrist_pt, axis=-1, keepdims=True) / palm_len
        ext_p_w = tf.norm(p_tip - wrist_pt, axis=-1, keepdims=True) / palm_len
        ext_m_w = tf.norm(m_tip - wrist_pt, axis=-1, keepdims=True) / palm_len
        ext_i_w = tf.norm(i_tip - wrist_pt, axis=-1, keepdims=True) / palm_len
 
        ja_shaka = (ext_t_w + ext_p_w) / (ext_m_w + 1e-4)
        index_isolation = ext_i_w / (ext_m_w + ext_p_w + 1e-4)
 
        finger_metrics = tf.concat(
            [
                flat_hand_score,
                knospe_score,
                pinch_ratio,
                ext_i_mcp,
                ext_m_mcp,
                ext_r_mcp,
                ext_p_mcp,
                ext_t_w,
                ext_i_w,
                ext_m_w,
                ext_p_w,
                d_tm / palm_len,
                ja_shaka,
                index_isolation,
            ],
            axis=-1,
        )  # 14 Dims
 
        # 4. Body-Centered Landmarks (13 Dims)
        nose = tf.reshape(inputs[:, :, 63:66], (-1, 90, 3))
        mouth = tf.reshape(inputs[:, :, 93:96], (-1, 90, 3))
 
        hand_y = wrist_pt[:, :, 1:2]
        tip_y = i_tip[:, :, 1:2]
 
        vec_to_mouth = i_tip - mouth
        dist_to_mouth = tf.norm(vec_to_mouth, axis=-1, keepdims=True)
 
        vec_to_nose = i_tip - nose
        dist_to_nose = tf.norm(vec_to_nose, axis=-1, keepdims=True)
 
        dist_to_chest = tf.norm(i_tip, axis=-1, keepdims=True)
 
        # Klare Mundnähe
        mouth_contact = tf.exp(-dist_to_mouth * 6.0)
 
        # Exakte Trennung Stirn/Schläfe vs Mund (Y-Differenz zur Nase):
        # < 0: Stirn (keineAhnung)
        # > 0: Mund / Kinn (essen, danke)
        tip_rel_nose_y = tip_y - nose[:, :, 1:2]
 
        # X-Abstand zur Gesichtsmitte (zentral vor Mund vs seitlich an Stirn)
        tip_rel_nose_x = tf.abs(i_tip[:, :, 0:1] - nose[:, :, 0:1])
 
        body_levels = tf.concat(
            [
                hand_y,  # 1 Dim
                tip_y,  # 1 Dim
                vec_to_mouth,  # 3 Dims
                dist_to_mouth,  # 1 Dim
                mouth_contact,  # 1 Dim
                tip_rel_nose_y,  # 1 Dim: Stirn vs Mund
                tip_rel_nose_x,  # 1 Dim: Gesichtszentrum vs Schläfe
                vec_to_nose,  # 3 Dims
                dist_to_chest,  # 1 Dim
            ],
            axis=-1,
        )  # 13 Dims
 
        # 5. Kinematics (6 Dims)
        i_vel = hand_velocity[:, :, 24:27]
        dx = tf.abs(i_vel[:, :, 0:1])
        dy = tf.abs(i_vel[:, :, 1:2])
        horiz_dominance = dx / (dx + dy + 1e-4)
 
        i_speed = tf.norm(i_vel, axis=-1, keepdims=True) + 1e-4
        direction = i_vel / i_speed
        z_push = i_vel[:, :, 2:3]
        hand_speed = (
            tf.norm(hand_velocity[:, :, 0:3], axis=-1, keepdims=True) + 1e-4
        )
 
        kinematics = tf.concat(
            [horiz_dominance, direction, z_push, hand_speed], axis=-1
        )  # 6 Dims
 
        # Gesamt: 63 + 63 + 14 + 13 + 6 = 159 Dimensionen
        return tf.concat(
            [
                hand_shape,
                hand_velocity,
                finger_metrics,
                body_levels,
                kinematics,
            ],
            axis=-1,
        )
 
    def compute_output_shape(
        self, input_shape: Tuple[int, ...]
    ) -> Tuple[int, ...]:
        return (input_shape[0], input_shape[1], 159)
 
 
def build_model(
    input_shape: tuple,
    train_data: np.ndarray,
    class_names: List[str],
) -> Model:
    """Builds a recurrent DGS network with Peak-Aware Temporal Pooling."""
    inputs = Input(shape=input_shape, name="raw_features")
 
    invariants = InvariantFeatureLayer(name="invariant_features")(inputs)
    x = BatchNormalization(name="batch_norm")(invariants)
 
    x = Bidirectional(
        LSTM(64, return_sequences=True, dropout=0.2), name="bi_lstm_1"
    )(x)
    lstm_seq = Bidirectional(
        LSTM(48, return_sequences=True, dropout=0.2), name="bi_lstm_2"
    )(x)
 
    max_pool = GlobalMaxPooling1D(name="peak_extractor")(lstm_seq)
    avg_pool = GlobalAveragePooling1D(name="context_extractor")(lstm_seq)
    pooled = Concatenate(name="temporal_fusion")([max_pool, avg_pool])
 
    dense = Dense(64, activation="relu", name="dense_features")(pooled)
    dense = BatchNormalization(name="dense_bn")(dense)
    dense = Dropout(0.3, name="dense_dropout")(dense)
 
    outputs = Dense(len(class_names), activation="softmax", name="prediction")(
        dense
    )
 
    model = Model(
        inputs=inputs, outputs=outputs, name="peak_aware_robust_dgs_model"
    )
    return model