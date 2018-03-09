import urllib
import io
import gzip
import pickle

def load_compressed_pickled_object(file_url):
    with urllib.request.urlopen(file_url) as response:
        compressed_string = response.read()
    compressedFile = io.BytesIO(compressed_string)
    decompressedFile = gzip.GzipFile(fileobj=compressedFile)
    loaded_object = pickle.load(decompressedFile)
    return loaded_object
    
