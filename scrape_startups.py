import requests
from bs4 import BeautifulSoup
import pandas as pd
from loguru import logger

url = "https://startit-x.com/index.php/actions/sprig-core/components/render"
page_number = 1  
startups_data = []
max_pages = 1  # Inicializamos en 1 para empezar la primera solicitud

# Parámetros comunes de solicitud
params = {
    "year[]": "2024",
    "search": "",
    "sprig:siteId": "9a161aa43461156175c50380f7e86fc1dd31bf173298b8309d921801a95076cf6",
    "sprig:id": "d490141b64de3eb5fd1db82ac07c001d3946faad1615ac315aafc6dec9a55873component-felgcc",
    "sprig:component": "ed6eb618b6d137da76401390928836d3316af8e3ca8be2812ce743ae947d3225",
    "sprig:template": "3fb4a808a4a72aee44e7c2d7812ef6bad78a4bc567bc2cc8e808a990cf2754da_partials/sprig/overview",
    "sprig:variables[overviewLayout]": "7806c98b96c38cff3fd438acc7b9ff42939cb97a4712fdd01505e49d99006a5agrid",
    "sprig:variables[overviewType]": "e559f44364fc32291720cc9820cf7fa4c95d8ab5d28573970c4a7fd38b4ec7ceclients",
    "sprig:variables[categories]": "732c2b9e36a902ec784914c91ffdaa427d2c11293480372cc44dcfebce1f7722[149005,149560,149007,148914,148946,149588,148915,149387,149218,149241,148939,149354,149474,148996,148942,148978,148960,148956,149070,148944,148936,148918,148962,148985,149289,148929,149401,148989,148933,149058,149449,149025,148913,148952,148973,148969,148911,149029,149021,148923,149113,148916,149595,149022,149028,148909,149407,149017,148920,148935,148950,148926,149468,149186,149010,149190,148976]",
    "sprig:variables[limit]": "b0850e6ffadcc2690b3c6bfe78786aa97bcef57e3e8a0b4fe3f4477fe9be46e720",
    "sprig:variables[entryId]": "2fddb0c55035ff4f7ba0336c51a4a12a510174d0b521917a1bd835a1a927079545458"
}

# Primera solicitud para obtener el número total de páginas
response = requests.get(url, params={**params, "page": page_number}, headers={"User-Agent": "Mozilla/5.0"})
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    pagination = soup.find("nav", class_="Nav Nav--pagination")
    if pagination:
        nav_list = pagination.find("ul", class_="Nav-list")
        if nav_list:
            nav_items = nav_list.find_all("li", class_="Nav_item")
            for item in reversed(nav_items):
                link_tag = item.find("a", class_="Nav-link")
                if link_tag and link_tag.text.isdigit():
                    max_pages = int(link_tag.text)
                    break
            logger.info(f"Total de paginasenco ntrado: {max_pages}")
        else:
            logger.error("No se encontro el elemento 'ul' con clase 'Nav_list'")
    else:
        logger.error("No se encontro el elemento 'nav' con clase 'Nav Nav--pagination'")    
else:
    logger.error("No se pudo obtener el total de páginas. Revisar el código o conexión.")

# Iniciar scraping de las páginas encontradas
while page_number <= max_pages:
    logger.info(f"Obteniendo data de página {page_number}")
    response = requests.get(url, params={**params, "page": page_number}, headers={"User-Agent": "Mozilla/5.0"})

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        startups_container = soup.find_all("div", class_="CardWrapper CardWrapper--clients")

        for card_wrapper in startups_container:
            card_body = card_wrapper.find_all("div", class_="Card Card--clients")

            for body in card_body:
                startup = body.find("div", class_="Card-body")

                if startup:
                    # Obtener el nombre de la startup
                    name_element = startup.find("h3", class_="Card-title")
                    name = name_element.text.strip() if name_element else "N/A"

                    # Obtener el año y las industrias
                    meta_div = startup.find("div", class_="Card-meta")
                    if meta_div:
                        year_element = meta_div.find("span", class_="Card-year")
                        year = year_element.text.strip() if year_element else "N/A"
                        industries = [industry.text.strip() for industry in meta_div.find_all("span", class_="Card-industry")] if meta_div.find_all("span", class_="Card-industry") else []
                    else:
                        year = "N/A"
                        industries = []

                    # Obtener enlaces de redes sociales
                    social_links = []
                    social_section = startup.find("ul", class_="Card-socials")
                    if social_section:
                        social_items = social_section.find_all("li", class_="Card-socialsItem")
                        for item in social_items:
                            link_tag = item.find("a", class_="Card-socialsLink", href=True)
                            if link_tag:
                                link = link_tag["href"]
                                social_links.append(link)

                    # Agregar los datos recolectados
                    startups_data.append({
                        "Name": name,
                        "Year": year,
                        "Industries": industries,
                        "Social Links": social_links
                    })

        logger.info(f"Página {page_number} completa.")
        page_number += 1
    else:
        logger.error(f"Fallo al obtener la página {page_number}. Estado: {response.status_code}")
        break  

# Guardar los datos en un CSV
df_startups = pd.DataFrame(startups_data)
df_startups.to_csv("startups_2024.csv", index=False)
logger.info("Los datos se han guardado en 'startups2_2024.csv'.")
