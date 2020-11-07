from typing import Union, Tuple, List, Callable, Any
import hashlib
import sys
import os
# sys.path.append((os.path.dirname(os.path.abspath(__file__))))
# from crypto.bn256 import *
from pypbc import Parameters, Pairing, Element, G1, G2, GT


class KeyManager():
    def __init__(self):
        #initiate the parameters
        params_string = "type a q 5190226450145940880746663486308966347220639714045250223182499121249068575513554544422970314418344770379996438351407014419358038003225732626831022128438331 h 7102594095788614028758769623913839942835962504311385389572759256033849452424444030966227463924769974838212 r 730750818665452757176057050065048642452048576511 exp2 159 exp1 110 sign1 1 sign0 -1 "
        # self.params: Parameters = Parameters(qbits=512, rbits=160)
        self.params: Parameters = Parameters(param_string=params_string)
        self.pairing: Pairing = Pairing(self.params)
        string_g = "03138C4D4FFBF34E2338783FF4968933C015AC8F34496A4BE5697D5C4BDE9F78B3E21306F3B4938C40571C9B9EDDE050DB8CE526FF1B8099E8DE790A8962E9443E"
        self.g : Element = Element(self.pairing, G1, value=string_g)
        self.e: Callable[[Element, Element], Element] = lambda e1, e2: self.pairing.apply(e1, e2)
        # public key list
        self.public_keys : List[Element] = []

    def add_key(self, key_string):
        """Takes a key as a string and adds it to the keys"""
        key_element = Element(self.pairing, G2, value=key_string)
        self.public_keys.append(key_element)
        return len(self.public_keys) - 1

    def get_key(self, user_id):
        """Returns the key of user with id user_id as a string"""
        assert user_id >= 0 and user_id < len(self.public_keys), f"Invalid id in get_key {user_id}"
        return str(self.public_keys[user_id])

    def get_parameters(self):
        """Returns the parameters as a string"""
        return str(self.params)

    def get_g(self):
        """Returns the value of generator g as a string"""
        return str(self.g)



if __name__ == "__main__":
    manager = KeyManager()
    key = Element.random(manager.pairing, G1)
    key_str = str(key)
    print(key_str)
    user_id = manager.add_key(key_str)
    key2_str = manager.get_key(user_id)
    key2 = Element(manager.pairing, G1, value=key2_str)
    assert key == key2, "The key storage was successful"
    print(manager.get_parameters())