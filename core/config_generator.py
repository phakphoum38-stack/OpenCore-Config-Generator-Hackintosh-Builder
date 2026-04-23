def generate_config(hardware, kexts):
    config = {
        "Booter": {},
        "Kernel": {
            "Add": kexts
        },
        "PlatformInfo": {
            "SMBIOS": "MacBookPro16,1"
        }
    }
    return config
