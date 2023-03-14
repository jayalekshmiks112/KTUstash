import requests
from bs4 import BeautifulSoup
import gdown
import os
import subprocess

url ="https://www.keralanotes.com/2022/06/KTU-S6-Compiler-Design-Notes.html#"

response=requests.get(url)
html_content=response.content

soup=BeautifulSoup(html_content,"html.parser")

drive_links=[]
output_dir = os.path.join(os.path.expanduser("~"), "Desktop", "KTU Study Materials")
os.makedirs(output_dir, exist_ok=True)

for link in soup.find_all('a',href=True):
    if 'drive.google.com' in link['href']:
        drive_links.append(link['href'])
        
for i, link in enumerate(drive_links):
    file_id = link.split('/')[-2]
    download_url = f'https://drive.google.com/uc?id={file_id}'
    filename = os.path.join(output_dir, f'{i}.pdf')
    gdown.download(download_url, filename, quiet=False)
"""
filepath=os.path.abspath(filename)
#subprocess.call(['open',filepath])
os.startfile(filepath)
"""
for filename in os.listdir(output_dir):
    if filename.endswith(".pdf"):
        filepath = os.path.join(output_dir, filename)
        subprocess.call(["open", filepath])