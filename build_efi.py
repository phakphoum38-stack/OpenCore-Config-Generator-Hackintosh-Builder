from core.kext_manager import resolve_kexts
from core.config_generator import generate_config, generate_config_plist
from core.validator import validate

import os
import shutil

# 🔧 hardware (เดี๋ยวค่อยเปลี่ยนเป็น YAML ได้)
hardware = {
    "cpu": "Intel Raptor Lake",
    "gpu": "Intel"
}

# 🔧 สร้างโครง EFI
def create_efi_structure():
    paths = [
        "EFI/OC",
        "EFI/OC/Kexts",
        "EFI/OC/ACPI",
        "EFI/OC/Drivers"
    ]

    for path in paths:
        os.makedirs(path, exist_ok=True)

    print("✅ EFI folder structure created")

# 🔧 zip EFI
def zip_efi():
    shutil.make_archive("EFI", 'zip', "EFI")
    print("📦 EFI.zip created")

# 🔥 process
kexts = resolve_kexts(hardware)
config = generate_config(hardware, kexts)

errors = validate(config)

if errors:
    print("❌ Error:", errors)
else:
    print("✅ EFI Ready")

    # 👇 สำคัญมาก (ของคุณยังไม่มี)
    create_efi_structure()

    # 👇 สร้าง config.plist
    generate_config_plist(config)

    # 👇 zip
    zip_efi()
