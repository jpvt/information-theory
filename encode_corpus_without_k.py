from compression import LZW

input_file_path = "test/data/corpus16MB.txt"
output_file_path = "test/data/encoded_corpus16MB"

lzw = LZW()
lzw.encode_from_file(input_file_path, verbose=False)
lzw.save_encoded_data(output_file_path)
