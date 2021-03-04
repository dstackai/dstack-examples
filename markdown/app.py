import dstack as ds

app = ds.app()  # Create an instance of the application

# A markdown output
app.markdown(text="Hello, **World!**")

# Deploy the application with the name "markdown" and print its URL
url = app.deploy("markdown")
print(url)