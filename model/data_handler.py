import pandas as pd


class DataHandler(object):
    def __init__(self, filename):
        self.setDataByFile(filename)
        self.tsdata = None
        self.train = None
        self.test = None
        self.outOfSample = None

    #
    # Sets the data for the class from the file.
    #
    def setDataByFile(self, filename):
        self.filename = filename
        if filename.endswith(".csv"):
            self.data = pd.read_csv(filename)
        else:
            self.data = pd.read_excel(filename)

    #
    # Returns a column of the dataframe based on header value.
    #
    def getColumnByHeader(self, header):
        return self.data.loc[:, self.data.columns == header]

    def getTSDataColumnByHeader(self, header):
        if self.tsdata is None:
            print("tsdata not set..")
            return None

        return self.tsdata.loc[:, self.data.columns == header].tolist()

    #
    # Converts the time series to a supervised learning problem
    # by creating a column that's "<lag> steps ahead".
    #
    def timeSeriesToSupervised(self, lag=1):
        df = pd.DataFrame(self.data)
        columns = [df.shift(i) for i in range(1, lag + 1)]
        columns.append(df)
        df = pd.concat(columns, axis=1)
        df.fillna(0, inplace=True)

        df.columns = ['DATE_LAG', 'TICKER_LAG', 'DATE', 'TICKER']
        self.tsdata = df

    def outsideTSToSupervised(self, data, lag=1):
        df = pd.DataFrame(data)
        columns = [df.shift(i) for i in range(1, lag + 1)]
        columns.append(df)
        df = pd.concat(columns, axis=1)
        df.fillna(0, inplace=True)

        return df

    #
    # Splits the data into train, test, and out of sample subsets.
    #
    def splitData(self, testSize, trainSize, outOfSampleSize):
        self.train = self.tsdata.values[:trainSize, :]
        self.test = self.tsdata.values[trainSize:(trainSize + testSize), :]
        self.outOfSample = self.tsdata.values[(trainSize + testSize):, :]

    #
    # Returns the train, test, and out of sample data set
    #
    def getDataSets(self):
        return self.train, self.test, self.outOfSample
