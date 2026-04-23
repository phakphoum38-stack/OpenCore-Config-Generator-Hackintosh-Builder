def resolve_kexts(hardware):
    kexts = ["Lilu", "VirtualSMC"]

    if hardware.get("gpu") == "AMD":
        kexts.append("WhateverGreen")

    return list(set(kexts))
