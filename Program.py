
countries = []
completedCountries = {}
day = 0



class Country:#клас, який уособлює країну

    def __init__(self, name, xb, yb, xe, ye):#ініціалізація атрибутів країни
        self.name = name
        self.xb = int(xb)
        self.yb = int(yb)
        self.xe = int(xe)
        self.ye = int(ye)
        self.cities = []
        self.completed = False
        self.connected = False

    def setCities(self):#створення записів про міста країни
        for y in range(self.yb, self.ye + 1):
            for x in range(self.xb, self.xe + 1):
                self.cities.append(City(x, y, self.name, countries))

    def Day(self):# ємуляція денного існування країни
        for city in self.cities:
            city.Day()

    def beCompleted(self):#встановлює статус країни, як завершений, якщо її кожне місто завершене
        for city in self.cities:
            if not city.beCompleted():
                return False
        self.completed = True

    def Update(self):#оновлює інформацію про місто після денного існування
        for city in self.cities:
            city.Update()

class City:#

    def __init__(self, x, y, country, valutesNames):#ініціалізація атрибутів міста
        self.x = x
        self.y = y
        self.country = country
        self.valutes = {}
        self.previousValutes = {}

        for valute in valutesNames:#
            if valute.name == country:
                self.previousValutes[country] = 1000000
                self.valutes[country] = 1000000
            else:
                self.previousValutes[valute.name] = 0
                self.valutes[valute.name] = 0

    def Exist(self, x, y):#перевіряє, чи існує місто з даними координатами
        for country in countries:
            for city in country.cities:
                if city.x == x and city.y == y:
                    return city
        return None

    def toN(self):#надсилає гроші місту, яке знаходиться на півночі, якщо воно існує
        city = self.Exist(self.x, self.y + 1)
        self.Send(city)

    def toS(self):#надсилає гроші місту, яке знаходиться на півдні, якщо воно існує
        city = self.Exist(self.x, self.y - 1)
        self.Send(city)


    def toW(self):#надсилає гроші місту, яке знаходиться на заході, якщо воно існує
        city = self.Exist(self.x - 1, self.y)
        self.Send(city)


    def toE(self):#надсилає гроші місту, яке знаходиться на сході, якщо воно існує
        city = self.Exist(self.x + 1, self.y)
        self.Send(city)
        #if city:#

    def Send(self, city):#надсилає гроші місту
        if city:
            for country in self.valutes.keys():
                city.valutes[country] += int(self.previousValutes[country] / 1000)
                self.previousValutes[country] -= int(self.previousValutes[country] / 1000)

    def Day(self):#ємулює процес денного проживання міста
        self.toN()
        self.toS()
        self.toW()
        self.toE()

    def Update(self):#оновлює дані про місто
        self.previousValutes = self.valutes

    def beCompleted(self):#перевіряє, чи є місто завершеним
        for valute in self.valutes.keys():
            if self.valutes[valute] < 1:
                return False
        return True


def CheckInput():#перевіряє правильність введених даних
    info = input()
    infoWords = info.split(' ')
    count = len(infoWords)
    if count != 5:
        return None
    name = infoWords[0]
    infoWordsDict = {'name': name}
    infoWordsDict['xb'] = int(infoWords[1])
    infoWordsDict['yb'] = int(infoWords[2])
    infoWordsDict['xe'] = int(infoWords[3])
    infoWordsDict['ye'] = int(infoWords[4])


    return infoWordsDict

def CheckRange(number):
    return int(number) >= 1 and int(number) <= 10

def CheckPoints(xb, yb, xe, ye):
    return xb <= xe and yb <= ye

def CountryExist(countryName):
    for country in countries:
        if country.name == countryName:
            return True
    return False

def Input(count):
    global countries, completedCountries, day
    countries = []
    completedCountries = {}
    day = 0
    position = 0
    while position < count:
        info = []
        try:
            info = CheckInput()
        except Exception as e:
            print("Дані введено неправильно")
            continue
        if not info:
            print("Дані введено неправильно")
            continue
        elif CountryExist(info['name']):
            print("Країна вже існує")
            continue
        elif CheckInfo(info):
            print("Невалідні координати")
            continue
        countries.append(Country(info['name'], info['xb'], info['yb'], info['xe'], info['ye']))
        position += 1

def CheckInfo(info):
    if not Free(info['xb'], info['yb'], info['xe'], info['ye']) or not CheckRange(info['xb']) \
    or not CheckRange(info['yb']) or not CheckRange(info['xe']) or not CheckRange(info['ye']) \
    or not CheckPoints(info['xb'], info['yb'], info['xe'], info['ye']):
        return True
    return False

def Set():#створює дані про міста країни
    for country in countries:
        country.setCities()


def Complete():#імітує процес існування країн до того моменту, поки всі вони не побувають завершеними
    length = len(countries)
    while length != len(completedCountries.keys()):
        Day()

def Check():#перевіряє країни на рахунок їх завершеності
    global day
    for country in countries:
        if country not in completedCountries.keys():
            if country.completed:
                completedCountries[country] = day

def Day():#емулює проживання країнами одного дня
    global day
    day += 1
    for country in countries:
            country.Day()
            country.Update()
            country.beCompleted()
            Check()


def SortName(country):
    return country.name

def SortDays(country):
    return completedCountries[country]

def ShowCompleted():#виводить результат обчислення кількості днів
    l = list(completedCountries)
    l.sort(key=SortName)
    l.sort(key=SortDays)
    for country in l:
        print(country.name + ' ' + str(completedCountries[country]))


def Program():
    count = 0
    while True:
        try:
            count = int(input())
        except Exception as e:
            print("Неправильно введене число")
            continue
        if not count:
            break
        else:
            Input(count)
            Set()
            if not checkConnections():
                print("Порушений порядок зв'язаності міст ")
                continue
            Complete()
            ShowCompleted()

def Free(xb, yb, xe, ye):#перевіряє, чи вільні координати, на які претендує нова країна
    for country in countries:
        if CheckLL(country, xb, yb, xe, ye) or CheckLU(country, xb, yb, xe, ye) or CheckRL(country, xb, yb, xe, ye) or CheckRU(country, xb, yb, xe, ye):
            return False
    return True

def CheckLL(country, xb, yb, xe, ye):#перевіряє, чи вільне місце за лівою нижньою координатою
    if (xb >= country.xb and xb <= country.xe and yb >= country.yb and yb <= country.ye):
        return True

def CheckLU(country, xb, yb, xe, ye):#перевіряє, чи вільне місце за лівою верньою координатою
    if (xb >= country.xb and xb <= country.xe and ye >= country.yb and ye <= country.ye):
        return True

def CheckRL(country, xb, yb, xe, ye):# перевіряє, чи вільне місце за правою нижньою координатою країни
    if (yb >= country.yb and yb <= country.ye and xe >= country.xb and xe <= country.xe):
        return True

def CheckRU(country, xb, yb, xe, ye):# перевіряє, чи вільне місце за правою верхньою координатою країни
    if (ye >= country.yb and ye <= country.ye and xe >= country.xb and xe <= country.xe):
        return True

def checkConnections():
    count = 1
    length = len(countries)
    while count < length:
        countriesTemp = countries[: count+1]
        country = countriesTemp[count]
        connected = CheckNear(country, countriesTemp)
        if not connected:
           return False
        count += 1
    return True

def CheckNear(country, countriesTemp):
    for city in country.cities:
        s = city.Exist(city.x, city.y - 1)
        w = city.Exist(city.x - 1, city.y)
        e = city.Exist(city.x + 1, city.y)
        n = city.Exist(city.x, city.y + 1)
        cities = [n, e, s, w]
        for country in countriesTemp:
            name = country.name
            if name == city.country:
                continue
            connected = CityFound(cities, name)
            if connected:
                return True
    return False


def CityFound (cities, name):
    connected = False
    for c in cities:
        if c:
            if c.country == name:
                return True
    return False

if __name__ == '__main__':
    Program()
