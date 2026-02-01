# 📁 Downloads Organizer (macOS Only)

A lightweight macOS automation that keeps your **Downloads** folder clean by automatically organizing files into categorized subfolders.

It runs silently in the background using a macOS **LaunchAgent**, safely handling browser downloads and avoiding partial or broken files.

---

## ✨ What It Does

- Automatically organizes `~/Downloads` into folders like:
  - Documents, Images, Videos, Music, Code, Archives, Apps, and more
- Skips partial browser downloads (`.download`, `.crdownload`, `.part`)
- Only moves files once they are fully downloaded and stable
- Handles duplicate filenames safely
- No UI, no notifications, near-zero system impact

---

## ⚙️ How It Works

- A macOS **LaunchAgent** runs the script every **20 seconds**
- Each run:
  1. Scans the Downloads folder
  2. Skips incomplete or temporary files
  3. Moves completed files into the correct category
  4. Exits immediately

This interval-based approach is more reliable than filesystem event triggers for browser downloads.

---

## 🛠️ Setup (Quick)

### 1. Clone the Repository
```bash
git clone https://github.com/boraytuna/Downloads-Organizer.git
cd Downloads-Organizer
```

---

### 2. Move the Script to a Permanent Location

```bash
mkdir -p ~/Scripts
cp downloads_organizer.py ~/Scripts/
chmod +x ~/Scripts/downloads_organizer.py
```

---

### 3. Install the LaunchAgent

Copy the provided `downloads_agent.plist` file to your LaunchAgents directory:

```bash
cp downloads_agent.plist ~/Library/LaunchAgents/com.user.downloadsorganizer.plist
```

* Open the plist and replace YOURUSERNAME with your macOS username.

---

### 4.Load the LaunchAgent
```bash
UID=$(id -u)

launchctl bootout gui/$UID ~/Library/LaunchAgents/com.user.downloadsorganizer.plist 2>/dev/null
launchctl bootstrap gui/$UID ~/Library/LaunchAgents/com.user.downloadsorganizer.plist
launchctl enable gui/$UID/com.user.downloadsorganizer
```
---

### 5. Grant Full Disk Access

1. Open **System Settings** → **Privacy & Security** → **Full Disk Access**
2. Add and enable:
```bash
/opt/homebrew/bin/python3
```

---

## 🧪 Test It

```bash
echo "test" > ~/Downloads/test_file.pdf
sleep 25
ls ~/Downloads/Documents | grep test_file
```
* If the file moves, eveything is working.

---

## 🔧 Managing the Service

Stop the background service:

```bash
launchctl unload ~/Library/LaunchAgents/com.user.downloadsorganizer.plist
```

Reload it:

```bash
launchctl load ~/Library/LaunchAgents/com.user.downloadsorganizer.plist
```

Check logs:

```bash
tail -f ~/Library/Logs/DownloadsOrganizer.log
```

LaunchAgent Errors:

```bash
/tmp/downloadsorganizer.err
```
---

## 📂 Categories & File Types

| Category | File Types |
|--------|------------|
| **Documents** | `.pdf`, `.doc`, `.docx`, `.txt`, `.rtf`, `.csv`, `.tsv`, `.ppt`, `.pptx`, `.key`, `.xls`, `.xlsx`, `.numbers`, `.pages`, `.md`, `.tex` |
| **Images** | `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.tif`, `.webp`, `.svg`, `.heic`, `.raw`, `.cr2`, `.nef`, `.arw`, `.dng` |
| **Videos** | `.mp4`, `.mov`, `.avi`, `.mkv`, `.flv`, `.wmv`, `.webm`, `.m4v`, `.mpeg`, `.mpg` |
| **Music** | `.mp3`, `.wav`, `.aiff`, `.aac`, `.flac`, `.m4a`, `.ogg`, `.alac` |
| **Code** | `.py`, `.js`, `.ts`, `.tsx`, `.jsx`, `.html`, `.css`, `.scss`, `.java`, `.kt`, `.cpp`, `.c`, `.hpp`, `.h`, `.cs`, `.swift`, `.rs`, `.go`, `.sh`, `.zsh`, `.bash`, `.rb`, `.php`, `.sql`, `.json`, `.yaml`, `.yml`, `.toml`, `.ipynb`, `.xml` |
| **Archives** | `.zip`, `.rar`, `.7z`, `.tar`, `.gz`, `.bz2`, `.xz`, `.tgz` |
| **DiskImages** | `.dmg`, `.iso` |
| **Installers** | `.pkg`, `.mpkg` |
| **Apps** | `.app` |
| **Fonts** | `.ttf`, `.otf`, `.woff`, `.woff2` |
| **Design** | `.fig`, `.sketch`, `.xd`, `.psd`, `.ai` |
| **3D** | `.blend`, `.fbx`, `.obj`, `.stl`, `.dae`, `.glb`, `.gltf` |
| **Torrents** | `.torrent` |
| **Subtitles** | `.srt`, `.vtt` |
| **Certificates** | `.pem`, `.crt`, `.cer`, `.key`, `.p12` |
| **VM** | `.ova`, `.ovf`, `.vdi`, `.vmdk` |
| **Logs** | `.log` |
| **Other** | Anything that doesn’t match the categories above |
---

## 🙌 Credits

Built with 💻 by [@boraytuna](https://github.com/boraytuna)

