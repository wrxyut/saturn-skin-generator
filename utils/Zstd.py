

import os
from utils.ZstdDict import Dict
from pyzstd import decompress, compress, ZstdDict

#    Saturn was proudly coded by wrxyut (https://github.com/wrxyut).
#    Copyright (c) 2022 wrxyut.
#    Saturn under the GNU GENERAL PUBLIC LICENSE Version3 (2007).

extension = ['.xml', '.bytes', '.txt']

# Method to compress data using Zstd
def ZstdCompress(bytes_data = b''):
    # Compress the input data using Zstd compression
    compress_bytes = bytearray(compress(bytes_data, 17, ZstdDict(Dict(), True)))

    # Add a 4-byte header to the compressed data
    compress_bytes[0:0] = b"\x22\x4a\x00\xef" + len(bytes_data).to_bytes(4, byteorder="little")
    return compress_bytes

# Method to decompress data using Zstd
def ZstdDecompress(bytes_data = b''):
    # Find the start of the compressed data (after the header)
    bytes_data = bytes_data[bytes_data.find(b"\x28\xb5\x2f\xfd"):]

    # Decompress the data using Zstd decompression
    decompress_bytes = decompress(bytes_data, ZstdDict(Dict(), True))
    return decompress_bytes

# Method to check the input data for compression or decompression
def headerHandler(bytes_string = b'/'):
    # If the input data is Zstd compressed
    if bytes_string[:4] == b'\x22\x4a\x00\xef':
        return ZstdDecompress(bytes_data=bytes_string)

    # If the input data is Zstd decompressed
    return ZstdCompress(bytes_string)

def ZstdStart(dir_path):
    # if the given path is a file, process it
    if os.path.isfile(dir_path):                                    
        for ext in extension:
            if dir_path.endswith(ext):
                with open(dir_path, "rb") as r:
                    processed_data = headerHandler(r.read())
                with open(dir_path, "wb") as w:
                    w.write(processed_data)
    
    # if the given path is a directory, process all files in it
    else:
        for file_name in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file_name)
            for ext in extension:
                if file_path.endswith(ext):
                    with open(file_path, "rb") as r:
                        processed_data = headerHandler(r.read())
                    with open(file_path, "wb") as w:
                        w.write(processed_data)
