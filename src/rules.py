
import re
from src.dataset import load_keywords


def normalize_text(text):
    """
    Convert text to lowercase and remove extra spaces.
    """
    text = str(text).lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def is_safety_warning(message):
    """
    Detect common safety reminders such as:
    'Never share your OTP with anyone.'

    This is a heuristic, not proof that a
    message is legitimate.
    """
    text = normalize_text(message)

    safety_patterns = [
        r"\bnever share\b",
        r"\bdo not share\b",
        r"\bdon't share\b",
        r"\bnever disclose\b",
        r"\bdo not disclose\b",
    ]

    sensitive_terms = [
        "otp",
        "pin",
        "password",
        "one-time password",
    ]

    has_warning = any(
        re.search(pattern, text)
        for pattern in safety_patterns
    )

    has_sensitive_term = any(
        re.search(
            r"(?<!\w)" + re.escape(term) + r"(?!\w)",
            text
        )
        for term in sensitive_terms
    )

    return has_warning and has_sensitive_term


def detect_fraud(message):
    """
    Check a message against keyword patterns
    from Excel and return a structured result.
    """

    if not isinstance(message, str) or not message.strip():
        return {
            "assessment": "Unknown",
            "category": "Unknown",
            "matched_patterns": [],
            "matched_keywords": [],
            "explanations": []
        }

    keywords_df = load_keywords()
    normalized_message = normalize_text(message)

    matched_patterns = []
    matched_keywords = []
    explanations = []
    categories = []

    concern_rank = {
        "Low": 1,
        "Review": 2,
        "High": 3
    }

    highest_concern = 0

    # ------------------------------------------
    # STEP 1: MATCH KEYWORDS FROM EXCEL
    # ------------------------------------------

    for _, row in keywords_df.iterrows():

        phrase = str(row["Example Phrase"]).strip()
        pattern_name = str(row["Pattern Name"])
        category = str(row["Category"])
        concern = str(row["Default Concern"]).strip()
        explanation = str(row["Why It Matters"])

        if not phrase or phrase.lower() == "nan":
            continue

        pattern = (
            r"(?<!\w)"
            + re.escape(normalize_text(phrase))
            + r"(?!\w)"
        )

        if re.search(pattern, normalized_message):

            matched_patterns.append(pattern_name)
            matched_keywords.append(phrase)
            explanations.append(explanation)
            categories.append(category)

            highest_concern = max(
                highest_concern,
                concern_rank.get(concern, 0)
            )

    # ------------------------------------------
    # STEP 2: CHECK SAFETY WARNING CONTEXT
    # ------------------------------------------

    safety_warning = is_safety_warning(message)

    if safety_warning:

        matched_patterns.append("Safety warning language")
        explanations.append(
            "The message contains advice against "
            "sharing sensitive credentials."
        )

        # Avoid treating a safety reminder as a
        # direct request to share an OTP.
        #
        # But do not automatically mark it Low:
        # a malicious message could contain both
        # a warning and a fraudulent instruction.

        if matched_keywords:
            assessment = "Review"
        else:
            assessment = "Unknown"

        category = (
            categories[0]
            if categories
            else "Security Awareness"
        )

    # ------------------------------------------
    # STEP 3: NORMAL RULE ASSESSMENT
    # ------------------------------------------

    elif not matched_keywords:

        assessment = "Unknown"
        category = "Unknown"

    else:

        assessment = {
            1: "Low",
            2: "Review",
            3: "High"
        }.get(highest_concern, "Review")

        category = categories[0]

    # ------------------------------------------
    # STEP 4: RETURN RESULT
    # ------------------------------------------

    return {
        "assessment": assessment,
        "category": category,
        "matched_patterns": matched_patterns,
        "matched_keywords": matched_keywords,
        "explanations": explanations
    }


if __name__ == "__main__":

    test_messages = [
        (
            "Your bank account will be blocked today. "
            "Share your OTP immediately to verify."
        ),
        (
            "Never share your OTP or PIN with anyone. "
            "This is a security reminder."
        ),
        (
            "Your monthly account statement is available "
            "in your bank app. Do not share your OTP."
        ),
        (
            "Your interview is scheduled tomorrow at 11 AM."
        ),
        (
            "Never share your OTP. However, send your "
            "password to this number to unlock your account."
        )
    ]

    print("\n========== SCAMSHIELD RULE ENGINE ==========\n")

    for index, message in enumerate(test_messages, start=1):

        result = detect_fraud(message)

        print(f"TEST {index}")
        print("Message:", message)
        print("Assessment:", result["assessment"])
        print("Category:", result["category"])
        print("Matched patterns:", result["matched_patterns"])
        print("Matched keywords:", result["matched_keywords"])
        print("Explanations:", result["explanations"])
        print("-" * 60)
