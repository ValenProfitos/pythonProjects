#! pyhton3
# buscaCasa.py 

import requests, bs4, csv

# URL
url = 'https://clasificados.lavoz.com.ar/inmuebles/todo/?operacion=alquileres&provincia=cordoba&ciudad=cordoba&barrio[0]=villa-centenario'

try: # usamos try (y except) para manejar posibles errores durante la solicitud HTTP
    res = requests.get(url)
    res.raise_for_status() #Lanza una excepción si la solicitud no fue exitosa
except requests.exceptions.RequestException as e:
    print(f"Error making the request: {e}")
else:
    soup = bs4.BeautifulSoup(res.content, 'html.parser')

    listings = soup.find_all('a', class_='text-decoration-none')

    houses = []

    # Loop through each listing and extract data
    for listing in listings:

        link = listing['href']    

        title_tag = listing.find('h2', class_='bold mx0 mt0 pt1 mb1 col-12 title-2lines h4')
        title = title_tag.text.strip() if title_tag else 'N/A'

        price_tag = listing.find('span', class_='price')
        price = price_tag.text.strip() if price_tag else 'N/A'

        location_tag = listing.find('div', class_='h5 mx0 mt0 mb1 col-12 font-light title-1lines')
        location = location_tag.text.strip()  if location_tag else 'N/A'

        if title != 'N/A' and price != 'N/A' and location != 'N/A':
            houses.append({
            'title': title,
            'price': price,
            'location': location,
            'link': link
        })

    # Output the data (print or save to a CVS file)

    # Print the data
    for house in houses:
        print(f"Title: {house['title']}")
        print(f"Price: {house['price']}")
        print(f"Location: {house['location']}")
        print(f"Link: {house['link']}")
        print("-" * 40)

    # Save the data to a CSV file
    with open('houses.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldNames = ['title', 'price', 'location', 'link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldNames)

        writer.writeheader()
        for house in houses:
            writer.writerow(house)