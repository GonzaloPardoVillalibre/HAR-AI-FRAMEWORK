import shutil, os

##################################################################
# Methods to manage files and directories                        #
##################################################################
def build_output_directory(output_path):
  #Clean output directory
  try:
    shutil.rmtree(output_path)
  except OSError as e:
    print("Error: %s - %s." % (e.filename, e.strerror))
  try:
    os.mkdir(output_path)
  except:
    pass

def load_files(input_path:str):
  _, _, files = next(os.walk(input_path))
  try:
    files.remove('config.json')
  except :
    print("config.json not in list")
  return files
