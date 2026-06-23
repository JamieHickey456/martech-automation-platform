import pandas as pd
from datetime import datetime


def decide_campaign_action(row):
    """
    Rules-based automation engine (Salesforce/Journey Builder-style).
    Returns: (campaign_name, priority, reason)
    Priority: P1 = highest urgency, P4 = lowest.
    """

    segment = row["segment"]
    churn = row["churn_risk"]
    purchases = int(row["purchases"])
    logins = int(row["logins"])
    spend = float(row["spend"])

    # -------------------------
    # P1 – Save / Retain
    # -------------------------
    if churn == "High":
        return ("Retention_Save", "P1", "High churn risk detected")

    # -------------------------
    # P2 – Reactivation / Win-back
    # Make sure this triggers for dormant-ish users across segments
    # -------------------------
    if logins <= 15 and purchases == 0:
        return ("Reactivation", "P2", "Dormant behavior (low engagement + no purchases)")

    # -------------------------
    # P2 – Engagement Nudge
    # Mid/High value users drifting but not yet high-churn
    # -------------------------
    if churn == "Medium" and segment in ["Mid Value", "High Value"]:
        return ("Engagement_Nudge", "P2", "Medium churn risk + valuable customer")

    # -------------------------
    # P3 – VIP Upsell
    # -------------------------
    if segment == "High Value" and churn == "Low":
        return ("VIP_Upsell", "P3", "High value customer upsell path")

    # -------------------------
    # P3 – Onboarding / Activation
    # -------------------------
    if segment == "Low Value" and purchases == 0:
        return ("Onboarding", "P3", "Low value + no purchases (activation journey)")

    # -------------------------
    # P4 – Cross-sell
    # Tighten so it doesn't swallow the whole mid segment
    # -------------------------
    if segment == "Mid Value" and churn == "Low" and purchases >= 3 and spend >= 500:
        return ("CrossSell", "P4", "High engagement mid-value cross-sell opportunity")

    # Default: No action
    return ("No_Action", "P4", "Does not meet trigger conditions")


def run_automation(profile_df):
    """
    Takes customer profiles and returns:
      1) actions_df: customer-level action log
      2) summary_df: campaign counts
    """

    actions = []
    run_ts = datetime.utcnow().isoformat()

    for _, row in profile_df.iterrows():
        campaign, priority, reason = decide_campaign_action(row)

        actions.append({
            "run_ts": run_ts,
            "customer_id": row["customer_id"],
            "segment": row["segment"],
            "churn_risk": row["churn_risk"],
            "campaign": campaign,
            "priority": priority,
            "reason": reason
        })

    actions_df = pd.DataFrame(actions)

    summary_df = actions_df["campaign"].value_counts().reset_index()
    summary_df.columns = ["campaign", "count"]

    ordering = {
        "Retention_Save": 1,
        "Reactivation": 2,
        "Engagement_Nudge": 3,
        "VIP_Upsell": 4,
        "Onboarding": 5,
        "CrossSell": 6,
        "No_Action": 99
    }
    summary_df["order"] = summary_df["campaign"].map(ordering).fillna(50)
    summary_df = summary_df.sort_values("order").drop(columns=["order"]).reset_index(drop=True)

    return actions_df, summary_df