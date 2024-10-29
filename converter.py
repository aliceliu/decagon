from bs4 import BeautifulSoup


def convert_html_to_text(doc: str):
    soup = BeautifulSoup(doc, "html.parser")
    main = soup.body.main
    return format_main(main)

def format_main(main):
    text_nodes = main.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p"])
    text = ""
    for node in text_nodes:
        if is_header(node):
            text += format_header(node) 
        elif has_li_parent(node):
            text += format_li(node) 
        else:
            text += node.get_text() + "\n"
    return text


def is_header(node):
    return node.name in ["h1", "h2", "h3", "h4", "h5", "h5", "h6"]

def format_header(node):
    return "\n" + "#" * int(node.name[1]) + " " + node.get_text() + "\n"

def format_li(node):
    return "* " + node.get_text() + "\n"
    
def has_li_parent(node):
    while node.parent is not None: 
        if node.parent.name == 'li':
            return True
        node = node.parent
    return False