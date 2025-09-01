
import cv2
import pytesseract
import numpy as np

"""
ocr for spreadsheet
"""

def ocr_spreadsheet(path):

    # Step 1: Load the spreadsheet as an image
    image = cv2.imread(path)  
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Step 2: Apply adaptive thresholding to get binary image
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 5
    )

    # Step 3: Dilate to connect text into blocks
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    dilated = cv2.dilate(thresh, kernel, iterations=1)

    # Step 4: Find contours (potential blocks)
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    blocks = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        
        # Optional: filter out very small blocks
        if w < 50 or h < 20:
            continue
        
        block = image[y:y+h, x:x+w]
        blocks.append(block)
        
        # Draw rectangle for visualization
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Step 5: OCR on each block
    for i, block in enumerate(blocks):
        text = pytesseract.image_to_string(block, config="--psm 6")
        print(f"Block {i+1} text:")
        print(text)
        print("-" * 40)

    # Step 6: Show image with detected blocks
    cv2.imshow("Detected Blocks", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()