import dstack as ds
import plotly.express as px

app = ds.app()  # create an instance of the application


# an utility function that loads the data
def get_data():
    return px.data.stocks()


siebar = app.sidebar() # create a sidebar

# a drop-down control that shows stock symbols
stock = siebar.select(items=get_data().columns[1:].tolist())


# a handler that updates the plot based on the selected stock
def output_handler(self, stock):
    symbol = stock.value()  # the selected stock
    # a plotly line chart where the X axis is date and Y is the stock's price
    self.data = px.line(get_data(), x='date', y=symbol)


# a plotly chart output
app.output(handler=output_handler, depends=[stock])

# deploy the application with the name "stocks_sidebar" and print its URL
url = app.deploy("stocks_sidebar")
print(url)
