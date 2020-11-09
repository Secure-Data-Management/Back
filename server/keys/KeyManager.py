import csv
from typing import Union, Tuple, List, Callable, Any, Dict

from pypbc import Parameters, Pairing, Element, G1, G2


class KeyManager():
    def __init__(self):
        #initiate the parameters
        params_string = "type a q 5190226450145940880746663486308966347220639714045250223182499121249068575513554544422970314418344770379996438351407014419358038003225732626831022128438331 h 7102594095788614028758769623913839942835962504311385389572759256033849452424444030966227463924769974838212 r 730750818665452757176057050065048642452048576511 exp2 159 exp1 110 sign1 1 sign0 -1 "
        # self.params: Parameters = Parameters(qbits=512, rbits=160)
        self.params: Parameters = Parameters(param_string=params_string)
        self.pairing: Pairing = Pairing(self.params)
        string_g = "032F098B7A139CD885793702C3D8A03859A2B6D35643C9D3971DA924CD7CD65AE7E8FE9AC1B5A287B825E1B960D2F7005DD5E6D86DD9AB96608AE6E8F790471A88"
        self.g : Element = Element(self.pairing, G1, value=string_g)
        self.e: Callable[[Element, Element], Element] = lambda e1, e2: self.pairing.apply(e1, e2)
        # public key dict
        self.user_id = {}
        self.public_keys : Dict[Element] = {}

        #HACK: consultant is considered to be user_id = 0 since he is the first to be created. His name is consultant
        #TODO: create consultant key in the KeyManager itself?

        #empty the database
        with open('accounts.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                username = row[1]
                key_string = row[2]
                key_element = Element(self.pairing, G1, value=key_string)
                self.public_keys[username] = key_element
                user_id = len(self.public_keys) - 1
                self.user_id[username] = user_id

        print("KeyManager started, current keys are")
        for username in self.public_keys:
            print(f"\t{username}: {str(self.public_keys[username])}")


    def add_key(self, key_string, username):
        """Takes a key as a string and a username and adds it to the keys"""
        key_element = Element(self.pairing, G1, value=key_string)
        self.public_keys[username] = key_element
        user_id = len(self.public_keys) - 1
        self.user_id[username] = user_id
        with open("accounts.csv", "a+") as f:
            line = f"{user_id},{username},{key_string}\n"
            f.write(line)
        return user_id

    def get_key(self, username):
        """Returns (user_id, key) of user with name=username as a string"""
        # assert user_id >= 0 and user_id < len(self.public_keys), f"Invalid id in get_key {user_id}"
        if username in self.user_id:
            user_id = self.user_id[username]
            key = str(self.public_keys[username])
            return (user_id, key)

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
    user_id = manager.add_key(key_str, "test")
    key2_str = manager.get_key(user_id)
    key2 = Element(manager.pairing, G1, value=key2_str)
    assert key == key2, "The key storage was successful"
    print(manager.get_parameters())