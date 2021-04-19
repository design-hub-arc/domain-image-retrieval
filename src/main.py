import sys, os
from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import util
import arguments

if __name__ == "__main__":

    args = arguments.make_args()
    main_url = args.url

    # check if credentials needed
    if args.login:
        print("logging in")

    # get domain
    domain = urlparse(main_url).netloc
    scheme = urlparse(main_url).scheme

    # make soup
    soup = util.make_soup(main_url)

    # get href links
    link_tags = soup.find_all("a")

    # create main output if not existing
    main_folder_path = os.path.join(os.getcwd(), "domains")
    if not os.path.isdir(main_folder_path):
        os.mkdir(main_folder_path)

    # create instance folder
    folder_name = "{}".format(domain.replace(".","-"))
    folder_path = util.make_folder(folder_name, main_folder_path)

    # write domain links to file
    domain_urls = util.get_domain_links(link_tags, main_url)
    util.write_to_file(domain_urls, "pages", folder_path, folder_name)

    # write image links to file
    img_urls = util.get_img_links(domain_urls, main_url) 
    util.write_to_file(img_urls, "imgs", folder_path, folder_name)