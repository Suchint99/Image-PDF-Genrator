# Image Packing PDF Generator

A Python application that efficiently packs images of random sizes into PDF pages while minimizing wasted space.

## Features

- 🖼️ Processes PNG, JPEG, and other image formats
- 📄 Efficient rectangle packing algorithm (MaxRects)
- 🎯 Maintains image aspect ratios
- 📦 Compresses images for smaller PDF size
- 🔄 Handles transparent backgrounds
- 📊 Generates multi-page PDFs automatically

## Installation

1. Clone the repository:
bash
git clone https://github.com/your-username/image-packing-pdf.git

cd image-packing-pdf
How to Run the Project
Step 1: Prerequisites
Python 3.8 or higher

pip (Python package manager)

Step 2: Setup Project
Create project folder:

bash
mkdir image-packing-pdf
cd image-packing-pdf
Create virtual environment:

bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
Install dependencies:

bash
pip install pillow reportlab
Step 3: Create Project Files
Create these files in your project folder:

1. requirements.txt

txt
Pillow>=10.0.0
reportlab>=4.0.0
2. sample_data_generation.py (use the code from your original file)

3. task_1_solution.py (use the fixed code I provided earlier)

4. README.md (create with content below)

Step 4: Generate Sample Data
bash
python sample_data_generation.py
This creates an input_images/ folder with 50 sample PNG images.

Step 5: Generate PDF
bash
python task_1_solution.py
This processes all images and creates output.pdf with efficiently packed images.

 Complete File Structure
text
image-packing-pdf/
│
├── task_1_solution.py          # Main solution with packing algorithm
├── sample_data_generation.py   # Creates test images
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Files to ignore in Git
│
├── input_images/               # Generated sample images
│   ├── img_01.png
│   ├── img_02.png
│   └── ...
│
└── output.pdf                  # Generated PDF (after running)
 Complete Code Files
1. README.md
markdown
# Image Packing PDF Generator

A Python application that efficiently packs images of random sizes into PDF pages while minimizing wasted space.

## Features

- Processes PNG, JPEG, and other image formats
- Efficient rectangle packing algorithm (MaxRects)
- Maintains image aspect ratios
- Compresses images for smaller PDF size
- Handles transparent backgrounds
- Generates multi-page PDFs automatically

## Installation

1. Clone the repository:
bash
git clone https://github.com/your-username/image-packing-pdf.git
cd image-packing-pdf
Create a virtual environment:

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:

bash
pip install -r requirements.txt
Usage
Generate sample images (optional):

bash
python sample_data_generation.py
Run the PDF generator:

bash
python task_1_solution.py
Output
Input: Images from input_images/ folder

Output: output.pdf with all images efficiently packed

Algorithm
Uses the MaxRects algorithm for efficient rectangle packing:

Sorts images by area (largest first)

Places images in optimal positions

Minimizes empty space

Handles oversized images by scaling

Dependencies
Pillow - Image processing

ReportLab - PDF generation

Python 3.8+

License
MIT License

text

### 2. **.gitignore**
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
temp/
tmp/
*.tmp
*.temp
