from helpers import read_data, write_data
from time import time

class LZW:

    def __init__(
            self
    ) -> None:
        self.input_path = None
        self.encoded_output_path = None
        self.original_data = None
        self.original_set = None
        self.encoded_data = None
        self.decoded_data = None


    def encode(
            self, 
            input_path: str, 
            save_file: bool = True, 
            verbose: bool = True
    )->list:
        
        if verbose:
            total_time_start = time()
        self.original_data, self.original_set = read_data(input_path=input_path, save_set=True)

        if verbose:
            encoding_time_start = time()

        dictionary = {(value,): i for i, value in enumerate(sorted(self.original_set))}

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

        if verbose:
            encoding_time_end = time()
            print(f"Final dictionary: {dictionary}")

        if save_file:
            write_data(f"encoded_{input_path}.lzw", output)

        self.encoded_data = output

        if verbose:
            total_time_end = time()
            print(f"Encoding time: {encoding_time_end-encoding_time_start} seconds")
            print(f"Total time: {total_time_end-total_time_start} seconds")

        return output
    
    def decode(
            self,
            input_path: str = "",
            save_file: bool = True, 
            verbose: bool = None
    )->list:
        pass

    