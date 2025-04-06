#Cristea Andrei si Nicula Andrei --- grupa 134

import numpy as np
import matplotlib.pyplot as plt
from reedsolo import RSCodec

#---------------------------------------------------------------------------
#functions

def adauga_finder_patterns_1(matrice, x = 0, y = 0):
    matrice[x: x + 7, y: y + 7] = 1
    matrice[x + 1: x + 6, y + 1: y + 6] = 0
    matrice[x + 2: x + 5, y + 2: y + 5] = 1


def adauga_finder_patterns_2(matrice):
    matrice[16: 21, 16: 21] = 1
    matrice[17: 20, 17: 20] = 0
    matrice[18, 18] = 1


def adauga_timing_patterns(matrice):
    y = 6
    for x in range(8, 17):
        if x % 2 == 0:
            matrice[x, y] = 1
    x = 6
    for y in range(8, 17):
        if y % 2 == 0:
            matrice[x, y] = 1
    matrice[17,8] = 1


def highlight_format_information_bits(matrice):
    matrice[18: dimension, 8] = 127
    matrice[8, 18: dimension] = 127
    for y in range(0, 9):
        if y != 6:
            matrice[8, y] = 127
    for x in range(0, 8):
        if x != 6:
            matrice[x, 8] = 127


def is_reserved(i, j):
    if i <= 8 and (j <= 8 or j >= 17):
        return True
    if i >= 17 and j <= 8:
        return True
    if 16 <= i <= 20 and 16 <= j <= 20:
        return True
    if i == 6 or j == 6:
        return True
    return False


def parcurge_matricea(dimension, matrice, bit_array):
    index = 0
    for p_l in range(12, 0, -1):
        if p_l % 2 == 0:
            for x in range(24, -1, -1):
                if not is_reserved(x, 2 * p_l):
                    matrice[x, 2 * p_l] = bit_array[index]
                    index += 1
                    if index == len(bit_array) - 1:
                        return
                if not is_reserved(x, 2 * p_l - 1):
                    matrice[x, 2 * p_l - 1] = bit_array[index]
                    index += 1
                    if index == len(bit_array) - 1:
                        return
        else:
            for x in range(0, dimension):
                if not is_reserved(x, 2 * p_l):
                    matrice[x, 2 * p_l] = bit_array[index]
                    index += 1
                    if index == len(bit_array) - 1:
                        return
                if not is_reserved(x, 2 * p_l - 1):
                    matrice[x, 2 * p_l - 1] = bit_array[index]
                    index += 1
                    if index == len(bit_array) - 1:
                        return
    for x in range(24, -1, -1):
        if not is_reserved(x, 0):
            matrice[x, 0]= bit_array[index]
            index += 1
            if index == len(bit_array) - 1:
                return


def decimal_to_binary(n):
    if n < 0 or n > 255:
        return "Eroare!"
    binary = ""
    for i in range(8):
        binary = str(n % 2) + binary
        n = n // 2
    return binary

def byte_padding(count, bit_string):
    for i in range(count):
        if i % 2 == 0:
            bit_string.extend([1, 1, 1, 0, 1, 1, 0, 0])
        else:
            bit_string.extend([0, 0, 0, 1, 0, 0, 0, 1])

def add_correction_bits(length_string, string, bit_string):
    # Conversie de la biti la bytes
    data_bytes = []
    for i in range(0, len(bit_string), 8):
        byte_str = "".join(str(b) for b in bit_string[i:i + 8])
        data_bytes.append(int(byte_str, 2))
    rsc = RSCodec(10)
    list_of_chars = bytearray(data_bytes)
    encoded_string = rsc.encode(list_of_chars)
    final_bytes = list(encoded_string)
    final_bits = []
    for b in final_bytes:
        final_bits.extend([int(x) for x in format(b, '08b')])
    return final_bits

def transform_string_to_binary(string):
    binary = []
    for char in string:
        byte_integer = ord(char)
        byte_binary = format(byte_integer, "08b")
        binary.append(byte_binary)
    return binary

def rules(mask_id, i, j):
    if mask_id == 0:
        return (i + j) % 2 == 0
    if mask_id == 1:
        return i % 2 == 0
    if mask_id == 2:
        return j % 3 == 0
    if mask_id == 3:
        return (i + j) % 3 == 0
    if mask_id == 4:
        return (i // 2 + j // 3) % 2 == 0
    if mask_id == 5:
        return (i * j) % 2 + (i * j) % 3 == 0
    if mask_id == 6:
        return ((i * j) % 3 + i * j) % 2 == 0
    if mask_id == 7:
        return ((i * j) % 3 + i + j) % 2 == 0

def XOR_masking(dimension, QR_Code, mask_count):
    applied_masks = np.empty((mask_count, dimension, dimension), dtype = np.uint8)
    for k in range(mask_count):
        for i in range(dimension):
            for j in range(dimension):
                if is_reserved(i, j):
                    applied_masks[k, i, j] = QR_Code[i][j]
                elif rules(k, i, j):
                    if QR_Code[i][j] == 0:
                        applied_masks[k, i, j] = 1
                    elif QR_Code[i][j] == 1:
                        applied_masks[k, i, j] = 0
                else:
                    applied_masks[k, i, j] = QR_Code[i][j]
    return applied_masks

def position_format_bits(matrix, mask_id):
    # HARDCODARE Format strip pentru fiecare masca in parte (Default error correction = Low)
    format_bits_string = np.empty(15, dtype = np.uint8)
    if mask_id == 0:
        format_bits_string = np.array([1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0])
    elif mask_id == 1:
        format_bits_string = np.array([1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1])
    elif mask_id == 2:
        format_bits_string = np.array([1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0])
    elif mask_id == 3:
        format_bits_string = np.array([1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1])
    elif mask_id == 4:
        format_bits_string = np.array([1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1])
    elif mask_id == 5:
        format_bits_string = np.array([1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0])
    elif mask_id == 6:
        format_bits_string = np.array([1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1])
    elif mask_id == 7:
        format_bits_string = np.array([1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0])
    matrix[8, 0: 6] = matrix[24: 18: -1, 8] = format_bits_string[0: 6]
    matrix[8, 7] = matrix[18, 8] = format_bits_string[6]
    matrix[8, 8] = matrix[8, 17] = format_bits_string[7]
    matrix[7, 8] = matrix[8, 18] = format_bits_string[8]
    matrix[5:: -1, 8] = matrix[8, 19: 25] = format_bits_string[9: 25]

def mask_score(matrix, dimension):
    final_score = 0
    #RULE 1
    #Horizontal
    for i in range(dimension):
        p, length, color = 1, 1, matrix[i][0]
        while p < dimension:
            if matrix[i][p] == color:
                length += 1
            else:
                if length >= 5:
                    final_score += length - 2
                length = 1
                color = matrix[i][p]
            p += 1
        if length >= 5:
            final_score += length - 2
    #Vertical
    for j in range(dimension):
        p, length, color = 1, 1, matrix[0][j]
        while p < dimension:
            if matrix[p][j] == color:
                length += 1
            else:
                if length >= 5:
                    final_score += length - 2
                length = 1
                color = matrix[p][j]
            p += 1
        if length >= 5:
            final_score += length - 2
    #RULE 2
    for i in range(dimension - 1):
        for j in range(dimension - 1):
            if matrix[i][j] == matrix[i + 1][j] == matrix[i][j + 1] == matrix[i + 1][j + 1]:
                final_score += 3
    #RULE 3
    wrong_pattern_1 = np.array([1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0])
    wrong_pattern_2 = np.array([0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1])
    #Horizontal
    for i in range(dimension):
        for j in range(dimension - 10):
            if np.array_equal(matrix[i, j: j + 11], wrong_pattern_1) or np.array_equal(matrix[i, j: j + 11], wrong_pattern_2):
                final_score += 40
    #Vertical
    for i in range(dimension - 10):
        for j in range(dimension):
            if np.array_equal(matrix[i: i + 11, j], wrong_pattern_1) or np.array_equal(matrix[i: i + 11, j], wrong_pattern_2):
                final_score += 40
    #RULE 4
    black_bits_count = 0
    for i in range(dimension):
        for j in range(dimension):
            if matrix[i][j] == 1:
                black_bits_count += 1
    black_bits_percentage = black_bits_count / (dimension * dimension) * 100
    if black_bits_percentage < 50:
        multiple_of_5 = 50
        while multiple_of_5 - 5 >= black_bits_percentage:
            multiple_of_5 -= 5
        final_score += (50 - multiple_of_5) * 2
    else:
        multiple_of_5 = 50
        while multiple_of_5 + 5 <= black_bits_percentage:
            multiple_of_5 += 5
        final_score += (multiple_of_5 - 50) * 2
    return final_score

def best_score_position(scores, score_count):
    p = 0
    for i in range(1, score_count):
        if scores[i] < scores[p]:
            p = i
    return p

def display_matrix(matrix, output_file):
    for i in range(dimension):
        for j in range(dimension):
            if matrix[i][j] == 0:
                matrix[i][j] = 255
            elif matrix[i][j] == 1:
                matrix[i][j] = 0
    plt.imshow(matrix, cmap="grey")
    plt.axis("off")
    plt.savefig(output_file)
    plt.close()


def initializeza_matricea():
    matrix = np.zeros((dimension, dimension), dtype=np.uint8)
    adauga_finder_patterns_1(matrix)
    adauga_finder_patterns_1(matrix, y=18)
    adauga_finder_patterns_1(matrix, x=18)
    adauga_finder_patterns_2(matrix)
    adauga_timing_patterns(matrix)
    highlight_format_information_bits(matrix)
    return matrix


def format_input(string):
    #string = input("Textul de transformat in QR Code: ")
    length_string = len(string)
    bit_string = [0, 1, 0, 0]  # Datatype = Byte
    bit_string.extend([int(bit) for bit in decimal_to_binary(length_string)])
    data_bits = transform_string_to_binary(string)
    data_bits = "".join(data_bits)
    data_bits = [int(x) for x in data_bits]
    bit_string.extend(data_bits)
    bit_string.extend([0, 0, 0, 0])  # Terminator
    byte_padding(32 - length_string, bit_string)  # Byte padding

    bit_string = add_correction_bits(length_string, string, bit_string)
    return bit_string

def mascare_output(matrix):
    mask_count = 8
    applied_masks = XOR_masking(dimension, matrix, mask_count)

    for i in range(mask_count):
        position_format_bits(applied_masks[i], i)
        # display_matrix(applied_masks[i], f"qr{i + 1}.png")

    scores = [mask_score(applied_masks[i], dimension) for i in range(mask_count)]
    position = best_score_position(scores, mask_count)

    matrix = applied_masks[position]

    print(f"S-a aplicat masca cu numarul {position}.\n"
          f"Aceasta a obtinut scorul {scores[position]}.\n"
          f"Codul qr a fost salvat in format png sub numele: qr_code.png.")
    display_matrix(matrix, f"qr_code.png")


def full_task(string):
    qr_matrix = initializeza_matricea()

    bit_string = format_input(string)

    parcurge_matricea(dimension, qr_matrix, bit_string)

    mascare_output(qr_matrix)
    pass


#---------------------------------------------------------------------------
#global data

dimension = 25

#---------------------------------------------------------------------------
#input


#full_task("Andrei & Andrei Codes")

full_task("https://cs.unibuc.ro/~crusu")

# str_inp = input("Introdu textul care va fi pus in qr: ")
# full_task(str_inp)
#---------------------------------------------------------------------------

