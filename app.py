


import streamlit as st
import os
from dotenv import load_dotenv

from pdf_extractor import extract_text_from_pdf
from report_analyzer import analyze_report
from ai_explainer import generate_explanation

import io
import re
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet

load_dotenv()


def generate_pdf(results, explanation):
    from datetime import datetime
    from xml.sax.saxutils import escape
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_CENTER

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=45,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Custom PDF styles
    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontSize=22,
        textColor=colors.HexColor("#17324D"),
        alignment=TA_CENTER,
        spaceAfter=12
    )

    heading_style = ParagraphStyle(
        "ReportHeading",
        parent=styles["Heading2"],
        fontSize=14,
        textColor=colors.HexColor("#24527A"),
        spaceBefore=12,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["BodyText"],
        fontSize=9,
        leading=14,
        spaceAfter=6
    )

    elements = []

    # Professional title
    elements.append(
        Paragraph("MEDICAL REPORT EXPLAINER", title_style)
    )

    elements.append(
        Paragraph(
            "Blood Test Analysis Report",
            heading_style
        )
    )

    elements.append(
        Paragraph(
            f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            body_style
        )
    )

    elements.append(Spacer(1, 15))

    # Sample report notice
    elements.append(
        Paragraph(
            "<b>Report Analysis</b><br/>"
            "This application provides automated explanations "
            "of laboratory results for informational purposes.",
            body_style
        )
    )

    elements.append(Spacer(1, 15))

    # Blood Test Results
    elements.append(
        Paragraph("1. Blood Test Results", heading_style)
    )

    data = [[
        "Test", "Value", "Unit", "Reference Range", "Status"
    ]]

    status_colors = {
        "Normal": colors.HexColor("#21865B"),
        "High": colors.HexColor("#C0392B"),
        "Low": colors.HexColor("#D68910")
    }

    for _, row in results.iterrows():

        status = str(row["Status"])
        status_color = status_colors.get(status, colors.black)

        data.append([
            Paragraph(escape(str(row["Test"])), body_style),
            str(row["Value"]),
            str(row["Unit"]),
            str(row["Reference Range"]),
            Paragraph(
                f'<font color="{status_color.hexval()}">'
                f'<b>{escape(status)}</b></font>',
                body_style
            )
        ])

    table = Table(
        data,
        colWidths=[145, 55, 55, 120, 75],
        repeatRows=1
    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0),
         colors.HexColor("#17324D")),

        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("GRID", (0, 0), (-1, -1), 0.5,
         colors.HexColor("#D7DEE5")),

        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#F2F6FA")]),

        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        ("ALIGN", (1, 1), (-1, -1), "CENTER"),

        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    # Analysis Summary
    elements.append(
        Paragraph("2. Analysis Summary", heading_style)
    )

    normal = int((results["Status"] == "Normal").sum())
    high = int((results["Status"] == "High").sum())
    low = int((results["Status"] == "Low").sum())

    summary_data = [
        ["NORMAL", "HIGH", "LOW"],
        [str(normal), str(high), str(low)]
    ]

    summary_table = Table(
        summary_data,
        colWidths=[150, 150, 150]
    )

    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1),
         colors.HexColor("#E8F5EE")),

        ("BACKGROUND", (1, 0), (1, -1),
         colors.HexColor("#FCEDEA")),

        ("BACKGROUND", (2, 0), (2, -1),
         colors.HexColor("#FFF6DB")),

        ("GRID", (0, 0), (-1, -1), 0.5,
         colors.HexColor("#D7DEE5")),

        ("ALIGN", (0, 0), (-1, -1), "CENTER"),

        ("FONTSIZE", (0, 0), (-1, -1), 12),

        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),

        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))

    elements.append(summary_table)
    elements.append(Spacer(1, 20))

    # AI Explanation
    elements.append(
        Paragraph(
            "3. AI Medical Report Explanation",
            heading_style
        )
    )

    for line in explanation.splitlines():

        line = line.strip()

        if not line or line == "---":
            elements.append(Spacer(1, 5))
            continue

        # Remove Markdown heading symbols
        line = re.sub(r"^#{1,6}\s*", "", line)

        # Escape HTML special characters
        line = escape(line)

        # Convert Markdown bold and italic
        line = re.sub(
            r"\*\*(.+?)\*\*",
            r"<b>\1</b>",
            line
        )

        line = re.sub(
            r"\*(.+?)\*",
            r"<i>\1</i>",
            line
        )

        # Format bullet points
        if line.startswith("- ") or line.startswith("* "):
            line = "&#8226;  " + line[2:]

        elements.append(
            Paragraph(line, body_style)
        )

    elements.append(Spacer(1, 15))

    # Disclaimer
    disclaimer = Table(
        [[Paragraph(
            "<b>IMPORTANT DISCLAIMER</b><br/>"
            "This report is for educational and informational "
            "purposes only. It is not a substitute for professional "
            "medical advice, diagnosis or treatment. "
            "Consult a qualified healthcare professional.",
            body_style
        )]],
        colWidths=[450]
    )

    disclaimer.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1),
         colors.HexColor("#FFF6DB")),

        ("BOX", (0, 0), (-1, -1), 0.7,
         colors.HexColor("#E8D28A")),

        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))

    elements.append(disclaimer)

    # Footer and page number
    def add_footer(canvas, doc):

        canvas.saveState()

        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.grey)

        canvas.drawString(
            40, 25,
            "Medical Report Explainer"
        )

        canvas.drawRightString(
            A4[0] - 40,
            25,
            f"Page {doc.page}"
        )

        canvas.restoreState()

    doc.build(
        elements,
        onFirstPage=add_footer,
        onLaterPages=add_footer
    )

    buffer.seek(0)

    return buffer

    from datetime import datetime
    from xml.sax.saxutils import escape

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()
    elements = []

    # PDF Title
    elements.append(
        Paragraph("MEDICAL REPORT EXPLAINER", styles["Title"])
    )

    elements.append(
        Paragraph(
            "Blood Test Analysis Report",
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph(
            f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 20))

    # Blood Test Results
    elements.append(
        Paragraph("1. Blood Test Results", styles["Heading2"])
    )

    data = [[
        "Test", "Value", "Unit", "Reference Range", "Status"
    ]]

    status_colors = {
        "Normal": colors.green,
        "High": colors.red,
        "Low": colors.orange
    }

    for _, row in results.iterrows():
        status = str(row["Status"])
        status_color = status_colors.get(status, colors.black)

        data.append([
            Paragraph(escape(str(row["Test"])), styles["BodyText"]),
            str(row["Value"]),
            str(row["Unit"]),
            str(row["Reference Range"]),
            Paragraph(
                f'<font color="{status_color.hexval()}">'
                f'<b>{escape(status)}</b></font>',
                styles["BodyText"]
            )
        ])

    table = Table(
        data,
        colWidths=[150, 55, 55, 120, 75],
        repeatRows=1
    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#243B64")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#F0F4F8")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (1, 1), (1, -1), "CENTER"),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    # Analysis Summary
    elements.append(
        Paragraph("2. Analysis Summary", styles["Heading2"])
    )

    normal = int((results["Status"] == "Normal").sum())
    high = int((results["Status"] == "High").sum())
    low = int((results["Status"] == "Low").sum())

    summary_data = [
        ["Normal", "High", "Low"],
        [str(normal), str(high), str(low)]
    ]

    summary_table = Table(
        summary_data,
        colWidths=[150, 150, 150]
    )

    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0),
         colors.HexColor("#DCE6F1")),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("PADDING", (0, 0), (-1, -1), 9),
    ]))

    elements.append(summary_table)
    elements.append(Spacer(1, 20))

    # AI Explanation
    elements.append(
        Paragraph("3. AI Medical Report Explanation",
                  styles["Heading2"])
    )

    for line in explanation.splitlines():
        line = line.strip()

        if not line:
            elements.append(Spacer(1, 6))
            continue

        safe_line = escape(line)
        safe_line = re.sub(
            r"\*\*(.*?)\*\*",
            r"<b>\1</b>",
            safe_line
        )

        elements.append(
            Paragraph(safe_line, styles["BodyText"])
        )
        elements.append(Spacer(1, 5))

    # Medical Disclaimer
    elements.append(Spacer(1, 15))

    elements.append(
        Paragraph(
            "<b>Disclaimer:</b> This report is for educational "
            "and informational purposes only. It is not a "
            "substitute for professional medical advice. "
            "Consult a qualified healthcare professional.",
            styles["BodyText"]
        )
    )

    # Footer and Page Number
    def add_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(colors.grey)

        canvas.drawString(40, 25, "Medical Report Explainer")

        canvas.drawRightString(
            A4[0] - 40,
            25,
            f"Page {doc.page}"
        )

        canvas.restoreState()

    doc.build(
        elements,
        onFirstPage=add_footer,
        onLaterPages=add_footer
    )

    buffer.seek(0)
    return buffer


st.set_page_config(
    page_title="Medical Report Explainer",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 Medical Report Explainer")
st.subheader("Understand your blood test reports easily")

st.info(
    "Upload your blood test report PDF to understand "
    "your laboratory results."
)

uploaded_file = st.file_uploader(
    "Upload Blood Test Report",
    type=["pdf"]
)

if uploaded_file is not None:

    st.success("PDF uploaded successfully!")

    with st.spinner("Extracting PDF text..."):
        extracted_text = extract_text_from_pdf(uploaded_file)

    if extracted_text:

        st.subheader("Extracted Report Text")

        with st.expander("View extracted text"):
            st.text(extracted_text)

        results = analyze_report(extracted_text)

        if not results.empty:

            st.subheader("Blood Test Analysis")

            st.dataframe(
                results,
                use_container_width=True,
                hide_index=True
            )

            st.subheader("Analysis Summary")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Normal",
                int((results["Status"] == "Normal").sum())
            )

            col2.metric(
                "High",
                int((results["Status"] == "High").sum())
            )

            col3.metric(
                "Low",
                int((results["Status"] == "Low").sum())
            )

            st.divider()

            st.subheader("🤖 AI Medical Report Explanation")

            if st.button(
                "✨ Explain My Medical Report with AI",
                type="primary"
            ):

                api_key = os.getenv("GEMINI_API_KEY")

                if not api_key:
                    st.error(
                        "Gemini API key not found. "
                        "Please check your .env file."
                    )

                else:
                    with st.spinner(
                        "Gemini AI is analyzing your report..."
                    ):

                        explanation = generate_explanation(
                            results,
                            api_key
                        )

                    if explanation.startswith("AI Explanation Error:"):
                        st.error(explanation)
                    else:
                        st.markdown(explanation)

                        pdf_file = generate_pdf(results, explanation)

                        st.download_button(
                        label="📄 Download Medical Report PDF",
                        data=pdf_file,
                        file_name="Medical_Report_Analysis.pdf",
                        mime="application/pdf"
                    )

        else:
            st.warning(
                "No supported test values found."
            )

    else:
        st.error("Could not extract text from PDF.")

st.warning(
    "Disclaimer: This application provides informational "
    "explanations only, not medical advice. Consult a "
    "qualified healthcare professional."
)
