import sys
from copystatic import copystatic # Move to gencontent.py: also in the test suite
from gencontent import generate_pages_recursive

def main():
    #textnode = TextNode("This is a text node", TextType.BOLD_TEXT, "https://www.boot.dev")
    #print(textnode)
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
        
    copystatic("./static", "./docs")

    generate_pages_recursive("./content", "template.html",  "./docs", basepath)

main()