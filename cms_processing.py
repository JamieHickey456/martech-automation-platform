import pandas as pd


def process_content(df):

    processed = []

    for _, row in df.iterrows():

        content_id = row["content_id"]
        content_type = row["content_type"]
        category = row["category"]
        word_count = row["word_count"]
        quality_score = row["quality_score"]
        seo_score = row["seo_score"]
        publish_status = row["publish_status"]

        # 🔹 Tagging logic
        tags = []

        if content_type == "Blog":
            tags.append("Thought Leadership")

        if content_type == "Product Page":
            tags.append("Conversion")

        if category == "Finance":
            tags.append("Finance")

        if category == "Energy":
            tags.append("Energy")

        if word_count > 1200:
            tags.append("Long Read")

        # 🔹 Content score (simple weighted score)
        content_score = round((quality_score * 0.6 + seo_score * 0.4), 2)

        # 🔹 Readiness classification
        if content_score >= 0.75:
            readiness = "High"
        elif content_score >= 0.55:
            readiness = "Medium"
        else:
            readiness = "Low"

        processed.append({
            "content_id": content_id,
            "content_type": content_type,
            "category": category,
            "content_score": content_score,
            "readiness": readiness,
            "tags": ", ".join(tags),
            "original_status": publish_status
        })

    return pd.DataFrame(processed)


if __name__ == "__main__":

    df = pd.read_csv("cms_content.csv")

    processed_df = process_content(df)

    print("\nCONTENT SCORE DISTRIBUTION")
    print(processed_df["readiness"].value_counts())

    print("\nSAMPLE OUTPUT")
    print(processed_df.head())

    processed_df.to_csv("cms_content_processed.csv", index=False)

    print("\n✅ Exported: cms_content_processed.csv")
    