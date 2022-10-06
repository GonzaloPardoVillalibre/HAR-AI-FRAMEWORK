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

         

        #Encoder
        layers.Reshape((input_rows, input_columns)), #squeeze channel dimension
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
# "GRLA_X","GRLA_Y","GRLA_Z","GRUA_X","GRUA_Y","GRUA_Z","GBACK_X","GBACK_Y","GBACK_Z","GLUA_X","GLUA_Y","GLUA_Z","GLLA_X","GLLA_Y","GLLA_Z","GRC_X","GRC_Y","GRC_Z","GRT_X","GRT_Y","GRT_Z","GLT_X","GLT_Y","GLT_Z","GLC_X","GLC_Y","GLC_Z", "ARLA_X","ARLA_Y","ARLA_Z",ARUA_X","ARUA_Y","ARUA_Z","ABACK_X","ABACK_Y","ABACK_Z","ALUA_X","ALUA_Y","ALUA_Z","ALLA_X","ALLA_Y","ALLA_Z", "ARC_X","ARC_Y","ARC_Z",
            #"ART_X","ART_Y","ART_Z","ALT_X","ALT_Y","ALT_Z","ALC_X","ALC_Y","ALC_Z",