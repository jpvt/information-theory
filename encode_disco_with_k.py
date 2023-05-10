from compression import LZW
from compression.helpers import read_data
import os

file = "disco.mp4"
times = []
RC1 = []
RC2 = []

with open(f"test/data/log_{file}.txt", "w") as f:
    f.write(f"dict_k\t\t| Time\t\t| RC1\t\t| RC2\n")

len_original_file = os.path.getsize(f"test/data/{file}")
for dict_k in range(9, 17):
    lzw = LZW(dictionary_k=dict_k)
    output, dictionary, total_time = lzw.encode_from_file(
        f"test/data/{file}", False)

    times.append(total_time)

    lzw.save_encoded_data(f"test/data/varying_k/encoded_{file}")
    del lzw

    LZW().decode_from_file(
        f"test/data/varying_k/encoded_{file}.{dict_k}", f"test/data/varying_k/decoded_{file}_with_k{dict_k}.txt")
    decoded_data, _ = read_data(
        f"test/data/varying_k/decoded_{file}_with_k{dict_k}.txt", False)
    original_data, _ = read_data(f"test/data/{file}", False)

    len_encoded_file = os.path.getsize(
        f"test/data/varying_k/encoded_{file}.{dict_k}")

    RC1.append(len_original_file/len_encoded_file)
    RC2.append(len_original_file/(len(output)*dict_k/8))

    with open(f"test/data/log_{file}.txt", "a") as f:
        f.write(
            f"{dict_k}\t\t| {total_time:.4}\t\t| {RC1[-1]:.4}\t\t| {RC2[-1]:.4}\n")
