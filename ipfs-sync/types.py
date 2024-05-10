from typing import List, Dict

class Link:
    def __init__(self, name: str, hash: str, size: int, type: int, target: str):
        self.name = name
        self.hash = hash
        self.size = size
        self.type = type
        self.target = target

class Object:
    def __init__(self, links: List[Link], hash: str):
        self.links = links
        self.hash = hash
