# 📁 Downloads Organizer (macOS Only)

This Python script automatically organizes your **Downloads** folder by sorting files into categorized subfolders whenever files are added. It runs silently in the background on macOS using **LaunchAgents**.

---

## ✅ Features

* Sorts files into: `Images`, `Videos`, `Documents`, `Music`, `Code`, and `Other`
* Detects code folders and organizes them too
* Handles duplicate filenames gracefully
* Runs automatically whenever the Downloads folder changes

---

## 💻 Requirements

* macOS (Monterey or newer recommended)
* Homebrew-installed Python 3.13 (preferred)

  * Check with: `brew install python@3.13`
  * Verify with: `python3 --version`

> ⚠️ You must grant **Full Disk Access** to the Python binary so it can manage your Downloads folder. Instructions are below.

---

## 🛠️ Setup Instructions (macOS)

### 1. Clone This Repository

```bash
git clone https://github.com/boraytuna/Downloads-Organizer.git
cd Downloads-Organizer
```

---

### 2. Move the Script to a Permanent Location

```bash
mkdir -p ~/Scripts
cp downloads_organizer.py ~/Scripts/
```

---

### 3. Install the LaunchAgent

Copy the provided `downloads_agent.plist` file to your LaunchAgents directory:

```bash
cp downloads_agent.plist ~/Library/LaunchAgents/com.user.downloadsorganizer.plist
```

The plist is configured to:

* Watch your `~/Downloads` folder
* Run the organizer script **once** whenever the folder changes

---

### 4. Update the Plist to Use Your Homebrew Python

First, locate the full path of Homebrew’s Python:

```bash
readlink -f /opt/homebrew/bin/python3
```

It should look like:

```
/opt/homebrew/Cellar/python@3.13/3.13.7/Frameworks/Python.framework/Versions/3.13/bin/python3.13
```

Edit the `ProgramArguments` section of the plist to use this path instead of `/usr/bin/python3`.

---

### 5. Grant Full Disk Access

1. Open **System Settings** → **Privacy & Security** → **Full Disk Access**
2. Click **+** and add the Python binary you found above (e.g., `python3.13` from the Cellar path)
3. Toggle it **ON**

This allows the script to manage files in `~/Downloads`.

---

### 6. Load the LaunchAgent

```bash
launchctl load ~/Library/LaunchAgents/com.user.downloadsorganizer.plist
```

Now the script will run silently in the background whenever a file is added to `~/Downloads`.

---

## 🧪 Test It

Drop a file into `~/Downloads`:

```bash
touch ~/Downloads/test.txt
sleep 2
tail -n 20 ~/Library/Logs/DownloadsOrganizer.log
```

You should see a log entry moving the file to `~/Downloads/Documents/test.txt`.

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

---

## 🧼 What Gets Organized

| Category      | File Types Included                               |
| ------------- | ------------------------------------------------- |
| **Images**    | .jpg, .jpeg, .png, .gif, .bmp, .webp, .svg        |
| **Videos**    | .mp4, .mov, .avi, .mkv                            |
| **Documents** | .pdf, .docx, .txt, .csv, .pptx, .xlsx             |
| **Music**     | .mp3, .wav, .aac, .flac                           |
| **Code**      | .py, .js, .html, .css, .java, .cpp, .json, .ipynb |
| **Other**     | Anything that doesn’t fit the above               |

---

## 🙌 Credits

Built with 💻 by [@boraytuna](https://github.com/boraytuna)

---

### 🚀 Quick One-Liner to Reactivate Service

If you ever want to reload and see logs:

```bash
launchctl unload ~/Library/LaunchAgents/com.user.downloadsorganizer.plist 2>/dev/null; \
launchctl load ~/Library/LaunchAgents/com.user.downloadsorganizer.plist; \
tail -n 20 ~/Library/Logs/DownloadsOrganizer.log
```
