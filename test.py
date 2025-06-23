from data_cleanner import DataCleanner

data = DataCleanner("data/immoweb-dataset.csv")
df = data.load_data_file()
df = data.normalization()
print (df)

