import pandas as pd

# ================= CONFIG =================
DATA_FILE = "posts.csv"
ENGAGEMENT_THRESHOLD = 0.05  # 5%
# ==========================================

def load_data():
    return pd.read_csv(DATA_FILE)

def calculate_metrics(df):
    df["engagement"] = (df["likes"] + df["comments"] + df["shares"]) / df["impressions"]
    return df

def generate_summary(df):
    total_posts = len(df)
    avg_engagement = df["engagement"].mean()

    top_post = df.loc[df["engagement"].idxmax()]
    low_post = df.loc[df["engagement"].idxmin()]

    return {
        "total_posts": total_posts,
        "average_engagement": round(avg_engagement * 100, 2),
        "top_post_type": top_post["post_type"],
        "top_engagement": round(top_post["engagement"] * 100, 2),
        "low_post_type": low_post["post_type"],
        "low_engagement": round(low_post["engagement"] * 100, 2),
    }

def recommendations(summary):
    recs = []

    if summary["top_post_type"] == "Reel":
        recs.append("Increase focus on Reels — highest engagement format.")

    if summary["average_engagement"] < ENGAGEMENT_THRESHOLD * 100:
        recs.append("Overall engagement is low — review posting times and captions.")

    recs.append("Repurpose high-performing content into future campaigns.")

    return recs

def main():
    df = load_data()
    df = calculate_metrics(df)
    summary = generate_summary(df)
    recs = recommendations(summary)

    print("\nSOCIAL MEDIA PERFORMANCE REPORT\n")
    print(f"Total posts analyzed: {summary['total_posts']}")
    print(f"Average engagement rate: {summary['average_engagement']}%")
    print(f"Top-performing content: {summary['top_post_type']} ({summary['top_engagement']}%)")
    print(f"Lowest-performing content: {summary['low_post_type']} ({summary['low_engagement']}%)")

    print("\nRECOMMENDATIONS")
    for r in recs:
        print(f"- {r}")

if __name__ == "__main__":
    main()

