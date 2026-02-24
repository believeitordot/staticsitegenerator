from textnode import TextNode
from textnode import TextType

def main():
    textnode = TextNode("This is a text node", TextType.BOLD_TEXT, "https://www.boot.dev")
    print(textnode)

main()