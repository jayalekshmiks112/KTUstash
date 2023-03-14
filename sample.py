import typer
import requests
from bs4 import BeautifulSoup

app = typer.Typer()

url = 'https://www.keralanotes.com/p/ktu-study-materials.html?m=1#'
response = requests.get(url)

unique_links = set()

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    for link in soup.find_all('a', href=True):
        if "Notes" in link["href"] and "New-Scheme" in link["href"]:
            if link['href'] not in unique_links:
                unique_links.add(link['href'])
else:
    print('Error:', response.status_code)

@app.command()
def download_semester(semester: int = typer.prompt("Enter semester number")):
    semester_links = []
    for link in unique_links:
        if f'S{semester}' in link:
            semester_links.append(link)

    if len(semester_links) == 0:
        print(f"No study materials found for semester {semester}")
        return

    print(f"Study materials found for semester {semester}:")
    for i, link in enumerate(semester_links):
        print(f"{i+1}. {link}")
    selected_index = typer.prompt("Enter index of link to download")

    if not selected_index.isdigit() or int(selected_index) < 1 or int(selected_index) > len(semester_links):
        print("Invalid index")
        return

    selected_link = semester_links[int(selected_index)-1]

    response = requests.get(selected_link)
    html_content = response.content
    soup = BeautifulSoup(html_content, "html.parser")

    subject_links = []
    for link in soup.find_all('a', href=True):
        if "Subjects" in link.text and f"S{semester}" in link["href"]:
            subject_links.append(link)

    if len(subject_links) == 0:
        print(f"No subjects found for semester {semester}")
        return

    print(f"Subjects found for semester {semester}:")
    for i, link in enumerate(subject_links):
        print(f"{i+1}. {link.text}: {link['href']}")

    selected_index = typer.prompt("Enter index of subject to download")

    if not selected_index.isdigit() or int(selected_index) < 1 or int(selected_index) > len(subject_links):
        print("Invalid index")
        return

    selected_link = subject_links[int(selected_index)-1]["href"]
    response = requests.get(selected_link)
    html_content = response.content
    soup = BeautifulSoup(html_content, "html.parser")

    drive_links = []
    for link in soup.find_all('a', href=True):
        if 'drive.google.com' in link['href']:
            drive_links.append(link['href'])
            print(link)

    if len(drive_links) == 0:
        print("No study materials found for selected subject")
        return
"""
    print("Downloading study materials:")
    for i, link in enumerate(drive_links):
        file_id = link.split('/')[-2]
        download_url = f'https://drive.google.com/uc?id={file_id}'
        filename = f'S{semester}_{selected_link.split("/")[-2]}_{i}.pdf'
        response = requests.get(download_url)
        with open(filename, "wb") as f:
            f.write(response.content)
"""
if __name__ == "__main__":
    app()
