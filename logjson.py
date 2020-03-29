import sys
import json
import csv

def jsonify(filename):
    logFile = open(filename, 'r')
    result = {}
    index = 0
    for row in logFile:
        data = json.loads(row)
        result[str(index)] = data
        index += 1

    return json.dumps(result, indent=4)


if __name__ == "__main__":

    if len(sys.argv) == 3:
        logFilename = sys.argv[1]
        jsonFilename = sys.argv[2]
    else:
        print("Please provide a valid filename to process.")
        exit()
    
    logFile = open(logFilename, 'r')
    jsonFile = open(jsonFilename, 'w')

    result = {}

    index = 0
    for row in logFile:
        data = json.loads(row)
        result[str(index)] = data
        index += 1

    jsonFile.write(json.dumps(result, indent=4))
