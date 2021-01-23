import os, re, json

def filter_files_by_regex(files:list, regex:str):
    filtered_list = [val for val in files if re.search(regex, val)]
    return filtered_list

def build_regex_for_subjects(subjects:list):
    user_regex_string ="^("
    for subject in subjects:
        user_regex_string = (user_regex_string + subject + '|')
    user_regex_string = user_regex_string[:-1] + ')'
    user_regex_string = re.compile(user_regex_string)
    return user_regex_string

def split_dataset(files:list, cfg:json):
    # Load train set
    train_user_regex_string = build_regex_for_subjects(cfg["train-subjects"])
    train_files = filter_files_by_regex(files, train_user_regex_string)
    # Load test set
    test_user_regex_string = build_regex_for_subjects(cfg["test-subjects"])
    test_files = filter_files_by_regex(files, test_user_regex_string)
    # Load validation set
    validation_user_regex_string = build_regex_for_subjects(cfg["validation-subjects"])
    validation_files = filter_files_by_regex(files, validation_user_regex_string)

    print("Total original train files: " + str(len(filter_files_by_regex(train_files, r'-0.csv$'))))
    print("Total train files including rotation: " + str(len(train_files)))
    print("Total original validation files: " + str(len(filter_files_by_regex(validation_files, r'-0.csv$'))))
    print("Total validation files including rotation: " + str(len(validation_files)))
    print("Total original test files: " + str(len(filter_files_by_regex(test_files, r'-0.csv$'))))
    print("Total test files including rotation: " + str(len(test_files)))

    return train_files, test_files, validation_files