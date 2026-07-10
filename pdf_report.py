from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER

from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from datetime import datetime

# ------------------------------------------
# Register Font (optional)
# ------------------------------------------

try:
    pdfmetrics.registerFont(
        TTFont(
            "Arial",
            "arial.ttf"
        )
    )

    FONT = "Arial"

except:

    FONT = "Helvetica"


# ------------------------------------------
# Header and Footer
# ------------------------------------------

def add_page(canvas, doc):

    canvas.saveState()

    width, height = A4

    # Header Line

    canvas.setStrokeColor(colors.HexColor("#0A4C86"))
    canvas.setLineWidth(2)

    canvas.line(
        40,
        height-45,
        width-40,
        height-45
    )

    canvas.setFillColor(colors.HexColor("#0A4C86"))

    canvas.setFont(
        FONT,
        10
    )

    canvas.drawString(
        45,
        height-35,
        "Medical Device Risk Assessment Tool"
    )

    # Footer Line

    canvas.setStrokeColor(colors.grey)

    canvas.line(
        40,
        35,
        width-40,
        35
    )

    canvas.setFont(
        FONT,
        9
    )

    canvas.drawRightString(
        width-45,
        20,
        f"Page {doc.page}"
    )

    canvas.restoreState()


# ------------------------------------------
# Main PDF Function
# ------------------------------------------

def generate_pdf(

    hazards,

    fmea_records

):

    pdf = SimpleDocTemplate(

        "Risk_Assessment_Report.pdf",

        pagesize=A4,

        leftMargin=0.75*inch,

        rightMargin=0.75*inch,

        topMargin=0.9*inch,

        bottomMargin=0.8*inch

    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    heading = styles["Heading1"]
    subheading = styles["Heading2"]
    normal = styles["BodyText"]

    title_style.alignment = TA_CENTER

    content = []

    # ==========================================
    # COVER PAGE
    # ==========================================

    content.append(
        Spacer(1,40)
    )

    content.append(
        Paragraph(
            "<font color='#0A4C86'><b>MEDICAL DEVICE RISK ASSESSMENT REPORT</b></font>",
            title_style
        )
    )

    content.append(
        Spacer(1,15)
    )

    content.append(
        Paragraph(
            "<b>ISO 14971 Inspired Risk Management System</b>",
            subheading
        )
    )

    content.append(
        Spacer(1,40)
    )

    info = f"""

<b>Prepared By :</b> G. Subiksha

<br/><br/>

<b>Department :</b> Biomedical Engineering

<br/><br/>

<b>Date :</b> {datetime.now().strftime('%d-%m-%Y')}

<br/><br/>

<b>Generated Time :</b>

{datetime.now().strftime('%I:%M %p')}

"""

    content.append(

        Paragraph(

            info,

            normal

        )

    )

    content.append(
        Spacer(1,80)
    )

    content.append(
        Paragraph(
            "<font color='#0A4C86'><b>Executive Summary</b></font>",
            heading
        )
    )

    total_hazards = len(hazards)
    total_fmea = len(fmea_records)

    critical = 0
    high = 0
    medium = 0
    low = 0

    for hazard in hazards:

        if hazard[5] == "Critical":
            critical += 1

        elif hazard[5] == "High":
            high += 1

        elif hazard[5] == "Medium":
            medium += 1

        else:
            low += 1

    summary = [

        ["Metric","Value"],

        ["Total Hazards",total_hazards],

        ["Total FMEA Records",total_fmea],

        ["Critical Risks",critical],

        ["High Risks",high],

        ["Medium Risks",medium],

        ["Low Risks",low]

    ]

    table = Table(

        summary,

        colWidths=[3.3*inch,2.2*inch]

    )

    table.setStyle(

        TableStyle([

            ('BACKGROUND',(0,0),(-1,0),colors.HexColor("#0A4C86")),

            ('TEXTCOLOR',(0,0),(-1,0),colors.white),

            ('GRID',(0,0),(-1,-1),1,colors.black),

            ('FONTNAME',(0,0),(-1,0),"Helvetica-Bold"),

            ('BACKGROUND',(0,1),(-1,-1),colors.beige),

            ('ALIGN',(0,0),(-1,-1),"CENTER"),

            ('BOTTOMPADDING',(0,0),(-1,0),8)

        ])

    )

    content.append(table)

    content.append(PageBreak())
        # ==========================================
    # HAZARD ANALYSIS
    # ==========================================

    content.append(
        Paragraph(
            "<font color='#0A4C86'><b>Hazard Analysis</b></font>",
            heading
        )
    )

    content.append(
        Spacer(1,15)
    )

    hazard_data = [[
        "Hazard",
        "Severity",
        "Probability",
        "Risk Score",
        "Risk Level"
    ]]

    for hazard in hazards:

        hazard_data.append([

            str(hazard[1]),

            str(hazard[2]),

            str(hazard[3]),

            str(hazard[4]),

            str(hazard[5])

        ])

    hazard_table = Table(

        hazard_data,

        colWidths=[
            2.3*inch,
            0.8*inch,
            0.9*inch,
            1.0*inch,
            1.2*inch
        ]

    )

    hazard_table.hAlign = "CENTER"

    hazard_table.setStyle(

        TableStyle([

            ('BACKGROUND',(0,0),(-1,0),colors.HexColor("#0A4C86")),

            ('TEXTCOLOR',(0,0),(-1,0),colors.white),

            ('FONTNAME',(0,0),(-1,0),"Helvetica-Bold"),

            ('GRID',(0,0),(-1,-1),1,colors.black),

            ('ALIGN',(0,0),(-1,-1),"CENTER"),

            ('VALIGN',(0,0),(-1,-1),"MIDDLE"),

            ('BACKGROUND',(0,1),(-1,-1),colors.whitesmoke),

            ('BOTTOMPADDING',(0,0),(-1,0),10),

            ('TOPPADDING',(0,1),(-1,-1),8),

            ('BOTTOMPADDING',(0,1),(-1,-1),8)

        ])

    )

    content.append(hazard_table)

    content.append(
        Spacer(1,25)
    )

    # ==========================================
    # RISK LEVEL LEGEND
    # ==========================================

    content.append(
        Paragraph(
            "<font color='#0A4C86'><b>Risk Level Legend</b></font>",
            subheading
        )
    )

    legend = [

        ["Risk Level","Meaning"],

        ["Low","Acceptable Risk"],

        ["Medium","Monitor & Review"],

        ["High","Mitigation Required"],

        ["Critical","Immediate Action Required"]

    ]

    legend_table = Table(

        legend,

        colWidths=[
            2.4*inch,
            3.2*inch
        ]

    )

    legend_table.setStyle(

        TableStyle([

            ('BACKGROUND',(0,0),(-1,0),colors.darkblue),

            ('TEXTCOLOR',(0,0),(-1,0),colors.white),

            ('GRID',(0,0),(-1,-1),1,colors.black),

            ('BACKGROUND',(0,1),(-1,-1),colors.beige),

            ('FONTNAME',(0,0),(-1,0),"Helvetica-Bold"),

            ('ALIGN',(0,0),(-1,-1),"CENTER"),

            ('BOTTOMPADDING',(0,0),(-1,0),10)

        ])

    )

    content.append(legend_table)

    content.append(
        Spacer(1,30)
    )

    # ==========================================
    # FMEA ANALYSIS
    # ==========================================

    content.append(
        Paragraph(
            "<font color='#0A4C86'><b>Failure Mode and Effects Analysis (FMEA)</b></font>",
            heading
        )
    )

    content.append(
        Spacer(1,15)
    )

    fmea_data = [[

        "Failure Mode",

        "Effect",

        "Cause",

        "S",

        "O",

        "D",

        "RPN"

    ]]

    for record in fmea_records:

        fmea_data.append([

            str(record[1]),

            str(record[2]),

            str(record[3]),

            str(record[4]),

            str(record[5]),

            str(record[6]),

            str(record[7])

        ])

    fmea_table = Table(

        fmea_data,

        colWidths=[

            1.6*inch,

            1.4*inch,

            1.4*inch,

            0.45*inch,

            0.45*inch,

            0.45*inch,

            0.65*inch

        ]

    )

    fmea_table.hAlign = "CENTER"

    fmea_table.setStyle(

        TableStyle([

            ('BACKGROUND',(0,0),(-1,0),colors.HexColor("#0A4C86")),

            ('TEXTCOLOR',(0,0),(-1,0),colors.white),

            ('GRID',(0,0),(-1,-1),1,colors.black),

            ('FONTNAME',(0,0),(-1,0),"Helvetica-Bold"),

            ('ALIGN',(0,0),(-1,-1),"CENTER"),

            ('VALIGN',(0,0),(-1,-1),"MIDDLE"),

            ('BACKGROUND',(0,1),(-1,-1),colors.whitesmoke),

            ('BOTTOMPADDING',(0,0),(-1,0),10),

            ('TOPPADDING',(0,1),(-1,-1),8),

            ('BOTTOMPADDING',(0,1),(-1,-1),8)

        ])

    )

    content.append(fmea_table)

    content.append(
        PageBreak()
    )
        # ==========================================
    # REGULATORY COMPLIANCE
    # ==========================================

    content.append(
        Paragraph(
            "<font color='#0A4C86'><b>Regulatory Compliance</b></font>",
            heading
        )
    )

    content.append(
        Spacer(1,15)
    )

    compliance = """

<b>ISO 14971</b><br/><br/>

The Medical Device Risk Assessment Tool follows the
general principles of ISO 14971 for medical device risk
management. Hazard identification, risk estimation,
evaluation and mitigation activities are documented
systematically.

<br/><br/>

<b>IEC 60601</b><br/><br/>

Electrical safety aspects of medical devices should be
evaluated according to IEC 60601 standards wherever
applicable.

<br/><br/>

<b>FDA Quality System Regulation (21 CFR Part 820)</b><br/><br/>

The generated documentation supports quality management,
risk documentation and traceability during the product
development lifecycle.

"""

    content.append(
        Paragraph(
            compliance,
            normal
        )
    )

    content.append(
        Spacer(1,25)
    )

    # ==========================================
    # RECOMMENDATIONS
    # ==========================================

    content.append(
        Paragraph(
            "<font color='#0A4C86'><b>Recommendations</b></font>",
            heading
        )
    )

    recommendations = """

• Review all Critical Risks immediately.

<br/><br/>

• Implement mitigation strategies before deployment.

<br/><br/>

• Update FMEA whenever new hazards are identified.

<br/><br/>

• Review residual risk after mitigation.

<br/><br/>

• Maintain audit trail records for traceability.

<br/><br/>

• Periodically review the risk management file.

"""

    content.append(
        Paragraph(
            recommendations,
            normal
        )
    )

    content.append(
        Spacer(1,25)
    )

    # ==========================================
    # CONCLUSION
    # ==========================================

    content.append(
        Paragraph(
            "<font color='#0A4C86'><b>Conclusion</b></font>",
            heading
        )
    )

    conclusion = """

The Medical Device Risk Assessment Tool provides a
structured workflow for hazard identification,
risk evaluation and Failure Mode and Effects Analysis.

The application demonstrates ISO 14971 inspired
risk management practices and supports engineers in
maintaining comprehensive documentation for medical
device quality assurance.

"""

    content.append(
        Paragraph(
            conclusion,
            normal
        )
    )

    content.append(
        Spacer(1,35)
    )

    # ==========================================
    # APPROVAL
    # ==========================================

    content.append(
        Paragraph(
            "<font color='#0A4C86'><b>Approval</b></font>",
            heading
        )
    )

    approval = [

        ["Prepared By","G. Subiksha"],

        ["Reviewed By","________________________"],

        ["Approved By","________________________"],

        ["Date",datetime.now().strftime("%d-%m-%Y")]

    ]

    approval_table = Table(

        approval,

        colWidths=[
            2.5*inch,
            3.2*inch
        ]

    )

    approval_table.setStyle(

        TableStyle([

            ('GRID',(0,0),(-1,-1),1,colors.black),

            ('BACKGROUND',(0,0),(0,-1),colors.HexColor("#D9EAF7")),

            ('FONTNAME',(0,0),(0,-1),"Helvetica-Bold"),

            ('BOTTOMPADDING',(0,0),(-1,-1),10),

            ('TOPPADDING',(0,0),(-1,-1),10),

            ('LEFTPADDING',(0,0),(-1,-1),8),

            ('RIGHTPADDING',(0,0),(-1,-1),8)

        ])

    )

    content.append(approval_table)

    content.append(
        Spacer(1,30)
    )

    # ==========================================
    # CONFIDENTIALITY NOTICE
    # ==========================================

    content.append(
        Paragraph(
            "<b>Confidentiality Notice</b>",
            subheading
        )
    )

    content.append(
        Paragraph(
            "This report is generated for educational purposes. "
            "The methodology is inspired by ISO 14971 and intended "
            "to demonstrate medical device risk management concepts.",
            normal
        )
    )

    content.append(
        Spacer(1,30)
    )

    content.append(
        Paragraph(
            "<b><font color='#0A4C86'>***** END OF REPORT *****</font></b>",
            title_style
        )
    )

    # ==========================================
    # BUILD PDF
    # ==========================================

    pdf.build(
        content,
        onFirstPage=add_page,
        onLaterPages=add_page
    )