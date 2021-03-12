from time import sleep
import dstack as ds

from dstack import trange

# Create an instance of the application
app = ds.app()


# A handler that sets the text to the markdown control
def markdown_handler(self):
    for _ in trange(100, desc="Calculating some stupid data", unit="task"):
        sleep(0.5)
    self.text = "Finished"


# A markdown control
app.markdown(handler=markdown_handler)

# Deploy the application with the name "tqdm" and print its URL
result = app.deploy("tqdm")
print(result.url)
