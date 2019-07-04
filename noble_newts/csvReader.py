import csv

# Extracts the Average annual temprature and date values from a given spreadsheet,
# and returns the result as a dictionary  {Year: Temp}


def gsoy_data(path):
    tempData = {}
    # confirms that the given .csv file contains the TAVG value by checking if
    # it is in the Temp_Data file
    with open(path, newline='') as csvfile:
        rowList = [row for row in csv.reader(csvfile)]
        tempIndex = rowList[0].index('TAVG')
        dateIndex = rowList[0].index('DATE')
        for line in rowList[1:]:
            if line[tempIndex] != '':
                tempData.update({int(line[dateIndex]): float(line[tempIndex])})
        return tempData
    

def monthly_data(path):
    tempData = {}
    with open(path, newline='') as csvfile:
        rowList = [row for row in csv.reader(csvfile)]
        tempIndex = rowList[0].index('TAVG')
        dateIndex = rowList[0].index('DATE')
        for line in rowList[1:]:
            if line[tempIndex] != '':
                tempData.update({line[dateIndex]: float(line[tempIndex])})
        return tempData

def getdata(file):
    final = {}
    month_data = gsom_data('gsom-latest/' + file)
    year_data = gsoy_data('gsoy-latest/' + file)
    last = sorted([list(month_data.keys())[0], list(year_data.keys())[0]])[0]
    first = sorted([list(month_data.keys())[-1], list(year_data.keys())[-1]])[1]
    for i in range(last, first + 1):
        if year_data.get(i) and month_data.get(i):
            val = (month_data.get(i) + year_data.get(i)) / 2
            final.update({i: val})
        elif year_data.get(i):
            final.update({i: year_data.get(i)})
        elif month_data.get(i):
            final.update({i: month_data.get(i)})
    print(len(list(final.values())), len(list(month_data.values())), len(list(year_data.values())))
    return final


def merge_set(set1, set2):
    final = {}
    last = sorted([list(set1.keys())[0], list(set2.keys())[0]])[0]
    first = sorted([list(set1.keys())[-1], list(set2.keys())[-1]])[1]
    if type(last) == str:
        last = int(last.split('-')[0])
        first = int(first.split('-')[0])
    print(last, first)
    for year in range(last, first):
        for month in range(1, 13):
            if len(str(month)) <= 1:
                month = f'0{month}'
            date = f'{year}-{month}'
            if set1.get(date) and set2.get(date):
                val = round((set1.get(date) + set2.get(date)) / 2, 2)
                final.update({date: val})
            elif set1.get(date):
                final.update({date: set1.get(date)})
            elif set2.get(date):
                final.update({date: set2.get(date)})
    return final
