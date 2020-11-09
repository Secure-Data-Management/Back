from pypbc import Element, G1
# from server.keys.KeyManager import KeyManager
from server.keys.KeyManager import KeyManager
from typing import List, Union


def Test(_A, _B, _C, T, user_id, genkey: KeyManager):
    #  S = [A, B, C]
    # convert A, B, C and T[:3] to Elements
    A = Element(genkey.pairing, G1, value=_A)  # g^r
    B = {}
    for id_key in _B:
        B[id_key] = Element(genkey.pairing, G1, value=_B[id_key])

    #if there is no B for this user, the file has not been encrypted for this user
    # then return 0
    if user_id not in B:
        return -1
    else:
        C = [Element(genkey.pairing, G1, value=el) for el in _C]  # l total crypted keywords (h^r)(f^s)
        for i in range(3):
            T[i] = Element(genkey.pairing, G1, value=T[i])
        I: List[int] = T[3:]  # m indexes of keywords from the query
        # Intermediate computation
        keywords_product: Element = Element.one(genkey.pairing, G1)
        for i in I:
            keywords_product *= C[i]
        E1: Element = genkey.e(T[0], keywords_product)
        G3: Element = genkey.e(A, T[1])
        G2: Element = genkey.e(B[user_id], T[2])
        E2: Element = G3 * G2
        # print("A=", A, "\nB=", B[user_id], "\nC=", C, "\nT=", T, "\nTEST:", "\nE1:", E1, "\nE2:", E2)
        # Test verification
        if E1 == E2:
            return 1  # keywords match
        else:
            return 0  # keywords don't match
