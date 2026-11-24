# LZW compression and decompression taken from:
# https://rosettacode.org/wiki/LZW_compression#Python

import pickle


def compress(uncompressed):
    """Compress a string to a list of output symbols."""

    dict_size = 256
    dictionary = dict((chr(i), i) for i in range(dict_size))

    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = c

    if w:
        result.append(dictionary[w])
    return result


def decompress(compressed):
    """Decompress a list of output ks to a string."""
    from io import StringIO

    dict_size = 256
    dictionary = dict((i, chr(i)) for i in range(dict_size))

    result = StringIO()
    w = chr(compressed.pop(0))
    result.write(w)

    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError('Bad compressed k: %s' % k)
        result.write(entry)

        dictionary[dict_size] = w + entry[0]
        dict_size += 1

        w = entry
    return result.getvalue()


def write_results(fname, data):
    with open(fname, 'wb') as file:
        pickle.dump(data, file)


def read_results(fname):
    with open(fname, 'rb') as file:
        compressed = pickle.load(file)

    decompressed = decompress(compressed)
    decompressed = decompressed.encode("latin-1").decode("utf-8")

    print(decompressed[:45])


def main():
    with open("Alice.txt", "r", encoding="latin-1", newline="") as file:
        text = file.read()

    compressed = compress(text)

    write_results('compressed.pickle', compressed)

    read_results('compressed.pickle')


if __name__ == "__main__":
    main()