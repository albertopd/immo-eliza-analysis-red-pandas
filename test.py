from data_cleanner import DataCleanner
data = DataCleanner("data/test.csv")

df = data.load_data_file()

"""df=data.clean_errors()
data.send_output_file("data/test.csv")

"""
print (df.value_counts("type"), df.value_counts("subtype"))