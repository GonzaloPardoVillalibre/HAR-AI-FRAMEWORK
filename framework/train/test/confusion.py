import csv

# with open('/home/gonzalo/Desktop/TFG/framework/train/trainOutcomes/2021-02-15 19:52:39.429685/tmp/test.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     final_list= []
#     for row in csv_reader:
#         array = row[0].replace("\n", " ").replace("[", " ").replace("]", " ")[1:]
#         for char in array:
#             if char.isdigit():
#                 final_list.append(int(char))
#         print("hola")

 csv_reader = csv.reader(file_path+ '/test.csv', delimiter=',')
    test_labels= []
    for row in csv_reader:
        array = row[0].replace("\n", " ").replace("[", " ").replace("]", " ")[1:]
        for char in array:
            if char.isdigit():
                test_labels.append(int(char))