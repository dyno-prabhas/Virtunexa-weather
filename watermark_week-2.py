from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os

def add_watermark(input_path, output_path, watermark_text, position='bottom-right', opacity=128, font_size=30):
    """Adds a watermark to an image."""
    try:
        # Open the original image
        image = Image.open(input_path).convert("RGBA")
        
        # Create a watermark layer
        watermark = Image.new("RGBA", image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark)
        
        # Load a font
        font = ImageFont.load_default()
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            print("Arial font not found, using default font.")
        
        text_size = draw.textbbox((0, 0), watermark_text, font=font)
        text_width, text_height = text_size[2] - text_size[0], text_size[3] - text_size[1]
        
        # Determine position
        positions = {
            "top-left": (10, 10),
            "top-right": (image.width - text_width - 10, 10),
            "center": ((image.width - text_width) // 2, (image.height - text_height) // 2),
            "bottom-left": (10, image.height - text_height - 10),
            "bottom-right": (image.width - text_width - 10, image.height - text_height - 10)
        }
        pos = positions.get(position, positions['bottom-right'])
        
        # Apply text with transparency
        draw.text(pos, watermark_text, fill=(255, 255, 255, opacity), font=font)
        
        # Merge layers
        watermarked = Image.alpha_composite(image, watermark)
        
        # Convert back to RGB and save
        watermarked = watermarked.convert("RGB")
        watermarked.save(output_path)
        print(f"Watermark added to {input_path}, saved as {output_path}")
    except Exception as e:
        print(f"Error processing {input_path}: {e}")


def batch_process(input_folder, output_folder, watermark_text, position='bottom-right', opacity=128, font_size=30):
    """Processes all images in a folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('png', 'jpg', 'jpeg')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            add_watermark(input_path, output_path, watermark_text, position, opacity, font_size)
    print("Batch processing complete.")


if __name__ == "__main__":
    input_path = input("Enter the image file path: ").strip('"')  
    output_folder = input("Enter the output folder path: ").strip('"')
    watermark_text = input("Enter the watermark text: ")
    position = input("Enter position (top-left, top-right, center, bottom-left, bottom-right): ") or "bottom-right"
    opacity = int(input("Enter opacity (0-255): ") or 128)
    font_size = int(input("Enter font size: ") or 30)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_path = os.path.join(output_folder, os.path.basename(input_path))
    add_watermark(input_path, output_path, watermark_text, position, opacity, font_size)
