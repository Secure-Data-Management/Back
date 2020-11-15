import csv
from typing import Union, Tuple, List, Callable, Any, Dict

from pypbc import Parameters, Pairing, Element, G1, G2


class KeyManager():
    def __init__(self, params_string: str, string_g: str):
        # initiate the parameters
        # self.params: Parameters = Parameters(qbits=512, rbits=160)
        self.params: Parameters = Parameters(param_string=params_string)
        self.pairing: Pairing = Pairing(self.params)
        self.g: Element = Element(self.pairing, G1, value=string_g)
        self.e: Callable[[Element, Element], Element] = lambda e1, e2: self.pairing.apply(e1, e2)
        # public key dict
        self.users: Dict[str, int] = {}
        self.public_keys: Dict[str, Element] = {}
        self.public_keys_string: Dict[str, str] = {}

        with open('accounts.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                username = row[1]
                key_string = row[2]
                key_element = Element(self.pairing, G1, value=key_string)
                self.public_keys[username] = key_element
                self.public_keys_string[username] = str(key_element)
                user_id = len(self.public_keys) - 1
                self.users[username] = user_id

        print("KeyManager started, current keys are")
        for username in self.public_keys:
            print(f"\t{username}: {str(self.public_keys[username])}")

    def add_key(self, key_string, username):
        """Takes a key as a string and a username and adds it to the keys"""
        key_element = Element(self.pairing, G1, value=key_string)
        self.public_keys[username] = key_element
        user_id = len(self.public_keys) - 1
        self.users[username] = user_id
        with open("accounts.csv", "a+") as f:
            line = f"{user_id},{username},{key_string}\n"
            f.write(line)
        return user_id

    def get_key(self, username):
        """Returns (user_id, key) of user with name=username as a string"""
        # assert user_id >= 0 and user_id < len(self.public_keys), f"Invalid id in get_key {user_id}"
        if username in self.users:
            user_id = self.users[username]
            key = str(self.public_keys[username])
            return (user_id, key)

    def get_parameters(self):
        """Returns the parameters as a string"""
        return str(self.params)

    def get_g(self):
        """Returns the value of generator g as a string"""
        return str(self.g)

    def get_key_from_str_G1(self,key:str):
        return Element(self.pairing, G1, value=key)