
import pandas as pd

from src.dataset import load_messages
from src.rules import detect_fraud


def evaluate_rule_engine():

    df = load_messages()

    results = []

    for _, row in df.iterrows():

        message_id = row["Message ID"]
        message = row["Message Text (synthetic)"]
        actual_label = row["Ground Truth"]

        rule_result = detect_fraud(message)

        assessment = rule_result["assessment"]

        # Convert concern level into a binary prediction.
        # This is a provisional mapping for evaluation.
        if assessment in ["High", "Review"]:
            predicted_label = "Scam"

        elif assessment == "Low":
            predicted_label = "Legitimate"

        else:
            predicted_label = "Uncertain"

        results.append({
            "Message ID": message_id,
            "Message": message,
            "Actual Label": actual_label,
            "Rule Assessment": assessment,
            "Predicted Label": predicted_label,
            "Matched Keywords": ", ".join(
                rule_result["matched_keywords"]
            )
        })

    results_df = pd.DataFrame(results)

    # Calculate accuracy only for rows where:
    # 1. Ground truth is Scam or Legitimate
    # 2. The engine made a binary prediction
    evaluated = results_df[
        results_df["Actual Label"].isin(
            ["Scam", "Legitimate"]
        )
        &
        results_df["Predicted Label"].isin(
            ["Scam", "Legitimate"]
        )
    ]

    if len(evaluated) > 0:
        accuracy = (
            evaluated["Actual Label"]
            == evaluated["Predicted Label"]
        ).mean() * 100
    else:
        accuracy = 0

    coverage = (
        len(evaluated) / len(results_df) * 100
        if len(results_df) > 0
        else 0
    )

    print("\n========== SCAMSHIELD EVALUATION ==========")

    print("Total messages:", len(results_df))
    print("Binary predictions evaluated:", len(evaluated))
    print(f"Coverage: {coverage:.2f}%")
    print(f"Accuracy on evaluated predictions: {accuracy:.2f}%")

    print("\nPrediction Distribution:")
    print(results_df["Predicted Label"].value_counts())

    print("\nConfusion Matrix:")
    print(
        pd.crosstab(
            evaluated["Actual Label"],
            evaluated["Predicted Label"]
        )
    )

    # Save results to a new Excel file
    output_path = "data/scamshield_evaluation.xlsx"

    results_df.to_excel(
        output_path,
        index=False
    )

    print("\nEvaluation saved to:", output_path)


if __name__ == "__main__":
    evaluate_rule_engine()
