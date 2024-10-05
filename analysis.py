import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('products.csv')

if df.empty:
    print("The CSV file is empty. Please check the scraping script.")
else:
    df['price'] = df['price'].replace({r'\$': '', r',': ''}, regex=True).astype(float)

    most_expensive_product = df.loc[df['price'].idxmax()]
    cheapest_product = df.loc[df['price'].idxmin()]

    brand_counts = df.groupby('brand')['title'].count()
    seller_counts = df.groupby('seller')['title'].count()

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    brand_counts.plot(kind='bar', color='skyblue')
    plt.xlabel('Brand')
    plt.ylabel('Number of Products')
    plt.title('Number of Products by Brand')
    plt.xticks(rotation=45)

    plt.subplot(1, 2, 2)
    seller_counts.plot(kind='bar', color='lightcoral')
    plt.xlabel('Seller')
    plt.ylabel('Number of Products')
    plt.title('Number of Products by Seller')
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

    print(f"Most Expensive Product:\n{most_expensive_product}\n")
    print(f"Cheapest Product:\n{cheapest_product}\n")
