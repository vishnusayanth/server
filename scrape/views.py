from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup
from server.config import NEWS_URL_TO_SCRAPE, NEWS_LINK
from server.classes import GoogleNewsContent
from server.classes import DjangoAppLogger
import traceback

logger = DjangoAppLogger(__name__)


def fetch_news(request):
    try:
        url = NEWS_URL_TO_SCRAPE
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        headlines = soup.find_all("article")
        items = []
        for headline in headlines:
            i = headline.find_all("a")[-1]
            if len(i.text)>20: # and 'Hindustan Times' in i.text:
                content = i.text.strip()
                images = headline.find_all('figure')
                # Images cannot be loaded since google blocked the usage of their images now.
                for img in images:
                    image = img.find('img')
                    image['src'] = NEWS_LINK[:-1] + image['src']
                    response = requests.head(image['src'], allow_redirects=True)
                    image['src'] = response.url
                    image['srcset'] = image['src']
                    # image['crossorigin'] = 'anonymous'
                link = NEWS_LINK + i['href']
                obj = GoogleNewsContent(content, link, str(image))
                items.append(obj.tojson())
        data = {'data': items}
        return JsonResponse(data)
    except Exception as ex:
        logger.write_to_console(str(ex),traceback, 'fetch google news.')
        request.session['message'] = str(ex)
        return None
