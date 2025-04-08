import os
import random
import shutil

# Paths
base_dir = 'datasets'  # adjust if needed
train_image_dir = os.path.join(base_dir, 'Train/images')
train_label_dir = os.path.join(base_dir, 'Train/labels')

val_image_dir = os.path.join(base_dir, 'Val/images')
val_label_dir = os.path.join(base_dir, 'Val/labels')

# Create Val/ folders
os.makedirs(val_image_dir, exist_ok=True)
os.makedirs(val_label_dir, exist_ok=True)

# Get list of image files
image_files = [f for f in os.listdir(train_image_dir) if f.endswith(('.jpg', '.png'))]
random.shuffle(image_files)

# Split 80/20
val_ratio = 0.2
val_count = int(len(image_files) * val_ratio)
val_images = image_files[:val_count]

for image_file in val_images:
    name, ext = os.path.splitext(image_file)
    label_file = name + '.txt'

    # Paths
    src_img = os.path.join(train_image_dir, image_file)
    src_lbl = os.path.join(train_label_dir, label_file)

    dst_img = os.path.join(val_image_dir, image_file)
    dst_lbl = os.path.join(val_label_dir, label_file)

    # Move files to Val/
    shutil.move(src_img, dst_img)
    if os.path.exists(src_lbl):
        shutil.move(src_lbl, dst_lbl)

print(f"Moved {len(val_images)} images and labels to Val/")