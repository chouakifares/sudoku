#! C:\Users\USER\AppData\Local\Programs\Python\Python37-32\python.exe
import webview
from model import Grid
grid=Grid()
w=webview.create_window("hello world",url="vue.html",js_api=grid)
w.expose(grid.get_cell)
webview.start()

