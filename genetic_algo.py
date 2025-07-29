import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tpot import TPOTClassifier

# load the data
telescope = pd.read_csv('telescope_data.csv')
telescope.columns = telescope.columns.str.strip()  # ensure clean column names
print(telescope.columns)

# clean the data
tele = telescope.sample(frac=1).reset_index(drop=True)

"""telescope_shuffle = telescope.iloc[np.random.permutation(len(telescope))]
tele = telescope_shuffle.reset_index(drop=True)"""

# store 2 classes
tele['class'] = tele['class'].map({'g':0, 'h':1})
tele_class = tele['class'].values

# split training, tresting and validation
training_indices, validation_indices = train_test_split(
	tele.index,
	stratify=tele_class,
	train_size=0.75, 
	test_size=0.25
	)

# let Genetic Programming find best ML model and hypermarameters
tpot = TPOTClassifier(generations=5, verbosity=2)
tpot.fit(tele.drop('class', axis=1).loc[training_indices].values, tele.loc[training_indices, 'class'].values)

# score the accuracy
#tpot.score(tele.drop('class', axis=1).loc[validation_indices.values], tele.loc[validation_indices, 'class'].values)
print("Accuracy:", tpot.score(
    tele.drop('class', axis=1).loc[validation_indices].values,
    tele.loc[validation_indices, 'class'].values))


# export the generated code
tpot.export('pipeline.py')