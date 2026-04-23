import plistlib

def generate_config_plist(config: dict, output_path="EFI/OC/config.plist"):
    with open(output_path, "wb") as f:
        plistlib.dump(config, f)

    print(f"✅ Generated: {output_path}")
