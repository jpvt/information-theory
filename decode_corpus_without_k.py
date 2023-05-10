from compression import LZW
from compression.helpers import read_data

LZW().decode_from_file("test/data/encoded_corpus16MB.bin",
                       "test/data/decoded_corpus16MB.txt")
decoded_data, _ = read_data("test/data/decoded_corpus16MB.txt", False)
original_data, _ = read_data("test/data/corpus16MB.txt", False)

#print(decoded_data)
#print(original_data)
print("Verificando se arquivo decodificado é igual ao original: ",
      decoded_data == original_data)
