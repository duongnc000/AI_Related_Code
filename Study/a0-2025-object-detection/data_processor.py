import os
from PIL import Image

def convert_box(img_width, img_height, x_min, y_min, x_max, y_max):
    # Calculate normalized values
    x_center = (x_min + x_max) / 2.0 / img_width
    y_center = (y_min + y_max) / 2.0 / img_height
    width = (x_max - x_min) / img_width
    height = (y_max - y_min) / img_height
    return x_center, y_center, width, height

def convert_labels(label_folder, image_folder):
    for label_file in os.listdir(label_folder):
        if not label_file.endswith('.txt'):
            continue
        image_file = label_file.replace('.txt', '.jpg')  # or .png if that's your format
        image_path = os.path.join(image_folder, image_file)
        label_path = os.path.join(label_folder, label_file)

        if not os.path.exists(image_path):
            print(f"Image not found for {label_file}")
            continue

        img = Image.open(image_path)
        w, h = img.size

        with open(label_path, 'r') as f:
            lines = f.readlines()

        new_lines = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) != 5:
                print(f"Skipping malformed line in {label_file}: {line}")
                continue
            class_id, x_min, y_min, x_max, y_max = map(float, parts)
            x_center, y_center, width, height = convert_box(w, h, x_min, y_min, x_max, y_max)
            new_lines.append(f"{int(class_id)} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

        with open(label_path, 'w') as f:
            f.write('\n'.join(new_lines))

    print("Label conversion complete!")

# Example usage
convert_labels('datasets/Train/labels', 'datasets/Train/images')
