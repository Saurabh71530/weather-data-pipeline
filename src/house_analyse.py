import pandas as pd


def analyze_house_prices():
    try:
        df = pd.read_csv("data/house_prices.csv")

        print("\n🏠 HOUSE PRICE ANALYSIS")
        print("====================")

        df.columns = df.columns.str.lower()

        avg_price = df["price"].mean()
        max_price = df["price"].max()

        print(f"Average Price: {avg_price}")
        print(f"Max Price: {max_price}")

    except Exception as e:
        print(f"❌ CSV Error: {e}")


if __name__ == "__main__":
    analyze_house_prices()