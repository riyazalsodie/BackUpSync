# 🌌 BackUp Sync

<p align="center">
  <img src="backupsync_mockup.png" alt="BackUp Sync Mockup" width="600">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/PyQt6-v6.4+-41CD52?style=for-the-badge&logo=qt&logoColor=white" alt="PyQt6">
  <img src="https://img.shields.io/badge/Windows-Supported-0078D4?style=for-the-badge&logo=windows&logoColor=white" alt="Windows">
  <img src="https://img.shields.io/badge/Status-Production--Ready-success?style=for-the-badge" alt="Production Ready">
</p>

---

## ✨ Overview

**BackUp Sync** is a professional-grade, high-performance directory synchronization utility meticulously crafted for power users and developers. Combining a stunning **OLED Dark Aesthetic** with a robust synchronization engine, it ensures your data is always safe, organized, and synced with clinical precision.

Developed by **[R ! Y 4 Z](https://riyazz.dev)**, this tool isn't just a utility—it's a statement of UI/UX excellence.

---

## 🚀 Elite Features

### 💎 Premium OLED Interface
- **Frameless Window Design**: Clean, modern edges with intuitive drag-and-drop movement.
- **Glassmorphism & Glow**: Custom components featuring subtle glows and translucent frames.
- **Rainbow Typography**: Dynamic headers that shift colors for a premium feel.
- **System Tray Dominance**: Seamlessly minimizes to the tray with custom notifications.

### ⚙️ Professional Sync Engine
- **Conflict Strategies**: 
    - `Overwrite`: Force consistency across directories.
    - `Skip`: Preserve existing targets if they exist.
    - `Create`: Generate unique variants for conflicting files.
    - `Smart Sync`: Intelligent merging based on file metadata.
- **Pattern Filtering**: Comprehensive `.gitignore` support to exclude `node_modules`, `.git`, temporary logs, and build artifacts.
- **Real-Time Analytics**: Monitor throughput (MB/s), file counts, and elapsed time with an animated progress tracking system.

### 🛡️ Reliability & Integration
- **Always-on-Top (Pin)**: Keep your sync status visible while you work.
- **Boot Persistence**: Optional system startup integration to keep your backups automated from the moment you log in.
- **Toast Notifications**: Smooth, non-intrusive feedback upon task completion.

---

## 🛠 Installation & Usage

### 📦 For Users (Executable)
1. Download the latest `BackUpSync.exe` from the [Releases](#) tab.
2. Launch and select your **Source** and **Target** directories.
3. Configure your **Conflict Strategy** and **Filters**.
4. Hit **BACKUP** and let the engine handle the rest.

### 🧪 For Developers (Source)
```bash
# Clone the repository
git clone https://github.com/riyazalsodie/BackUpSync.git

# Enter the directory
cd BackUpSync

# Install dependencies
pip install PyQt6

# Run the application
python main.py
```

---

## 📊 Technical Stack

| Component | Technology |
| :--- | :--- |
| **Core Framework** | Python 3.x |
| **GUI Framework** | PyQt6 (Qt v6.4+) |
| **Styles** | Custom QSS (OLED Optimized) |
| **Packaging** | PyInstaller |
| **Logic** | Multi-threaded Backup Engine |

---

## 🤝 Contribution

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="center">
  <br>
  Built with ❤️ by <b>R ! Y 4 Z</b>
</p>
