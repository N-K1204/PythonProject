import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import ConvLSTM2D, BatchNormalization
from tensorflow.keras.optimizers import RMSprop

'''
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 conv_lstm2d (ConvLSTM2D)    (None, 10, 64, 64, 256)   2387968   
                                                                 
 batch_normalization (BatchN  (None, 10, 64, 64, 256)  1024      
 ormalization)                                                   
                                                                 
 conv_lstm2d_1 (ConvLSTM2D)  (None, 10, 64, 64, 64)    737536    
                                                                 
 batch_normalization_1 (Batc  (None, 10, 64, 64, 64)   256       
 hNormalization)                                                 
                                                                 
 conv_lstm2d_2 (ConvLSTM2D)  (None, 10, 64, 64, 64)    295168    
                                                                 
 batch_normalization_2 (Batc  (None, 10, 64, 64, 64)   256       
 hNormalization)                                                 
                                                                 
 conv_lstm2d_3 (ConvLSTM2D)  (None, 64, 64, 3)         816       
                                                                 
=================================================================
Total params: 3,423,024
Trainable params: 3,422,256
Non-trainable params: 768
_________________________________________________________________
'''


def ConvLSTM_network(input_shape, return_seq=False):
    model = Sequential()
    
    # 3層の畳み込みLSTMブロックとBatchNormalization
    model.add(ConvLSTM2D(filters=256, kernel_size=(3, 3), padding='same', return_sequences=True, input_shape=input_shape))
    model.add(BatchNormalization())
    model.add(ConvLSTM2D(filters=64, kernel_size=(3, 3), padding='same', return_sequences=True))
    model.add(BatchNormalization())
    model.add(ConvLSTM2D(filters=64, kernel_size=(3, 3), padding='same', return_sequences=True))
    model.add(BatchNormalization())
    
    # 1x1で畳み込み
    model.add(ConvLSTM2D(filters=3, kernel_size=(1, 1), padding='same', activation='tanh', return_sequences=return_seq))

    
    return model
    

if __name__ == '__main__':
    # modelの作成
    model = ConvLSTM_network((10, 128, 128, 3), return_seq=True)
    model.compile(optimizer='rmsprop', loss='mae', metrics=['accuracy'])
    model.summary()

