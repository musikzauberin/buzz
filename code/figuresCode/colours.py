"""Testing colours"""

import numpy as np
import seaborn as sns
import matplotlib.pyplot as pl



sns.set(rc={"figure.figsize": (6, 6)})
np.random.seed(sum(map(ord, "palettes")))

sns.palplot(sns.color_palette("cubehelix_r", 8))

pl.show()