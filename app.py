import pandas as pd
import streamlit as st

from auth import login, logout

from risk_engine import (
    calculate_risk,
    classify_risk
)

from fmea import (
    calculate_rpn,
    classify_rpn
)

from database import (
    initialize_database,
    add_hazard,
    get_all_hazards,
    add_fmea,
    get_all_fmea,
    add_audit_log,
    get_audit_logs
)

from pdf_report import generate_pdf


# -------------------------
# INITIALIZE DATABASE
# -------------------------

initialize_database()


# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(
    page_title="Medical Device Risk Tool",
    layout="wide"
)


# -------------------------
# SESSION STATE
# -------------------------

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False


# -------------------------
# LOGIN
# -------------------------

if not st.session_state["logged_in"]:

    login()

else:

    st.markdown("""
# 🏥 Medical Device Risk Assessment Tool
### ISO 14971 Inspired Risk Management System
""")

    st.sidebar.title("Medical Device Risk Tool")

    if "username" in st.session_state:
        st.sidebar.success(
            f"Logged in as: {st.session_state['username']}"
        )

    st.sidebar.markdown("---")

    menu = st.sidebar.selectbox(
        "Select Module",
        [
            "Dashboard",
            "Hazard Management",
            "FMEA Analysis",
            "Audit Trail",
            "Risk Report"
        ]
    )

    # =====================================================
    # DASHBOARD
    # =====================================================

    if menu == "Dashboard":

        st.header("📊 Risk Management Dashboard")

        hazards = get_all_hazards()
        fmea_records = get_all_fmea()

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

            elif hazard[5] == "Low":
                low += 1

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Hazards", total_hazards)
        col2.metric("FMEA Records", total_fmea)
        col3.metric("Critical Risks", critical)
        col4.metric("High Risks", high)

        st.divider()

        st.subheader("📈 Risk Distribution")

        chart_data = pd.DataFrame(
            {
                "Risk Level": [
                    "Critical",
                    "High",
                    "Medium",
                    "Low"
                ],
                "Count": [
                    critical,
                    high,
                    medium,
                    low
                ]
            }
        )

        st.bar_chart(
            chart_data.set_index("Risk Level")
        )

        st.info(
            "This application follows the ISO 14971-inspired workflow for medical device risk assessment."
        )
            # =====================================================
    # HAZARD MANAGEMENT
    # =====================================================

    elif menu == "Hazard Management":

        st.header("⚠️ Medical Device Hazard Assessment")

        hazard_name = st.text_input("Hazard Name")

        severity = st.slider(
            "Severity",
            1,
            5,
            1
        )

        probability = st.slider(
            "Probability",
            1,
            5,
            1
        )

        mitigation = st.text_area(
            "Mitigation Action"
        )

        if st.button("Save Hazard"):

            risk_score = calculate_risk(
                severity,
                probability
            )

            risk_level = classify_risk(
                risk_score
            )

            add_hazard(
                hazard_name,
                severity,
                probability,
                risk_score,
                risk_level,
                mitigation
            )

            if "username" in st.session_state:

                add_audit_log(
                    st.session_state["username"],
                    f"Added Hazard: {hazard_name}"
                )

            st.success("Hazard Saved Successfully!")

            st.metric(
                "Risk Score",
                risk_score
            )

            st.metric(
                "Risk Level",
                risk_level
            )

        st.divider()

        st.subheader("📋 Hazard History")

        hazards = get_all_hazards()

        if hazards:

            for hazard in hazards:

                st.write(f"""
**ID:** {hazard[0]}

**Hazard:** {hazard[1]}

**Severity:** {hazard[2]}

**Probability:** {hazard[3]}

**Risk Score:** {hazard[4]}

**Risk Level:** {hazard[5]}

**Mitigation:** {hazard[6]}
""")

                st.divider()

        else:

            st.info("No hazards available.")

    # =====================================================
    # FMEA ANALYSIS
    # =====================================================

    elif menu == "FMEA Analysis":

        st.header("🔬 Failure Mode and Effects Analysis")

        failure_mode = st.text_input(
            "Failure Mode"
        )

        effect = st.text_input(
            "Effect"
        )

        cause = st.text_input(
            "Cause"
        )

        severity = st.slider(
            "Severity (S)",
            1,
            10,
            1
        )

        occurrence = st.slider(
            "Occurrence (O)",
            1,
            10,
            1
        )

        detection = st.slider(
            "Detection (D)",
            1,
            10,
            1
        )

        if st.button("Calculate RPN"):

            rpn = calculate_rpn(
                severity,
                occurrence,
                detection
            )

            risk_class = classify_rpn(
                rpn
            )

            add_fmea(
                failure_mode,
                effect,
                cause,
                severity,
                occurrence,
                detection,
                rpn
            )

            if "username" in st.session_state:

                add_audit_log(
                    st.session_state["username"],
                    f"Added FMEA: {failure_mode}"
                )

            st.success("FMEA Record Saved!")

            st.metric(
                "RPN",
                rpn
            )

            st.metric(
                "Risk Classification",
                risk_class
            )

        st.divider()

        st.subheader("📋 FMEA History")

        records = get_all_fmea()

        if records:

            for row in records:

                st.write(f"""
**ID:** {row[0]}

**Failure Mode:** {row[1]}

**Effect:** {row[2]}

**Cause:** {row[3]}

**Severity:** {row[4]}

**Occurrence:** {row[5]}

**Detection:** {row[6]}

**RPN:** {row[7]}
""")

                st.divider()

        else:

            st.info("No FMEA records available.")
                # =====================================================
    # AUDIT TRAIL
    # =====================================================

    elif menu == "Audit Trail":

        st.header("📜 Audit Trail")

        logs = get_audit_logs()

        if logs:

            for log in logs:

                st.write(f"""
**ID:** {log[0]}

**User:** {log[1]}

**Action:** {log[2]}

**Timestamp:** {log[3]}
""")

                st.divider()

        else:

            st.info("No audit records available.")

    # =====================================================
    # RISK REPORT
    # =====================================================

    elif menu == "Risk Report":

        st.header("📄 Risk Assessment Report")

        hazards = get_all_hazards()

        fmea_records = get_all_fmea()

        st.subheader("Hazard Summary")

        if hazards:

            hazard_df = pd.DataFrame(
                hazards,
                columns=[
                    "ID",
                    "Hazard",
                    "Severity",
                    "Probability",
                    "Risk Score",
                    "Risk Level",
                    "Mitigation",
                    "Created At"
                ]
            )

            st.dataframe(
                hazard_df,
                use_container_width=True
            )

        else:

            st.info("No Hazard Records Found.")

        st.divider()

        st.subheader("FMEA Summary")

        if fmea_records:

            fmea_df = pd.DataFrame(
                fmea_records,
                columns=[
                    "ID",
                    "Failure Mode",
                    "Effect",
                    "Cause",
                    "Severity",
                    "Occurrence",
                    "Detection",
                    "RPN",
                    "Created At"
                ]
            )

            st.dataframe(
                fmea_df,
                use_container_width=True
            )

        else:

            st.info("No FMEA Records Found.")

        st.divider()

        if st.button("📄 Generate Professional PDF Report"):

            generate_pdf(
                hazards,
                fmea_records
            )

            st.success(
                "✅ PDF Report Generated Successfully!"
            )

            try:

                with open(
                    "Risk_Assessment_Report.pdf",
                    "rb"
                ) as pdf_file:

                    st.download_button(
                        label="⬇ Download PDF Report",
                        data=pdf_file,
                        file_name="Risk_Assessment_Report.pdf",
                        mime="application/pdf"
                    )

            except FileNotFoundError:

                st.error(
                    "PDF file not found."
                )

    st.markdown("---")

    st.caption(
        "Developed by G. Subiksha | Biomedical Engineering | ISO 14971 Inspired Medical Device Risk Assessment Tool"
    )

