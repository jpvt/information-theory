from compression import LZW

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
