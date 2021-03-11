import dstack as ds
import pandas as pd


@ds.cache()
def get_data():
    return pd.read_csv("https://www.dropbox.com/s/cat8vm6lchlu5tp/data.csv?dl=1", index_col=0)


def regions_handler(self):
    df = get_data()
    self.items = df["Region"].unique().tolist()


def countries_handler(self: ds.Select, regions: ds.Select):
    df = get_data()
    self.items = df[df["Region"] == regions.value()]["Country"].unique().tolist()


app = ds.app()

sidebar = app.sidebar()

regions = sidebar.select(handler=regions_handler)
countries = sidebar.select(handler=countries_handler, multiple=True,
                           placeholder="Select a country", depends=[regions])


def output_handler(self: ds.Output, countries: ds.Select):
    df = get_data()
    self.data = df[df["Country"].isin(countries.value())]


output = app.output(handler=output_handler, depends=[countries], colspan=6)

result = app.deploy("select_and_cache")
print(result.url)
