# 2_document_processing.py
# Extract text from client documents using OCR

import os
import pytesseract
import pandas as pd

# Make sure you have Tesseract installed separately on your machine!
# Download link (Windows): https://github.com/tesseract-ocr/tesseract
# You may need to specify path if not auto-configured:
# pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'

# Define paths
input_folder = 'data/client_documents/'
output_csv = 'data/structured_data/ocr_extracted_data.csv'

# Read all text documents
extracted_data = []

for file_name in os.listdir(input_folder):
    if file_name.endswith('.txt'):  # for this dummy example, use .txt
        with open(os.path.join(input_folder, file_name), 'r') as file:
            text = file.read()

            client_name = None
            dob = None
            address = None
            income = None
            employment_status = None
            id_number = None

            for line in text.split('\n'):
                if 'Client Name:' in line:
                    client_name = line.split(':', 1)[-1].strip()
                elif 'Date of Birth:' in line:
                    dob = line.split(':', 1)[-1].strip()
                elif 'Address:' in line:
                    address = line.split(':', 1)[-1].strip()
                elif 'Income:' in line:
                    income = line.split('$')[-1].strip()
                elif 'Employment Status:' in line:
                    employment_status = line.split(':', 1)[-1].strip()
                elif 'ID Number:' in line:
                    id_number = line.split(':', 1)[-1].strip()

            extracted_data.append({
                'client_name': client_name,
                'dob': dob,
                'address': address,
                'income': income,
                'employment_status': employment_status,
                'id_number': id_number
            })

# Save extracted data
df = pd.DataFrame(extracted_data)
df.to_csv(output_csv, index=False)

print(f"OCR text extraction complete. Output saved to {output_csv}")
