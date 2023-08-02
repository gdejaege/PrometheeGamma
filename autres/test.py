import tkinter as tk



root = tk.Tk()
root.geometry('250x300')
#root.configure(cursor="arrow", height=2000, width=2000)
#root.maxsize(5000, 5000)
#root.minsize(150, 150)

root.update()

# Récupére la largeur
width = root.winfo_width() 
# Récupére la hauteur
height = root.winfo_height()

print("Largeur :", width)   # Affiche la largeur
print("Hauteur :", height)  # Affiche la hauteur

def pr():
    # Récupére la largeur
    width = root.winfo_width() 
    # Récupére la hauteur
    height = root.winfo_height()

    print("Largeur :", width)   # Affiche la largeur
    print("Hauteur :", height)  # Affiche la hauteur


b = tk.Button(root, text="test", command=pr)
b.pack()

root.mainloop()