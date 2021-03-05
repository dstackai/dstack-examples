import dstack as ds

# Create an instance of the application that has three columns
app = ds.app(columns=3)

# An input that takes one column and one row
input_1 = app.input(label="Input 1", colspan=1)
# An input that takes one column and one row
input_2 = app.input(label="Input 2", colspan=1)
# An input that takes one column and two rows
input_3 = app.input(label="Input 3", colspan=1, rowspan=2)

url = app.deploy("layout_1")
print(url)
