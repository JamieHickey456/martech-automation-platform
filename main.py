from data_simulation import generate_customer_events
from processing import build_customer_profiles
from automation import run_automation
from page_simulation import generate_page_data
from optimisation import analyse_pages


def main():
    customers_df, events_df = generate_customer_events(num_customers=5000, months=6)

    # Export raw events for later AWS upload
    events_df.to_csv("customer_events.csv", index=False)

    profile_df = build_customer_profiles(customers_df, events_df)

    print("\nSEGMENT BREAKDOWN")
    print(profile_df["segment"].value_counts())

    print("\nCHURN RISK BREAKDOWN")
    print(profile_df["churn_risk"].value_counts())

    actions_df, summary_df = run_automation(profile_df)

    print("\nCAMPAIGN SUMMARY (what the automation engine triggered)")
    print(summary_df)

    print("\nSAMPLE ACTION LOG")
    print(actions_df.head(10))

    profile_df.to_csv("customer_profiles.csv", index=False)
    actions_df.to_csv("campaign_actions.csv", index=False)

    print("\n✅ Exported: customer_events.csv, customer_profiles.csv and campaign_actions.csv")


if __name__ == "__main__":
    main()
    # 5. Page optimisation layer
page_df = generate_page_data()
page_df = analyse_pages(page_df)

print("\nPAGE OPTIMISATION INSIGHTS")
print(page_df.head())

page_df.to_csv("page_insights.csv", index=False)