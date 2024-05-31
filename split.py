#This is the python script i created for splitting and creation of the IPC and Bhartiya Nyaya Sanhita sections dataset
#The logic is simple: Every new section in both pdfs starts with a bold heading and an integer section number.
#So splitting condition= Split whenever you encounter a bold integer
#Further minimal cleaning, editing and indexing was done manually
import fitz  # install PyMuPDF if not exists
import csv

def is_bold(span):
    # Check if the font is bold by inspecting the font name or weight
    font_name = span["font"]
    font_flags = span["flags"]
    if "Bold" in font_name or font_flags & 262144 != 0:
        return True
    return False

def starts_with_integer(text):
    # Check if the text starts with an integer
    return text and text[0].isdigit()

def split_text(pdf_path):
    pdf_document = fitz.open(pdf_path)
    sections = []
    current_section = ""

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"]
                    if is_bold(span) and starts_with_integer(text):
                        # When bold text starting with an integer is found, start a new section
                        if current_section:
                            sections.append(current_section.strip())
                        current_section = text  # Start new section with the bold text
                    else:
                        current_section += text  # Continue current section

    if current_section:
        sections.append(current_section.strip())

    pdf_document.close()
    return sections

def save_sections_to_csv(sections, csv_path):
    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Serial Number', 'Section'])  # Write header
        for i, section in enumerate(sections, start=1):
            writer.writerow([i, section])

pdf_path = "Sections_PDF_path" #change to your pdf path
csv_path = "output_dataset.csv" #the csv file path that will be created
split_sections = split_text(pdf_path)
save_sections_to_csv(split_sections, csv_path)

print(f"Sections have been saved to {csv_path}")
