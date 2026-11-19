from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, black

root = Path.cwd()
target = root / 'output/pdf/Classroom_Discussion_Slips_S1-S25.pdf'
c = canvas.Canvas(str(target), pagesize=A4)
c.setTitle('Classroom discussion network: student slips S1-S25')
c.setAuthor('Petro Tolochko')
c.setSubject('Twenty-five discussion-partner collection slips, five per A4 page')
page_w, page_h = A4
left, right = 14 * mm, page_w - 14 * mm
row_h = 53 * mm
first_top = page_h - 12 * mm
ink = HexColor('#202020')
grey = HexColor('#777777')

for page in range(5):
    for row in range(5):
        number = page * 5 + row + 1
        top = first_top - row * row_h
        # ID occupies its own line and remains readable when the slip is held up.
        c.setFillColor(ink)
        c.setFont('Helvetica-Bold', 27)
        c.drawString(left + 3 * mm, top - 11 * mm, f'S{number}')
        c.setFont('Helvetica', 11)
        c.drawString(left + 3 * mm, top - 18 * mm,
                     'Who have you discussed a course exercise with during this class?')
        c.drawString(left + 3 * mm, top - 23 * mm,
                     'List their IDs (S1-S25), not names. Leave out your own ID.')
        c.setFont('Helvetica', 10)
        c.drawString(left + 3 * mm, top - 29 * mm,
                     'Discussion partners (list each person once):')
        c.setStrokeColor(grey)
        c.setLineWidth(0.45)
        for offset in (36, 43):
            c.line(left + 3 * mm, top - offset * mm,
                   right - 3 * mm, top - offset * mm)
        c.setStrokeColor(black)
        c.setFillColor(ink)
        c.setLineWidth(0.65)
        c.setFont('Helvetica', 9.5)
        base = top - 49.5 * mm
        for x, label in [(left + 3 * mm, 'No discussions')]:
            c.rect(x, base - 0.2 * mm, 3 * mm, 3 * mm, stroke=1, fill=0)
            c.drawString(x + 5 * mm, base + 0.25 * mm, label)
        # Dashed line between slips.
        if row < 4:
            c.saveState()
            c.setStrokeColor(HexColor('#999999'))
            c.setLineWidth(0.5)
            c.setDash(3, 3)
            y = top - row_h
            c.line(left, y, right, y)
            c.restoreState()
    c.setFillColor(grey)
    c.setFont('Helvetica', 8)
    c.drawRightString(right, 9 * mm, f'{page + 1} / 5')
    c.showPage()
    # Empty reverse side for duplex printers, including the final sheet.
    c.showPage()
c.save()
print(target)
