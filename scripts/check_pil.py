import sys
try:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
    print("PIL is available")
except ImportError:
    print("PIL not available")
