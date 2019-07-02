import csv

# Extracts the Average annual temprature and date values from a given spreadsheet,
# and returns the result as a dictionary  {Year: Temp}


def getData(path):
    tempData = {}
    # confirms that the given .csv file contains the TAVG value by checking if
    # it is in the Temp_Data file
    if path.split('/')[-1] in ''.join(open('Temp_Data.txt', 'r').readlines()):
        with open(path, newline='') as csvfile:
            rowList = [row for row in csv.reader(csvfile)]
            tempIndex = rowList[0].index('TAVG')
            dateIndex = rowList[0].index('DATE')
            for line in rowList[1:]:
                if line[tempIndex] != '':
                    tempData.update({line[dateIndex]: float(line[tempIndex])})
        return tempData
    return None
