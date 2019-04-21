import re
import os
import bs4
import requests
import tqdm

pages = [str(i+1) for i in range(10)]
image_urls = []
out_dir = "/mnt/c/Temp/galaxy"
prefix = "https://cdn.spacetelescope.org/archives/images/screen/"
postfix = ".jpg"


for page in pages:
    url = "https://spacetelescope.org/images/viewall/page/" + page

    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.content, 'html.parser')
    data = str(soup.script)

    search = "id: '(.*)',\\n"
    re_search = re.finditer(search, data)
    ids = [m.group(1) for m in re_search]

    image_urls.extend([(prefix + id + postfix, id) for id in ids])

for im, id in tqdm.tqdm(image_urls):
    r = requests.get(im)

    filepath = os.path.join(out_dir, id + ".jpg")

    with open(filepath, 'wb') as out_file:
        out_file.write(r.content)
