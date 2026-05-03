import streamlit as st
from io import BytesIO
from datetime import datetime
import matplotlib.pyplot as plt
from reportlab.platypus import Image

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


def render_equation(eq, width=4.8, fontsize=12):
    img_buffer = BytesIO()

    plt.rcParams["mathtext.fontset"] = "stix"
    plt.rcParams["font.family"] = "serif"

    fig, ax = plt.subplots(figsize=(width, 0.75))
    ax.text(0.02, 0.5, eq, fontsize=fontsize, va="center")
    ax.axis("off")

    plt.savefig(
        img_buffer,
        format="png",
        dpi=300,
        bbox_inches="tight",
        transparent=True,
        pad_inches=0.03
    )

    plt.close(fig)
    img_buffer.seek(0)
    return img_buffer

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Bridge Calc App",
    layout="wide"
)


# ---------------------------------------------------
# PDF REPORT FUNCTION
# ---------------------------------------------------

def create_pdf_report(
    fc, fy, b, h, cover, bar_size, num_bars, Mu,
    Ab, db, As, d, a, Mn, phi, phi_Mn, DCR, result
):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    story = []

    # Title block
    title_data = [
        ["Project:", "Sample Bridge Design", "Date:", datetime.now().strftime("%b %d, %Y")],
        ["Engineer:", "Rushil Mojidra", "Rev:", "0"],
        ["Calculation:", "Bent Cap Flexural Check", "Page:", "1"],
    ]

    title_table = Table(title_data, colWidths=[75, 245, 55, 110])
    title_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.6, colors.grey),
        ("BACKGROUND", (0, 0), (-1, -1), colors.whitesmoke),
        ("FONTNAME", (0, 0), (-1, -1), "Times-Roman"),
        ("FONTNAME", (0, 0), (0, -1), "Times-Bold"),
        ("FONTNAME", (2, 0), (2, -1), "Times-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
    ]))

    story.append(title_table)
    story.append(Spacer(1, 18))

    story.append(Paragraph("<b>Bent Cap Flexural Capacity Calculation</b>", styles["Title"]))
    story.append(Spacer(1, 16))

    # Input summary
    story.append(Paragraph("<b>Input Summary</b>", styles["Heading2"]))

    input_data = [
        ["Parameter", "Value", "Parameter", "Value"],
        ["f'<sub>c</sub>", f"{fc:.2f} ksi", "b", f"{b:.2f} in"],
        ["f<sub>y</sub>", f"{fy:.2f} ksi", "h", f"{h:.2f} in"],
        ["Cover", f"{cover:.2f} in", "Bar size", bar_size],
        ["A<sub>b</sub>", f"{Ab:.2f} in<sup>2</sup>", "d<sub>b</sub>", f"{db:.3f} in"],
        ["Number of bars", f"{num_bars}", "M<sub>u</sub>", f"{Mu:.2f} kip-ft"],
        ["φ", f"{phi:.2f}", "", ""],
    ]

    input_table = Table(input_data, colWidths=[105, 120, 105, 120])
    input_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e9eef3")),
        ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Times-Roman"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (1, 1), (1, -1), "RIGHT"),
        ("ALIGN", (3, 1), (3, -1), "RIGHT"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
    ]))

    story.append(input_table)
    story.append(Spacer(1, 18))

    # Calculations
    story.append(Paragraph("<b>Calculations</b>", styles["Heading2"]))
    story.append(Spacer(1, 10))
    
    equations = [
    
        rf"$A_s = n A_b$",
    
        rf"$A_s = {num_bars}({Ab:.2f}) = {As:.2f}\ \mathrm{{in}}^2$",
    
    
        rf"$d = h - cover - \frac{{d_b}}{{2}}$",
    
        rf"$d = {h:.2f} - {cover:.2f} - \frac{{{db:.3f}}}{{2}} = {d:.2f}\ \mathrm{{in}}$",
    
    
        rf"$a = \frac{{A_s f_y}}{{0.85 f'_c b}}$",
    
        rf"$a = \frac{{({As:.2f})({fy:.2f})}}{{0.85({fc:.2f})({b:.2f})}} = {a:.2f}\ \mathrm{{in}}$",
    
    
        rf"$M_n = \frac{{A_s f_y (d-a/2)}}{{12}}$",
    
        rf"$M_n = \frac{{({As:.2f})({fy:.2f})({d:.2f}-{a:.2f}/2)}}{{12}} = {Mn:.2f}\ \mathrm{{kip-ft}}$",
    
    
        rf"$\phi M_n = {phi:.2f}({Mn:.2f}) = {phi_Mn:.2f}\ \mathrm{{kip-ft}}$",
    
    
        rf"$DCR = \frac{{M_u}}{{\phi M_n}}$",
    
        rf"$DCR = \frac{{{Mu:.2f}}}{{{phi_Mn:.2f}}} = {DCR:.3f}$",
    ]
    
    for eq in equations:
    
        eq_img = render_equation(eq)
    
        img = Image(eq_img)
    
        # Keep original aspect ratio.
        img.drawWidth = 360
        img.drawHeight = 360 * img.imageHeight / img.imageWidth
    
        story.append(img)
        story.append(Spacer(1, 12))

    story.append(Spacer(1, 8))
    # Results
    story.append(Paragraph("<b>Results</b>", styles["Heading2"]))

    result_color = colors.green if result == "OK" else colors.red

    result_data = [
        ["φM<sub>n</sub>", f"{phi_Mn:.2f} kip-ft"],
        ["M<sub>u</sub>", f"{Mu:.2f} kip-ft"],
        ["DCR", f"{DCR:.3f}"],
        ["Final Result", result],
    ]

    result_table = Table(result_data, colWidths=[160, 160])
    result_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (-1, -1), colors.whitesmoke),
        ("FONTNAME", (0, 0), (0, -1), "Times-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Times-Roman"),
        ("TEXTCOLOR", (1, 3), (1, 3), result_color),
        ("FONTNAME", (1, 3), (1, 3), "Times-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
    ]))

    story.append(result_table)

    doc.build(story)

    buffer.seek(0)
    return buffer


# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("Bridge Calculation App")
st.markdown("### Bent Cap Flexural Capacity Check")
st.markdown("---")


# ---------------------------------------------------
# BAR DATA
# ---------------------------------------------------

bar_area = {
    "#6": 0.44,
    "#7": 0.60,
    "#8": 0.79,
    "#9": 1.00,
    "#10": 1.27,
    "#11": 1.56,
}

bar_diameter = {
    "#6": 0.750,
    "#7": 0.875,
    "#8": 1.000,
    "#9": 1.128,
    "#10": 1.270,
    "#11": 1.410,
}


# ---------------------------------------------------
# LAYOUT
# ---------------------------------------------------

left, right = st.columns([1, 1.3])


# ---------------------------------------------------
# INPUT SIDE
# ---------------------------------------------------

with left:
    st.header("Input Data")

    with st.expander("Material", expanded=True):
        fc = st.number_input("Concrete strength, f'c (ksi)", value=4.0, min_value=0.1)
        fy = st.number_input("Steel yield strength, fy (ksi)", value=68.0, min_value=1.0)

    with st.expander("Geometry", expanded=True):
        b = st.number_input("Width, b (in)", value=60.0, min_value=1.0)
        h = st.number_input("Height, h (in)", value=60.0, min_value=1.0)
        cover = st.number_input("Cover (in)", value=2.0, min_value=0.0)

    with st.expander("Reinforcement", expanded=True):
        bar_size = st.selectbox("Bar Size", ["#6", "#7", "#8", "#9", "#10", "#11"], index=5)
        num_bars = st.number_input("Number of Bars", value=19, min_value=1, step=1)

    with st.expander("Loads and Factors", expanded=True):
        Mu = st.number_input("Factored Moment, Mu (kip-ft)", value=8250.0, min_value=0.0)
        phi = st.number_input("Strength reduction factor, φ", value=1.0, min_value=0.1, max_value=1.0)

    calculate = st.button("Generate Report", type="primary")


# ---------------------------------------------------
# REPORT SIDE
# ---------------------------------------------------

with right:
    st.header("Calculation Report")

    if calculate:
        Ab = bar_area[bar_size]
        db = bar_diameter[bar_size]

        As = num_bars * Ab
        d = h - cover - db / 2
        a = (As * fy) / (0.85 * fc * b)
        Mn = As * fy * (d - a / 2) / 12
        phi_Mn = phi * Mn
        DCR = Mu / phi_Mn

        result = "OK" if DCR <= 1.0 else "NG"

        st.subheader("Input Summary")

        st.markdown(f"""
| Parameter | Value |
|---|---:|
| $f'_c$ | {fc:.2f} ksi |
| $f_y$ | {fy:.2f} ksi |
| $b$ | {b:.2f} in |
| $h$ | {h:.2f} in |
| Cover | {cover:.2f} in |
| Bar Size | {bar_size} |
| Bar Area, $A_b$ | {Ab:.2f} in² |
| Bar Diameter, $d_b$ | {db:.3f} in |
| Number of Bars | {num_bars} |
| $M_u$ | {Mu:.2f} kip-ft |
| $\\phi$ | {phi:.2f} |
""")

        st.subheader("Calculations")

        st.latex(r"A_s = n A_b")
        st.latex(rf"A_s = {num_bars} \times {Ab:.2f} = {As:.2f}\ \mathrm{{in}}^2")

        st.latex(r"d = h - cover - \frac{d_b}{2}")
        st.latex(rf"d = {h:.2f} - {cover:.2f} - \frac{{{db:.3f}}}{{2}} = {d:.2f}\ \mathrm{{in}}")

        st.latex(r"a = \frac{A_s f_y}{0.85 f'_c b}")
        st.latex(
            rf"a = \frac{{({As:.2f})({fy:.2f})}}{{0.85({fc:.2f})({b:.2f})}} = {a:.2f}\ \mathrm{{in}}"
        )

        st.latex(r"M_n = \frac{A_s f_y (d - a/2)}{12}")
        st.latex(
            rf"M_n = \frac{{({As:.2f})({fy:.2f})({d:.2f} - {a:.2f}/2)}}{{12}} = {Mn:.2f}\ \mathrm{{kip-ft}}"
        )

        st.latex(r"\phi M_n = \phi \times M_n")
        st.latex(rf"\phi M_n = {phi:.2f}({Mn:.2f}) = {phi_Mn:.2f}\ \mathrm{{kip-ft}}")

        st.latex(r"DCR = \frac{M_u}{\phi M_n}")
        st.latex(rf"DCR = \frac{{{Mu:.2f}}}{{{phi_Mn:.2f}}} = {DCR:.3f}")

        st.subheader("Results")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("φMn", f"{phi_Mn:.2f} kip-ft")

        with col2:
            st.metric("DCR", f"{DCR:.3f}")

        if result == "OK":
            st.success(f"Final Result: {result}")
        else:
            st.error(f"Final Result: {result}")

        pdf_buffer = create_pdf_report(
            fc, fy, b, h, cover, bar_size, num_bars, Mu,
            Ab, db, As, d, a, Mn, phi, phi_Mn, DCR, result
        )

        st.download_button(
            label="Download PDF Report",
            data=pdf_buffer,
            file_name="bent_cap_flexural_report.pdf",
            mime="application/pdf"
        )

    else:
        st.info("Press 'Generate Report' to run calculations.")
