import os
import shutil
import time
from pathlib import Path
from PyQt6.QtCore import QThread, pyqtSignal

class BackupEngine(QThread):
    progress = pyqtSignal(int, str, int, int, float)  # percentage, message, current, total, size_mb
    finished = pyqtSignal(bool, str, dict) # success, message, stats

    def __init__(self, source, target, gitignore_handler, mode="overwrite"):
        super().__init__()
        self.source = Path(source)
        self.target = Path(target)
        self.handler = gitignore_handler
        self.mode = mode.lower()
        self._is_running = True

    def stop(self):
        self._is_running = False

    def run(self):
        stats = {
            "total_files": 0,
            "total_size": 0,
            "elapsed_time": 0,
            "speed": 0
        }
        start_time = time.time()
        
        try:
            if not self.source.exists():
                self.finished.emit(False, f"Source directory does not exist: {self.source}", stats)
                return
            
            self.target.mkdir(parents=True, exist_ok=True)
            
            # Count total files for progress calculation
            all_files = []
            total_size_bytes = 0
            
            self.progress.emit(0, "Scanning directories...", 0, 0, 0.0)
            
            for root, dirs, files in os.walk(self.source):
                if not self._is_running: return
                
                # Check for .gitignore in current directory
                if ".gitignore" in files:
                    gi_path = Path(root) / ".gitignore"
                    try:
                        with open(gi_path, "r", encoding="utf-8") as f:
                            rel_root = Path(root).relative_to(self.source)
                            # Scope patterns to this directory if it's not the root
                            scope = rel_root if rel_root != Path('.') else None
                            self.handler.add_patterns(f.read(), scope_path=scope)
                    except Exception:
                        pass # Silently skip malformed gitignores

                # Prune dirs in-place to avoid walking into ignored directories
                dirs[:] = [d for d in dirs if not self.handler.is_ignored(Path(root) / d, self.source)]
                
                for f in files:
                    file_path = Path(root) / f
                    if not self.handler.is_ignored(file_path, self.source):
                        all_files.append(file_path)
                        total_size_bytes += file_path.stat().st_size
            
            total_files = len(all_files)
            stats["total_files"] = total_files
            stats["total_size"] = total_size_bytes
            
            if total_files == 0:
                self.finished.emit(True, "No files to backup (all ignored or empty).", stats)
                return

            for i, src_file in enumerate(all_files):
                if not self._is_running: break
                
                rel_path = src_file.relative_to(self.source)
                dest_file = self.target / rel_path
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                
                skip = False
                if dest_file.exists():
                    if self.mode == "skip":
                        skip = True
                    elif self.mode == "create":
                        # Create versioned name: file (1).txt
                        base = dest_file.stem
                        suffix = dest_file.suffix
                        counter = 1
                        while dest_file.exists():
                            dest_file = dest_file.parent / f"{base} ({counter}){suffix}"
                            counter += 1
                    elif self.mode == "smart sync":
                        src_stat = src_file.stat()
                        dest_stat = dest_file.stat()
                        
                        # Use a 1.0s threshold for modification time comparison
                        time_diff = abs(src_stat.st_mtime - dest_stat.st_mtime)
                        size_match = src_stat.st_size == dest_stat.st_size
                        
                        # If time diff is small AND size is the same, skip
                        if time_diff < 1.0 and size_match:
                            skip = True
                    # Overwrite is default behavior (shutil.copy2)

                if not skip:
                    try:
                        os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                        shutil.copy2(src_file, dest_file)
                        stats["files_copied"] = stats.get("files_copied", 0) + 1
                        stats["total_size"] = stats.get("total_size", 0) + os.path.getsize(src_file)
                    except (PermissionError, OSError):
                        pass # Skip locked files
                
                percent = int(((i + 1) / total_files) * 100)
                size_mb = stats["total_size"] / (1024 * 1024)
                self.progress.emit(percent, f"Backing up: {rel_path}", i + 1, total_files, size_mb)
                
                if i % 100 == 0: time.sleep(0.01) # Yield to system

            end_time = time.time()
            duration = end_time - start_time
            stats["elapsed_time"] = duration
            if duration > 0:
                stats["speed"] = total_size_bytes / duration / (1024 * 1024) # MB/s

            if self._is_running:
                self.finished.emit(True, f"Backup completed successfully! {len(all_files)} files processed.", stats)
            else:
                self.finished.emit(False, "Backup stopped by user.", stats)

        except Exception as e:
            self.finished.emit(False, f"Error during backup: {str(e)}", stats)
