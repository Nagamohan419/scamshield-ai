
import streamlit as st

from datetime import datetime
from io import StringIO

from src.rules import detect_fraud
from src.gemma_service import analyze_with_gemma
from src.response_agent import create_response_plan
from src.translation_service import translate_analysis


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="ScamShield AI",
    page_icon="🛡️",
    layout="centered"
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "response_plan" not in st.session_state:
    st.session_state.response_plan = None

if "translation_cache" not in st.session_state:
    st.session_state.translation_cache = {}


# --------------------------------------------------
# TRANSLATION HELPER
# --------------------------------------------------

def get_translated_data(data, language, cache_key):
    """
    Translate structured AI results and cache them
    to avoid unnecessary repeat API calls.
    """

    if language == "English":
        return data

    key = (cache_key, language)

    if key not in st.session_state.translation_cache:

        with st.spinner(
            f"Translating into {language} using Gemma 4..."
        ):
            translated = translate_analysis(
                data,
                language
            )

            st.session_state.translation_cache[key] = translated

    return st.session_state.translation_cache[key]


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🛡️ ScamShield AI")

st.subheader("AI-Powered Scam Message Analyzer")

st.write(
    "Analyze suspicious SMS, WhatsApp, banking, UPI, "
    "job, shopping, and investment messages using "
    "an Excel-based rule engine and Gemma 4."
)

st.info(
    "ScamShield provides fraud-awareness guidance, "
    "not a definitive fraud or safety verification."
)


# --------------------------------------------------
# LANGUAGE SELECTION
# --------------------------------------------------

language = st.selectbox(
    "🌐 Choose explanation language",
    ["English", "Hindi", "Telugu"],
    index=0
)


# --------------------------------------------------
# SAMPLE MESSAGES
# --------------------------------------------------

sample_messages = {
    "Choose a sample": "",

    "Banking Scam":
        "Your bank account will be blocked today. "
        "Share your OTP immediately to verify.",

    "UPI Scam":
        "Congratulations! You have received Rs 5000. "
        "Enter your UPI PIN to receive your reward.",

    "Job Scam":
        "You have been selected for a job. "
        "Pay a registration fee of Rs 999 to confirm.",

    "Legitimate Message":
        "Your interview is scheduled tomorrow at 11 AM. "
        "Please join using the meeting invitation."
}

selected_sample = st.selectbox(
    "Try a sample message",
    list(sample_messages.keys())
)


# --------------------------------------------------
# USER INPUT
# --------------------------------------------------

message = st.text_area(
    "Paste the message you want to analyze",
    value=sample_messages[selected_sample],
    height=160,
    placeholder="Paste a suspicious message here...",
    max_chars=3000
)


# --------------------------------------------------
# ANALYSIS BUTTON
# --------------------------------------------------

if st.button(
    "🔍 Analyze Message",
    type="primary",
    use_container_width=True
):

    if not message.strip():

        st.warning("Please enter a message to analyze.")

    else:

        with st.spinner(
            "Analyzing message with ScamShield AI..."
        ):

            try:

                rule_result = detect_fraud(message)

                ai_result = analyze_with_gemma(
                    message,
                    rule_result
                )

                st.session_state.analysis = {
                    "message": message,
                    "rule_result": rule_result,
                    "ai_result": ai_result
                }

                st.session_state.response_plan = None
                st.session_state.translation_cache = {}

            except Exception as error:

                st.error("Analysis could not be completed.")
                st.code(str(error))


# --------------------------------------------------
# DISPLAY ANALYSIS RESULTS
# --------------------------------------------------

analysis = st.session_state.analysis

if analysis and analysis["message"] == message:

    rule_result = analysis["rule_result"]
    original_ai_result = analysis["ai_result"]

    # ------------------------------------------
    # TRANSLATE ANALYSIS
    # ------------------------------------------

    try:

        ai_result = get_translated_data(
            original_ai_result,
            language,
            "analysis"
        )

    except Exception as error:

        st.warning(
            "Translation unavailable. "
            "Showing English analysis."
        )

        ai_result = original_ai_result

    st.divider()

    st.header("Analysis Results")

    # ------------------------------------------
    # AI ASSESSMENT
    # ------------------------------------------

    assessment = original_ai_result.get(
        "assessment",
        "Unknown"
    )

    if assessment == "High":
        st.error("🚨 High Concern")

    elif assessment == "Review":
        st.warning("⚠️ Needs Review")

    elif assessment == "Low":
        st.success("🟢 Low Concern")

    else:
        st.info("❓ Inconclusive")

    # ------------------------------------------
    # CATEGORY
    # ------------------------------------------

    st.write(
        "**Message Category:**",
        original_ai_result.get(
            "category",
            "Unknown"
        )
    )

    # ------------------------------------------
    # SUMMARY
    # ------------------------------------------

    st.subheader("🧠 ScamShield AI Explanation")

    st.write(
        ai_result.get(
            "summary",
            "No explanation available."
        )
    )

    # ------------------------------------------
    # WARNING SIGNS
    # ------------------------------------------

    st.subheader("🚩 Warning Signs")

    red_flags = ai_result.get(
        "red_flags",
        []
    )

    if red_flags:

        for flag in red_flags:
            st.write("•", flag)

    else:
        st.write(
            "No specific warning signs identified. "
            "This does not guarantee the message is safe."
        )

    # ------------------------------------------
    # RECOMMENDED ACTIONS
    # ------------------------------------------

    st.subheader("🛡️ Recommended Actions")

    actions = ai_result.get(
        "recommended_actions",
        []
    )

    if actions:

        for index, action in enumerate(
            actions,
            start=1
        ):
            st.write(f"{index}. {action}")

    else:
        st.write(
            "Verify unexpected requests using "
            "official channels."
        )

    # ------------------------------------------
    # EXCEL RULE ENGINE RESULTS
    # ------------------------------------------

    with st.expander(
        "🔎 View Excel Rule Engine Findings"
    ):

        st.write(
            "**Rule Assessment:**",
            rule_result["assessment"]
        )

        st.write(
            "**Detected Keywords:**",
            rule_result["matched_keywords"]
        )

        st.write(
            "**Matched Patterns:**",
            rule_result["matched_patterns"]
        )

        st.write(
            "**Explanations:**",
            rule_result["explanations"]
        )

    st.caption(
        "Powered by Gemma 4 and an Excel-based "
        "fraud-pattern dataset. "
        "Do not submit passwords, OTPs, account numbers, "
        "or other sensitive personal information."
    )

    # ==================================================
    # SCAM RESPONSE AGENT
    # ==================================================

    st.divider()

    st.header("🤖 Scam Response Agent")

    st.write(
        "ScamShield can create a personalized safety "
        "plan based on what happened after you "
        "received this message."
    )

    # Offer guidance appropriate to the analysis result.
    assessment = original_ai_result.get("assessment", "Unknown")

    if assessment == "High":
        st.error(
            "This message has concerning scam indicators. "
            "Choose what happened to get suitable guidance."
        )
        situation_options = {
            "I only received the message": "not_shared",
            "I shared an OTP, PIN, or password": "shared",
            "I already transferred money": "paid",
        }
    elif assessment == "Review":
        st.warning("This message needs verification. Choose what you need help with.")
        situation_options = {
            "Help me verify this message": "not_shared",
            "I shared sensitive information": "shared",
            "I already transferred money": "paid",
        }
    elif assessment == "Low":
        st.success(
            "No major scam indicators were identified. "
            "You can still request a verification checklist."
        )
        situation_options = {
            "Give me a verification checklist": "not_shared",
            "I shared sensitive information and need guidance": "shared",
            "I transferred money and need guidance": "paid",
        }
    else:
        st.info(
            "The message is inconclusive. You can verify its sender "
            "or request guidance based on what happened."
        )
        situation_options = {
            "Help me verify this message": "not_shared",
            "I shared sensitive information": "shared",
            "I already transferred money": "paid",
        }

    # A new analysis gets a new widget key so old choices do not carry over.
    import hashlib
    message_key = hashlib.sha256(message.encode("utf-8")).hexdigest()[:12]
    selected_situation = st.radio(
        "What would you like help with?",
        options=list(situation_options.keys()),
        index=None,
        key=f"customer_situation_{assessment}_{message_key}",
    )
    situation = (
        situation_options[selected_situation]
        if selected_situation is not None
        else None
    )

    if st.button(
        "🛡️ Get My Guidance",
        use_container_width=True,
        disabled=situation is None
    ):

        with st.spinner(
            "Gemma 4 is preparing your safety plan..."
        ):

            try:

                response_plan = create_response_plan(
                    message=message,
                    rule_result=rule_result,
                    ai_result=original_ai_result,
                    situation=situation
                )

                st.session_state.response_plan = {
                    "message": message,
                    "situation": situation,
                    "plan": response_plan
                }

                # Clear cached agent translations
                for key in list(
                    st.session_state.translation_cache
                ):
                    if key[0] == "agent":
                        del st.session_state.translation_cache[key]

            except Exception as error:

                st.error(
                    "The safety plan could not be generated."
                )

                st.code(str(error))

    # ------------------------------------------
    # DISPLAY AGENT RESPONSE
    # ------------------------------------------

    saved_response = st.session_state.response_plan

    if (
        saved_response
        and situation is not None
        and saved_response["message"] == message
        and saved_response["situation"] == situation
    ):

        original_plan = saved_response["plan"]

        # ------------------------------------------
        # TRANSLATE RESPONSE PLAN
        # ------------------------------------------

        try:

            plan = get_translated_data(
                original_plan,
                language,
                "agent"
            )

        except Exception:

            st.warning(
                "Safety-plan translation unavailable. "
                "Showing English."
            )

            plan = original_plan

        st.subheader("📋 Your Personalized Safety Plan")

        st.success(plan["headline"])

        st.write(plan["explanation"])

        st.markdown("#### ✅ Immediate Actions")

        for index, action in enumerate(
            plan["immediate_actions"],
            start=1
        ):
            st.write(f"{index}. {action}")

        st.markdown("#### 🚫 Things to Avoid")

        for action in plan["avoid_actions"]:
            st.write(f"• {action}")

        st.markdown("#### 📢 Reporting Guidance")

        st.write(plan["reporting_guidance"])

        st.markdown("#### 💡 Scam Awareness Tip")

        st.info(plan["awareness_tip"])

        st.caption(
            "AI-generated safety guidance. "
            "Use official channels to verify "
            "important information."
        )

        # ==================================================
        # DOWNLOADABLE MULTILINGUAL SCAM REPORT
        # ==================================================

        st.divider()

        st.subheader("📄 Download Scam Report")

        st.write(
            "Download your scam-awareness report "
            "with AI explanations and safety guidance "
            f"in {language}."
        )

        report = StringIO()

        report.write(
            "SCAMSHIELD AI - SCAM AWARENESS REPORT\n"
        )

        report.write("=" * 50 + "\n\n")

        report.write(
            "Generated: "
            + datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            + "\n"
        )

        report.write(
            f"Explanation Language: {language}\n\n"
        )

        # ------------------------------------------
        # ORIGINAL MESSAGE
        # ------------------------------------------

        report.write("ORIGINAL MESSAGE\n")
        report.write("-" * 50 + "\n")
        report.write(message + "\n\n")

        # ------------------------------------------
        # AI ASSESSMENT
        # ------------------------------------------

        report.write("GEMMA 4 AI ASSESSMENT\n")
        report.write("-" * 50 + "\n")

        report.write(
            "Concern Level: "
            + original_ai_result.get(
                "assessment",
                "Unknown"
            )
            + "\n"
        )

        report.write(
            "Category: "
            + original_ai_result.get(
                "category",
                "Unknown"
            )
            + "\n"
        )

        report.write(
            "Explanation: "
            + ai_result.get(
                "summary",
                ""
            )
            + "\n\n"
        )

        # ------------------------------------------
        # WARNING SIGNS
        # ------------------------------------------

        report.write("WARNING SIGNS\n")
        report.write("-" * 50 + "\n")

        for flag in ai_result.get(
            "red_flags",
            []
        ):
            report.write(f"- {flag}\n")

        report.write("\n")

        # ------------------------------------------
        # RULE ENGINE FINDINGS
        # ------------------------------------------

        report.write("EXCEL RULE ENGINE FINDINGS\n")
        report.write("-" * 50 + "\n")

        report.write(
            "Rule Assessment: "
            + rule_result.get(
                "assessment",
                "Unknown"
            )
            + "\n"
        )

        report.write(
            "Matched Keywords: "
            + ", ".join(
                rule_result.get(
                    "matched_keywords",
                    []
                )
            )
            + "\n\n"
        )

        # ------------------------------------------
        # PERSONALIZED RESPONSE PLAN
        # ------------------------------------------

        report.write("PERSONALIZED RESPONSE PLAN\n")
        report.write("-" * 50 + "\n")

        report.write(
            f"Customer Situation: {selected_situation}\n"
        )

        report.write(
            f"Headline: {plan['headline']}\n"
        )

        report.write(
            f"Explanation: {plan['explanation']}\n\n"
        )

        report.write("IMMEDIATE ACTIONS\n")

        for index, action in enumerate(
            plan["immediate_actions"],
            start=1
        ):
            report.write(
                f"{index}. {action}\n"
            )

        report.write("\nTHINGS TO AVOID\n")

        for action in plan["avoid_actions"]:
            report.write(f"- {action}\n")

        report.write("\nREPORTING GUIDANCE\n")

        report.write(
            plan["reporting_guidance"]
            + "\n\n"
        )

        report.write("SCAM AWARENESS TIP\n")

        report.write(
            plan["awareness_tip"]
            + "\n\n"
        )

        report.write("=" * 50 + "\n")

        report.write(
            "DISCLAIMER:\n"
            "This is an AI-generated fraud-awareness "
            "report, not an official complaint or "
            "verified fraud determination.\n"
            "Review and remove sensitive information "
            "before sharing this report.\n"
        )

        # ------------------------------------------
        # DOWNLOAD BUTTON
        # ------------------------------------------

        st.download_button(
            label=f"⬇️ Download {language} Scam Report",
            data=report.getvalue().encode("utf-8-sig"),
            file_name=(
                "scamshield_report_"
                + language.lower()
                + ".txt"
            ),
            mime="text/plain; charset=utf-8",
            use_container_width=True
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "ScamShield AI | Open-Source AI Hackathon Project"
)
