import random
from pathlib import Path
import subprocess
import sys
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
    root.geometry("1100x750")
    
    # Create a frame for the images
    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    # Labels to store image references
    char_image_label = ttk.Label(frame)
    vehicle_image_label = ttk.Label(frame)
    cup_image_label = ttk.Label(frame)
    char_name_label = ttk.Label(frame, font=("Arial", 10))
    vehicle_name_label = ttk.Label(frame, font=("Arial", 10))
    cup_name_label = ttk.Label(frame, font=("Arial", 10))
    
    # Create bounding boxes (frames with fixed size) for each image
    char_box = tk.Frame(frame, width=320, height=320, bg="lightgray")
    char_box.grid(row=2, column=0, padx=10, pady=10)
    char_box.grid_propagate(False)  # Prevent frame from resizing
    
    vehicle_box = tk.Frame(frame, width=320, height=320, bg="lightgray")
    vehicle_box.grid(row=2, column=1, padx=10, pady=10)
    vehicle_box.grid_propagate(False)
    
    cup_box = tk.Frame(frame, width=320, height=320, bg="lightgray")
    cup_box.grid(row=2, column=2, padx=10, pady=10)
    cup_box.grid_propagate(False)
    
    # Place image labels inside the bounding boxes (centered)
    char_image_label = ttk.Label(char_box)
    char_image_label.pack(expand=True)
    
    vehicle_image_label = ttk.Label(vehicle_box)
    vehicle_image_label.pack(expand=True)
    
    cup_image_label = ttk.Label(cup_box)
    cup_image_label.pack(expand=True)
    
    def load_and_display_images(char_path, vehicle_path):
        """Load and display the character and vehicle images."""
        nonlocal char_image_label, vehicle_image_label
        
        # Load and display character image
        try:
            char_image = Image.open(char_path)
            char_image.thumbnail((300, 300), Image.Resampling.LANCZOS)
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
            vehicle_image.thumbnail((300, 300), Image.Resampling.LANCZOS)
            vehicle_photo = ImageTk.PhotoImage(vehicle_image)
            
            vehicle_image_label.config(image=vehicle_photo)
            vehicle_image_label.image = vehicle_photo  # Keep a reference
            
            # Update vehicle name
            vehicle_name = format_filename(vehicle_path.name)
            vehicle_name_label.config(text=vehicle_name)
        except Exception as e:
            vehicle_image_label.config(text=f"Error loading vehicle: {e}")
            vehicle_name_label.config(text="Error")
    
    def load_and_display_cup(cup_path):
        """Load and display the cup image."""
        nonlocal cup_image_label
        
        try:
            cup_image = Image.open(cup_path)
            cup_image.thumbnail((300, 300), Image.Resampling.LANCZOS)
            cup_photo = ImageTk.PhotoImage(cup_image)
            
            cup_image_label.config(image=cup_photo)
            cup_image_label.image = cup_photo  # Keep a reference
            
            # Update cup name
            cup_name = format_filename(cup_path.name)
            cup_name_label.config(text=cup_name)
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
        """Randomize and display a new cup."""
        cups_folder = Path(__file__).parent / "Cups"
        cup_image = get_random_image(cups_folder)
        
        if cup_image:
            load_and_display_cup(cup_image)
    
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
    char_name_label.grid(row=3, column=0, padx=10, pady=5)
    vehicle_name_label.grid(row=3, column=1, padx=10, pady=5)
    cup_name_label.grid(row=3, column=2, padx=10, pady=5)
    
    # Randomize button for character and vehicle
    randomize_button = ttk.Button(frame, text="Randomize", command=randomize)
    randomize_button.grid(row=4, column=0, columnspan=2, pady=20)
    
    # Randomize button for cup
    randomize_cup_button = ttk.Button(frame, text="Randomize", command=randomize_cup)
    randomize_cup_button.grid(row=4, column=2, pady=20)
    
    # Close button
    close_button = ttk.Button(frame, text="Close", command=root.destroy)
    close_button.grid(row=5, column=0, columnspan=3, pady=5)
    
    # Load initial images
    randomize()
    randomize_cup()
    
    root.mainloop()

if __name__ == "__main__":
    # Open the window immediately
    display_image(None, None)


workingPath = r"C:\Users\Austin\OneDrive - Elizabethtown College\ComputerScience\Random\MarioKartRandomizer"
