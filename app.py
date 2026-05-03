import streamlit as st
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(
    page_title="Bridge Calc App",
    layout="wide"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("Bridge Calculation App")

st.markdown("---")

# ---------------------------------------------------
# LAYOUT
# ---------------------------------------------------

left, right = st.columns([1, 1])

# ---------------------------------------------------
# INPUT SIDE
# ---------------------------------------------------

with left:

    st.header("Input Data")

    st.subheader("Material")

    fc = st.number_input(
        "Concrete strength, f'c (ksi)",
        value=4.0
    )

    fy = st.number_input(
        "Steel yield strength, fy (ksi)",
        value=68.0
    )

    st.subheader("Geometry")

    b = st.number_input(
        "Width, b (in)",
        value=60.0
    )

    h = st.number_input(
        "Height, h (in)",
        value=60.0
    )

    cover = st.number_input(
        "Cover (in)",
        value=2.0
    )

    st.subheader("Reinforcement")

    bar_size = st.selectbox(
        "Bar Size",
        ["#6", "#7", "#8", "#9", "#10", "#11"]
    )

    bar_area = {
        "#6": 0.44,
        "#7": 0.60,
        "#8": 0.79,
        "#9": 1.00,
        "#10": 1.27,
        "#11": 1.56
    }

    bar_diameter = {
        "#6": 0.75,
        "#7": 0.875,
        "#8": 1.00,
        "#9": 1.128,
        "#10": 1.27,
        "#11": 1.41
    }

    num_bars = st.number_input(
        "Number of Bars",
        value=19,
        step=1
    )

    st.subheader("Loads")

    Mu = st.number_input(
        "Factored Moment, Mu (kip-ft)",
        value=8250.0
    )

    calculate = st.button("Generate Report")

# ---------------------------------------------------
# REPORT SIDE
# ---------------------------------------------------

with right:

    st.header("Calculation Report")

    if calculate:

        As = num_bars * bar_area[bar_size]

        db = bar_diameter[bar_size]

        d = h - cover - db / 2

        a = (As * fy) / (0.85 * fc * b)

        Mn = As * fy * (d - a / 2) / 12

        phi = 1.0

        phi_Mn = phi * Mn

        DCR = Mu / phi_Mn

        result = "OK" if DCR <= 1.0 else "NG"

        st.subheader("Input Summary")

        st.markdown(f"""
| Parameter | Value |
|---|---|
| $f'_c$ | {fc:.2f} ksi |
| $f_y$ | {fy:.2f} ksi |
| $b$ | {b:.2f} in |
| $h$ | {h:.2f} in |
| Cover | {cover:.2f} in |
| Bar Size | {bar_size} |
| Number of Bars | {num_bars} |
| $M_u$ | {Mu:.2f} kip-ft |
""")

        st.subheader("Calculations")

        st.latex(r"A_s = nA_b")

        st.latex(
            rf"A_s = {num_bars} \times {bar_area[bar_size]:.2f}"
        )

        st.latex(
            rf"A_s = {As:.2f}\ \mathrm{{in}}^2"
        )

        st.latex(r"d = h - cover - \frac{d_b}{2}")

        st.latex(
            rf"d = {h:.2f} - {cover:.2f} - \frac{{{db:.2f}}}{{2}}"
        )

        st.latex(
            rf"d = {d:.2f}\ \mathrm{{in}}"
        )

        st.latex(
            r"a = \frac{A_s f_y}{0.85 f'_c b}"
        )

        st.latex(
            rf"a = \frac{{({As:.2f})({fy:.2f})}}{{0.85({fc:.2f})({b:.2f})}}"
        )

        st.latex(
            rf"a = {a:.2f}\ \mathrm{{in}}"
        )

        st.latex(
            r"M_n = \frac{A_s f_y (d-a/2)}{12}"
        )

        st.latex(
            rf"M_n = \frac{{({As:.2f})({fy:.2f})({d:.2f}-{a:.2f}/2)}}{{12}}"
        )

        st.latex(
            rf"M_n = {Mn:.2f}\ \mathrm{{kip-ft}}"
        )

        st.subheader("Results")

        st.metric(
            "φMn (kip-ft)",
            f"{phi_Mn:.2f}"
        )

        st.metric(
            "Demand-Capacity Ratio",
            f"{DCR:.3f}"
        )

        if result == "OK":
            st.success(f"Final Result: {result}")
        else:
        st.error(f"Final Result: {result}")
        pdf_buffer = create_pdf_report(
        fc, fy, b, h, cover, bar_size, num_bars, Mu,
        As, d, a, Mn, phi_Mn, DCR, result
        )

        st.download_button(
            label="Download PDF Report",
            data=pdf_buffer,
            file_name="bent_cap_flexural_report.pdf",
            mime="application/pdf"
        )
    else:

def create_pdf_report(fc, fy, b, h, cover, bar_size, num_bars, Mu, As, d, a, Mn, phi_Mn, DCR, result):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>Bridge Calculation Report</b>", styles["Title"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Project:</b> Sample Bridge", styles["Normal"]))
    story.append(Paragraph("<b>Engineer:</b> Rushil Mojidra", styles["Normal"]))
    story.append(Paragraph("<b>Calculation:</b> Bent Cap Flexural Check", styles["Normal"]))
    story.append(Spacer(1, 16))

    story.append(Paragraph("<b>Input Summary</b>", styles["Heading2"]))
    story.append(Paragraph(f"f'<sub>c</sub> = {fc:.2f} ksi", styles["Normal"]))
    story.append(Paragraph(f"f<sub>y</sub> = {fy:.2f} ksi", styles["Normal"]))
    story.append(Paragraph(f"b = {b:.2f} in", styles["Normal"]))
    story.append(Paragraph(f"h = {h:.2f} in", styles["Normal"]))
    story.append(Paragraph(f"Cover = {cover:.2f} in", styles["Normal"]))
    story.append(Paragraph(f"Bar size = {bar_size}", styles["Normal"]))
    story.append(Paragraph(f"Number of bars = {num_bars}", styles["Normal"]))
    story.append(Paragraph(f"M<sub>u</sub> = {Mu:.2f} kip-ft", styles["Normal"]))
    story.append(Spacer(1, 16))

    story.append(Paragraph("<b>Calculations</b>", styles["Heading2"]))

    story.append(Paragraph(f"A<sub>s</sub> = n A<sub>b</sub> = {num_bars}(1.56) = {As:.2f} in<sup>2</sup>", styles["Normal"]))
    story.append(Spacer(1, 8))

    story.append(Paragraph(f"d = h - cover - d<sub>b</sub>/2 = {d:.2f} in", styles["Normal"]))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        f"a = A<sub>s</sub> f<sub>y</sub> / (0.85 f'<sub>c</sub> b) = {a:.2f} in",
        styles["Normal"]
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        f"M<sub>n</sub> = A<sub>s</sub> f<sub>y</sub>(d - a/2) / 12 = {Mn:.2f} kip-ft",
        styles["Normal"]
    ))
    story.append(Spacer(1, 16))

    story.append(Paragraph("<b>Results</b>", styles["Heading2"]))
    story.append(Paragraph(f"φM<sub>n</sub> = {phi_Mn:.2f} kip-ft", styles["Normal"]))
    story.append(Paragraph(f"DCR = {DCR:.3f}", styles["Normal"]))
    story.append(Paragraph(f"<b>Final Result: {result}</b>", styles["Normal"]))

    doc.build(story)

    buffer.seek(0)
    return buffer

        st.info("Press 'Generate Report' to run calculations.")
