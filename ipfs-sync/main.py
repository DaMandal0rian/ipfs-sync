import time
import logging
import argparse
from sync import sync_cids
from utils import read_cids_from_file, slice_to_cids_struct, get_cids_from_source

logging.basicConfig(level=logging.INFO)

def main():
    parser = argparse.ArgumentParser(description="Sync IPFS objects")
    parser.add_argument("--source", "-s", required=True, help="IPFS source endpoint")
    parser.add_argument("--destination", "-d", required=True, help="IPFS destination endpoint")
    parser.add_argument("--from-file", "-f", help="Sync CIDs from file")
    args = parser.parse_args()

    time_start = time.time()
    failed = 0
    synced = 0

    if args.from_file:
        logging.info(f"Syncing from {args.source} to {args.destination} using the file <{args.from_file}> as input")
        cids = read_cids_from_file(args.from_file)
        cids_struct = slice_to_cids_struct(cids)
    else:
        logging.info(f"Syncing from {args.source} to {args.destination}")
        cids_struct = get_cids_from_source(args.source)

    synced, failed = sync_cids(args.source, args.destination, cids_struct)

    logging.info(f"Total number of objects: {len(cids_struct)}; Synced: {synced}; Failed: {failed}")
    logging.info(f"Total time: {time.time() - time_start}")

if __name__ == "__main__":
    main()
