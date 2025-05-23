# 📁 Downloads Organizer (macOS + Windows)

This Python script automatically organizes your **Downloads** folder by sorting files into subfolders based on file extensions. It runs silently in the background and can be configured to launch on startup.

---

## ✅ What It Does

- Organizes files every 60 seconds into:
  - `Images`, `Videos`, `Documents`, `Music`, `Code`, and `Other`
- Automatically handles duplicate files
- Detects folders containing code and moves them into the `Code` folder
- Supports macOS LaunchAgent setup for always-on functionality

---

## 💻 Supported Platforms

- ✅ macOS (background automation via LaunchAgent)
- ✅ Windows (via Task Scheduler or manual run)

---

## 🔧 Setup Instructions (macOS)

### 1. Clone the Repo

```bash
git clone https://github.com/boraytuna/Downloads-Organizer.git
cd Downloads-Organizer
