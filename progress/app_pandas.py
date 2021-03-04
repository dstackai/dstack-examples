import pandas as pd
import numpy as np
import dstack as ds

from dstack import tqdm

app = ds.app()


def output_handler(self):
    tqdm.pandas()
    df = pd.DataFrame(np.random.randint(0, int(1e8), (10000, 1000)))
    self.data = df.groupby(0).progress_apply(lambda x: x ** 2).head(100)


app.output(handler=output_handler)

result = app.deploy("tqdm_pandas")
print(result.url)