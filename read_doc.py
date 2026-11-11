import zipfile
import xml.etree.ElementTree as ET

docx_path = r'extracted_doc/Pixieland_Project_Documentation.docx'
z = zipfile.ZipFile(docx_path)
tree = ET.fromstring(z.read('word/document.xml'))

ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
paragraphs = []
for p in tree.iter(f"{{{ns['w']}}}p"):
    texts = [node.text for node in p.iter(f"{{{ns['w']}}}t") if node.text]
    if texts:
        paragraphs.append("".join(texts))

with open(r'extracted_doc/pixieland_content.txt', 'w', encoding='utf-8') as f:
    f.write("\n\n".join(paragraphs))

print(f"Extracted {len(paragraphs)} paragraphs successfully.")

