import pickle, struct
import msgpack

def read_data(input_path: str, save_set: bool = True):
    with open(input_path, 'rb') as file:
        data = list(file.read())

    data_set = set(data) if save_set else None
    return data, data_set
    
def write_data(output_path: str, data: list)->None:
    with open(output_path, 'wb') as f:
        for item in data:
            f.write(item.to_bytes(1,'big'))

# def write_encoded_data(output_path: str, obj)->None:
#     with open(output_path, "wb") as f:
#         pickle.dump(obj, f)

def write_encoded_data(output_path: str, data:list, data_set:list=None)->None:

    packed_data = bytearray(b''.join(struct.pack('<I', num) for num in data))
    if data_set is not None:
        packed_set = bytearray(b''.join(struct.pack('<I', num) for num in data_set))
        output = (packed_data, packed_set)
    else:
        output = packed_data

    with open(output_path, "wb") as f:
        f.write(msgpack.packb(output, use_bin_type=True))

# def read_encoded_data(input_path: str):
#     with open(input_path, "rb") as f:
#         obj = pickle.load(f)
#     return obj

def read_encoded_data(input_path: str, get_data_set: bool = True):
    with open(input_path, "rb") as f:
        packed_data = msgpack.unpackb(f.read(), raw=False)
    
    if get_data_set: 
        data = list(struct.iter_unpack('<I', packed_data[0]))
        data = [num[0] for num in data]
        data_set = list(struct.iter_unpack('<I', packed_data[1]))
        data_set = [num[0] for num in data_set]
        return data, data_set
    
    else:
        data = list(struct.iter_unpack('<I', packed_data))
        data = [num[0] for num in data]
        return data
