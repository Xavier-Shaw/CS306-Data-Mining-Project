import numpy as np
import pandas as pd
import json

df = pd.read_csv("bus_path.csv")

df['next_lng'] = df['lng'].shift(-1).where(df['names'] == df['names'].shift(-1))
df['next_lat'] = df['lat'].shift(-1).where(df['names'] == df['names'].shift(-1))
df

def row_to_json(row):
    data = {'start': row[['lng', 'lat']].values.tolist(), 'end': row[['next_lng', 'next_lat']].values.tolist(), 'name': row['names']}
    return json.dumps(data, cls=NpEncoder)

# Define the output file path
output_file = 'bus_path.json'
df = df.dropna()
# Convert the grouped_data_serializable array to JSON format
data = df.apply(row_to_json, axis=1).where(~pd.isnull(df['next_lat']))

# 将数据转换为JSON格式并写入文件
with open(output_file, 'w') as file:
    json.dump(list(data), file)

print(f"Data successfully written to '{output_file}'.")
