from collections import OrderedDict
import csv
from dateutil.parser import parse
import datetime,time
import csv

from collections import OrderedDict

class DataFrame(object):
    @classmethod
    def from_csv(cls,path):
        with open(path,'rU') as f:
            reader =csv.reader(f,delimiter=',',quotechar='"')
            data = []
            for row in reader:
                data.append(row)
        return cls(data)

    def DupHeader(self,iterable):
        a = set()
        for item in iterable:
            if item not in a:
                a.add(item)
            else:
                raise Exception('Duplicate value found')
                break

    def __init__(self,list_of_lists,header=True):
        if header:
            self.data = list_of_lists[1:]
            self.header = list_of_lists[0]
            # ============task 1============
            self.DupHeader(self.header)
            #if len(set(self.header)) != len(self.header):
                #raise Exception('duplicates found')
        else:
            self.header = ['column' + str(i+1) for i in range(len(list_of_lists[0]))]
            self.data = list_of_lists
        # ============task 2============
        self.data = [map(lambda x:x.strip(),row) for row in self.data]
        self.data = [OrderedDict(zip(self.header,row)) for row in self.data]


    def __getitem__(self, item):
        if isinstance(item,(int,slice)):
            return self.data[item]

        elif isinstance(item,str):
            return [row[item] for row in self.data]

        elif isinstance(item,tuple):
            if isinstance(item[0],list) or isinstance(item[1],list):
                if isinstance(item[0],list):
                    rowz = [row for index,row in enumerate(self.data) if index in item[0]]
                else:
                    rowz = self.data[item[0]]

                if isinstance(item[1],list):
                    if all([isinstance(i,int) for i in item[1]]):
                        # python3 use values(),keys(),items() instead of itervalues()...
                        return [[column_value for index,column_value in enumerate(row.values()) if index in item[1]] for row in rowz]
                    elif all([isinstance(i,str) for i in item[1]]):
                        return [[row[col] for col in item[1]] for row in rowz]
                    else:
                        raise TypeError('type error')

                else:
                    return rowz[item[1]]

            else:
                if isinstance(item[0],(int,slice)) and isinstance(item[1],(int,slice)):
                    # python3 use values(),keys(),items() instead of itervalues()...
                    return [list(row.values())[item[1]] for row in self.data[item[0]]]
                elif isinstance(item[1],str):
                    return [row[item[1]] for row in self.data[item[0]]]
                else:
                    raise TypeError('type error')

        elif isinstance(item,list):
             return [[ value for key ,value in row.items() if key in item] for row in self.data]

    # ============task 3============
    def transform_type(self,col_name):
        is_time = 0
        try:
            # try if col is numeric
            nums = [float(row[col_name].replace(',','')) for row in self.data]
            return nums, 1 if is_time else 0
        except:
            try:
                # if not numeric, is time?
                nums = [parse(row[col_name].replace(',','')) for row in self.data]
                # transform to seconds
                nums= [time.mktime(num.timetuple()) for num in nums]
                is_time = 1
                return nums, 1 if is_time else 0
            except:
                raise TypeError('text values cannot be calculated')


    def min(self,col_name):
        nums ,is_time= self.transform_type(col_name)
        rslt = min(nums)
        return datetime.datetime.fromtimestamp(rslt) if is_time else rslt

    def max(self,col_name):
        nums, is_time = self.transform_type(col_name)
        rslt = max(nums)
        return datetime.datetime.fromtimestamp(rslt) if is_time else rslt

    def median(self,col_name):
        nums, is_time = self.transform_type(col_name)
        nums = sorted(nums)
        center = int(len(nums) / 2)
        if len(nums) % 2 == 0:
            rslt = sum(nums[center - 1:center + 1]) / 2.0
            return datetime.datetime.fromtimestamp(rslt) if is_time else rslt
        else:
            rslt = nums[center]
            return datetime.datetime.fromtimestamp(rslt) if is_time else rslt

    def mean(self,col_name):
        nums, is_time = self.transform_type(col_name)
        rslt = sum(nums)/len(nums)
        return datetime.datetime.fromtimestamp(rslt) if is_time else rslt

    # sum/std of time make more sense when in the format of seconds so I won't transform to Y-M-D H-M format
    def sum(self,col_name):
        nums,is_time = self.transform_type(col_name)
        return sum(nums)

    def std(self,col_name):
        nums ,is_time = self.transform_type(col_name)
        mean = sum(nums)/len(nums)
        return (sum([(num-mean)**2 for num in nums])/len(nums))**0.5

    def get_rows_where_column_has_value(self, column_name, value, index_only=False):
        if index_only:
            return [index for index, row_value in enumerate(self[column_name]) if row_value==value]
        else:
            return [row for row in self.data if row[column_name]==value]


    # ============task 4==============
    def add_rows(self,list_of_lists):
        col_count = len(self.header)
        # check the length of every new added row equals to len(header)
        if sum([len(row) == col_count for row in list_of_lists]) == len(list_of_lists):
            self.data = self.data + [OrderedDict(zip(self.header, row)) for row in list_of_lists]
            return self
        else:
            raise Exception('incorrect number of columns')




infile = open('SalesJan2009.csv')
lines = infile.readlines()
lines = lines[0].split('\r')
data = [l.split(',') for l in lines]
things = lines[559].split('"')
data[559] = things[0].split(',')[:-1] + [things[1]] + things[-1].split(',')[1:]
df = DataFrame(list_of_lists=data)
print df.min('Price')

df.add_rows([['1/5/09 4:10', 'Product1', '1200', 'Mastercard', 'Nicola', 'Roodepoort', 'Gauteng', 'South Africa', '1/5/09 2:33', '1/7/09 5:13', '-26.1666667', '27.8666667']])
print df.data[998]

