from guizero import App, Slider, Text, TextBox, PushButton, Window
import os
from main import main

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


def changePath(new_dir, app2, path):
    app2.destroy()
    print("changing path")
    path += "\\" + new_dir + "\\"
    directories = get_immediate_subdirectories(path)

    app2 = Window(app, title="Hello world")

    widgets = []

    widgets.append(Text(app2, text="Current path = " + path))

    widgets.append(PushButton(app2, text="GO BACK", command=lambda: goBackPath(app2, path)))

    index = 0
    for dir in directories:
        widgets.append(PushButton(app2, text=directories[index], command=lambda: changePath(directories[index], app2, path)))
        index += 1

    app.display()


def goBackPath(app2, path):
    app2.destroy()
    print("going back path")
    paths = path.split("\\")
    path = ""
    index = 0
    while index < len(paths)-2:
        path += paths[index] + "\\"
        index += 1

    directories = get_immediate_subdirectories(path)

    app2 = Window(app, title="Hello world")

    widgets = []
    widgets.append(Text(app2, text="Current path = " + path))

    widgets.append(PushButton(app2, text="GO BACK", command=lambda: goBackPath(app2, path)))

    index = 0
    indexes = []
    for dir in directories:
        indexes.append(index)
        widgets.append(PushButton(app2, text=dir, command=lambda: changePath(directories[index], app2, path)))
        index += 1

    app.display()


def chooseDirectory():

    path = app.children[4].value

    directories = get_immediate_subdirectories(path)

    app2 = Window(app, title="Hello world")

    widgets = []

    widgets.append(Text(app2, text="Current path = " + path))

    widgets.append(PushButton(app2, text="GO BACK", command=lambda: goBackPath(app2, path)))

    index = 0
    for dir in directories:
        widgets.append(PushButton(app2, text=dir, command=lambda: changePath(directories[index], app2, path)))
        index += 1

    app.display()


def change_directory():
    app.children[6].value = "C:\\Users\\tesser\\PycharmProjects\\formTabsToPdfs\\"
    app.display()


def start_download():
    if app.children[4].value != "":
        main(app.children[2].value, str(app.children[4].value))


app = App(title="From Ultimate Guitare To Pdf")
message = Text(app, text="Welcome to the get pdf from ultimate guitar app!")
url_text = Text(app, text="URL")
url_input = TextBox(app, width=50)
dir_text = Text(app, text="Current directory")
dir_input = TextBox(app, width=50)
app.children[4].value = "files/"
dir_button = PushButton(app, text="Change Directory", command=change_directory)
download_button = PushButton(app, text="Download", command=start_download)

app.display()

