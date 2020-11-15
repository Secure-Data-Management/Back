from typing import Tuple

from pypbc import Parameters, Pairing, Element, G1


def create(qbits: int = 512, rbits: int = 160) -> Tuple[str, str]:
    params: Parameters = Parameters(qbits=qbits, rbits=rbits)
    pairing: Pairing = Pairing(params)
    g: Element = Element.random(pairing, G1)
    return str(params), str(g)


def write_to_env(params: str, g: str):
    f = open(".env", "w")
    env_str = f"""
PARAMS="{params}"
G="{g}"
"""
    f.write(env_str)
    f.close()


def generate_config():
    params, g = create()
    write_to_env(params, g)


if __name__ == '__main__':
    generate_config()
