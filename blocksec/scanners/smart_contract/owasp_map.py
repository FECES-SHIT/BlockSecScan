"""Slither detector → OWASP Smart Contract Top 10 (SWC) mapping."""

DETECTOR_TO_SWC: dict[str, dict] = {
    "reentrancy": {"swc": "SWC-107", "title": "Reentrancy", "url": "https://swcregistry.io/docs/SWC-107"},
    "unprotected": {"swc": "SWC-105", "title": "Access Control / Unprotected Function", "url": "https://swcregistry.io/docs/SWC-105"},
    "tx-origin": {"swc": "SWC-115", "title": "Tx.Origin Authentication", "url": "https://swcregistry.io/docs/SWC-115"},
    "suicidal": {"swc": "SWC-106", "title": "Self-Destruct / Suicidal", "url": "https://swcregistry.io/docs/SWC-106"},
    "arbitrary-send": {"swc": "SWC-105", "title": "Access Control / Arbitrary Send", "url": "https://swcregistry.io/docs/SWC-105"},
    "unchecked-lowlevel": {"swc": "SWC-104", "title": "Unchecked Call Return Value", "url": "https://swcregistry.io/docs/SWC-104"},
    "unchecked-send": {"swc": "SWC-104", "title": "Unchecked Call Return Value", "url": "https://swcregistry.io/docs/SWC-104"},
    "timestamp": {"swc": "SWC-116", "title": "Timestamp Dependence", "url": "https://swcregistry.io/docs/SWC-116"},
    "weak-prng": {"swc": "SWC-120", "title": "Weak Randomness", "url": "https://swcregistry.io/docs/SWC-120"},
    "divide-before-multiply": {"swc": "SWC-101", "title": "Arithmetic / Integer Overflow", "url": "https://swcregistry.io/docs/SWC-101"},
    "locked-ether": {"swc": "SWC-105", "title": "Access Control / Locked Ether", "url": "https://swcregistry.io/docs/SWC-105"},
    "assembly": {"swc": "SWC-118", "title": "Assembly Usage", "url": "https://swcregistry.io/docs/SWC-118"},
    "naming-convention": {"swc": "SWC-129", "title": "Typographical Error", "url": "https://swcregistry.io/docs/SWC-129"},
    "solc-version": {"swc": "SWC-102", "title": "Outdated Compiler Version", "url": "https://swcregistry.io/docs/SWC-102"},
    "unused-return": {"swc": "SWC-104", "title": "Unchecked Return", "url": "https://swcregistry.io/docs/SWC-104"},
    "incorrect-equality": {"swc": "SWC-132", "title": "Incorrect Equality", "url": "https://swcregistry.io/docs/SWC-132"},
    "shadowing": {"swc": "SWC-119", "title": "Shadowed Variable", "url": "https://swcregistry.io/docs/SWC-119"},
    "controlled-delegatecall": {"swc": "SWC-112", "title": "Delegatecall to Untrusted", "url": "https://swcregistry.io/docs/SWC-112"},
    "constant-function": {"swc": "SWC-131", "title": "Constant State Variable", "url": "https://swcregistry.io/docs/SWC-131"},
    "deprecated-standards": {"swc": "SWC-103", "title": "Deprecated Functions", "url": "https://swcregistry.io/docs/SWC-103"},
    "reentrancy-benign": {"swc": "SWC-107", "title": "Reentrancy (Benign)", "url": "https://swcregistry.io/docs/SWC-107"},
    "reentrancy-no-eth": {"swc": "SWC-107", "title": "Reentrancy (No ETH)", "url": "https://swcregistry.io/docs/SWC-107"},
}


def map_detector_to_owasp(detector_name: str) -> dict:
    for keyword, info in DETECTOR_TO_SWC.items():
        if keyword in detector_name:
            return info
    return {"swc": "N/A", "title": "Other", "url": ""}
