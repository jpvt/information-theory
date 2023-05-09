from compression.helpers import read_data, write_data
from time import time

class LZW:

    def __init__(
            self,
            dictionary_k: int = -1
    ) -> None:
        if dictionary_k != -1:
            assert dictionary_k >= 3
        self.dictionary_k = dictionary_k


    def encode(
            self,
            original_data: list,
            original_set: set, 
            verbose: bool = True
    )->tuple:
        
        if verbose:
            total_time_start = time()

        self.original_data, self.original_set = original_data, original_set
        del original_data 
        del original_set

        if verbose:
            encoding_time_start = time()

        dictionary = {(value,): i for i, value in enumerate(self.original_set)}

        if verbose:
            print(f"Starting dictionary: {dictionary}")

        output = []
        current_arr = (self.original_data[0],)
        next_idx = len(self.original_set)

        for num in self.original_data[1:]:
            combined_arr = current_arr + (num,)
            if combined_arr in dictionary:
                current_arr = combined_arr
            else:
                output.append(dictionary[current_arr])
                dictionary[combined_arr] = next_idx
                next_idx += 1
                current_arr = (num,)

        if current_arr:
            output.append(dictionary[current_arr])
            combined_arr = current_arr + (-1,)
            dictionary[combined_arr] = next_idx

        if verbose:
            encoding_time_end = time()
            print(f"Final dictionary: {dictionary}")

        self.encoded_data = output

        if verbose:
            total_time_end = time()
            print(f"Encoding time: {encoding_time_end-encoding_time_start} seconds")
            print(f"Total time: {total_time_end-total_time_start} seconds")

        return output, dictionary
    
    def encode_from_file(
            self,
            input_path: str,
            verbose: bool = True
    )->tuple:
        get_set = (self.dictionary_k == -1)
        data, data_set = read_data(input_path, save_set=get_set)

        if data_set is None:
            data_set = {i for i in range(2**self.dictionary_k)}

        return self.encode(data, data_set, verbose)
    
    def decode(
            self,
            encoded_data: list,
            data_set: set,
            verbose: bool = True
    )->list:
    
        if verbose:
            total_time_start = time()
            encoding_time_start = time()

        reverse_dictionary = {i: (value,) for i, value in enumerate(sorted(data_set))}

        if verbose:
            print(f"Starting dictionary: {reverse_dictionary}")

        current_arr = encoded_data[0]
        output = [reverse_dictionary[current_arr]]

        for idx in encoded_data[1:]:
            if idx in reverse_dictionary:
                decoded_arr = reverse_dictionary[idx]
            else:
                decoded_arr = reverse_dictionary[current_arr] + (reverse_dictionary[current_arr][0],)

            output.append(decoded_arr)
            combined_arr = reverse_dictionary[current_arr] + (decoded_arr[0],)
            reverse_dictionary[len(reverse_dictionary)] = combined_arr
            current_arr = idx

        if verbose:
            encoding_time_end = time()
            print(f"Final dictionary: {reverse_dictionary}")

        output = [item for sublist in output for item in sublist]

        if verbose:
            total_time_end = time()
            print(f"Encoding time: {encoding_time_end-encoding_time_start} seconds")
            print(f"Total time: {total_time_end-total_time_start} seconds")

        return output
