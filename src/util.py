import sys
import os
import shutil
from typing import List
from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.parse import urljoin
from bs4 import BeautifulSoup

def make_soup(url): 
    """
    returns soup representation of webpage
    """
    # get HTTPResponse into page
    page = urlopen(url)

    # read
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")

    # soup time
    return BeautifulSoup(html, "html5lib")

def make_folder(folder_name, main_folder_path) -> str:
    """
    create folder to store extracted info
    returns absolute path
    """
    path = os.path.join(main_folder_path, folder_name)
    if not os.path.isdir(path):
        os.mkdir(path)
    return path

def write_to_file(data, data_type, folder_path, folder_name) -> str:
    """
    Write links to file
    Specify images or page links through data_type
    returns absolute path
    """
    file_name = "{}_{}.txt".format(folder_name, data_type)
    file_total_path = os.path.join(folder_path, file_name)
    with open(file_total_path, "w") as f:
        for link in data:
            f.write(f"{link}\n")
    return file_total_path

def get_domain_links(tags, url) -> List[str]:
    """
    Returns all unique links within domain.
    """
    link_urls = []
    for href in tags:
        # merge paths
        link_url = href["href"]
        if link_url[0] == '/':
            full_link_url = urljoin(url,link_url)
            # record if unique
            if full_link_url not in link_urls:
                link_urls.append(full_link_url) 
    return link_urls

def get_img_links(domain_urls, main_url) -> List[str]:
    img_urls = []
    """
    return all images found in all domain urls
    """
    # get soup
    for url in domain_urls:
        soup = make_soup(url)
        # get images
        image_tags = soup.find_all("img")

        for img in image_tags:
            img_url = img["src"]
            # merge if relative path
            full_img_url = urljoin(main_url, img_url) if img_url[0] == '/' else img_url
            # record if unique
            if full_img_url not in img_urls:
                img_urls.append(full_img_url) 

    return img_urls