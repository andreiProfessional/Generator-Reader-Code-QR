#Cristea Andrei si Nicula Andrei --- grupa 134

#import qrcode
import numpy as np
#import matplotlib.pyplot as plt
import cv2
import math




# def genereaza_matrice_fara_margine(data, version=2, border=4):
#     qr = qrcode.QRCode(
#         version=version,  #versiunea 2 a QR
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=10,
#         border=border,
#     )
#     qr.add_data(data)
#     qr.make(fit=True)
#
#     #extrag matricea de pixeli
#     matrix = qr.get_matrix()
#
#     #transform matricea in 0 si 255 in functie de valorile true si false
#     matrix_numpy = np.array(matrix, dtype=int)
#     matrix_numpy = np.where(matrix_numpy == 1, 0, 255)
#
#     #elimin  marginea
#     matrix_without_border = matrix_numpy[border:-border, border:-border]
#
#     return matrix_without_border

def afiseaza_matrice(matrice):
    for rand in matrice:
        print(" ".join(str(element) for element in rand))



def afla_tipul_mastii(matrix):
    if matrix[8,2] == 255:
        if matrix[8, 3] == 255:
            if matrix[8, 4] == 255:
                return 5
                #alb alb alb
            elif matrix[8, 4] == 0:
                return 4
                #alb alb negru
        elif matrix[8, 3] == 0:
            if matrix[8, 4] == 255:
                return 7
                #alb negru alb
            elif matrix[8, 4] == 0:
                return 6
                #alb negru negru
    elif matrix[8,2] == 0:
        if matrix[8,3] == 255:
            if matrix[8,4] == 255:
                return 1
                #negru alb alb
            elif matrix[8,4] == 0:
                return 0
                #negru alb negru
        elif matrix[8,3] == 0:
            if matrix[8, 4] == 255:
                return 3
                #negru negru alb
            elif matrix[8, 4] == 0:
                return 2
                #negru negru negru

def is_reserved_from_masking(i, j):
    if i <= 8 and (j <= 8 or j >= 17):
        return True
    if i >= 17 and j <= 8:
        return True
    if 16 <= i <= 20 and 16 <= j <= 20:
        return True
    if i == 6 or j == 6:
        return True
    return False

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
        return i * j % 2 + i * j % 3 == 0
    if mask_id == 6:
        return (i * j % 2 + i * j % 3) % 2 == 0
    if mask_id == 7:
        return ((i + j) % 2 + i * j % 3) % 2 == 0


def xor_masking(dimension, qr_code, mask_id):

    #creez o matrice noua cu numpy
    new_matrix = np.empty((dimension, dimension), dtype=np.uint8)

    #aplic regulile de xor in functie de masca folosita
    for i in range(dimension):
        for j in range(dimension):
            if is_reserved_from_masking(i, j):  #daca e reservat nu il modific
                new_matrix[i][j] = qr_code[i][j]
            elif rules(mask_id, i, j):  # aplic regulile specifice
                new_matrix[i][j] = qr_code[i][j] ^ 255  # xor cu 255 ca sa modific culorea bitului
            else:
                new_matrix[i][j] = qr_code[i][j]

    return new_matrix

def este_spatiu_liber(x,y):
    if x <= 8 and (y <= 8 or y >= 17):
        return False
    if x >= 17 and y <= 8:
        return False
    if 16 <= x <= 20 and 16 <= y <= 20:
        return False
    if x == 6 or y == 6:
        return False
    if x >= 23 and y >= 23:
        return False
    return True


def parcurge_matricea(matrice):
    # p_l = pereche_linie
    sir_biti = []
    for p_l in range(12, 0, -1):
        if p_l % 2 == 0:
            for x in range(24, -1, -1):
                if este_spatiu_liber(x, 2*p_l):
                    if matrice[x, 2*p_l] == 255:
                        sir_biti.append(0)
                    else:
                        sir_biti.append(1)
                    #sir_biti.append(matrice[x][2 * p_l])
                if este_spatiu_liber(x, 2 * p_l -1):
                    if matrice[x, 2*p_l-1] == 255:
                        sir_biti.append(0)
                    else:
                        sir_biti.append(1)
                    #sir_biti.append(matrice[x][2 * p_l - 1])

        else:
            for x in range(0, 25):
                if este_spatiu_liber(x, 2 * p_l):
                    if matrice[x, 2*p_l] == 255:
                        sir_biti.append(0)
                    else:
                        sir_biti.append(1)
                    #sir_biti.append(matrice[x][2 * p_l])
                if este_spatiu_liber(x, 2 * p_l - 1):
                    if matrice[x, 2*p_l-1] == 255:
                        sir_biti.append(0)
                    else:
                        sir_biti.append(1)
                    #sir_biti.append(matrice[x][2 * p_l - 1])

    for x in range(24,-1,-1):
        if este_spatiu_liber(x, 0):
            if matrice[x, 0] == 255:
                sir_biti.append(0)
            else:
                sir_biti.append(1)
            #sir_biti.append(matrice[x][0])
    return sir_biti


def decode_bits_to_ascii(bits):
    #impart lista de biti in bytes
    byte_list = [bits[i:i + 8] for i in range(8, len(bits), 8)] # incep de la 8
    #pt ca primul byte tine lungimea codului
    decoded_message = ""

    # convertesc fiecare byte in caracter ascii
    for byte in byte_list:
        #verific daca nu s a ajuns la word ul pt stop
        if byte[:4] == [0, 0, 0, 0]:
            return decoded_message
        if len(byte) == 8: # verific sa nu se fi terminat bitii
            #transform lista de biti din byte intr un int
            byte_value = int("".join(map(str, byte)), 2)
            #adaug caracterul ascii pentru acel int de biti din byte
            decoded_message += chr(byte_value)

    return decoded_message


def qr_to_matrix(image_path):
    #functie pentru primirea unui input in format png si extragerea matricii
    #qr din poza, folosind cv2

    # 1 citesc imaginea in greyscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None: #verific daca s a putut citi
        raise ValueError("Imaginea nu a putut fi citita!!!")

    # 2 imaginea -> format binar (fundal alb si biti negri)
    _, bin_img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)

    # 3 functie pentru center crop
    h, w = bin_img.shape
    side = min(h, w)
    start_y = (h - side) // 2
    start_x = (w - side) // 2
    square_img = bin_img[start_y:start_y + side, start_x:start_x + side]

    # 4 functie pentru eliminarea marginilor, acel white border din jurul matricii qr
    coords = np.argwhere(square_img == 0)
    if coords.size > 0:
        # np.argwhere returnează [row, col] pentru fiecare pixel negru
        y_min, x_min = coords.min(axis=0)
        y_max, x_max = coords.max(axis=0)
        cropped_img = square_img[y_min:y_max + 1, x_min:x_max + 1]
    else:
        cropped_img = square_img  # dacă nu există pixeli negri iau toata imaginea

    # 5 iau dimensiunile
    ch, cw = cropped_img.shape
    # calculez dimensiunea medie a unui modul(vreau sa fie cat mai apropiate)
    module_size_x = cw / 25.0
    module_size_y = ch / 25.0
    module_size = (module_size_x + module_size_y) / 2.0

    # 6 construiesc matricea in numpy folosind media valorica a fiecarui modul(daca e mai mult negru -> il fac negru)
    matrix = np.zeros((25, 25), dtype=np.uint8)
    for i in range(25):
        for j in range(25):
            # calculez limitele regiunii pentru modulul (i, j)
            #folosesc floor pentru a asigura acoperirea fara suprapuneri sau lipsuri
            x0 = int(math.floor(j * module_size))
            # pentru ultimul modul ma asigur ca ajung pana la margine
            x1 = int(math.floor((j + 1) * module_size)) if j < 24 else cw
            y0 = int(math.floor(i * module_size))
            y1 = int(math.floor((i + 1) * module_size)) if i < 24 else ch

            # daca regiunea e goala o fac alba
            if x1 <= x0 or y1 <= y0:
                pixel_val = 255
            else:
                # extrag regiunea modulului
                region = cropped_img[y0:y1, x0:x1]
                # calculez media valorica pe fiecare regiune in parte
                avg_val = np.mean(region)
                pixel_val = 0 if avg_val < 128 else 255
            matrix[i, j] = pixel_val

    return matrix


def citeste_codul_qr(image_path):
    matrice = qr_to_matrix(image_path)
    matrice_demascata = xor_masking(25, matrice, afla_tipul_mastii(matrice))
    # plt.imshow(matrice_demascata, cmap='gray', interpolation='nearest')
    # plt.axis('off')
    # plt.savefig('qr_codeInput.png')
    # plt.close()
    lista_biti_de_decodat = parcurge_matricea(matrice_demascata)
    string = decode_bits_to_ascii(lista_biti_de_decodat)
    return string

def citeste_codul_qr2(data):

    matrice = genereaza_matrice_fara_margine(data,2,4)
    matrice_demascata = xor_masking(25, matrice, afla_tipul_mastii(matrice))
    # plt.imshow(matrice_demascata, cmap='gray', interpolation='nearest')
    # plt.axis('off')
    # plt.savefig('qr_codeInput.png')
    # plt.close()
    lista_biti_de_decodat = parcurge_matricea(matrice_demascata)
    string = decode_bits_to_ascii(lista_biti_de_decodat)
    return string


def afisare_output(img_path):
    print(f"Continutul imaginii aflate la adresa {img_path} este:\n"
          f"{citeste_codul_qr(img_path)}")

##################################################################

afisare_output("qr_link_pagina_cursului.png")
afisare_output("Andrei & Andrei Codes.png")


#print(citeste_codul_qr2("test"))

# afisez matricea pentru debug

# plt.imshow(matrice_testare, cmap='gray', interpolation='nearest')
# plt.axis('off')
# plt.savefig('qr_codeInput.png')
# plt.close()
