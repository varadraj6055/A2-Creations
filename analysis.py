import pandas as pd
import matplotlib.pyplot as plt

# Read the extracted data from the CSV file
df = pd.read_csv('products.csv')

# Check if the DataFrame is empty
if df.empty:
    print("The CSV file is empty. Please check the scraping script.")
else:
    # Ensure 'price' is numeric for analysis
    df['price'] = df['price'].replace({r'\$': '', r',': ''}, regex=True).astype(float)

    # Analyze the data
    most_expensive_product = df.loc[df['price'].idxmax()]
    cheapest_product = df.loc[df['price'].idxmin()]

    # Group the data by brand and count the number of products
    brand_counts = df.groupby('brand')['title'].count()

    # Group the data by seller and count the number of products
    seller_counts = df.groupby('seller')['title'].count()

    # Plot the results
    plt.figure(figsize=(12, 6))

    # Number of Products by Brand
    plt.subplot(1, 2, 1)
    brand_counts.plot(kind='bar', color='skyblue')
    plt.xlabel('Brand')
    plt.ylabel('Number of Products')
    plt.title('Number of Products by Brand')
    plt.xticks(rotation=45)

    # Number of Products by Seller
    plt.subplot(1, 2, 2)
    seller_counts.plot(kind='bar', color='lightcoral')
    plt.xlabel('Seller')
    plt.ylabel('Number of Products')
    plt.title('Number of Products by Seller')
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

    # Print the most and least expensive products
    print(f"Most Expensive Product:\n{most_expensive_product}\n")
    print(f"Cheapest Product:\n{cheapest_product}\n")
