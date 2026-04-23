import requests
import zipfile
import os
import shutil

def download_opencore():
    api_url = "https://api.github.com/repos/acidanthera/OpenCorePkg/releases/latest"

    # 🔥 กันโหลดซ้ำ
    if os.path.exists("resources/OpenCore/X64"):
        print("⚡ OpenCore already exists, skip download")
        return

    print("⬇️ Downloading OpenCore...")

    # ✅ ใช้ response ตัวเดียว
    response = requests.get(api_url)

    if response.status_code != 200:
        print("❌ Failed to connect GitHub")
        return

    res = response.json()

    if "assets" not in res:
        print("❌ GitHub API error")
        return

    # 🔍 หา zip
    zip_url = None
    for asset in res.get("assets", []):
        if "RELEASE" in asset["name"] and asset["name"].endswith(".zip"):
            zip_url = asset["browser_download_url"]
            break

    if not zip_url:
        print("❌ OpenCore release not found")
        return

    os.makedirs("resources", exist_ok=True)
    zip_path = "resources/opencore.zip"

    # 📥 download
    with requests.get(zip_url, stream=True) as r:
        with open(zip_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    print("✅ Download complete")

    # 📦 unzip
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall("resources/")

    print("📦 Extracted OpenCore")

    # 📂 ย้าย X64
    for folder in os.listdir("resources"):
        if folder.startswith("OpenCore"):
            src = os.path.join("resources", folder, "X64")
            dst = "resources/OpenCore/X64"

            if os.path.exists(dst):
                shutil.rmtree(dst)

            os.makedirs("resources/OpenCore", exist_ok=True)
            os.rename(src, dst)

            print("✅ OpenCore ready at resources/OpenCore/X64")
            break
