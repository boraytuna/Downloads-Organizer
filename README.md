# 📁 Downloads Organizer (macOS Only)

This Python script automatically organizes your **Downloads** folder by sorting files into categorized subfolders every 60 seconds. It runs quietly in the background and can be set to launch every time your Mac starts up.

---

## ✅ Features

- Sorts files into: `Images`, `Videos`, `Documents`, `Music`, `Code`, and `Other`
- Detects folders with code and organizes them
- Handles duplicate filenames gracefully
- Runs in the background 24/7 using macOS LaunchAgents

---

## 💻 Requirements

- macOS (Monterey or newer recommended)
- Python 3 (check by running: `python3 --version`)

---

## 🛠️ Setup Instructions (macOS)

### 1. Clone This Repository

Run the following commands in your terminal:

git clone https://github.com/boraytuna/Downloads-Organizer.git  
cd Downloads-Organizer

---

### 2. Move the Script Somewhere Permanent

mkdir -p ~/Scripts  
cp downloads_organizer.py ~/Scripts/

---

## 3. Create a LaunchAgent to Run at Login

Copy the `downloads_agent.plist` file from this repo to your LaunchAgents directory:

cp downloads_agent.plist ~/Library/LaunchAgents/com.user.downloadsorganizer.plist

> 📌 Make sure to replace `YOUR_USERNAME` in the file path with your actual macOS username before running the next step.


---

### 4. Load the LaunchAgent

launchctl load ~/Library/LaunchAgents/com.user.downloadsorganizer.plist

The script will now run in the background and auto-start whenever your Mac reboots.

---

## 🧪 Optional: Test It Immediately

To run the script manually and confirm it works:

python3 ~/Scripts/downloads_organizer.py

To stop it later, press Control + C.

---

## 🔧 Managing the Background Script

To stop the background service:

launchctl unload ~/Library/LaunchAgents/com.user.downloadsorganizer.plist

To check logs:

tail -f /tmp/downloadsorganizer.out

---

## 🧼 What Gets Organized

| Category   | File Types Included |
|------------|---------------------|
| **Images** | .jpg, .jpeg, .png, .gif, .bmp, .webp, .svg |
| **Videos** | .mp4, .mov, .avi, .mkv |
| **Documents** | .pdf, .docx, .txt, .csv, .pptx, .xlsx |
| **Music** | .mp3, .wav, .aac, .flac |
| **Code** | .py, .js, .html, .css, .java, .cpp, .json |
| **Other** | Anything that doesn’t fit the above |

---

## 🙌 Credits

Built with 💻 by [@boraytuna](https://github.com/boraytuna)