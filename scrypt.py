import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    #1.
    df = pd.read_csv('worldData.csv')
    
    #2. 
    df = df.drop("iso_a2.1", axis=1)
    df = df.drop("Unnamed: 0", axis=1)
    df = df.drop_duplicates()
    df = df.dropna()
    df = df[(df['pop'] < 2000000000) & (df['pop'] > 100)]
    df = df[(df['lifeExp'] < 100) & (df['lifeExp'] > 20)]
    df = df[(df['gdpPercap'] < 200000) & (df['gdpPercap'] > 100)]

    df.to_csv('cleanedWorldData.csv', index=False)
    
    #3.
    #a.
    country_count = df[(df["type"] == "Country") | (df["type"] == "Sovereign country")].groupby("continent").size()
    continent_with_most_countries = country_count.idxmax()
    print("a. " + continent_with_most_countries)
    #b.
    region_area = df.groupby("region_un")['area_km2'].sum()
    region_with_largest_area = region_area.idxmax()
    print("b. " + region_with_largest_area)
    #c.
    highest_life_expectancy_index = df[(df["type"] == "Country") | (df["type"] == "Sovereign country")]["lifeExp"].idxmax()
    highest_life_expectancy = df.loc[highest_life_expectancy_index]["name_long"]
    print("c. " + highest_life_expectancy)
    #d.
    subregion_average_gpd = df.groupby("subregion")["gdpPercap"].mean()
    highest_average_gpd = subregion_average_gpd.idxmax()
    lowest_average_gpd = subregion_average_gpd.idxmin()
    print("d. lowest: " + lowest_average_gpd + " highest: " + highest_average_gpd)

    #5.
    df["density"] = df["pop"] / df["area_km2"]
    average_density = df.groupby("region_un").mean("density").reset_index()
    plt.bar(average_density["region_un"], average_density["density"])
    plt.xlabel('Regions')
    plt.ylabel('Population Density (N/km^2)')
    plt.title('Mean Population Density of Regions')
    plt.show()

    plt.scatter(df["lifeExp"], df["gdpPercap"])
    plt.xlabel('Life Expectancy')
    plt.ylabel('GPD per Capita')
    plt.title('Life Expectancy vs GPD per Capita')
    plt.show()

    fig, axes = plt.subplots(2, 3)
    axes = axes.flatten()
    
    continents = df["continent"].unique()
    binwidth = 3
    bins=range(int(min(df["lifeExp"])), int(max(df["lifeExp"])) + binwidth, binwidth)
    for c in range(len(continents)):
        ax = axes[c]
        ax.hist(df[df["continent"] == continents[c]]["lifeExp"], edgecolor = "black", bins = bins)
        ax.set_title(continents[c])
    
    plt.suptitle('Histograms of Life Expectancy in Continents')
    plt.tight_layout()
    plt.show()
