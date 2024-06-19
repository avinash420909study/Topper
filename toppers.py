from flask import Flask
from flask import render_template
import requests
import csv
from io import StringIO

app=Flask(__name__)
app.secret_key="secretkey"


sheet_url = "https://docs.google.com/spreadsheets/export?id=1fiShF6Waa6S31btnlkwT2fzQQN0EHmP5NNvO8XU9PmE&exportFormat=csv&gid=1825414532"

# Open the Google Sheet by its URL
response = requests.get(sheet_url)
response.raise_for_status()

csv_content = response.text
csv_data = StringIO(csv_content)
reader = csv.DictReader(csv_data)

# Extract headers
column_headers = reader.fieldnames

# Convert CSV rows to a list of dictionaries
data = [row for row in reader]

# print(column_headers)

@app.route('/')
def index():
    data_dict = {}
    # Iterate over each row in the data
    for row in data:
        level = row['Level']
        category = row['Category']
        year = row['Year']
        

        if year not in data_dict:
            data_dict[year] = {}
            data_dict[year][level]=[category]
        elif level not in data_dict[year]:
            data_dict[year][level]=[category]
        elif category not in data_dict[year][level]:
            data_dict[year][level].append(category)
        
        
    return render_template('toppers_landing.html', data=data_dict)


@app.route('/<int:year>/<level>/<category>')
def toppers(year, level, category=None):
    
    toppers_data = [] #Main content list

    data_dict={} #navbar content
    for row in data:
        data_level = row['Level']
        data_category = row['Category']
        data_year = row['Year']
        
        # Fetching data from GSheet to navbar
        if data_year not in data_dict:
            data_dict[data_year] = {}
            data_dict[data_year][data_level]=[data_category]
        elif data_level not in data_dict[data_year]:
            data_dict[data_year][data_level]=[data_category]
        elif data_category not in data_dict[data_year][data_level]:
            data_dict[data_year][data_level].append(data_category)

        # Fetching data for the main card content
        if (row['Year'],row['Level'],row['Category']) == (str(year),level,category):
            _={}
            for column in column_headers[3:]:
                _[column] = row[column]
            toppers_data.append(_)


    return render_template('toppers.html', 
                           data=toppers_data, 
                           year=year, 
                           level=level,
                           category = category, 
                           navbar_data = data_dict, 
                           desc = {'Highest CGPA': 'Toppers in the level', 'Certificate of Academic Distinction': 'CGPA > 9.5', 'Certificate of Merit':'CGPA > 9.0'})

if __name__=='__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)
