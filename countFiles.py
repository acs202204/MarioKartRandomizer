from pathlib import Path

def count_images_in_folder(folder_path):
    """Count images in a specific folder."""
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    image_count = 0
    
    for file in folder_path.rglob('*'):
        if file.is_file() and file.suffix.lower() in image_extensions:
            image_count += 1
    
    return image_count

def count_images(directory=None):
    """Count the number of image files in each subfolder."""
    if directory is None:
        directory = Path(__file__).parent
    else:
        directory = Path(directory)
    
    # Get all subdirectories (not including the root directory itself)
    subdirs = [d for d in directory.iterdir() if d.is_dir()]
    
    total_images = 0
    
    for subdir in sorted(subdirs):
        count = count_images_in_folder(subdir)
        print(f"Folder: {subdir.name}: {count} images")
        total_images += count
    
    print(f"\nTotal images found: {total_images}")
    
    return total_images

if __name__ == "__main__":
    total = count_images()
