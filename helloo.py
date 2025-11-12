import os
import random
from PIL import Image, ImageDraw, ImageFont

SHAPES = ["rectangle", "ellipse", "triangle", "line"]

def draw_one_shape(draw, width, height):
    """
    Draw exactly one random shape with random color and position.
    """
    shape_type = random.choice(SHAPES)

    pad_w = int(width * 0.1)
    pad_h = int(height * 0.1)

    x1 = random.randint(pad_w, int(width * 0.3))
    y1 = random.randint(pad_h, int(height * 0.3))
    x2 = random.randint(int(width * 0.7), width - pad_w)
    y2 = random.randint(int(height * 0.7), height - pad_h)

    fill_color = tuple(random.randint(60, 220) for _ in range(3)) + (180,)  # semi-transparent fill
    outline_color = tuple(random.randint(0, 120) for _ in range(3)) + (255,)
    outline_width = max(2, int(min(width, height) * 0.02))

    if shape_type == "rectangle":
        draw.rectangle([x1, y1, x2, y2], fill=fill_color, outline=outline_color, width=outline_width)

    elif shape_type == "ellipse":
        draw.ellipse([x1, y1, x2, y2], fill=fill_color, outline=outline_color, width=outline_width)

    elif shape_type == "triangle":
        points = [
            (random.randint(x1, x2), y1),
            (x1, y2),
            (x2, y2)
        ]
        draw.polygon(points, fill=fill_color, outline=outline_color)

    elif shape_type == "line":
        draw.line([(x1, y1), (x2, y2)], fill=outline_color, width=outline_width * 2)


def generate_transparent_images(output_dir="input_images", count=50, min_w=200, max_w=800, min_h=200, max_h=1000):
    """
    Generate PNGs with one random shape, text label, and transparent background.
    """
    os.makedirs(output_dir, exist_ok=True)

    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except Exception:
        font = ImageFont.load_default()

    for i in range(1, count + 1):
        width = random.randint(min_w, max_w)
        height = random.randint(min_h, max_h)

        # Transparent background (RGBA)
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img, "RGBA")

        # Draw single shape
        draw_one_shape(draw, width, height)

        # Add text in center or bottom
        text = f"IMG-{i:02d} | {width}x{height}"
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
        except AttributeError:
            text_w, text_h = draw.textsize(text, font=font)

        text_x = (width - text_w) // 2
        text_y = height - text_h - 10

        # Semi-transparent white box for text background
        # box_padding = 8
        # draw.rectangle(
        #     [text_x - box_padding, text_y - box_padding,
        #      text_x + text_w + box_padding, text_y + text_h + box_padding],
        #     fill=(255, 255, 255, 160),
        #     outline=(0, 0, 0, 80)
        # )

        # Text on top
        # draw.text((text_x, text_y), text, fill=(0, 0, 0, 255), font=font)

        fname = os.path.join(output_dir, f"img_{i:02d}.png")
        img.save(fname, "PNG")

    print(f"✅ Generated {count} transparent images with one shape each in '{output_dir}'.")


if __name__ == "__main__":
    generate_transparent_images(count=50)