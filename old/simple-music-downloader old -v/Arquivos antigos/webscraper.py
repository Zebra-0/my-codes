from urllib.request import urlopen

def title(url):
    #pagina = url
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")

    title_index = html.find("<title>")
    start_index = title_index + len("<title>")
    end_index = html.find("</title>")
    title = html[start_index:end_index]
    if "- YouTube" in title:
        full_title = title.replace("- YouTube", "")

    return str(full_title)

print(title("https://youtu.be/NHffhGkpgFA?list=RDAHukwv_VX9A"))