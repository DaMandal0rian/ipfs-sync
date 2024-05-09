import logging
from typing import List, Dict
from utils import get_cid, post_cid, parse_http_body, get_cid_version, print_log_message, unmarshal_ipfs_response

def sync_cids(src: str, dst: str, cids: List[Dict[str, str]]) -> tuple[int, int]:
    synced = 0
    failed = 0

    for index, cid_data in enumerate(cids, start=1):
        cid = cid_data["cid"]
        print_log_message(index, len(cids), cid, "Syncing")

        try:
            src_url = f"{src}{CAT_ENDPOINT}{cid}"
            response = get_cid(src_url)
            payload = parse_http_body(response)

            dst_url = f"{dst}{IPFS_PIN_ENDPOINT}?cid-version={get_cid_version(cid)}"
            response = post_cid(dst_url, payload)
            result = unmarshal_ipfs_response(response)

            if any(item["Hash"] == cid for item in result):
                print_log_message(index, len(cids), cid, "Successfully synced")
                synced += 1
            else:
                raise Exception("The source and destination IPFS Hash differ")

        except Exception as e:
            print_log_message(index, len(cids), cid, str(e))
            failed += 1

    return synced, failed
