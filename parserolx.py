import matplotlib.pyplot as plt, requests, csv, re
from requests import get
from bs4 import BeautifulSoup

with open('rynok.csv', 'w', encoding='utf-8', newline='') as f:
    csvw = csv.writer(f)
    csvw.writerow(['No.','Title','Price','Year'])

def writecsv(count, title, price, year):
    with open('rynok.csv', 'a', encoding='utf-8', newline='') as f:
            csvw = csv.writer(f)
            csvw.writerow([count, title, price, year])

def extractdata(item):
    title = item.find('h6', class_='css-16v5mdi er34gjf0').text.strip()
    price = item.find('p', class_='css-10b0gli er34gjf0').text.strip()
    year = item.find('div', class_='css-efx9z5')

    if year:
        year = year.text.strip()
    else:
        year = "Year not specified"

    price = re.sub(r'[^0-9]', '', price)

    if price:
        price = int(price)
    else:
        price = None

    year = year[:4]
    return title, price, year

def process(count, soup):
    machina = soup.find_all('div', class_='css-qfzx1y')

    while count <= PAGES:
        for item in machina:
            title, price, year = extractdata(item)

            writecsv(count, title, price, year)

            count += 1

            years.append(int(year))
            prices.append(price)

            print(f'Car No. {count}')
            print(f'Title: {title}')
            print(f'Price: {price}')
            print(f'Year: {year}' + '\n')

def main():
    count = 0
    try:
        url = f'{URL}?page={count}'
        response = get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        process(count, soup)
    except requests.exceptions.RequestException as e:
        print(f"An error occured when requested {url}: {e}")
    except Exception as e:
        print(f"Oops... Something goes wrong...: {e}")

    years.sort()

def makegraph():
    plt.plot(years,prices)
    plt.title('Car prices depending on the year of manufacture')
    plt.xlabel('Years')
    plt.ylabel('Prices, UAH')

    def price_formatter(x, pos):
        if x >= 1e6:
            return f'{int(x / 1e6)}.{int((x % 1e6) / 1e3)} millions'
        else:
            return f'{int(x / 1e3)} thousands'
        
    formatter = price_formatter
    ax = plt.gca()
    ax.get_yaxis().set_major_formatter(formatter)


    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    years = []
    prices = []
    URL = 'https://www.olx.ua/uk/transport/legkovye-avtomobili/'
    PAGES = 300
    main()
    makegraph()