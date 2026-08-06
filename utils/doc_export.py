# utils/doc_export.py

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from io import BytesIO
import requests
from PIL import Image
from io import BytesIO as ByteIO
import re
import random

def export_to_docx(title, content, images=None):
    """Export article with images AFTER content, NOT immediately after headings"""
    
    doc = Document()
    
    # Styles
    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(12)
    
    # ----- TITLE -----
    title_para = doc.add_heading(title, 0)
    title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_para.runs[0].font.size = Pt(26)
    title_para.runs[0].font.color.rgb = RGBColor(124, 58, 237)
    title_para.paragraph_format.space_after = Pt(18)
    
    # ----- PROCESS IMAGES -----
    image_list = []
    if images and len(images) > 0:
        for img in images[:6]:
            try:
                if isinstance(img, str) and img.startswith('http'):
                    response = requests.get(img, timeout=10)
                    if response.status_code == 200:
                        img_bytes = ByteIO(response.content)
                        image_list.append(img_bytes)
                elif isinstance(img, bytes):
                    image_list.append(ByteIO(img))
                elif hasattr(img, 'getvalue'):
                    image_list.append(img)
            except:
                pass
    
    image_descriptions = [
        "Image: Topic related",
        "Image: Visual representation",
        "Image: Related content",
        "Image: Illustration",
    ]
    
    # ----- PARSE CONTENT -----
    lines = content.split('\n')
    image_index = 0
    image_count = len(image_list)
    paragraph_count = 0
    content_after_heading = 0  # ✅ Track content after each heading
    
    # ✅ Track if we've added image after H1
    h1_content_count = 0
    h1_image_added = False
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            doc.add_paragraph()
            continue
        
        # ----- H1 HEADING (Main Title) -----
        if line.startswith('# ') and not line.startswith('## ') and not line.startswith('### '):
            doc.add_heading(line.replace('# ', ''), 1)
            h1_content_count = 0  # ✅ Reset counter for H1 content
            h1_image_added = False  # ✅ Reset flag for H1 image
            continue
            
        # ----- H2 HEADING (Main Sections) -----
        elif line.startswith('## '):
            doc.add_heading(line.replace('## ', ''), 2)
            content_after_heading = 0  # ✅ Reset counter
            continue
        
        # ----- H3 HEADING (Sub-sections) -----
        elif line.startswith('### '):
            doc.add_heading(line.replace('### ', ''), 3)
            content_after_heading = 0  # ✅ Reset counter
            continue
        
        # ----- BULLET POINTS -----
        if line.startswith('- ') or line.startswith('* ') or line.startswith('• '):
            para = doc.add_paragraph(line[2:], style='List Bullet')
            para.paragraph_format.space_after = Pt(6)
            paragraph_count += 1
            content_after_heading += 1
            h1_content_count += 1
            continue
        
        # ----- NUMBERED LIST -----
        if re.match(r'^\d+\.\s', line):
            para = doc.add_paragraph(line, style='List Number')
            para.paragraph_format.space_after = Pt(6)
            paragraph_count += 1
            content_after_heading += 1
            h1_content_count += 1
            continue
        
        # ----- NORMAL PARAGRAPH -----
        para = doc.add_paragraph(line)
        para.style = 'Normal'
        para.paragraph_format.space_after = Pt(12)
        para.paragraph_format.line_spacing = 1.5
        para.paragraph_format.first_line_indent = Inches(0.3)
        paragraph_count += 1
        content_after_heading += 1
        h1_content_count += 1
        
        # ============================================================
        # ✅ IMAGE INSERTION LOGIC - AFTER CONTENT
        # ============================================================
        
        # ✅ For H1: Add image after 2-3 paragraphs of content
        if not h1_image_added and h1_content_count >= 2 and image_index < image_count:
            add_image_to_doc(doc, image_list[image_index], f"📷 {random.choice(image_descriptions)}")
            image_index += 1
            h1_image_added = True
        
        # ✅ For other sections: Add image after 3-4 paragraphs of content
        elif content_after_heading >= 3 and image_index < image_count:
            # ✅ Don't add image if we're too close to another image
            if image_index < image_count:
                add_image_to_doc(doc, image_list[image_index], f"📷 {random.choice(image_descriptions)}")
                image_index += 1
                content_after_heading = 0  # ✅ Reset counter after adding image
    
    # ----- ADD REMAINING IMAGES AT THE END -----
    while image_index < image_count:
        add_image_to_doc(doc, image_list[image_index], f"📷 {random.choice(image_descriptions)}")
        image_index += 1
    
    # ----- FOOTER -----
    section = doc.sections[0]
    footer = section.footer
    footer_para = footer.paragraphs[0]
    footer_para.text = f"{title[:50]} | Page "
    footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer_para.style.font.size = Pt(8)
    
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    
    def create_page_number(run):
        fldChar1 = OxmlElement('w:fldChar')
        fldChar1.set(qn('w:fldCharType'), 'begin')
        instrText = OxmlElement('w:instrText')
        instrText.text = "PAGE"
        fldChar2 = OxmlElement('w:fldChar')
        fldChar2.set(qn('w:fldCharType'), 'end')
        run._r.append(fldChar1)
        run._r.append(instrText)
        run._r.append(fldChar2)
    
    footer_para.add_run()
    create_page_number(footer_para.runs[-1])
    
    bio = BytesIO()
    doc.save(bio)
    return bio.getvalue()


def add_image_to_doc(doc, img_stream, caption):
    """Helper function to add image with caption"""
    try:
        img_stream.seek(0)
        
        # ✅ Add a blank paragraph before image for spacing
        doc.add_paragraph()
        
        # ✅ Image centered
        para = doc.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = para.add_run()
        run.add_picture(img_stream, width=Inches(4.5))
        
        # ✅ Caption below image (centered)
        desc = doc.add_paragraph()
        desc.alignment = WD_ALIGN_PARAGRAPH.CENTER
        desc_run = desc.add_run()
        desc_run.text = caption
        desc_run.font.size = Pt(8)
        desc_run.font.color.rgb = RGBColor(128, 128, 128)
        desc_run.italic = True
        
        # ✅ Add blank paragraph after image for spacing
        doc.add_paragraph()
    except Exception as e:
        print(f"⚠️ Image add error: {e}")
        pass