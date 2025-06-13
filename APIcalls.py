import requests
import customtkinter
from PIL import Image, ImageTk
import io

# This script retrieves information about a Pokémon from the PokeAPI
api_URL = "https://pokeapi.co/api/v2/"

def get_pokemon_info(name):
    url = f"{api_URL}/pokemon/{name.lower()}"
    response = requests.get(url)
    
    if response.status_code == 200:
       pokemon_data = response.json()
       return(pokemon_data)
    else:
        print(f"Failed to retrieve data: {response.status_code}")
# Define a functiion to handle the submission of the Pokemon name
def submitPokemonName():
    for widget in outputFrame.winfo_children():
        widget.destroy()
    # Gets the name of the Pokemon from the textbox
    pokemon_name = inputPokemonNameTB.get("1.0", "end-1c")
    pokemonData = get_pokemon_info(pokemon_name)

    # if the pokemonData is None, it means the Pokemon was not found
    if not pokemonData:
        error_label = customtkinter.CTkLabel(outputFrame, text="Pokemon not found!", text_color="red", font=("Arial", 14))
        error_label.pack(pady=20)
        return

    # Get the sprite URL
    sprite_url = pokemonData["sprites"]["front_default"]
    response = requests.get(sprite_url)
    
    # Convert to CTkImage
    image_data = response.content
    pil_image = Image.open(io.BytesIO(image_data))
    ctk_img = customtkinter.CTkImage(
        light_image=pil_image,
        dark_image=pil_image,
        size=(150, 150))
    # Create image label
    img_label = customtkinter.CTkLabel(outputFrame, image=ctk_img, text="")
    img_label.image = ctk_img  # Keep reference
    img_label.pack(pady=10)

    # Gets the abilities of the Pokemon and displays them
    ability_names = [ability["ability"]["name"] for ability in pokemonData["abilities"]]
    # Saves the abilities to a variable
    display_data = [
        f"Name: {pokemonData["name"]}\n"
        f"ID: {pokemonData["id"]}\n"
        f"Abilities: {', '.join(ability_names)}\n"
        ]
    # Loops throught the abilities and adds them to the display data
    for data in display_data:
        label = customtkinter.CTkLabel(outputFrame, text=data, font=("Arial", 28), text_color="#0F0F0F")
        label.pack(pady=5, padx=5)



# This part of the code creates the simple GUI using CTK
app = customtkinter.CTk()
app.geometry("500x500")
app.title("Pokemon Info Fetcher")
# Label(s) for the GUI
Mainlabel = customtkinter.CTkLabel(app,
                                   text="Enter pokemon name here!",
                                   fg_color="transparent",
                                   text_color="#FBFBFB",
                                   font=("Arial", 14)
                                   )

Mainlabel.place(relx=0.5, rely=0.04, anchor="center")
# Creates a textbox for the user to input the name of the Pokemon
inputPokemonNameTB = customtkinter.CTkTextbox(app, 
                                          width=200, 
                                          height=30,
                                          fg_color="#BCABAE",
                                          border_color="#0F0F0F", 
                                          border_width=1.2,
                                          text_color="#0F0F0F", 
                                          font=("Arial", 12)
                                          )

inputPokemonNameTB.place(relx=0.5, rely=0.1, anchor="center")
# Button to submit the name of the Pokemon
submitButton = customtkinter.CTkButton(app,
                                       text="Submit",
                                       command=submitPokemonName,
                                       fg_color="#E3350D",
                                       hover_color="#C22E28")
submitButton.place(relx=0.5, rely=0.18, anchor="center")
# Output Frame
outputFrame = customtkinter.CTkFrame(app, width=400, height=300, fg_color="#BCABAE")
outputFrame.place(relx=0.5, rely=0.56, anchor="center")

app.mainloop()

