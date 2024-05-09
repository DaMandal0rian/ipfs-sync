import os
import requests

# Read the CIDs from a file
with open('cids.txt', 'r') as file:
    cids = file.read().splitlines()

# Set the source and destination IPFS gateways
source_gateway = 'https://ipfs.thegraph.com'
destination_gateway = 'https://api.thegraph.com'

# Create a directory to store the downloaded files
os.makedirs('downloaded_files', exist_ok=True)

# Iterate over each CID
for cid in cids:
    # Construct the source URL
    source_url = f"{source_gateway}/ipfs/api/v0/cat?arg={cid}"

    # Download the file from the source gateway
    response = requests.get(source_url)

    # Save the file locally
    file_path = os.path.join('downloaded_files', cid)
    with open(file_path, 'wb') as file:
        file.write(response.content)

    # Add the file to the destination gateway
    add_url = f"{destination_gateway}/ipfs/api/v0/add?pin=true&cid-version=1"
    files = {'file': open(file_path, 'rb')}
    response = requests.post(add_url, files=files)

    if response.status_code == 200:
        print(f"Copied and pinned file: {cid}")
    else:
        print(f"Failed to copy and pin file: {cid}")
        print(f"Error: {response.text}")

print("Finished copying and pinning files.")
