from tkinter import Tk

from tkknapsack.objects.interface import Interface

window = Tk()
window.geometry("950x500")
window.resizable(False, False)
window.option_add("*Background", "#2E3440")
window.option_add("*Foreground", "#ECEFF4")
window.option_add("*Font", "Helvetica 10")
window.option_add("*Label.Background", "#3B4252")
window.option_add("*Checkbutton.borderWidth", 0)
window.option_add("*Checkbutton.highlightThickness", 0)
window.configure(bg="#2E3440")
window.title("Knapsack Problem")
ui = Interface(window)
ui.mainloop()
