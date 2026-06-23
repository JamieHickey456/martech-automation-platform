import pandas as pd


def generate_report(df):

    # Summary metrics
    total_pages = len(df)
    avg_ctr = round(df["ctr"].mean(), 4)

    status_counts = df["status"].value_counts()

    # Top performers
    top_pages = df.sort_values("ctr", ascending=False).head(10)

    # Pages needing attention
    attention_pages = df[df["status"] == "Needs Attention"].sort_values("ctr")

    # Below benchmark
    below_benchmark = df[df["status"] == "Below Benchmark"]

    report = {
        "total_pages": total_pages,
        "average_ctr": avg_ctr,
        "status_counts": status_counts,
        "top_pages": top_pages,
        "attention_pages": attention_pages,
        "below_benchmark": below_benchmark
    }

    return report


if __name__ == "__main__":

    df = pd.read_csv("cms_performance.csv")

    report = generate_report(df)

    print("\n📊 CMS PERFORMANCE REPORT")
    print(f"Total Pages: {report['total_pages']}")
    print(f"Average CTR: {report['average_ctr']}")

    print("\nSTATUS BREAKDOWN")
    print(report["status_counts"])

    print("\nTOP PERFORMING PAGES")
    print(report["top_pages"][["content_id", "ctr", "status"]])

    print("\nPAGES NEEDING ATTENTION")
    print(report["attention_pages"][["content_id", "ctr", "status"]])

    # Export key outputs
    report["top_pages"].to_csv("top_pages.csv", index=False)
    report["attention_pages"].to_csv("pages_needing_attention.csv", index=False)
    report["below_benchmark"].to_csv("below_benchmark_pages.csv", index=False)

    print("\n✅ Exported reports:")
    print(" - top_pages.csv")
    print(" - pages_needing_attention.csv")
    print(" - below_benchmark_pages.csv")