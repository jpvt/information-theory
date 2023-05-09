from compression import LZW
from compression.helpers import read_data

class TestLZW:
    def test_encode(self)->None:
        abracadabra_data = [ord(val) for val in "abracadabra"]
        abracadabra_set = sorted(set(abracadabra_data))
        expected_data = [0, 1, 4, 0, 2, 0, 3, 5, 7]
        expected_dict = {
            (97,): 0, (98,): 1, (99,): 2, (100,): 3, (114,): 4, (97, 98): 5, 
            (98, 114): 6, (114, 97): 7, (97, 99): 8, (99, 97): 9, (97, 100): 10, 
            (100, 97): 11, (97, 98, 114): 12, (114, 97, -1): 13
        }

        encoded_data, final_dict = LZW().encode(original_data=abracadabra_data, original_set=abracadabra_set, verbose=False)

        assert encoded_data == expected_data
        assert final_dict == expected_dict

    def test_encode_from_file(self)->None:
        expected_data = [0, 1, 4, 0, 2, 0, 3, 5, 7]
        expected_dict = {
            (97,): 0, (98,): 1, (99,): 2, (100,): 3, (114,): 4, (97, 98): 5, 
            (98, 114): 6, (114, 97): 7, (97, 99): 8, (99, 97): 9, (97, 100): 10, 
            (100, 97): 11, (97, 98, 114): 12, (114, 97, -1): 13
        }

        encoded_data, final_dict = LZW().encode_from_file("test/data/abracadabra.txt", False)

        assert encoded_data == expected_data
        assert final_dict == expected_dict

    def test_decode(self)->None:
        abracadabra_data = [ord(val) for val in "abracadabra"]
        abracadabra_set = sorted(set(abracadabra_data))

        encoded_data, _ = LZW().encode(original_data=abracadabra_data, original_set=abracadabra_set, verbose=False)
        decoded_data = LZW().decode(encoded_data, abracadabra_set, verbose=False)

        assert abracadabra_data == decoded_data

    def test_encode_decode_filesystem(self)->None:
        lzw = LZW()
        lzw.encode_from_file("test/data/abracadabra.txt", False)
        lzw.save_encoded_data("test/data/encoded_abracadabra")
        del lzw

        decoded_data = LZW().decode_from_file("test/data/encoded_abracadabra.pickle", "test/data/decoded_abracadabra.txt")
        decoded_str = "".join([chr(val) for val in decoded_data])

        assert decoded_str == "abracadabra"

    def test_encode_decode_filesystem_with_k(self)->None:
        dict_k = 8
        lzw = LZW(dictionary_k=dict_k)
        lzw.encode_from_file("test/data/abracadabra.txt", False)
        lzw.save_encoded_data("test/data/encoded_abracadabra")
        del lzw

        decoded_data = LZW().decode_from_file(f"test/data/encoded_abracadabra.{dict_k}", "test/data/decoded_abracadabra.txt")
        decoded_str = "".join([chr(val) for val in decoded_data])

        assert decoded_str == "abracadabra"

    def test_corpus(self)->None:
        lzw = LZW()
        lzw.encode_from_file("test/data/corpus16MB.txt", False)
        lzw.save_encoded_data("test/data/encoded_corpus16MB")
        del lzw

        LZW().decode_from_file("test/data/encoded_corpus16MB.pickle", "test/data/decoded_corpus16MB.txt")
        decoded_data, _ = read_data("test/data/decoded_corpus16MB.txt", False)
        original_data, _ = read_data("test/data/corpus16MB.txt", False)

        assert decoded_data == original_data

    def test_corpus_with_k(self)->None:
        dict_k = 16
        lzw = LZW(dictionary_k=dict_k)
        lzw.encode_from_file("test/data/corpus16MB.txt", False)
        lzw.save_encoded_data("test/data/encoded_corpus16MB")
        del lzw

        LZW().decode_from_file(f"test/data/encoded_corpus16MB.{dict_k}", "test/data/decoded_corpus16MB_with_k.txt")
        decoded_data, _ = read_data("test/data/decoded_corpus16MB_with_k.txt", False)
        original_data, _ = read_data("test/data/corpus16MB.txt", False)

        assert decoded_data == original_data


