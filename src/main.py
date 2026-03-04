#from textnode import TextType, TextNode
from copystatic import copystatic # Move to gencontent.py: also in the test suite
from gencontent import generate_pages_recursive

def main():
    #textnode = TextNode("This is a text node", TextType.BOLD_TEXT, "https://www.boot.dev")
    #print(textnode)
    copystatic("./static", "./public")

    generate_pages_recursive("./content", "template.html",  "./public")

main()