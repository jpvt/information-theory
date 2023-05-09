def read_data(input_path: str, save_set: bool = True):
    with open(input_path, 'rb') as text_file:
        data = [byte_val for byte_val in text_file.read()]

    if save_set:
        data_set = set(data)
        return data, data_set
    else:
        return data
    
def write_data(output_path: str, data: list)->None:
    with open(output_path, 'wb') as f:
        for item in data:
            f.write(item.to_bytes(1,'big'))