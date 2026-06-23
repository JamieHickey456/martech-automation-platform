import pandas as pd
import random


def simulate_live_page_performance(df):

    performance = []

    for _, row in df.iterrows():
        content_id = row["content_id"]
        content_type = row["content_type"]
        category = row["category"]
        tags = row["tags"]

        page_views = random.randint(500, 15000)
        pdf_clicks = random.randint(0, max(1, int(page_views * 0.15)))
        ctr = round(pdf_clicks / page_views, 4)

        benchmark_ctr = 0.03

        if ctr < 0.015:
            status = "Needs Attention"
        elif ctr < benchmark_ctr:
            status = "Below Benchmark"
        else:
            status = "Healthy"

        performance.append({
            "content_id": content_id,
            "content_type": content_type,
            "category": category,
            "tags": tags,
            "page_views": page_views,
            "pdf_clicks": pdf_clicks,
            "ctr": ctr,
            "benchmark_ctr": benchmark_ctr,
            "status": status
        })

    return pd.DataFrame(performance)


if __name__ == "__main__":
    df = pd.read_csv("cms_content_processed.csv")

    performance_df = simulate_live_page_performance(df)

    print("\nCTR STATUS BREAKDOWN")
    print(performance_df["status"].value_counts())

    print("\nSAMPLE OUTPUT")
    print(performance_df.head())

    performance_df.to_csv("cms_performance.csv", index=False)

    print("\n✅ Exported: cms_performance.csv")