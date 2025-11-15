import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Flatten, GlobalAveragePooling2D, Concatenate, Dropout, BatchNormalization
from tensorflow.keras.applications import ResNet50

# ResNet50とMLPを組み合わせたモデル
def build_ResNet50_mlp(input_shape, numerical_shape, categorical_shape):
    img_input = Input(shape=input_shape)
    base_model = ResNet50(include_top=False, input_tensor=img_input, weights=None)
    image_features = Flatten()(base_model.output)

    numerical_input = Input(shape=numerical_shape)
    numerical_features = Dense(128, activation='relu')(numerical_input)
    
    categorical_input = Input(shape=categorical_shape)
    categorical_features = Dense(128, activation='relu')(categorical_input)

    combined_features = Concatenate()([image_features, numerical_features, categorical_features])
    x = Dense(256, activation='relu')(combined_features)
    output = Dense(1, activation='sigmoid')(x)

    model = Model(inputs=[img_input, numerical_input, categorical_input], outputs=output)
    return model

def build_ResNet50_mlp_improved(input_shape, numerical_shape, categorical_shape, use_pretrained=True):
    # 画像入力と転移学習ベースモデルの構築
    img_input = Input(shape=input_shape)
    weights = "imagenet" if use_pretrained else None
    base_model = ResNet50(include_top=False, input_tensor=img_input, weights=weights)
    image_features = GlobalAveragePooling2D()(base_model.output)
    image_features = Dense(256, activation='relu')(image_features)
    image_features = BatchNormalization()(image_features)
    image_features = Dropout(0.5)(image_features)

    # 数値データの入力と処理
    numerical_input = Input(shape=numerical_shape)
    numerical_features = Dense(64, activation='relu')(numerical_input)
    numerical_features = BatchNormalization()(numerical_features)
    numerical_features = Dropout(0.3)(numerical_features)

    # カテゴリーデータの入力と処理
    categorical_input = Input(shape=categorical_shape)
    categorical_features = Dense(64, activation='relu')(categorical_input)
    categorical_features = BatchNormalization()(categorical_features)
    categorical_features = Dropout(0.3)(categorical_features)

    # 複数の特徴を統合
    combined_features = Concatenate()([image_features, numerical_features, categorical_features])
    
    # 統合後の全結合層
    x = Dense(256, activation='relu')(combined_features)
    x = BatchNormalization()(x)
    x = Dropout(0.5)(x)
    x = Dense(128, activation='relu')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.4)(x)
    output = Dense(1, activation='sigmoid')(x)

    model = Model(inputs=[img_input, numerical_input, categorical_input], outputs=output)
    return model

if __name__ == '__main__':
    img_shape = (128, 128, 3)
    numerical_shape = (2)
    categorical_shape = (17)
    model = build_ResNet50_mlp_improved(img_shape, numerical_shape, categorical_shape)
    model.summary()