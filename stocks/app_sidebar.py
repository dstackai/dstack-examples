import dstack as ds
import plotly.express as px

app = ds.app()  # Create an instance of the application


# An utility function that loads the data
def get_data():
    return px.data.stocks()


siebar = app.sidebar()  # Create a sidebar

# A drop-down control that shows stock symbols
stock = siebar.select(items=get_data().columns[1:].tolist())


# A handler that updates the plot based on the selected stock
def output_handler(self, stock):
    symbol = stock.value()  # The selected stock
    # A plotly line chart where the X axis is date and Y is the stock's price
    self.data = px.line(get_data(), x='date', y=symbol)


# A plotly chart output
app.output(handler=output_handler, depends=[stock])

# Deploy the application with the name "stocks_sidebar" and print its URL
url = app.deploy("stocks_sidebar")
print(url)
