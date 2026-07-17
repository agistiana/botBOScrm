# utils.py
import os
import shutil
from datetime import datetime

def get_file_size(filepath):
    """Mendapatkan ukuran file dalam format yang mudah dibaca"""
    try:
        size = os.path.getsize(filepath)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} GB"
    except:
        return "0 B"

def get_file_info(filepath):
    """Mendapatkan informasi file"""
    if not os.path.exists(filepath):
        return None
    stat = os.stat(filepath)
    return {
        'name': os.path.basename(filepath),
        'size': get_file_size(filepath),
        'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
        'created': datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
    }

def generate_unique_filename(original_name):
    """Generate nama file unik dengan timestamp"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    name, ext = os.path.splitext(original_name)
    return f"{name}_{timestamp}{ext}"

def safe_delete_file(filepath):
    """Menghapus file dengan aman"""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
    except:
        pass
    return False