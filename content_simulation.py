import pandas as pd
import random
from datetime import datetime


def generate_content(num_items=200):

    content_types = ["Blog", "Landing Page", "Product Page", "Article"]
    categories = ["Finance", "Tech", "Health", "Energy", "Retail"]
    authors = ["Alice", "Bob", "Charlie", "David", "Emma"]

    content = []

    for i in range(1, num_items + 1):

        content_id = f"CONTENT_{i}"
        content_type = random.choice(content_types)
        category = random.choice(categories)
        author = random.choice(authors)

        word_count = random.randint(300, 2000)
        quality_score = round(random.uniform(0.3, 0.95), 2)
        seo_score = round(random.uniform(0.3, 0.95), 2)

        publish_status = random.choice(["Draft", "Review", "Published"])

        created_at = datetime.now().isoformat()

        content.append({
            "content_id": content_id,
            "content_type": content_type,
            "category": category,
            "author": author,
            "word_count": word_count,
            "quality_score": quality_score,
            "seo_score": seo_score,
            "publish_status": publish_status,
            "created_at": created_at
        })

    return pd.DataFrame(content)


if __name__ == "__main__":

    df = generate_content(200)

    print("\nCONTENT SAMPLE")
    print(df.head())

    print("\nPUBLISH STATUS BREAKDOWN")
    print(df["publish_status"].value_counts())

    df.to_csv("cms_content.csv", index=False)

    print("\n✅ Exported: cms_content.csv")