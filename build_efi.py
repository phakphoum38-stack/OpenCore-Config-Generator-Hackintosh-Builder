import os
import shutil
import requests
import zipfile

# ------------------------
# 1. Download OpenCore
# ------------------------
def download_opencore():
    api_url = "https://api.github.com/repos/acidanthera/OpenCorePkg/releases/latest"

    if os.path.exists("resources/OpenCore/X64"):
        print("⚡ OpenCore already exists, skip download")
        return

    print("⬇️ Downloading OpenCore...")

    response = requests.get(api_url)
    if response.status_code != 200:
        print("❌ Failed to connect GitHub")
        return

    res = response.json()
    if "assets" not in res:
        print("❌ GitHub API error")
        return

    zip_url = None
    for asset in res["assets"]:
        if "RELEASE" in asset["name"] and asset["name"].endswith(".zip"):
            zip_url = asset["browser_download_url"]
            break

    if not zip_url:
        print("❌ OpenCore release not found")
        return

    os.makedirs("resources", exist_ok=True)
    zip_path = "resources/opencore.zip"

    with requests.get(zip_url, stream=True) as r:
        with open(zip_path, "wb") as f:
            for chunk in r.iter_content(8192):
                if chunk:
                    f.write(chunk)

    print("✅ Download complete")

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall("resources/")

    print("📦 Extracted OpenCore")

    # move X64
    for folder in os.listdir("resources"):
        if folder.startswith("OpenCore"):
            src = os.path.join("resources", folder, "X64")
            dst = "resources/OpenCore/X64"

            if os.path.exists(dst):
                shutil.rmtree(dst)

            os.makedirs("resources/OpenCore", exist_ok=True)
            os.rename(src, dst)

            print("✅ OpenCore ready")
            break


# ------------------------
# 2. Create EFI structure
# ------------------------
def create_efi():
    os.makedirs("EFI/OC/Kexts", exist_ok=True)
    os.makedirs("EFI/OC/ACPI", exist_ok=True)
    os.makedirs("EFI/OC/Drivers", exist_ok=True)
    print("📁 EFI structure created")


# ------------------------
# 3. Copy OpenCore
# ------------------------
def copy_opencore():
    src = "resources/OpenCore/X64/EFI"
    dst = "EFI"

    if not os.path.exists(src):
        print("❌ OpenCore not found")
        return

    shutil.copytree(src, dst, dirs_exist_ok=True)
    print("✅ OpenCore copied")


# ------------------------
# 4. Dummy config.plist
# ------------------------
def create_config():
    config_path = "EFI/OC/config.plist"
    with open(config_path, "w") as f:
        f.write("<plist><dict><key>Sample</key><string>OK</string></dict></plist>")
    print("🧾 config.plist created")


# ------------------------
# 5. Zip EFI
# ------------------------
def zip_efi():
    if not os.path.exists("EFI"):
        print("❌ EFI not found")
        return

    shutil.make_archive("EFI", "zip", "EFI")
    print("📦 EFI.zip created")


# ------------------------
# MAIN
# ------------------------
def main():
    download_opencore()
    create_efi()
    copy_opencore()
    create_config()
    zip_efi()

if __name__ == "__main__":
    main()
