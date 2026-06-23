import pandas as pd
from datetime import datetime


def generate_recommendations(profiles_df):

    recommendations = []

    for _, row in profiles_df.iterrows():

        customer_id = row["customer_id"]
        segment = row["segment"]
        churn = row["churn_risk"]
        purchases = row["purchases"]
        spend = row["spend"]
        engagement = row["engagement_score"]

        recommendation = "No_Action"
        priority = "Low"
        reason = "No immediate action required"
        score = 0.20
        confidence = "Low"

        # High-value retention case
        if churn == "High" and segment == "High Value":
            recommendation = "Retention_Save"
            priority = "High"
            reason = "High value customer at high risk of churn"
            score = 0.95
            confidence = "High"

        # General retention case
        elif churn == "High":
            recommendation = "Retention_Save"
            priority = "Medium"
            reason = "Customer at risk of churn"
            score = 0.82
            confidence = "High"

        # VIP upsell
        elif segment == "High Value" and purchases > 5:
            recommendation = "VIP_Upsell"
            priority = "Medium"
            reason = "High value, engaged customer"
            score = 0.78
            confidence = "Medium"

        # Cross-sell
        elif segment == "Mid Value" and purchases > 3:
            recommendation = "CrossSell"
            priority = "Medium"
            reason = "Engaged mid-value customer"
            score = 0.72
            confidence = "Medium"

        # Onboarding / activation
        elif purchases == 0 and engagement < 10:
            recommendation = "Onboarding"
            priority = "High"
            reason = "Low engagement customer with no purchases"
            score = 0.88
            confidence = "High"

        recommendations.append({
            "customer_id": customer_id,
            "segment": segment,
            "churn_risk": churn,
            "recommendation": recommendation,
            "priority": priority,
            "reason": reason,
            "score": round(score, 2),
            "confidence": confidence,
            "generated_at": datetime.now().isoformat()
        })

    return pd.DataFrame(recommendations)


if __name__ == "__main__":

    profiles_df = pd.read_csv("customer_profiles.csv")

    recs_df = generate_recommendations(profiles_df)

    print("\nRECOMMENDATION SUMMARY")
    print(recs_df["recommendation"].value_counts())

    print("\nPRIORITY BREAKDOWN")
    print(recs_df["priority"].value_counts())

    print("\nSAMPLE OUTPUT")
    print(recs_df.head())

    recs_df.to_csv("agent_recommendations.csv", index=False)

    print("\n✅ Exported: agent_recommendations.csv")