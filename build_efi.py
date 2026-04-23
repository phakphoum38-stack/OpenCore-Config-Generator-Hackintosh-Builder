from core.kext_manager import resolve_kexts
from core.config_generator import generate_config
from core.validator import validate

hardware = {
    "cpu": "Intel Raptor Lake",
    "gpu": "Intel"
}

kexts = resolve_kexts(hardware)
config = generate_config(hardware, kexts)

errors = validate(config)

if errors:
    print("❌ Error:", errors)
else:
    print("✅ EFI Ready")
