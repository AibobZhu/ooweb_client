import sys
sys.path.append(".")
sys.path.append("..")

from components_client import WebPage


if __name__ == '__main__':
    test_page = WebPage(test=True)
    test_page.test_start()
