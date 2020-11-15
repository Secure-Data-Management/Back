import json
import os
from django.shortcuts import render
from django.http import HttpResponse
from pypbc import Element

from server.global_variables import KEY_MANAGER, PARAMS, G
from django.views.decorators.csrf import csrf_exempt
from backend_project.settings import MEDIA_ROOT
from server.mpeck_test import Test


# Create your views here.
def home(request):
    # TODO banner
    return HttpResponse("mPECK server")


# Views for /keys/
def get_params(request):
    return HttpResponse(PARAMS)


def get_generator(request):
    """Returns the generator g as a string"""
    return HttpResponse(G)


def add_key(request):
    """Receives the key as a get parameter (?key=...) and a username (?user=...) and adds it to the KeyManager"""
    new_key = request.GET.get("key", "")
    username = request.GET.get("user", "")
    if new_key == "":
        return HttpResponse("No key sent")
    else:
        if username == "":
            return HttpResponse("Username was not defined !")
        if new_key in KEY_MANAGER.public_keys.values():
            return HttpResponse("The key already exists ! Are you trying to spoof yourself ?")
        if username in KEY_MANAGER.public_keys:
            return HttpResponse("User already exists !")
        else:
            if username not in KEY_MANAGER.users:
                user_id = KEY_MANAGER.add_key(new_key, username)
                return HttpResponse(str(user_id))
            else:
                return HttpResponse(str(-1))


def get_username(request):
    """Receive a public key and return the associated username"""
    key_string = request.GET.get("key", "")
    if key_string == "":
        return HttpResponse("No key specified")
    else:
        # check the key belong to the group first
        try:
            KEY_MANAGER.get_key_from_str_G1(key_string)
        except Exception as e:
            return HttpResponse(e)
        if key_string not in KEY_MANAGER.public_keys_string.values():
            return HttpResponse("No key exist on the server like that one, please register first")
        l = [k for (k, v) in KEY_MANAGER.public_keys_string.items() if v == key_string]
        if len(l) != 1:
            return HttpResponse("The server can not decide which username to send out, something is wrong !")
        return HttpResponse(str(l[0]))


def get_key(request):
    """Receives a username in get paramater and returns his public key (if user exists)"""
    username = request.GET.get("user", "")
    if username == "":
        return HttpResponse("No user specified")
    else:
        if username not in KEY_MANAGER.public_keys:
            print(f"Request for key of {username}, but this user does not exist")
            return HttpResponse("This user does not exist")
        else:
            user_id, key_string = KEY_MANAGER.get_key(username)
            print(f"Sent key of {user_id}: {key_string}")
            return HttpResponse(f"{user_id},{key_string}")


def get_users(request):
    """Returns the list of usernames, ids and keys..."""
    list_usernames = KEY_MANAGER.public_keys.keys()
    response = []
    for user_name in list_usernames:
        user_id, key_string = KEY_MANAGER.get_key(user_name)
        user = {}
        user["id"] = user_id
        user["name"] = user_name
        user["key"] = key_string
        response.append(user)
    response_json = json.dumps(response)
    return HttpResponse(response_json)


# Views for /file/
@csrf_exempt
def upload(request):
    """Receives an encrypted file (with encrypted index) and adds it to the database"""
    body = request.body.decode("ascii")
    message_dict = json.loads(body)
    # bind each element of B to a user_id using a dict ?
    B_list = message_dict["B"].copy()
    message_dict["B"] = {}
    for i, b in enumerate(B_list):
        user_id = message_dict["id_list"][i]
        message_dict["B"][user_id] = b
    del message_dict["id_list"]
    n_files = len(os.listdir(MEDIA_ROOT))
    new_filename = f"{MEDIA_ROOT}file_{n_files + 1}.json"
    print(message_dict)
    with open(new_filename, 'w') as outfile:
        json.dump(message_dict, outfile)
    print(f"File uploaded, there are {n_files + 1} on the server")

    return HttpResponse("File uploaded !")


@csrf_exempt
def search(request):
    """Receives a trapdoor in the request and performs a search in all the files, replies with a list of matching ciphertexts (encoded with base64)"""
    body = request.body.decode("ascii")
    # HACK: Use json to obtain list, does only work if string delimiters in the list are double quotes
    request_dict = json.loads(body)
    trapdoor_list = request_dict["trapdoor"]
    user_id = str(request_dict["id"])
    # TODO: fix user id, using a dict...
    list_files = os.listdir(MEDIA_ROOT)
    list_files = [file for file in list_files if not file.startswith(".")]
    list_results = []
    for file_to_test in list_files:
        with open(MEDIA_ROOT + file_to_test, "r") as file_in:
            ciphertext_dict = json.load(file_in)
            # Test(_A: Element, _B: List[Element], _C: List[Element], T: List[Union[int, Element]], j: int, genkey: KeyManager):
            test_result = Test(ciphertext_dict["A"], ciphertext_dict["B"], ciphertext_dict["C"], trapdoor_list, user_id, KEY_MANAGER)
            print(file_to_test, test_result)
            if test_result == 1:
                # add the ciphertext to the list that should be sent back
                result = {}
                result["E"] = ciphertext_dict["E"]
                result["A"] = ciphertext_dict["A"]
                result["B"] = ciphertext_dict["B"][user_id]
                list_results.append(result)

    # the response is a JSON list of elements, each one containing E, A and bj
    response = json.dumps(list_results)
    return HttpResponse(response)
