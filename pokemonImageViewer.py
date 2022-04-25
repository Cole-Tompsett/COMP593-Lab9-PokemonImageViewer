from tkinter import *
from tkinter import ttk
import os
import sys
import ctypes
from pokeApi import Getting_poke_info, pokemon_url
from pokeApi import get_list
import requests

def main():

    script_dir = sys.path[0]
#creates the path for the images to be stored
    images_dir = os.path.join(script_dir,'pokemon images')
    if not os.path.isdir(images_dir):
        os.makedirs(images_dir)

#building the gui window and creating a title
    root = Tk()
    root.title("PokemonImageViewer")

#setting the icon for the app to be a pokeball    
    app_id = 'PokemonImageViewer'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    root.iconbitmap(os.path.join(script_dir, "pokeball-1.ico"))
#keeps everything in the center of the window    
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0,weight=1)    
#creating the frame for the elements of the gui to sit in

    frm = ttk.Frame(root)
    frm.grid(sticky=(N,S,E,W))
#keeps everything in the center of the frame when adjusted
    frm.columnconfigure(0, weight=1)
    frm.rowconfigure(0,weight=1)

#creating the launch image you first see when starting the app
    img_pokemon = PhotoImage(file=os.path.join(script_dir, 'pokeball_launch.png'))
    lbl_image = Label(frm, image= img_pokemon)
    lbl_image.grid(row=0, column=0, padx=10, pady=10)

#calls the get_list function and sets the limit to 1000 names. After fetching the names it will then sort them
    pokemon_list = get_list(limit=1000)
    pokemon_list.sort()

#creating the combo box for the user to select what pokemon they want to see 
    cbo_pokemon_sel = ttk.Combobox(frm, values= pokemon_list, state= 'readonly')
    cbo_pokemon_sel.set('Select a Pokemon')
    cbo_pokemon_sel.grid(row=1, column=0)

#when something is selceted from th combobox this will call a function to grab the url. It will then download the image but if it is already download it will just diplay that image.
    def handle_cbo_pokemon(event):
        pokemon_name =cbo_pokemon_sel.get()
        image_url = pokemon_url(pokemon_name) 
        image_path = os.path.join(images_dir,pokemon_name + '.png')
        if download_image_from_url(image_url,image_path):
            img_pokemon['file'] = image_path    
            btn_set_desktop.state(['!disabled'])   

#if you select something fromt the combobox it will call the fucntion that'll show you an image of the pokemon
    cbo_pokemon_sel.bind('<<ComboboxSelected>>',handle_cbo_pokemon)

def btn_set_desktop_click():
    pokemon_name = cbo_pokemon_sel.get()
    image_path = os.path.join(images_dir, pokemon_name +'.png')
    set_desktop(image_path)



#creating a button for the user to use that will 
    btn_set_desktop = ttk.Button(frm, text='Set as Desktop Image', command=btn_set_desktop_click)
    btn_set_desktop.state(['disabled'])
    btn_set_desktop.grid(row=2, column=0,padx=10, pady=10)


    root.mainloop()

def download_image_from_url(url,path):

#downloads the image from the provided url   
    resp_msg =requests.get(url)

#if the status code is "200" it will save the image to the disk in the folder provided
    if resp_msg.status_code == 200:
        try:
            img_data = resp_msg.content
            with open(path, 'wb') as fp:
                fp.write(img_data)
            return path
        except:
            return
#if status code is not "200" it will output error messages
    else:
        print("Failed to donwload image.")
        print("Repsonse code:", resp_msg.status_code)
        print(resp_msg.text)
    
def set_desktop(path):
#sets the background image of the computer to the selected pokemon
   ctypes.windll.user32.SystemParametersInfoW(20, 0, path , 0)

main()