from tkinter import *
import pandas as pd
from tkinter import messagebox
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():

    import random
    from random import randint
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letter = [random.choice(letters) for i in range(randint(8, 10))]
    password_symbols = [random.choice(symbols) for j in range(randint(2, 4))]
    password_number = [random.choice(numbers) for k in range(randint(2, 4))]

    password_list = password_letter + password_symbols + password_number

    random.shuffle(password_list)

    password = "".join(password_list)
    pyperclip.copy(password)
    password_entry.delete(0, END)
    password_entry.insert(0, password)



# ---------------------------- SAVE PASSWORD ------------------------------- #

def PasswordManager():
    web = web_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    new_json = {
        web : {
            "email" : email,
            "password" : password
        }
    }

    if len(web) == 0 or len(password) == 0:
        messagebox.showinfo(title= "Invalid Information", message= "Please Fill required information")
    else:
        messagebox.askokcancel(title = "Details", message = f"Here your details:\nemail:{email}\n"
                                                        f"website:{web}\npassword:{password}")

    df = pd.read_csv("data.csv")
    new_dict = {
        "Websites" : [web],
        "Email/Username" : [email],
        "Password" : [password]
    }
    new_df = pd.DataFrame(new_dict)
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv("data.csv", index=False, header = True)

    with open("data.txt", 'a') as file:
        file.write(f"{web} | {email} | {password}\n")

    try:
        with open("data.json", 'r') as file:
            json_data = json.load(file)
    except FileNotFoundError:
        with open("data.json", 'w') as file:
            json.dump(new_json, file, indent=4)
    else:
        json_data.update(new_json)
        with open("data.json", 'w') as file:
            json.dump(json_data, file, indent=4)

    finally:
        web_entry.delete(0, END)
        password_entry.delete(0, END)


# ---------------------------- SEARCH PASSWORD ------------------------------- #

def search_passwd():
    web = web_entry.get()
    with open("data.json", 'r') as file:
        data = json.load(file)
        email= data[web]["email"]
        passwd= data[web]["password"]
        if web in data:
            messagebox.showinfo(title="Credential", message= f"email: {email}\npassword: {passwd}")
        else:
            messagebox.showinfo(title="Credential", message= f"Website Doesn't Exist")
        print(data[web])




# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx = 50, pady = 50)

canvas = Canvas(width = 200, height = 189)
img = PhotoImage(file = "logo.png")
canvas.create_image(100, 95, image = img)
canvas.grid(row = 0, column = 1)

# Labels and Entries
website_label = Label(text="Website:", bg="white")
website_label.grid(row=1, column=0, sticky="e", padx=(0, 5), pady=5)
web_entry = Entry(width=35, bg="white")
web_entry.grid(row=1, column=1, sticky="ew", pady=5)
web_entry.focus()

email_label = Label(text="Email/Username:", bg="white")
email_label.grid(row=2, column=0, sticky="e", padx=(0, 5), pady=5)
email_entry = Entry(width=35, bg="white")
email_entry.grid(row=2, column=1, columnspan=2, sticky="ew", pady=5)
email_entry.insert(0, "rudra@gmail.com")

def on_email_click(event):
    if email_entry.get() == "rudra@gmail.com":
        email_entry.delete(0, END)
        email_entry.config(fg='black')

def on_email_keyrelease(event):
    current_text = email_entry.get()
    if not current_text.endswith("@gmail.com") and "@gmail.com" not in current_text:
        if current_text and not current_text == "rudara@gmail.com":
            email_entry.delete(0, END)
            email_entry.insert(0, current_text + "@gmail.com")
            email_entry.icursor(len(current_text))


email_entry.bind("<FocusIn>", on_email_click)
email_entry.bind("<KeyRelease>", on_email_keyrelease)

password_label = Label(text="Password:", bg="white")
password_label.grid(row=3, column=0, sticky="e", padx=(0, 5), pady=5)
password_entry = Entry(width=21, bg="white")
password_entry.grid(row=3, column=1, sticky="ew", pady=5)


# Buttons
generate_password_button = Button(text="Generate Password", bg="#d32f2f", fg="white", font=("Arial", 8), command = generate_password)
generate_password_button.grid(row=3, column=2, padx=(5, 0), pady=5)

add_button = Button(text="Add", width=36, bg="#d32f2f", fg="white", command= PasswordManager)
add_button.grid(row=4, column=1, columnspan=2, pady=10)

# Search Button
search_button = Button(text= "Search", width= 16, bg="#d32f2f", fg="white", font=("Arial", 8), command= search_passwd)
search_button.grid(row = 1, column= 2, padx=(5, 0), pady=5)


window.mainloop()