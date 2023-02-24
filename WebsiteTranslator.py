import asyncio
import os
from googletrans import Translator
from bs4 import BeautifulSoup,Comment

tr = {}

loop = asyncio.get_event_loop()

async def translate_content(content):
    translator = Translator()
    trans = await loop.run_in_executor(None, translator.translate, content, 'hi')
    tr[content] = trans.text

async def translate_html(html): 
    global soup
    soup = BeautifulSoup(html, 'html.parser')
    tasks = []
    for tag in soup.find_all():
        if  tag.name in ['script', 'style']:
            continue
        for content in tag.contents:
            if isinstance(content, str):
                if(content =='\n' or content == ' '):
                    continue
                if isinstance(content, Comment):
                    continue
                if(content in tr):
                    continue
                tasks.append(asyncio.ensure_future(translate_content(content)))
        if 'placeholder' in tag.attrs:
            placeholder = tag.attrs['placeholder']
            if isinstance(placeholder, str):
                if(placeholder in tr):
                    continue
                tasks.append(asyncio.ensure_future(translate_content(placeholder)))
        if 'title' in tag.attrs:
            title = tag.attrs['title']
            if isinstance(title, str):
                if(title in tr):
                    continue
                tasks.append(asyncio.ensure_future(translate_content(title)))
    await asyncio.gather(*tasks)

def OpenAndWriteHTML(HTMLfile):
    with open(HTMLfile, 'r', encoding='utf-8') as file:
        html = file.read() 
    loop.run_until_complete(translate_html(html))

    for tag in soup.find_all():
        if tag.name in ['script', 'style']:
            continue

        for content in tag.contents:
            if isinstance(content, str):
                if(content =='\n' or content == ' '):
                    continue
                if isinstance(content, Comment):
                    continue
                content.replace_with(tr[content])
        if tag.name == 'input' and 'placeholder' in tag.attrs:
            placeholder = tag.attrs['placeholder']
            if isinstance(placeholder, str):
                tag.attrs['placeholder'] = tr[placeholder]
        if 'title' in tag.attrs:
                title = tag.attrs['title']
                if isinstance(title, str):
                    tag.attrs['title'] = tr[title]

    fullpth = os.path.join("classcentralTranslated", os.path.dirname(HTMLfile))
    filepth =os.path.join(fullpth ,os.path.basename(HTMLfile))
    if not os.path.exists(fullpth):
        os.makedirs(fullpth)

    with open(filepth, 'w', encoding='utf-8') as file:
        file.write(str(soup))

for dirpath, dirnames, filenames in os.walk("classcentral"):
    for filename in filenames:
        file_path = os.path.join(dirpath, filename)
        OpenAndWriteHTML(file_path)
