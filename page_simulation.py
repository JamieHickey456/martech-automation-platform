import pandas as pd
import numpy as np


def generate_page_data(num_pages=20):
    np.random.seed(42)

    pages = []

    for i in range(num_pages):
        page = f"/page_{i+1}"

        visits = np.random.randint(1000, 10000)
        conversions = np.random.randint(10, visits // 5)
        avg_time = np.random.uniform(10, 120)

        pages.append({
            "page": page,
            "visits": visits,
            "conversions": conversions,
            "conversion_rate": conversions / visits,
            "avg_time_on_page": avg_time
        })

    return pd.DataFrame(pages)