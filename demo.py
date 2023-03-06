import tkinter as tk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class MyHandler(FileSystemEventHandler):
    def __init__(self, text_box):
        self.text_box = text_box

    def on_modified(self, event):
        self.text_box.delete('1.0', 'end')
        with open(r'C:\Users\hui\Desktop\emba.log', 'r') as f:
            self.text_box.insert('end', f.read())


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('日志文件展示')
        self.master.geometry('800x600')

        self.text_box = tk.Text(self.master)
        self.text_box.pack(fill='both', expand=True)

        self.observer = Observer()
        self.observer.schedule(MyHandler(self.text_box), './', recursive=True)
        self.observer.start()

    def __del__(self):
        self.observer.stop()
        self.observer.join()


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
