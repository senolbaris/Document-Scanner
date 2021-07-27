from document_scanner import get_coor
import tkinter.filedialog
import tkinter

root = tkinter.Tk()
root.withdraw()

print("******Document Scanner by BS******")
print("Please choose an image then mark corners (top-left, top-right, bottom-left, bottom-right). \nAfter marked all corner press SPACE to end the process.")
print("At the end you can press 's' twice to save the image.")

command = input("To start type 'go': ")

def browse_file():
	path = tkinter.filedialog.askopenfilename()
	return path


if command.lower() == 'go':
	path = browse_file()
	get_coor(path)
else:
	print("Okey. Bye...")


