# Content-Slicer 🚀

**Content-Slicer** is a modern Python application designed to automate video editing tasks. Built with `customtkinter` and `FFmpeg`, it provides a sleek, dark-themed interface for splitting videos, generating highlights, and optimizng content for TikTok/Reels.

## ✨ Features

- **🎞️ Smart Splitting:**
  - **Split by Parts:** Divide a video into `N` equal parts.
  - **Split by Size:** Automatically calculate parts to fit a specific file size (e.g., 25MB for Discord/WhatsApp).
- **🔥 Highlight Generation:**
  - **Random Highlights:** Extract random interesting segments (e.g., 6 clips of 20 seconds).
  - **Sequential Distribution:** Ensures highlights are spread across the entire video.
- **📱 TikTok/Shorts Mode:**
  - Converts horizontal videos to vertical (9:16).
  - Creates a dynamic montage with crossfade transitions.
  - Adds a professional fade-out effect.
- **🔇 Audio Tools:**
  - Remove audio functionality.

## 🛠️ Prerequisites

1. **Python 3.10+**
2. **FFmpeg** installed and added to your system PATH.
   - [Guide to install FFmpeg](https://ffmpeg.org/download.html)

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ripnsfw222/content-slicer.git
   cd content-slicer
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

Run the main application:
```bash
python main_app.py
```

### How to Use
1. **Drag & Drop** a video file into the window (or use the "Selecionar Vídeo" button).
2. Choose an action from the sidebar or the main panel:
   - **Destaques**: Auto-generate clips.
   - **Gerar TikTok**: CREATE a vertical viral clip.
   - **Cortar**: Split the video as needed.
3. Check the **Log Console** to see the progress.
4. The output files will be saved in the **same folder** as the original video.

## 📝 License

This project is open-source. Feel free to modify and distribute.
