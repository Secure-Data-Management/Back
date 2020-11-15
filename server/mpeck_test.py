from typing import List

from pypbc import Element, G1
from server.keys.KeyManager import KeyManager


def Test(_A, _B, _C, T, I: List[int], user_id, genkey: KeyManager):
    A = Element(genkey.pairing, G1, value=_A)  # g^r
    B = {}
    for id_key in _B:
        B[id_key] = Element(genkey.pairing, G1, value=_B[id_key])

    # if there is no B for this user, the file has not been encrypted for this user
    if user_id not in B:
        return False
    else:
        C = [Element(genkey.pairing, G1, value=el) for el in _C]  # l total crypted keywords (h^r)(f^s)
        for i in range(3):
            T[i] = Element(genkey.pairing, G1, value=T[i])

        # Intermediate computation
        keywords_product: Element = Element.one(genkey.pairing, G1)
        for i in I:
            keywords_product *= C[i]
        E1: Element = genkey.e(T[0], keywords_product)
        G3: Element = genkey.e(A, T[1])
        G2: Element = genkey.e(B[user_id], T[2])
        E2: Element = G3 * G2
        return E1 == E2
