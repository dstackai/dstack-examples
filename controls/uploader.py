import dstack as ds
import pandas as pd

app = ds.app()  # Create an instance of the application


# A handler that loads a dataframe from the content of the uploaded CSV file and passes it to the output
def app_handler(self, uploader):
    if len(uploader.uploads) > 0:
        with uploader.uploads[0].open() as f:
            self.label = uploader.uploads[0].file_name
            self.data = pd.read_csv(f).head(100)
    else:
        self.label = "No file selected"
        self.data = None


# A file uploader control
uploader = app.uploader(label="Select a CSV file")

# An output control that shows the content of the uploaded file
app.output(handler=app_handler, depends=[uploader])

# Deploy the application with the name "controls/uploader" and print its URL
url = app.deploy("controls/uploader")
print(url)
