import dstack as ds

app = ds.app()  # Create an instance of the application


# A handler that updates the label of the checkbox based on wether it's selected or not
def checkbox_handler(self):
    if self.selected:
        self.label = "Selected"
    else:
        self.label = "Not selected"


# A checkbox control
name = app.checkbox(handler=checkbox_handler, colspan=2)

# Deploy the application with the name "controls/checkbox" and print its URL
url = app.deploy("controls/checkbox")
print(url)
