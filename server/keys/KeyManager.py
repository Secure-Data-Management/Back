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
        self.params: Parameters = Parameters(qbits=512, rbits=160)
        self.pairing: Pairing = Pairing(self.params)
        self.g : Element = Element.random(self.pairing, G1)
        self.e: Callable[[Element, Element], Element] = lambda e1, e2: self.pairing.apply(e1, e2)
        # public key list
        self.public_keys : List(Element) = []

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