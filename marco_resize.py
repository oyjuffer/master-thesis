from PIL import Image
import os

def resize_images_in_folders(root_folder):
    # Define the output root directory for resized images
    output_root = os.path.join("MARCO_IMAGES_resized")
    os.makedirs(output_root, exist_ok=True)

    # Iterate through the numbered folders
    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        
        # Check if the item in the root folder is a directory
        if os.path.isdir(folder_path):
            output_folder = os.path.join(output_root, folder_name)
            os.makedirs(output_folder, exist_ok=True)

            # Loop through images in subfolders and resize them
            for subdir, _, files in os.walk(folder_path):
                for filename in files:
                    filepath = os.path.join(subdir, filename)
                    
                    # Check if the file is an image
                    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                        with Image.open(filepath) as img:
                            # Resize the image to 608x608
                            img_resized = img.resize((608, 608))
                            
                            # Save the resized image in the corresponding output folder
                            output_filename = os.path.join(output_folder, filename)
                            img_resized.save(output_filename, "JPEG")
                            print(f"Resized and saved: {output_filename}")

# Provide the root folder containing subfolders (0, 1, 2, 3) with images
root_folder_path = "MARCO_IMAGES"
resize_images_in_folders(root_folder_path)
