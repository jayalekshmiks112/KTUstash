import typer
import requests
from bs4 import BeautifulSoup
import gdown
import os
import re

app = typer.Typer()

url = 'https://www.keralanotes.com/p/ktu-study-materials.html?m=1#'
response = requests.get(url)

unique_links = set()

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    for link2 in soup.find_all('a', href=True):
        if "Notes" in link2["href"] and "New-Scheme" in link2["href"]:
            if link2['href'] not in unique_links:
                unique_links.add(link2['href'])
        
else:
    print('Error:', response.status_code)

@app.command()
def downloadall(semester: int = typer.prompt("Enter semester number(1-6)")):
    for link1 in unique_links:
        if f'S{semester}' in link1:
            if semester!=4:
                link1="https://www.keralanotes.com"+link1
            else:
                link1=link1
            url1 = link1   
            response = requests.get(url1)
            html_content = response.content
            soup = BeautifulSoup(html_content, "html.parser")

            sub={}
            index =1
            for link in soup.find_all("a", href=True):
                if re.match(r"(CST|HUT)", link.text) and link["href"]:
                    sub[index]=link['href']
                    index+=1
            sub1={}
            for i, link in enumerate(sub.values()):
                if f'S{semester}-' in link:
                    sub_code = link.split(f'S{semester}-')[1].split('/')[0]
                    if '.html' in sub_code:
                        sub1[i]=sub_code.split('.html')[0]
                        print(f"{i+1}: {sub1[i]}")
            
            n = int(input("Enter the index"))
            url2 = sub[n]
            response = requests.get(url2)
            html_content = response.content
            soup = BeautifulSoup(html_content, "html.parser")

            drive_links=[]
            output_dir = os.path.join(os.path.expanduser("~"), "Desktop", "KTU Study Materials")
            semester_dir = os.path.join(output_dir, f"Semester {semester}")
            subject_dir = os.path.join(semester_dir, sub1[n-1])
            os.makedirs(subject_dir, exist_ok=True)


            for link in soup.find_all('a', href=True):
                if 'drive.google.com' in link['href']:
                    drive_links.append(link['href'])

            for link in drive_links:
                file_id = link.split('/')[-2]
                url = f'https://drive.google.com/uc?id={file_id}'
                response = requests.get(url, stream=True)
                file_name = ''
                content_disposition = response.headers.get('Content-Disposition')
                if content_disposition:
                    file_name = re.findall("filename=(.+)", content_disposition)[0]
                    file_name = re.sub(r'[\\/*?:"<>|]', '', file_name)  
                else:
                    file_name = file_id + '.pdf'
                file_path = os.path.join(subject_dir, file_name)
                with open(file_path, 'wb') as f:
                    f.write(response.content)


if __name__ == "__main__":
    app()  
