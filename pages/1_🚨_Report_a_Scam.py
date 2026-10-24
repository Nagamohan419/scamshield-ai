
import streamlit as st

st.set_page_config(
    page_title="Report a Scam | ScamShield AI",
    page_icon="🚨",
    layout="centered"
)

st.title("🚨 Report a Scam in India")

st.write(
    "Find the appropriate official government channel "
    "for reporting suspicious communications and cybercrime."
)

st.info(
    "ScamShield AI is an independent awareness project. "
    "It does not file complaints on your behalf and is "
    "not affiliated with any government agency."
)

# --------------------------------------------------
# REPORTING DECISION HELPER
# --------------------------------------------------

st.subheader("🧭 Where should I report?")

incident = st.radio(
    "What happened?",
    [
        "I received a suspicious SMS, call, or WhatsApp message",
        "I already lost money in an online scam",
        "I experienced another type of cybercrime",
        "I want to report a suspicious number or website"
    ]
)

if incident == (
    "I received a suspicious SMS, call, or WhatsApp message"
):
    st.success(
        "Use Chakshu on Sanchar Saathi to report "
        "suspected fraudulent communications."
    )

    st.link_button(
        "Open Chakshu",
        "https://sancharsaathi.gov.in/sfc/",
        use_container_width=True
    )

elif incident == (
    "I already lost money in an online scam"
):
    st.error(
        "Contact your bank or payment provider immediately "
        "through official channels. Call 1930 promptly "
        "to report suspected financial cyber fraud."
    )

    st.link_button(
        "Open National Cyber Crime Portal",
        "https://cybercrime.gov.in/",
        use_container_width=True
    )

elif incident == (
    "I experienced another type of cybercrime"
):
    st.warning(
        "Use the National Cyber Crime Reporting Portal "
        "to register a cybercrime complaint."
    )

    st.link_button(
        "File a Cybercrime Complaint",
        "https://cybercrime.gov.in/",
        use_container_width=True
    )

else:
    st.info(
        "Use the official Report Suspect facility to "
        "submit suspicious phone numbers, websites, "
        "email addresses, or social media identifiers."
    )

    st.link_button(
        "Report a Suspect",
        "https://cybercrime.gov.in/webform/cyber_suspect.aspx",
        use_container_width=True
    )


# --------------------------------------------------
# OFFICIAL CONTACTS
# --------------------------------------------------

st.divider()

st.header("📞 Official Cyber Safety Contacts")

st.subheader("National Cybercrime Helpline: 1930")

st.write(
    "For suspected online financial fraud, contact "
    "your bank immediately and call 1930 promptly."
)

st.markdown(
    "**Official website:** "
    "https://cybercrime.gov.in/"
)

st.subheader("Chakshu - Sanchar Saathi")

st.write(
    "Report suspected fraudulent calls, SMS, "
    "and WhatsApp communications."
)

st.markdown(
    "**Official website:** "
    "https://sancharsaathi.gov.in/sfc/"
)

st.subheader("Report a Suspect")

st.write(
    "Report suspicious phone numbers, website URLs, "
    "email addresses, and other identifiers."
)

st.link_button(
    "Open Report Suspect",
    "https://cybercrime.gov.in/webform/cyber_suspect.aspx",
    use_container_width=True
)


# --------------------------------------------------
# PREPARE BEFORE REPORTING
# --------------------------------------------------

st.divider()

st.header("📋 Prepare Your Complaint")

st.write(
    "Depending on the incident, the official portal "
    "may ask for the following information:"
)

st.checkbox("Date and approximate time of incident")
st.checkbox("Description of what happened")
st.checkbox("Screenshots or relevant evidence")
st.checkbox("Suspicious phone number, URL, or account details")
st.checkbox(
    "Transaction reference, amount, and bank details "
    "(if money was transferred)"
)

st.caption(
    "This checklist is for your preparation only. "
    "ScamShield does not collect or submit these details."
)


# --------------------------------------------------
# SUSPECT SEARCH
# --------------------------------------------------

st.divider()

st.header("🔎 Check a Suspicious Identifier")

st.write(
    "The National Cyber Crime Reporting Portal has "
    "a suspect repository where you can check "
    "certain reported identifiers."
)

st.link_button(
    "Open Official Suspect Search",
    "https://cybercrime.gov.in/webform/suspect_search_repository.aspx",
    use_container_width=True
)

st.warning(
    "An identifier not appearing in the repository "
    "does not mean it is safe. Reported information "
    "may be incomplete or subject to investigation."
)


# --------------------------------------------------
# SAFETY REMINDER
# --------------------------------------------------

st.divider()

st.subheader("🛡️ Important Safety Reminder")

st.write(
    "Never share OTPs, UPI PINs, passwords, "
    "or other confidential credentials with anyone. "
    "Verify requests using official channels."
)

st.caption(
    "ScamShield AI | Independent Open-Source "
    "Cyber Safety Awareness Project"
)
