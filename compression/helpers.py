import pickle

def read_data(input_path: str, save_set: bool = True):
    with open(input_path, 'rb') as text_file:
        data = [byte_val for byte_val in text_file.read()]

    data_set = set(data) if save_set else None
    return data, data_set
    
def write_data(output_path: str, data: list)->None:
    with open(output_path, 'wb') as f:
        for item in data:
            f.write(item.to_bytes(1,'big'))

def write_encoded_data(output_path: str, obj)->None:
    with open(output_path, "wb") as f:
        pickle.dump(obj, f)

def read_encoded_data(input_path: str):
    with open(input_path, "rb") as f:
        obj = pickle.load(f)
    return obj
