import sys

from content_copy import copy_content
from generate_page_functions import generate_page, generate_pages_recursive


def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = '/'

    copy_content(r"static",
                 r"docs")
    #generate_page(basepath, r"content/index.md", r"template.html", r"public/index.html")
    generate_pages_recursive(basepath,
                             r'content',
                             r'template.html',
                             r'docs')

if __name__ == "__main__":
    main()

