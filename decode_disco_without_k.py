from compression import LZW
from compression.helpers import read_data

LZW().decode_from_file("test/data/encoded_disco.bin",
                       "test/data/decoded_disco.mp4")

decoded_data, _ = read_data("test/data/decoded_disco.mp4", False)
original_data, _ = read_data("test/data/disco.mp4", False)

# print("Verificando se arquivo decodificado é igual ao original: ",
#     decoded_data == original_data)
