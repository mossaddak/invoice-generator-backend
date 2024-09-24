import os

from django.urls import reverse

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph

from invoice_generator.settings import BASE_DIR


def create_invoice(
    request,
    company_name,
    issue_date,
    due_date,
    total,
    paid_amount,
    invoice_items,
    filename="invoice.pdf",
):
    media_invoices_dir = os.path.join(BASE_DIR, "media", "invoices")

    os.makedirs(media_invoices_dir, exist_ok=True)
    file_path = os.path.join(media_invoices_dir, filename)
    pdf = SimpleDocTemplate(file_path, pagesize=A4)

    # Container for the PDF elements
    elements = []

    # Add company details
    styles = getSampleStyleSheet()
    company_info = Paragraph(
        f"<b>Company Name: {company_name}</b><br/>Issue Date: {issue_date}<br/>Due Date: {due_date}",
        styles["Normal"],
    )
    elements.append(company_info)

    # Add a space
    elements.append(Paragraph("<br/>", styles["Normal"]))

    # Product Table data
    table_data = [
        ["Product Name", "Quantity", "Total Price"],
    ]

    for data in invoice_items:
        table_data.append([data["title"], data["quantity"], data["total"]])

    # Create Table and Style
    table = Table(table_data)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 12),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )
    elements.append(table)

    # Add total and paid amount details
    total_amount = Paragraph(
        f"<br/><b>Total Amount:</b>{total:.2f} tk", styles["Normal"]
    )
    paid_amount_paragraph = Paragraph(
        f"<b>Paid Amount:</b> {paid_amount:.2f} tk", styles["Normal"]
    )
    remaining_amount = total - paid_amount
    remaining_amount_paragraph = Paragraph(
        f"<b>Amount Due:</b>{remaining_amount:.2f} tk", styles["Normal"]
    )

    elements.append(total_amount)
    elements.append(paid_amount_paragraph)
    elements.append(remaining_amount_paragraph)

    # Build the PDF
    pdf.build(elements)
    # return f"http://{request.get_host()}/media/invoices/{filename}"
    return f"http://{request.get_host()}/invoice-generator-backend/media/invoices/{filename}"