
import sys
import subprocess

def check_pil_installed():
    """Check if PIL is installed, prompt for installation if not."""
    try:
        from PIL import Image, ImageTk
        return True
    except ImportError:
        print("PIL (Pillow) is not installed.")
        response = input("Would you like to install it now? (y/n): ").strip().lower()
        if response == 'y':
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
                print("Pillow installed successfully!")
                return True
            except subprocess.CalledProcessError:
                print("Failed to install Pillow. Please install it manually.")
                return False
        else:
            print("PIL is required to run this script. Exiting.")
            return False

if not check_pil_installed():
    sys.exit(1)

import random
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def get_random_image(folder_path):
    """Select a random image from the specified folder."""
    folder = Path(folder_path)
    
    # Get all image files in the folder
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    image_files = [f for f in folder.iterdir() if f.is_file() and f.suffix.lower() in image_extensions]
    
    if not image_files:
        print(f"No image files found in {folder}")
        return None
    
    # Select random image
    random_image = random.choice(image_files)
    print(f"Selected image: {random_image.name}")
    
    return random_image

def format_filename(filename):
    """Convert filename to readable format."""
    # Remove file extension
    name = filename.rsplit('.', 1)[0]
    
    # Handle underscore-separated names (convert to spaces)
    if '_' in name:
        name = name.replace('_', ' ')
    else:
        # Handle camelCase - insert spaces before capital letters
        formatted = []
        for i, char in enumerate(name):
            if i > 0 and char.isupper():
                formatted.append(' ')
            formatted.append(char)
        name = ''.join(formatted)
    
    # Capitalize first letter of each word
    name = ' '.join(word.capitalize() for word in name.split())
    
    return name


def display_image(character_path, vehicle_path):
    """Display both images in a tkinter popup window."""
    # Create the main window
    root = tk.Tk()
    root.title("Mario Kart Randomizer")
    root.update()  # Update to get accurate screen dimensions
    
    # Get screen dimensions and set window to 80% of screen size
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = int(screen_width * 0.5)
    window_height = int(screen_height * 0.75)
    root.geometry(f"{window_width}x{window_height}")
    
    # Calculate scaling factor based on screen size (use smaller dimension for consistency)
    scale_factor = min(screen_width, screen_height) / 1440  # 1440 is reference size
    
    # Create a frame for the images
    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    # Labels to store image references
    char_image_label = ttk.Label(frame)
    vehicle_image_label = ttk.Label(frame)
    cup_image_label = ttk.Label(frame)
    course_image_label = ttk.Label(frame)
    char_name_label = ttk.Label(frame, font=("Arial", 10))
    vehicle_name_label = ttk.Label(frame, font=("Arial", 10))
    cup_name_label = ttk.Label(frame, font=("Arial", 10))
    
    # Create bounding boxes with scaled dimensions
    char_box_size = int(320 * scale_factor)
    vehicle_box_size = int(320 * scale_factor)
    cup_box_size = int(200 * scale_factor)
    course_box_size = int(300 * scale_factor)
    thumbnail_char = int(300 * scale_factor)
    thumbnail_vehicle = int(300 * scale_factor)
    thumbnail_cup = int(190 * scale_factor)
    thumbnail_course = int(300 * scale_factor)
    
    # Create bounding boxes (frames with fixed size) for each image
    char_box = tk.Frame(frame, width=char_box_size, height=char_box_size, bg="lightgray")
    char_box.grid(row=2, column=0, padx=10, pady=10)
    char_box.grid_propagate(False)  # Prevent frame from resizing
    
    vehicle_box = tk.Frame(frame, width=vehicle_box_size, height=vehicle_box_size, bg="lightgray")
    vehicle_box.grid(row=2, column=1, padx=10, pady=10)
    vehicle_box.grid_propagate(False)
    
    cup_box = tk.Frame(frame, width=cup_box_size, height=char_box_size, bg="lightgray")
    cup_box.grid(row=2, column=2, padx=10, pady=10)
    cup_box.grid_propagate(False)
    
    course_box = tk.Frame(frame, width=course_box_size, height=char_box_size, bg="lightgray")
    course_box.grid(row=2, column=3, padx=10, pady=10)
    course_box.grid_propagate(False)
    
    # Place image labels inside the bounding boxes (centered)
    char_image_label = ttk.Label(char_box)
    char_image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    vehicle_image_label = ttk.Label(vehicle_box)
    vehicle_image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    cup_image_label = ttk.Label(cup_box)
    cup_image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    course_image_label = ttk.Label(course_box)
    course_image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    # Create fixed-size frames for name labels
    char_name_box = tk.Frame(frame, width=char_box_size, height=int(40 * scale_factor))
    char_name_box.grid(row=3, column=0, padx=10, pady=5)
    char_name_box.grid_propagate(False)
    
    vehicle_name_box = tk.Frame(frame, width=vehicle_box_size, height=int(40 * scale_factor))
    vehicle_name_box.grid(row=3, column=1, padx=10, pady=5)
    vehicle_name_box.grid_propagate(False)
    
    cup_name_box = tk.Frame(frame, width=cup_box_size + course_box_size, height=int(40 * scale_factor))
    cup_name_box.grid(row=3, column=2, columnspan=2, padx=10, pady=5)
    cup_name_box.grid_propagate(False)
    
    def load_and_display_images(char_path, vehicle_path):
        """Load and display the character and vehicle images."""
        nonlocal char_image_label, vehicle_image_label, thumbnail_char, thumbnail_vehicle
        
        # Load and display character image
        try:
            char_image = Image.open(char_path)
            char_image.thumbnail((thumbnail_char, thumbnail_char), Image.Resampling.LANCZOS)
            char_photo = ImageTk.PhotoImage(char_image)
            char_image_label.config(image=char_photo)
            char_image_label.image = char_photo  # Keep a reference
            
            # Update character name
            char_name = format_filename(char_path.name)
            char_name_label.config(text=char_name)
        except Exception as e:
            char_image_label.config(text=f"Error loading character: {e}")
            char_name_label.config(text="Error")
        
        # Load and display vehicle image
        try:
            vehicle_image = Image.open(vehicle_path)
            vehicle_image.thumbnail((thumbnail_vehicle, thumbnail_vehicle), Image.Resampling.LANCZOS)
            vehicle_photo = ImageTk.PhotoImage(vehicle_image)
            
            vehicle_image_label.config(image=vehicle_photo)
            vehicle_image_label.image = vehicle_photo  # Keep a reference
            
            # Update vehicle name
            vehicle_name = format_filename(vehicle_path.name)
            vehicle_name_label.config(text=vehicle_name)
        except Exception as e:
            vehicle_image_label.config(text=f"Error loading vehicle: {e}")
            vehicle_name_label.config(text="Error")
    
    def load_and_display_cup(cup_path, cup_folder_name):
        """Load and display the cup image and course image."""
        nonlocal cup_image_label, course_image_label, thumbnail_cup, thumbnail_course, scale_factor, cup_box_size, course_box_size, char_box_size
        
        try:
            # Find the cup image file (matching the folder name with any image extension)
            cup_folder_path = Path(__file__).parent / "Cups" / cup_folder_name
            image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
            cup_image_file = None
            
            for ext in image_extensions:
                potential_file = cup_folder_path / f"{cup_folder_name}{ext}"
                if potential_file.exists():
                    cup_image_file = potential_file
                    break
            
            if cup_image_file:
                cup_image = Image.open(cup_image_file)
                cup_image.thumbnail((thumbnail_cup, int(310 * scale_factor)), Image.Resampling.LANCZOS)
                cup_photo = ImageTk.PhotoImage(cup_image)
                
                cup_image_label.config(image=cup_photo)
                cup_image_label.image = cup_photo  # Keep a reference
            else:
                cup_image_label.config(text="Cup image not found")
        except Exception as e:
            cup_image_label.config(text=f"Error loading cup: {e}")
        
        try:
            # Load and display course image
            course_image = Image.open(cup_path)
            # Get the aspect ratio
            width, height = course_image.size
            aspect_ratio = width / height
            
            # Calculate dimensions to fill the scaled course box while preserving aspect ratio
            box_width = course_box_size
            box_height = char_box_size
            box_ratio = box_width / box_height
            
            if aspect_ratio > box_ratio:  # wider than the box ratio
                new_width = box_width
                new_height = int(box_width / aspect_ratio)
            else:  # taller than the box ratio
                new_height = box_height
                new_width = int(box_height * aspect_ratio)
            
            course_image = course_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            course_photo = ImageTk.PhotoImage(course_image)
            
            course_image_label.config(image=course_photo)
            course_image_label.image = course_photo  # Keep a reference
            
            # Update cup and course names
            cup_name = format_filename(cup_folder_name)
            course_name = format_filename(cup_path.name)
            cup_name_label.config(text=f"{cup_name} - {course_name}")
        except Exception as e:
            cup_image_label.config(text=f"Error loading cup: {e}")
            cup_name_label.config(text="Error")
    
    def randomize():
        """Randomize and display new character and vehicle."""
        sizes = ["Large", "Medium", "Small"]
        selected_size = random.choice(sizes)
        
        # Select random character
        characters_folder = Path(__file__).parent / "Characters" / selected_size
        character_image = get_random_image(characters_folder)
        
        # Randomly select between Bikes and Cars
        vehicle_types = ["Bikes", "Cars"]
        selected_vehicle_type = random.choice(vehicle_types)
        
        # Select random vehicle from the selected type
        vehicles_folder = Path(__file__).parent / "Vehicles" / selected_vehicle_type / selected_size
        vehicle_image = get_random_image(vehicles_folder)
        
        if character_image and vehicle_image:
            size_label.config(text=f"Size: {selected_size}")
            load_and_display_images(character_image, vehicle_image)
    
    def randomize_cup():
        """Randomize and display a new cup and course."""
        cups_folder = Path(__file__).parent / "Cups"
        
        # Get all cup folders
        cup_folders = [f for f in cups_folder.iterdir() if f.is_dir()]
        
        if not cup_folders:
            cup_image_label.config(text="No cups found")
            cup_name_label.config(text="Error")
            return
        
        # Select random cup folder
        selected_cup_folder = random.choice(cup_folders)
        
        # Get all course images in the selected cup folder
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
        course_files = [f for f in selected_cup_folder.iterdir() 
                       if f.is_file() and f.suffix.lower() in image_extensions]
        
        # Filter out courses that match the cup folder name (without extension)
        cup_folder_name_no_ext = selected_cup_folder.name.rsplit('.', 1)[0]
        filtered_courses = [f for f in course_files 
                           if f.stem.lower() != cup_folder_name_no_ext.lower()]
        
        # If no courses after filtering, use all courses
        if not filtered_courses:
            filtered_courses = course_files
        
        if not filtered_courses:
            cup_image_label.config(text="No courses found")
            cup_name_label.config(text="Error")
            return
        
        # Select random course
        selected_course = random.choice(filtered_courses)
        print(f"Selected cup: {selected_cup_folder.name}")
        print(f"Selected course: {selected_course.name}")
        
        load_and_display_cup(selected_course, selected_cup_folder.name)
    
    # Size label
    size_label = ttk.Label(frame, text="Size: ", font=("Arial", 12, "bold"))
    size_label.grid(row=0, column=0, columnspan=2, pady=10)
    
    # Cup title
    cup_title = ttk.Label(frame, text="Cup", font=("Arial", 11, "bold"))
    cup_title.grid(row=0, column=2, padx=10, pady=5)
    
    # Character label
    char_title = ttk.Label(frame, text="Character", font=("Arial", 11, "bold"))
    char_title.grid(row=1, column=0, padx=10, pady=5)
    
    # Vehicle label
    vehicle_title = ttk.Label(frame, text="Vehicle", font=("Arial", 11, "bold"))
    vehicle_title.grid(row=1, column=1, padx=10, pady=5)
    
    # Name labels
    char_name_label = ttk.Label(char_name_box, font=("Arial", 10))
    char_name_label.pack(expand=True)
    
    vehicle_name_label = ttk.Label(vehicle_name_box, font=("Arial", 10))
    vehicle_name_label.pack(expand=True)
    
    cup_name_label = ttk.Label(cup_name_box, font=("Arial", 10))
    cup_name_label.pack(expand=True)
    
    # Randomize button for character and vehicle
    randomize_button = ttk.Button(frame, text="Randomize", command=randomize)
    randomize_button.grid(row=4, column=0, columnspan=2, pady=20)
    
    # Randomize button for cup
    randomize_cup_button = ttk.Button(frame, text="Randomize", command=randomize_cup)
    randomize_cup_button.grid(row=4, column=2, columnspan=2, pady=20)
    
    # Close button
    close_button = ttk.Button(frame, text="Close", command=root.destroy)
    close_button.grid(row=5, column=0, columnspan=4, pady=5)
    
    # Load initial images
    randomize()
    randomize_cup()
    
    root.mainloop()

if __name__ == "__main__":
    # Open the window immediately
    display_image(None, None)
