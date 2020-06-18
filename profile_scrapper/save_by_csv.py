import csv
import requests

with open('프로필.csv', 'r') as raw:
    reader = csv.reader(raw)
    for lines in reader:
        print(lines)
        name = lines[0]
        img_data = requests.get(lines[2]).content
        if img_data:
            with open(f"{name}.jpg", 'wb') as handler:
                handler.write(img_data)
