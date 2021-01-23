import utils.utils as utils
import neuralNetworks.N2 as nn
import utils.dataGenerator as datagen
import tensorflow as tf 
import re, os, json

main_path = os.getcwd()
final_input_path = main_path + '/vicon/pre-processing/final-dataset/orientation/'
cfg_filename = main_path + '/vicon/processing/config.json'

# Load some useful configuration
with open(cfg_filename) as f:
  cfg = json.load(f)

_, _, files = next(os.walk(final_input_path))

rows, columns, movements, batch_size, train_steps, validation_steps, test_steps, epochs = utils.extract_info_from_config(cfg)

##########
#  Main  #
##########

train_set, validation_set, test_set = utils.split_dataset(files, cfg)

train_dataset = tf.data.Dataset.from_generator(datagen.tf_data_generator,args= [final_input_path, train_set, batch_size, movements],output_types = (tf.float32, tf.float32), output_shapes = ((None,rows,columns,1),(None,)))
test_dataset = tf.data.Dataset.from_generator(datagen.tf_data_generator,args= [final_input_path, test_set, batch_size, movements],output_types = (tf.float32, tf.float32), output_shapes = ((None,rows,columns,1),(None,)))
validation_dataset = tf.data.Dataset.from_generator(datagen.tf_data_generator,args= [final_input_path, validation_set, batch_size, movements],output_types = (tf.float32, tf.float32), output_shapes = ((None,rows,columns,1),(None,)))

model = nn.load_model()

model.fit(train_dataset, validation_data = validation_dataset, steps_per_epoch = train_steps,
         validation_steps = validation_steps, epochs = epochs)

test_loss, test_accuracy = model.evaluate(test_dataset, steps = test_steps)

print("Test loss: ", test_loss)
print("Test accuracy:", test_accuracy)