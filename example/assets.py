
import pandas as pd

import matplotlib.pyplot as plt
from pandas import DataFrame
from io import BytesIO
import base64


from dagster import asset, Output, AssetExecutionContext, MetadataValue

def countries_bar_graph(df: DataFrame) -> str:
    plt.figure(figsize=(10, 6))
    plt.bar(df.index, df["Population"])
    plt.xlabel('Country')
    plt.ylabel('Population')
    plt.title("Top 10 Most Populated Countries")
    plt.tight_layout()

    with BytesIO() as buffer:
        plt.savefig(buffer, format="png")
        image_data = base64.b64encode(buffer.getvalue())

        # Convert the image to Markdown
        md_content = f"![img](data:image/png;base64,{image_data.decode()})"

    return md_content

@asset
def country_population() -> pd.DataFrame:
    return pd.read_html(
        "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population"
    )[0]


@asset
def country_population_meta(context: AssetExecutionContext, country_population: pd.DataFrame) -> Output[pd.DataFrame]:
    top_10 = country_population[["Country / Dependency","Population"]].sort_values("Population", ascending=False).iloc[1:10].set_index("Country / Dependency")
    md_content = countries_bar_graph(top_10)
    context.add_output_metadata(metadata={"plot": MetadataValue.md(md_content)})
    return Output(country_population, metadata={"num_rows": len(country_population)})