from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import json

FONT_NAME = "Helvetica"
LOGO_TEXT = "MyPass"
BACKGROUND_COLOR = "white"
LOGO_FONT_COLOR = "white"
LABEL_FONT_COLOR = "black"
EMAIL = "your_email@email.com"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&',
               '(', ')', '*', '+', '_', '.', '~', '>', '<', '?', "'", '"', ';', ':', '-', '+']

    password_letters = [choice(letters) for char in range(randint(6, 9))]
    password_numbers = [choice(symbols) for char in range(randint(3, 4))]
    password_symbols = [choice(numbers) for char in range(randint(3, 4))]

    password_list = password_letters + password_numbers + password_symbols
    shuffle(password_list)
    password = "".join(password_list)
    window.clipboard_clear()
    window.clipboard_append(f"{password}")

    password_field = password_entry.get()
    if len(password_field) > 0:
        password_entry.delete(0, last=END)
    password_entry.insert(0, f"{password}")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_account():
    website = website_entry.get().lower()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if website == "" or len(password) < 8:
        messagebox.showinfo(title="Please try Again",
                            message="Please don't leave any fields empty or use a weak password!")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
                data.update(new_data)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
                website_entry.delete(0, last=END)
                password_entry.delete(0, last=END)
        except ValueError:
            messagebox.showinfo(title="Please try Again",
                                message="Please check your JSON file and make sure it contains valid JSON data or it isn't empty! Fix or delete the file and try again.")
        else:
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
                website_entry.delete(0, last=END)
                password_entry.delete(0, last=END)


# ---------------------------- SEARCH ACCOUNT ------------------------------- #
def find_password():
    website = website_entry.get().lower()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Please try again",
                            message="No data file found. Please correct the data file, or create a new record to create a new data file.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website,
                                message=f"Email: {email} \nPassword: {password} \n\nThe password has been copied for you!")
            window.clipboard_clear()
            window.clipboard_append(f"{password}")
        else:
            messagebox.showinfo(title="Please try again",
                                message="No details for the website exists. Please double check the correct spelling for the website or you may add a new record for this website.")

        # ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=100, pady=100, bg=BACKGROUND_COLOR)

canvas = Canvas(window, width=326, height=250,
                bg=BACKGROUND_COLOR, highlightthickness=0)
logo_img = PhotoImage(file="logo.gif")
canvas.create_image(170, 116, image=logo_img)
canvas.create_text(170, 230, text=LOGO_TEXT,
                   fill=LOGO_FONT_COLOR, font=(FONT_NAME, 20, "bold"))
canvas.grid(pady=40, column=1, row=0)

website_label = Label(padx=20, text="Website:",
                      fg=LABEL_FONT_COLOR, font=(FONT_NAME, 16, "bold"))
website_label.grid(column=0, row=1)
email_label = Label(text="Email/Username:",
                    fg=LABEL_FONT_COLOR, font=(FONT_NAME, 16, "bold"))
email_label.grid(column=0, row=2)
password_label = Label(
    text="Password:", fg=LABEL_FONT_COLOR, font=(FONT_NAME, 16, "bold"))
password_label.grid(column=0, row=3)

website_entry = Entry(width=39)
website_entry.grid(column=1, row=1)
website_entry.focus()
email_entry = Entry(width=60)
email_entry.insert(0, EMAIL)
email_entry.grid(column=1, row=2, columnspan=3)
password_entry = Entry(width=39)
password_entry.grid(column=1, row=3)

password_button = Button(
    width=17, text="Generate Password", command=generate_password)
password_button.grid(column=2, row=3)
add_button = Button(text="Add", width=58, command=save_account)
add_button.grid(column=1, row=4, columnspan=3)
search_button = Button(text="Search", width=17, command=find_password)
search_button.grid(column=2, row=1, columnspan=3)

window.mainloop()
