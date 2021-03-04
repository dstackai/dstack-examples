import dstack as ds
import plotly.express as px

# Create an instance of the application
app = ds.app()

# Create a tab
scatter_tab = app.tab("Scatter Chart")

# Create an output with a chart
scatter_tab.output(data=px.scatter(px.data.iris(), x="sepal_width", y="sepal_length", color="species"))

# Create a tab
bar_tab = app.tab("Bar Chart")

# Create an output with a chart
bar_tab.output(data=px.bar(px.data.tips(), x="sex", y="total_bill", color="smoker", barmode="group"))

# Deploy the application with the name "tabs" and print its URL
url = app.deploy("tabs")
print(url)
