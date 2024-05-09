import os
import json
import time
import requests
from typing import List, Dict, Union

DIR_LIST_ENDPOINT = "/ipfs/api/v0/ls?arg="
PIN_LIST_ENDPOINT = "/ipfs/api/v0/pin/ls?stream=true"
CAT_ENDPOINT = "/ipfs/api/v0/cat?arg="
IPFS_PIN_ENDPOINT = "/ipfs/api/v0/add"
HEADER_APP_JSON = "application/json"
DIR_ERROR = "this dag node is a directory"

def create_temp_dir_with_file(file_path: List[str]) -> str:
    dir_path = os.path.join(*file_path[:-1])
    os.makedirs(dir_path, exist_ok=True)
    file_name = os.path.join(dir_path, file_path[-1])
    open(file_name, "a").close()
    return file_name

def get_cid(url: str, payload: Union[Dict, None] = None) -> requests.Response:
    headers = {"User-Agent": "graphprotocol/ipfs-mgm"}
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code >= 400:
        error_response = response.json()
        if error_response.get("Message") == DIR_ERROR:
            raise Exception(f"Cannot get this IPFS CID. Error message: {error_response['Message']}")
        else:
            raise Exception(f"There was an error with the request. Error code: HTTP {response.status_code}")

    return response

def post_cid(dst: str, payload: bytes, file_path: str = "") -> requests.Response:
    if file_path:
        temp_file_name = file_path.split("/")
        base = temp_file_name[0]
        if len(temp_file_name) > 2:
            temp_file_name = temp_file_name[1:]
            base = temp_file_name[0]
    else:
        base = str(int(time.time() * 1e9))
        temp_file_name = [base, "ipfs-data.tmp"]

    temp_file = create_temp_dir_with_file(temp_file_name)

    with open(temp_file, "wb") as f:
        f.write(payload)

    with open(temp_file, "rb") as f:
        files = {"file": f}
        headers = {"User-Agent": "graphprotocol/ipfs-mgm"}

        if file_path:
            file_name_parts = temp_file_name[-1].split(".")
            file_name = file_name_parts[0]
            headers["Content-Disposition"] = f'form-data; name="{file_name}"; filename={os.path.basename(file_path)}'
            headers["Abspath"] = str(temp_file_name)

        response = requests.post(dst, files=files, headers=headers)

    os.remove(temp_file)

    if response.status_code >= 400:
        raise Exception(f"The endpoint responded with: HTTP {response.status_code}")

    return response

def parse_http_body(response: requests.Response) -> bytes:
    return response.content

def get_cid_version(cid: str) -> str:
    return "0" if cid.startswith("Qm") else "1"

def print_log_message(counter: int, length: int, cid: str, message: str) -> None:
    logging.info(f"{counter}/{length} ({cid}): {message}")

def slice_to_cids_struct(slice: List[str]) -> List[Dict[str, str]]:
    return [{"cid": item} for item in slice]

def unmarshal_ipfs_response(response: requests.Response) -> List[Dict[str, str]]:
    return response.json()

def read_cids_from_file(file_path: str) -> List[str]:
    with open(file_path, "r") as file:
        cids = file.read().splitlines()
    return cids

def get_cids_from_source(src: str) -> List[Dict[str, str]]:
    url = f"{src}{PIN_LIST_ENDPOINT}"
    response = get_cid(url)
    cids_struct = unmarshal_ipfs_response(response)
    return cids_struct
