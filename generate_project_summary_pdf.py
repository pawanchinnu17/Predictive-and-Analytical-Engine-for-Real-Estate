from fpdf import FPDF
import os

FONT_PATH = 'DejaVuSans.ttf'
if not os.path.exists(FONT_PATH):
    raise FileNotFoundError('DejaVuSans.ttf not found in the current directory. Please place it here.')

# Read the project summary from the text file
with open('project_summary_for_pdf.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

class PDF(FPDF):
    pass

pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.add_font('DejaVu', '', FONT_PATH, uni=True)
pdf.add_font('DejaVu', 'B', FONT_PATH, uni=True)

pdf.set_font('DejaVu', 'B', 18)
pdf.cell(0, 12, '99 Acres Property Insights & Prediction Project', ln=True, align='C')
pdf.ln(8)

current_section = None
body_lines = []

for line in lines:
    line = line.rstrip('\n')
    if line.strip() == '':
        continue
    # Section headings are numbered and underlined
    if line[0].isdigit() and line[1] == '.':
        if current_section and body_lines:
            pdf.set_font('DejaVu', '', 12)
            pdf.multi_cell(0, 8, '\n'.join(body_lines))
            pdf.ln(2)
            body_lines = []
        current_section = line
        pdf.set_font('DejaVu', 'B', 14)
        pdf.set_text_color(40, 40, 120)
        pdf.cell(0, 10, line, ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(2)
    elif set(line.strip()) == {'-'}:
        continue  # skip underline lines
    else:
        body_lines.append(line)

# Add the last section
if body_lines:
    pdf.set_font('DejaVu', '', 12)
    pdf.multi_cell(0, 8, '\n'.join(body_lines))

pdf.output('99_Acres_Project_Summary.pdf')
print('PDF generated: 99_Acres_Project_Summary.pdf') 