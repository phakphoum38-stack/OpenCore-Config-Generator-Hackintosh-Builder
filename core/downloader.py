import requests
import zipfile
import os

download_opencore()
def download_opencore():
    print("⬇️ Downloading OpenCore...")

    api_url = "https://api.github.com/repos/acidanthera/OpenCorePkg/releases/latest"
    res = requests.get(api_url).json()

    # หา asset zip
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

    # download
    with requests.get(zip_url, stream=True) as r:
        with open(zip_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    print("✅ Download complete")

    # unzip
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall("resources/")

    print("📦 Extracted OpenCore")

    # หาโฟลเดอร์ X64
    for folder in os.listdir("resources"):
        if folder.startswith("OpenCore"):
            src = os.path.join("resources", folder, "X64")
            dst = "resources/OpenCore/X64"

            if os.path.exists(dst):
                import shutil
                shutil.rmtree(dst)

            os.makedirs("resources/OpenCore", exist_ok=True)
            os.rename(src, dst)

            print("✅ OpenCore ready at resources/OpenCore/X64")
            break
