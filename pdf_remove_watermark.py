#pdf去水印，标注和内嵌文字，指定文字
import fitz
import os

# 路径
SRC = r"xxxxxxxxx"

# 要替换的目标
TARGET = ""


def process(pdf_src, pdf_dst):
    doc = fitz.open(pdf_src)

    for page in doc:
        for rect in page.searchFor(TARGET):
            old_rect = +rect
            fontsize = rect.height / 1.45
            h = (rect.y0 + rect.y1) / 2
            d = rect.height * 0.1
            rect.y0 = h - d
            rect.y1 = h + d
            annot = page.firstAnnot
            while annot:
                annot = page.deleteAnnot(annot)
            # annot = page.addRectAnnot(rect)
            # annot.setInfo(info='100')
            # annot.setBorder(border=100, width=100)
            # annot.setColors(fill=(0, 0, 1))
            # annot.setOpacity(1)
            # annot.update()
            page.addRedactAnnot(rect)
            page.apply_redactions()
            print(page.insertTextbox(old_rect, "", fontsize=fontsize, color=(1, 0, 0)))
    print("PROCESS:", pdf_src)
    doc.save(pdf_dst, garbage=3)
    print("SAVED:", pdf_dst)


for root, dirs, files in os.walk(SRC):
    print("root:", root)
    for file in files:
        if not file.endswith("pdf") and not file.endswith("PDF"):
            continue
        print("file:", file)
        src = os.path.join(root, file)

        part_list = os.path.splitext(src)
        dst = part_list[0] + '_2' + part_list[1]
        process(src, dst)
