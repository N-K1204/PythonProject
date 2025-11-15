import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Flatten, GlobalAveragePooling2D, BatchNormalization, Dropout
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Model

def build_ResNet50(input_shape):
    img_input = Input(shape=input_shape)
    base_model = ResNet50(include_top=False, input_tensor=img_input, weights=None)
    image_features = Flatten()(base_model.output)
    output = Dense(1, activation='sigmoid')(image_features)

    model = Model(inputs=img_input, outputs=output)
    return model

def build_ResNet50_improved(input_shape, use_pretrained=True):
    # 画像入力と転移学習ベースモデルの構築
    img_input = Input(shape=input_shape)
    weights = "imagenet" if use_pretrained else None
    base_model = ResNet50(include_top=False, input_tensor=img_input, weights=weights)
    x = GlobalAveragePooling2D()(base_model.output)
    x = Dense(256, activation='relu')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.5)(x)

    # 分類器ヘッドの構成（ResNet50_mlpの構成を踏襲）
    x = Dense(256, activation='relu')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.5)(x)
    x = Dense(128, activation='relu')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.4)(x)
    output = Dense(1, activation='sigmoid')(x)

    model = Model(inputs=img_input, outputs=output)
    return model

if __name__ == '__main__':
    img_shape = (128, 128, 3)
    model = build_ResNet50(img_shape)
    model.summary()