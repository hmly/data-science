import urllib.parse as parse
import urllib.request as rq
import csv
import os
from bs4 import BeautifulSoup

path = "/home/hmly/Documents/data-science/cas-faculty/"  # change to your desire path
url = "http://www.suffolk.edu"


def extract_facsinfo(links):
    facsinfo = []
    for li in links:
        # get parsed-html
        url2 = parse.urljoin(url, li)
        html = rq.urlopen(url2).read().decode("utf8")
        soup = BeautifulSoup(html, "lxml")

        # get name, rank
        soup = soup.findAll("div", {"class": "colBox"})[0]  # get 1st occurrence of class
        info = [el.strip() for el in str(soup.get_text()).split("\n") if el.strip() != ""]  # get text
        try:
            name, rank = info[1].split(", ")
            if rank == "PhD":
                rank = "Associate Professor"  # account for typo
        except ValueError:
            name = info[1]
            rank = "Professor"  # default if not specified

        # find index of str "education" in list of elements
        # find end by incrementing until a string that does
        # not match the specified format
        try:
            begin = info.index("Education")
        except ValueError:
            begin = 0
        end = begin + 1
        for el in info[begin + 1:]:
            pair = el.split(",")
            if len(pair) < 2 and (len(pair[0]) > 6
                    or "Master" in pair[0] or "Bachelor" in pair[0]):
                break    # if split is unsuccessful
            end += 1
        # print(name, info[begin: end])

        # Darlene C. Chisholm exception
        if name == "Darlene C. Chisholm":
            for i in range(1, 6):
                degree = info[begin + i].split(",")
                degree2 = degree[0].replace(".", "")
                if len(degree2.split()[0]) < 5:
                    dtype = degree[0].split()[0]  # get only the degree type
                    institution = info[begin + i - 1].split(",")[0]  # get previous el
                    facsinfo.append((name, rank, dtype, institution))

        # search from begin to end index
        # to avoid searching through the entire list
        # get the degree type and institution
        degree_len = 7  # avoid including diploma type
        for el in info[begin + 1: end]:
            degree = el.split(",")
            degree[0] = degree[0].replace("•\t", "")  # account for weird chars
            degree2 = degree[0].replace(".", "").replace(" ", "")  # remove "." and " "
            # only look at str with format of (MBA / Master, uni_name)
            if len(degree) in range(2, degree_len) and len(degree2) < degree_len and degree2.isalpha() \
                    or (degree2.startswith("Master") or degree2.startswith("Bachelor")):
                if len(degree) > 2:
                    # account for "degree suffolk uni, boston"
                    # and "degree, boston, suffolk uni"
                    if "College" in degree[2] or "University" in degree[2] or \
                                    "School" in degree[2] or "Institute" in degree[2] or \
                                    "Institution" in degree[2] or "Academy" in degree[2]:
                        institution = degree[2]
                    else:
                        institution = degree[1]
                    dtype = degree[0]
                else:
                    dtype, institution = degree
                facsinfo.append((name, rank, dtype, institution.strip()))  # remove extra whitespace in-front
            elif begin == 0:  # no education found
                facsinfo.append((name, rank, "", ""))
    return facsinfo


def extract_links():
    # get parsed-html
    url2 = parse.urljoin(url, "/college/6578.php")
    html = rq.urlopen(url2).read().decode("utf8")
    soup = BeautifulSoup(html, "lxml")
    links = []

    # extract faculties links
    for el in soup.findAll("div", {"class": "item"}):
        for cel in el.findChildren("a"):
            links.append(cel["href"])
    exc = links.index("http://www.suffolk.edu/college/12244.php")  # start looking from this index
    links[exc] = "/college/12244.php"  # account for Keri Iyall Smith exception
    return links


def tofile(facsinfo):
    ndir = path + "/results/"
    # check if the dir exists
    if not os.path.isdir(ndir):
        os.mkdir(ndir)
    # write to a csv file
    with open(ndir + "faculty-education.csv", "w") as outfile:
        outfile.write("Name,Rank,Degree,Institution\n")
        writer = csv.writer(outfile, delimiter=",")
        writer.writerows(facsinfo)


def main():
    print("Extracting links from main url...")
    links = extract_links()

    print("Extracting individual faculty info...")
    facsinfo = extract_facsinfo(links)

    print("Building csv file...")
    tofile(facsinfo)


if __name__ == "__main__":
    main()
