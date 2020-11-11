from dataclasses import dataclass


@dataclass
class SecondaryNode:
    port: str
    protocol: str = 'http'
    url: str = '127.0.0.1'
