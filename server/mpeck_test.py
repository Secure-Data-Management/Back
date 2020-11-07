from pypbc import Element, G1
# from server.keys.KeyManager import KeyManager
from server.keys.KeyManager import KeyManager
from typing import List, Union


def Test(_A, _B, _C, T, j, genkey: KeyManager):
    #  S = [A, B, C]
    #convert A, B, C and T[:3] to Elements
    A = Element(genkey.pairing, G1, value= _A)  # g^r
    B = [Element(genkey.pairing, G1, value= el) for el in _B]  # pk^s
    C = [Element(genkey.pairing, G1, value= el) for el in _C]  # l total crypted keywords (h^r)(f^s)
    for i in range(3):
        T[i] = Element(genkey.pairing, G1, value= T[i])
    print("A=",A)
    print("B=",B[j])
    print("C=", C)
    print("T=", T)
    I: List[int] = T[3:]  # m indexes of keywords from the query
    # Intermediate computation
    keywords_product: Element = Element.one(genkey.pairing, G1)
    for i in I:
        keywords_product *= C[i]
    E1: Element = genkey.e(T[0], keywords_product)
    G3: Element = genkey.e(A, T[1])
    G2: Element = genkey.e(B[j], T[2])
    E2: Element = G3 * G2
    print("TEST:")
    print("E1:", E1)
    print("E2:", E2)
    # Test verification
    if E1 == E2:
        return 1  # keywords match
    else:
        return 0  # keywords don't match