import dstack as ds

app = ds.app()  # create an instance of the application


# a handler that updates the markdown output based on the input text
def markdown_handler(self, name):
    if name.text:
        self.text = "Hi, **" + name.text + "**!"
    else:
        self.text = "No name"


# an input control
name = app.input(placeholder="What's your name?")

# a markdown output that greets the users using the given name
app.markdown(handler=markdown_handler, depends=[name])

# deploy the application with the name "controls/input" and print its URL
url = app.deploy("controls/input")
print(url)
