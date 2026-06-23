def analyse_pages(page_df):

    recommendations = []

    for _, row in page_df.iterrows():

        if row["visits"] > 5000 and row["conversion_rate"] < 0.02:
            rec = "High traffic but low conversion → Test CTA"
        elif row["avg_time_on_page"] > 60 and row["conversion_rate"] < 0.03:
            rec = "Users engaged but not converting → Check pricing or UX"
        elif row["visits"] < 2000:
            rec = "Low traffic → Improve SEO or campaigns"
        else:
            rec = "Performing well"

        recommendations.append(rec)

    page_df["recommendation"] = recommendations

    return page_df