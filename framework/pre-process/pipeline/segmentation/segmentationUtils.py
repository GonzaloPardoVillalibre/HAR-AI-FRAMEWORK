#########################
# Segmentation Utils    #
#########################
import pandas as pd
def segmentate(file, input_path, output_path, window_size, overlap):
    df = pd.read_csv(input_path + file)
    rows = df.shape[0]
    total_segments = calculate_total_segment_number(rows, window_size, overlap)
    
    first_segment = create_segment(df, 0, window_size)
    first_segment.to_csv(output_path + str(file[:-4]) +'-1.csv', index=False, float_format='%.15f')
    total_segments = total_segments

    second_segment_starting_point = window_size - overlap
    for i in range(total_segments):
        segment = create_segment(df, (i+1)*second_segment_starting_point, window_size)
        segment.to_csv(output_path + str(file[:-4]) +'-' + str(i+2) + '.csv', index=False, float_format='%.15f')


def calculate_total_segment_number(rows, window_size, overlap):
    return (rows-window_size)//(window_size - overlap)

def create_segment(df, start, size):
    return df.iloc[start: start+size]