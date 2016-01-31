from lxml import html
import requests

page = requests.get('http://fmls.oxfordjournals.org/content/42/3/322.5.extract')
tree = html.fromstring(page.content)
