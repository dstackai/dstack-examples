import dstack as ds
import plotly.express as px

app = ds.app()  # Сreate an instance of the application


# An utility function that loads the data
def get_data():
    return px.data.stocks()


# A drop-down control that shows stock symbols
stock = app.select(items=get_data().columns[1:].tolist())


# A handler that updates the plot based on the selected stock
def output_handler(self, stock):
    print("Calling output_handler")  # Log a message
    symbol = stock.value()  # the selected stock
    # a plotly line chart where the X axis is date and Y is the stock's price
    self.data = px.line(get_data(), x='date', y=symbol)


# A plotly chart output
app.output(handler=output_handler, depends=[stock], require_apply=True)

# Deploy the application with the name "stocks_logs" and print its URL
url = app.deploy("stocks_logs")
print(url)
