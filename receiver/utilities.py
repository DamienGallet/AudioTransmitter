def get_binary_from_char(char):
    value = ord(char)
    binary = []
    pattern = 2**7
    for i in range(8):
        digit = int(value/pattern)
        value -= digit*pattern
        pattern /= 2
        binary.append(digit)
    return binary


def get_char_from_binary(binary):
    value = 0
    pattern = 1
    for i in range(8):
        value += pattern*binary[7-i]
        pattern *=2
    return chr(value)

def get_binaries_from_char(chars):
    binaries = []
    for i in range(len(chars)):
        curr_bin = get_binary_from_char(chars[i])
        binaries.append(curr_bin)
    return binaries


