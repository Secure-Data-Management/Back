import json
import os
from django.shortcuts import render
from django.http import HttpResponse
from server.global_variables import KEY_MANAGER
from django.views.decorators.csrf import csrf_exempt
from backend_project.settings import MEDIA_ROOT
from server.mpeck_test import Test


# Create your views here.
def home(request):
    return HttpResponse("Test, 123")


# Views for /keys/
def get_params(request):
    params_string = KEY_MANAGER.get_parameters()
    return (HttpResponse(params_string))


def get_generator(request):
    """Returns the generator g as a string"""
    g_string = KEY_MANAGER.get_g()
    print("sending g: ", KEY_MANAGER.g)
    return HttpResponse(g_string)


def add_key(request):
    """Receives the key as a get parameter (?key=...) and a username (?user=...) and adds it to the KeyManager"""
    new_key = request.GET.get("key", "")
    username = request.GET.get("user", "")
    if new_key == "":
        return HttpResponse("No key sent")
    else:
        if username == "":
            n_users = len(KEY_MANAGER.public_keys)
            username = f"user_{n_users}"
        print(f"Received key: {new_key}, from user={username}")
        if username in KEY_MANAGER.public_keys:
            return HttpResponse("User already exists !")
        else:
            user_id = KEY_MANAGER.add_key(new_key, username)
            return HttpResponse(str(user_id))

def get_key(request):
    """Receives a username in get paramater and returns his public key (if user exists)"""
    username = request.GET.get("user", "")
    if username == "":
        return HttpResponse("No user specified")
    else:
        if username not in KEY_MANAGER.public_keys:
            return HttpResponse("This user does not exist")
        else:
            key_string = KEY_MANAGER.get_key(username)
            return HttpResponse(key_string)

# Views for /file/
@csrf_exempt
def upload(request):
    """Receives an encrypted file (with encrypted index) and adds it to the database"""
    body = request.body.decode("ascii")
    message_dict = json.loads(body)

    n_files = len(os.listdir(MEDIA_ROOT))
    print(f"There are {n_files} on the server")
    new_filename = f"{MEDIA_ROOT}file_{n_files + 1}.json"
    with open(new_filename, 'w') as outfile:
        json.dump(message_dict, outfile)

    return HttpResponse("File uploaded !")


@csrf_exempt
def search(request):
    """Receives a trapdoor in the request and performs a search in all the files, replies with a list of matching ciphertexts (encoded with base64)"""
    body = request.body.decode("ascii")
    # HACK: Use json to obtain list, does only work if string delimiters in the list are double quotes
    trapdoor_list = json.loads(body)
    # TODO: fix user id, using a dict...
    user_id = 0
    list_files = os.listdir(MEDIA_ROOT)
    list_results = []
    for file_to_test in list_files:
        with open(MEDIA_ROOT + file_to_test, "r") as file_in:
            ciphertext_dict = json.load(file_in)
            # Test(_A: Element, _B: List[Element], _C: List[Element], T: List[Union[int, Element]], j: int, genkey: KeyManager):
            test_result = Test(ciphertext_dict["A"], ciphertext_dict["B"], ciphertext_dict["C"], trapdoor_list, user_id, KEY_MANAGER)
            print(file_to_test, test_result)
            if test_result:
                # add the ciphertext to the list that should be sent back
                list_results.append(ciphertext_dict["E"])
    return HttpResponse(str(list_results))
