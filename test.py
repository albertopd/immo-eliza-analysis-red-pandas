from data_cleanner import DataCleanner

data = DataCleanner("data/immoweb-dataset.csv")
df = data.clean_errors()
print (df.describe())
#df = data.normalization()


