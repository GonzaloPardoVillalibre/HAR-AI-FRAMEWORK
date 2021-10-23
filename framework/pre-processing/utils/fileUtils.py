###########################################
# Methods to manage files and directories #
###########################################
import shutil, os, re, progressbar

def build_output_directory(output_path):
  #Clean output directory
  try:
    shutil.rmtree(output_path)
  except OSError as e:
    pass
    # print("Warn: %s - %s." % (e.filename, e.strerror))
  try:
    os.mkdir(output_path)
  except:
    pass

def load_files(input_path:str):
  _, _, files = next(os.walk(input_path))
  return files

def filter_files_by_regex(files:list, regex:str):
    filtered_list = [val for val in files if re.search(regex, val)]
    return filtered_list

def build_regex_for_contain_items(items:list):
    user_regex_string ="("
    for item in items:
        user_regex_string = (user_regex_string + item + '|')
    user_regex_string = user_regex_string[:-1] + ')'
    user_regex_string = re.compile(user_regex_string)
    return user_regex_string

def initialize_progress_bar(size:int):
  pbar = progressbar.ProgressBar(maxval=size)
  pbar.start()
  return pbar