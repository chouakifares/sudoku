# No need for this line below
# ! C:\Users\USER\AppData\Local\Programs\Python\Python37-32\python.exe

# Please follow Pep reccomendations, I
# f using Pycharm, you should have the warnings and you can fix them just by clicking on code -> reformat code
import webview
from model import Grid

if __name__ == "__main__":
    grid = Grid()
    w = webview.create_window("hello world", url="vue.html", js_api=grid)
    w.expose(grid.get_cell)
    webview.start()
