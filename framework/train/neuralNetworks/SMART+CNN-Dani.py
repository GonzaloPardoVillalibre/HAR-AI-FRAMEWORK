import tensorflow as tf
import utils.utils as nnUtils
from tensorflow.keras import layers
from sklearn.neighbors import KNeighborsClassifier
import math



def load_model(input_rows:int, input_columns:int, channels:int, movements_number:int):

    nnUtils.restrict_to_physcial_gpu()
    nnUtils.set_memory_growth()
    callback = tf.keras.callbacks.EarlyStopping(monitor='accuracy', patience=15)
    lstm_input_rows = math.ceil(input_rows/8)
    lstm_input_columns = math.ceil(input_columns/8)

    model = tf.keras.Sequential([

         layers.Conv2D(64, activation = "relu", input_shape = (input_rows,input_columns,channels), kernel_size=3,padding='same',strides=1),
        layers.MaxPooling2D(pool_size=2, strides=2, padding='same'),
        layers.BatchNormalization(axis=1),
        layers.Conv2D(64, activation='relu', kernel_size=4,padding='same',strides=1),
        layers.MaxPooling2D(pool_size=2, strides=2, padding='same'),
        layers.BatchNormalization(axis=1),
        layers.Conv2D(64, activation='relu', kernel_size=4,padding='same',strides=1),
        layers.MaxPooling2D(pool_size=2, strides=2, padding='same'),
        layers.BatchNormalization(axis=1),
        layers.Dropout(0.5),
        layers.Reshape((lstm_input_rows,lstm_input_columns*64)),


        #Encoder
        #layers.Reshape((input_rows, input_columns)), #squeeze channel dimension
        layers.LSTM(units=256, return_sequences=True),
        layers.LSTM(units=128,return_sequences=False),
        layers.BatchNormalization(),
        layers.Flatten(),
        layers.Dropout(0.5),
        
       
        layers.RepeatVector(movements_number),


        #Decoder
        layers.LSTM(units=128,return_sequences=True),
        layers.LSTM(units=256, return_sequences=True),

        layers.TimeDistributed(tf.keras.layers.Dense(256)),
        layers.TimeDistributed(tf.keras.layers.Dense(units=3)),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
     
        layers.Flatten(),
        layers.Dense(movements_number, activation = "softmax")
        #Output vector goes to knn
        #KNeighborsClassifier(n_neighbors = 5)
        #clustering = DBSCAN(eps=3, min_samples=2).fit(X)
        ])

#knn.fit(X_train, y_train)

#knn.score(X_test, y_test)
   

    # model.summary()

    model.compile(loss = "sparse_categorical_crossentropy", optimizer = "adam" , metrics = ["accuracy"])

    return model

# Autoencoder
# "RLA_1", "RLA_2", "RLA_3", "RLA_4","ARLA_X","ARLA_Y","ARLA_Z","GRLA_X","GRLA_Y","GRLA_Z"
# "RUA_1", "RUA_2", "RUA_3", "RUA_4","ARUA_X","ARUA_Y","ARUA_Z","GRUA_X","GRUA_Y","GRUA_Z"
# "BACK_1", "BACK_2", "BACK_3", "BACK_4","ABACK_X","ABACK_Y","ABACK_Z", "GBACK_X","GBACK_Y","GBACK_Z"
# "LUA_1", "LUA_2", "LUA_3", "LUA_4","ALUA_X","ALUA_Y","ALUA_Z","GLUA_X","GLUA_Y","GLUA_Z"
# "LLA_1", "LLA_2", "LLA_3", "LLA_4", "ALLA_X","ALLA_Y","ALLA_Z","GLLA_X","GLLA_Y","GLLA_Z"
# "GRC_X","GRC_Y","GRC_Z", "ARC_X","ARC_Y","ARC_Z",
# "GRT_X","GRT_Y","GRT_Z","ART_X","ART_Y","ART_Z",
# "GLT_X","GLT_Y","GLT_Z","ALT_X","ALT_Y","ALT_Z",
# "GLC_X","GLC_Y","GLC_Z","ALC_X","ALC_Y","ALC_Z",