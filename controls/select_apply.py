import dstack as ds
import pandas as pd

app = ds.app()  # Create an instance of the application


# An utility function that loads the data
def get_data():
    return pd.read_csv("https://www.dropbox.com/s/cat8vm6lchlu5tp/data.csv?dl=1", index_col=0)


# An utility function that returns regions
def regions_handler(self):
    df = get_data()
    self.items = df["Region"].unique().tolist()


# A drop-down control that shows regions
regions = app.select(handler=regions_handler, label="Region")


# A handler that updates the drop-down with counties based on the selected region
def countries_handler(self, regions):
    region = regions.value()  # the selected region
    df = get_data()
    self.items = df[df["Region"] == region]["Country"].unique().tolist()


# A drop-down control that shows countries
countries = app.select(handler=countries_handler, label="Country", depends=[regions])


# A handler that updates the table output based on the selected country
def output_handler(self, countries):
    country = countries.value()  # the selected country
    df = get_data()
    self.data = df[df["Country"] == country]  # we assign a pandas dataframe here to self.data


# An output that shows companies based on the selected country
app.output(handler=output_handler, depends=[countries], require_apply=True)

# Deploy the application with the name "controls/select_depends" and print its URL
url = app.deploy("controls/select_apply")
print(url)
