from content_copy import copy_content
from generate_page_functions import generate_page, generate_pages_recursive


def main():
    copy_content(r"/home/konstantin/static_site_generator/bootdev-static-site-generator/static",
                 r"/home/konstantin/static_site_generator/bootdev-static-site-generator/public")
    #generate_page(r"content/index.md", r"template.html", r"public/index.html")
    generate_pages_recursive(r'/home/konstantin/static_site_generator/bootdev-static-site-generator/content',
                             r'template.html',
                             r'/home/konstantin/static_site_generator/bootdev-static-site-generator/public')

if __name__ == "__main__":
    main()

