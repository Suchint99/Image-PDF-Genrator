import os
import math
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import tempfile

INPUT_DIR = "input_images"
OUTPUT_PDF = "output.pdf"
PAGE_SIZE = A4  # width, height in points (1 pt = 1/72 inch)

def preprocess_image(image_path: str):
    """This function should do all preprocessing of the images 

    Args:
        image_path (str): The Input path of the image

    Returns:
        _type_: The preprocessed image
    """
    image = Image.open(image_path).convert("RGBA")
    
    # If image has transparency, crop to visible area
    if image.mode == 'RGBA':
        # Get the bounding box of non-transparent area
        bbox = image.getbbox()
        if bbox:
            image = image.crop(bbox)
    
    return image

class BinPacker:
    """A more efficient bin packing algorithm using the maxrects approach"""
    
    def __init__(self, width, height, margin=10):
        self.width = int(width)
        self.height = int(height)
        self.margin = margin
        self.free_rectangles = [(margin, margin, self.width - 2*margin, self.height - 2*margin)]
        self.used_rectangles = []
    
    def find_best_position(self, rect_width, rect_height):
        """Find the best position for a rectangle using the best area fit"""
        best_score = float('inf')
        best_rect = None
        
        rect_width_with_margin = rect_width + self.margin
        rect_height_with_margin = rect_height + self.margin
        
        for i, (x, y, w, h) in enumerate(self.free_rectangles):
            if w >= rect_width_with_margin and h >= rect_height_with_margin:
                # Score based on remaining area (minimize waste)
                score = (w - rect_width_with_margin) * (h - rect_height_with_margin)
                if score < best_score:
                    best_score = score
                    best_rect = (x, y, w, h, i)
        
        return best_rect
    
    def place_rectangle(self, rect_width, rect_height):
        """Place a rectangle in the bin and update free spaces"""
        best = self.find_best_position(rect_width, rect_height)
        if not best:
            return None
        
        x, y, w, h, idx = best
        rect_width_with_margin = rect_width + self.margin
        rect_height_with_margin = rect_height + self.margin
        
        # Remove the used free rectangle
        del self.free_rectangles[idx]
        
        # Add the placed rectangle
        self.used_rectangles.append((x, y, rect_width, rect_height))
        
        # Split the remaining free space
        remaining_width = w - rect_width_with_margin
        remaining_height = h - rect_height_with_margin
        
        if remaining_width > 0 and rect_height_with_margin > 0:
            self.free_rectangles.append((x + rect_width_with_margin, y, remaining_width, rect_height_with_margin))
        
        if remaining_height > 0 and w > 0:
            self.free_rectangles.append((x, y + rect_height_with_margin, w, remaining_height))
        
        # Merge free rectangles
        self.merge_free_rectangles()
        
        return (x, y)
    
    def merge_free_rectangles(self):
        """Merge adjacent free rectangles to reduce fragmentation"""
        i = 0
        while i < len(self.free_rectangles):
            j = i + 1
            while j < len(self.free_rectangles):
                rect1 = self.free_rectangles[i]
                rect2 = self.free_rectangles[j]
                
                # Check if rectangles can be merged
                if (rect1[0] == rect2[0] and rect1[2] == rect2[2] and 
                    rect1[1] + rect1[3] == rect2[1]):
                    # Merge vertically adjacent
                    self.free_rectangles[i] = (rect1[0], rect1[1], rect1[2], rect1[3] + rect2[3])
                    del self.free_rectangles[j]
                elif (rect1[1] == rect2[1] and rect1[3] == rect2[3] and 
                      rect1[0] + rect1[2] == rect2[0]):
                    # Merge horizontally adjacent
                    self.free_rectangles[i] = (rect1[0], rect1[1], rect1[2] + rect2[2], rect1[3])
                    del self.free_rectangles[j]
                else:
                    j += 1
            i += 1

def pack_images_maxrects(images_data, page_width, page_height, margin=20):
    """Pack images using the maxrects algorithm"""
    # Convert to integers for the packing algorithm
    page_width = int(page_width)
    page_height = int(page_height)
    
    # Sort by area (largest first)
    sorted_images = sorted(images_data, key=lambda x: x['width_int'] * x['height_int'], reverse=True)
    
    packs = []
    current_bin = BinPacker(page_width, page_height, margin)
    current_page_placements = []
    
    for img_data in sorted_images:
        placed = current_bin.place_rectangle(img_data['width_int'], img_data['height_int'])
        
        if placed:
            x, y = placed
            current_page_placements.append((img_data, x, y))
        else:
            # Start new page
            if current_page_placements:
                packs.append(current_page_placements)
            current_bin = BinPacker(page_width, page_height, margin)
            current_page_placements = []
            
            # Try to place in new page
            placed = current_bin.place_rectangle(img_data['width_int'], img_data['height_int'])
            if placed:
                x, y = placed
                current_page_placements.append((img_data, x, y))
            else:
                # Image is too large for a single page, scale it down
                scale_factor = min(
                    (page_width - 2*margin) / img_data['width_int'],
                    (page_height - 2*margin) / img_data['height_int']
                )
                scaled_width = int(img_data['width_int'] * scale_factor)
                scaled_height = int(img_data['height_int'] * scale_factor)
                
                placed = current_bin.place_rectangle(scaled_width, scaled_height)
                if placed:
                    x, y = placed
                    # Update the image data with scaled dimensions
                    img_data_scaled = img_data.copy()
                    img_data_scaled['width_int'] = scaled_width
                    img_data_scaled['height_int'] = scaled_height
                    img_data_scaled['width'] = img_data['width'] * scale_factor
                    img_data_scaled['height'] = img_data['height'] * scale_factor
                    current_page_placements.append((img_data_scaled, x, y))
    
    if current_page_placements:
        packs.append(current_page_placements)
    
    return packs

def generate_pdf(input_dir: str, output_pdf_path: str, page_size):
    """This is the main function to generate the PDF"""

    if not os.path.exists(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist")
        return
    
    # Get all image files
    image_files = []
    for file in os.listdir(input_dir):
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            image_files.append(os.path.join(input_dir, file))
    
    if not image_files:
        print("No images found in input directory")
        return
    
    print(f"Found {len(image_files)} images")
    
    # Preprocess all images and collect data
    images_data = []
    temp_files = []
    
    for i, image_path in enumerate(image_files):
        try:
            # Preprocess image
            processed_img = preprocess_image(image_path)
            
            # Compress image
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
            temp_files.append(temp_file.name)
            compressed_path = compress_images(processed_img, temp_file.name)
            
            # Convert dimensions to points and integers for packing
            width_pt = processed_img.width
            height_pt = processed_img.height
            
            images_data.append({
                'path': compressed_path,
                'width': width_pt,  # Original float dimensions for PDF
                'height': height_pt,
                'width_int': int(width_pt),  # Integer dimensions for packing
                'height_int': int(height_pt),
                'original_path': image_path
            })
            
        except Exception as e:
            print(f"Error processing {image_path}: {str(e)}")
    
    # Get page dimensions
    page_width, page_height = page_size
    
    # Use maxrects packing algorithm
    packed_pages = pack_images_maxrects(images_data, page_width, page_height)
    
    # Generate PDF
    c = canvas.Canvas(output_pdf_path, pagesize=page_size)
    
    for page_num, page_placements in enumerate(packed_pages):
        print(f"Generating page {page_num + 1} with {len(page_placements)} images")
        
        for img_data, x, y in page_placements:
            try:
                # Draw image on PDF - convert coordinates for PDF system
                pdf_y = page_height - y - img_data['height']
                c.drawImage(
                    img_data['path'],
                    x, pdf_y,
                    width=img_data['width'],
                    height=img_data['height']
                )
            except Exception as e:
                print(f"Error drawing image {img_data['original_path']}: {str(e)}")
        
        # Add page number
        c.setFont("Helvetica", 10)
        c.drawString(30, 30, f"Page {page_num + 1}")
        
        if page_num < len(packed_pages) - 1:
            c.showPage()
    
    c.save()
    
    # Clean up temporary files
    for temp_file in temp_files:
        try:
            os.unlink(temp_file)
        except:
            pass
    
    print(f"PDF generated successfully: {output_pdf_path}")
    print(f"Total pages: {len(packed_pages)}")

def compress_images(image, output_image_path: str, compression_level: int = 5):
    """This function should compress the images to make the PDF size as minimum """

    # Convert to RGB if necessary (JPEG doesn't support transparency)
    if image.mode in ('RGBA', 'LA', 'P'):
        # Create white background
        background = Image.new('RGB', image.size, (255, 255, 255))
        if image.mode == 'P':
            image = image.convert('RGBA')
        background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
        image = background
    
    # Calculate quality based on compression level
    quality = 100 - (compression_level * 10)
    if quality < 10:
        quality = 10
    
    # Save with compression
    image.save(output_image_path, 'JPEG', quality=quality, optimize=True)
    
    return output_image_path

if __name__ == "__main__":
    generate_pdf(INPUT_DIR, OUTPUT_PDF, PAGE_SIZE)