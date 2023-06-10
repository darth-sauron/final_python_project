import random
import tkinter as tk
from tkinter import ttk
import DataBasePart as db
from tkinter import messagebox, font

the_d = 6
id_user = 0


def change_in_chars(frame_info, id_of_char):
    """
       Updates the character with the provided ID using the values from the entry widgets in the given frame.

       Args:
           frame_info (tk.Frame): The frame containing the entry widgets with the updated character information.
           id_of_char (int): The ID of the character to be updated.
    """
    entries = []
    for widget in frame_info.grid_slaves():
        if isinstance(widget, tk.Entry):
            entry_text = widget.get()
            entries.append(entry_text)

    db.change_character(id_of_char, entries[9], int(entries[8]), int(entries[3]), int(entries[7]), int(entries[2]),
                        int(entries[6]), int(entries[2]), int(entries[5]))


def view_characters(the_window):
    """
      Opens a window to view and interact with the list of characters.

      Args:
          the_window (tk.Tk or tk.Toplevel): The parent window where the characters window will be opened.
    """
    _id_ = 0

    def on_select(event):
        """
               Event handler for selecting a character from the list.

               Args:
                   event (tk.Event): The event object triggered by the selection.
        """

        selected = listbox.get(listbox.curselection())
        nonlocal _id_
        _id_ = selected.split(" : ")[0]
        db.show_char_stats(frame_info, _id_)

    chars_window = tk.Toplevel(the_window)
    chars_window.geometry("600x600")
    chars_window.configure(bg="#4C3E32")
    chars_window.resizable(False, False)
    chars_window.title("My Characters")

    frame_list = tk.Frame(chars_window, width=300, bg="#37312F", bd=5, relief=tk.SUNKEN)
    frame_list.pack(fill=tk.BOTH, expand=False, padx=20, pady=20)

    frame_info = tk.Frame(chars_window, width=300, bg="#37312F", bd=5, relief=tk.SUNKEN)
    frame_info.pack(fill=tk.BOTH, expand=False, padx=20, pady=20)

    listbox = tk.Listbox(frame_list, bg="#3F5C35", fg="#E0D5C7", selectbackground="#6C5748", selectforeground="#E0D5C7",
                         font=("Garamond", 12), relief=tk.FLAT)
    db.show_all_characters(id_user, listbox)
    listbox.bind("<<ListboxSelect>>", on_select)
    listbox.pack(fill="y", padx=10, pady=10)

    change_button = tk.Button(frame_info, text="Submit Changes", command=lambda: change_in_chars(frame_info, _id_),
                              bg="#DF6F18", fg="#2B1605", font=("Garamond", 12, "bold"), relief=tk.RAISED)
    change_button.grid(row=20, column=1, padx=10, pady=5)

    frame_list.pack(side="right", fill="y")
    frame_info.pack(side="left", fill="y")


def is_int(value):
    """
      Checks whether a value is a valid integer.

      Args:
          value (str): The value to be checked.

      Returns:
          bool: True if the value is a valid integer, False otherwise.
    """

    if value.isdigit() or value == '' or value == '-':
        return True
    else:
        return False


def roll_dice(label, d):
    """
        Simulates rolling a die with a specified number of sides.

        Args:
            label (tk.Label): The label to display the dice result.
            d (int): The number of sides on the dice.
    """

    label.config(text="\U000025A0\U000025A0\U000025A0", fg="gold")  # squares
    label.after(500, lambda: label.config(text=random.randint(1, d), fg="gold"))


def roll_all(list_, d):
    """
        Rolls multiple dice simultaneously.

        Args:
            list_ (list): A list of tk.Label objects representing the labels to display the dice results.
            d (int): The number of sides on the dice.
    """

    for label in list_:
        roll_dice(label, d)


def modify_field(entity, choice):
    """
       Modifies a Tkinter Entry widget by updating its value.

       Args:
           entity (tk.Entry): The Tkinter Entry widget to be modified.
           choice: The new value to be inserted into the Entry widget.
    """

    entity.config(state=tk.NORMAL)
    entity.delete(0, tk.END)
    entity.insert(0, choice)
    entity.config(state='readonly')


def show_races(frame, race_entry, frame2):
    """
       Displays a list of races in a Tkinter frame and allows the user to select a race.

       Args:
           frame (tk.Frame): The Tkinter frame where the list of races will be displayed.
           race_entry (tk.Entry): The Tkinter Entry widget where the selected race will be inserted.
           frame2 (tk.Frame): The Tkinter frame where the list of races will be populated.
    """

    selected = db.show_list(frame, "race", frame2)
    finish_button = tk.Button(frame, text="Done", bg="#DF6F18", fg="#2B1605",
                              command=lambda: modify_field(race_entry, selected.get()))
    finish_button.pack()
    finish_button.focus_set()


def show_classes(frame, class_entry, frame2):
    """
       Displays a list of classes in a Tkinter frame and allows the user to select a class.

       Args:
           frame (tk.Frame): The Tkinter frame where the list of classes will be displayed.
           class_entry (tk.Entry): The Tkinter Entry widget where the selected class will be inserted.
           frame2 (tk.Frame): The Tkinter frame where the list of classes will be populated.
    """

    selected = db.show_list(frame, "class", frame2)
    finish_button = tk.Button(frame, text="Done", bg="#DF6F18", fg="#2B1605",
                              command=lambda: modify_field(class_entry, selected.get()))
    finish_button.pack()
    finish_button.focus_set()


def create_dice(list_, n, window, d):
    """
        Creates a specified number of dice labels in a Tkinter window, that will then be clickable by the user.

        Args:
            list_ (list): The list to store the dice labels.
            n (int): The number of dice labels to create.
            window (tk.Tk or tk.Toplevel): The Tkinter window where the dice labels will be created.
            d (int): The number of sides on each die.
    """

    list_.clear()
    for child in window.winfo_children():
        if isinstance(child, tk.Label):
            child.destroy()
    for i in range(n):
        label = tk.Label(window, text=f"Die {i + 1}", bg="black", fg="gold")
        label.bind("<Button-1>", lambda _, label=label: roll_dice(label, d))
        label.pack(padx=10, pady=10)
        list_.append(label)


def assign(val):
    """
     Assigns a value to the global variable 'the_d'.

     Args:
         val: The value to assign to 'the_d'.
     """

    global the_d
    the_d = val


def die_window(the_window):
    """
       Creates a dice rolling window.

       Args:
           the_window: The parent window on top of which the dice window will be created.
    """

    dice_window = tk.Toplevel(the_window, bg="#4C3E32")
    dice_window.geometry("300x470")
    dice_window.configure(bg="#37312F")
    dice_window.resizable(False, False)
    dice_window.title("Roll them Dice")

    the_dice = []

    menu = tk.Menu(dice_window, bg="#4C3E32", fg="#E0D5C7", activebackground="#6C5748", activeforeground="#E0D5C7")
    dice_menu = tk.Menu(menu, tearoff=0, bg="#4C3E32", fg="#E0D5C7", activebackground="#6C5748",
                        activeforeground="#E0D5C7")
    for i in range(2, 21):
        dice_menu.add_command(label=f"d{i}", command=lambda val=i: assign(val),
                              activebackground="#6C5748", activeforeground="#E0D5C7")

    menu.add_cascade(label="dice", menu=dice_menu)
    num_menu = tk.Menu(menu, tearoff=0, bg="#4C3E32", fg="#E0D5C7", activebackground="#6C5748",
                       activeforeground="#E0D5C7")
    for i in range(1, 11):
        num_menu.add_command(label=f"{i}", command=lambda i=i: create_dice(the_dice, i, dice_window, the_d),
                             activebackground="#6C5748", activeforeground="#E0D5C7")
    menu.add_cascade(label="Number of Dice", menu=num_menu)

    button_frame = tk.Frame(dice_window, bg="#37312F")
    button_frame.pack(side="bottom", pady=10)

    roll_button = tk.Button(button_frame, text="Roll Them All", command=lambda: roll_all(the_dice, the_d),
                            bg="#DF6F18", fg="#2B1605")
    roll_button.pack(side="left", padx=10)

    done_button = tk.Button(button_frame, text="Done", command=dice_window.destroy, bg="#DF6F18", fg="#2B1605")
    done_button.pack(side="right", padx=10)

    dice_window.config(menu=menu)


def show_window():
    """
       Creates the main window of the application.
    """

    # initialize the window
    window = tk.Tk()
    window.geometry("1000x700")
    window.configure(bg="#1D1D21")
    window.resizable(False, False)
    window.title("Main Page")

    # bottom frame for dice
    frame = tk.Frame(window, bg="#573C1E")
    frame.pack(fill=tk.BOTH, expand=False)

    # right-hand side frame for character's stats
    frame_stats = tk.Frame(window, width=100, bg="#3F5C35")
    frame_stats.pack(fill=tk.BOTH, expand=False)

    # attributes of a character, modifiable by the user (all except class and race as it is chosen in a menu)
    attributes_bg = "#473226"
    attributes_fg = "#E6D9B9"

    name_label = tk.Label(frame_stats, text="Name:", bg=attributes_bg, fg=attributes_fg)
    name_label.grid(row=0, column=0, padx=10, pady=5)
    name_entry = tk.Entry(frame_stats, font=("Garamond", 12))
    name_entry.grid(row=1, column=1, padx=10, pady=5)
    strength_label = tk.Label(frame_stats, text="Strength:", bg=attributes_bg, fg=attributes_fg)
    strength_label.grid(row=2, column=0, padx=10, pady=5)
    strength_entry = tk.Entry(frame_stats, font=("Garamond", 12), validate="key",
                              validatecommand=(window.register(is_int), "%P"))
    strength_entry.grid(row=3, column=1, padx=10, pady=5)
    dexterity_label = tk.Label(frame_stats, text="Dexterity:", bg=attributes_bg, fg=attributes_fg)
    dexterity_label.grid(row=4, column=0, padx=10, pady=5)
    dexterity_entry = tk.Entry(frame_stats, font=("Garamond", 12), validate="key",
                               validatecommand=(window.register(is_int), "%P"))
    dexterity_entry.grid(row=5, column=1, padx=10, pady=5)
    constitution_label = tk.Label(frame_stats, text="Constitution:", bg=attributes_bg, fg=attributes_fg)
    constitution_label.grid(row=6, column=0, padx=10, pady=5)
    constitution_entry = tk.Entry(frame_stats, font=("Garamond", 12), validate="key",
                                  validatecommand=(window.register(is_int), "%P"))
    constitution_entry.grid(row=7, column=1, padx=10, pady=5)
    intelligence_label = tk.Label(frame_stats, text="Intelligence:", bg=attributes_bg, fg=attributes_fg)
    intelligence_label.grid(row=8, column=0, padx=10, pady=5)
    intelligence_entry = tk.Entry(frame_stats, font=("Garamond", 12), validate="key",
                                  validatecommand=(window.register(is_int), "%P"))
    intelligence_entry.grid(row=9, column=1, padx=10, pady=5)
    wisdom_label = tk.Label(frame_stats, text="Wisdom:", bg=attributes_bg, fg=attributes_fg)
    wisdom_label.grid(row=10, column=0, padx=10, pady=5)
    wisdom_entry = tk.Entry(frame_stats, font=("Garamond", 12), validate="key",
                            validatecommand=(window.register(is_int), "%P"))
    wisdom_entry.grid(row=11, column=1, padx=10, pady=5)
    charisma_label = tk.Label(frame_stats, text="Charisma:", bg=attributes_bg, fg=attributes_fg)
    charisma_label.grid(row=12, column=0, padx=10, pady=5)
    charisma_entry = tk.Entry(frame_stats, font=("Garamond", 12), validate="key",
                              validatecommand=(window.register(is_int), "%P"))
    charisma_entry.grid(row=13, column=1, padx=10, pady=5)
    hp_label = tk.Label(frame_stats, text="Hp:", bg=attributes_bg, fg=attributes_fg)
    hp_label.grid(row=14, column=0, padx=10, pady=5)
    hp_entry = tk.Entry(frame_stats, font=("Garamond", 12), validate="key",
                        validatecommand=(window.register(is_int), "%P"))
    hp_entry.grid(row=15, column=1, padx=10, pady=5)

    race_label = tk.Label(frame_stats, text="Race:", bg=attributes_bg, fg=attributes_fg)
    race_label.grid(row=16, column=0, padx=10, pady=5)
    race_entry = tk.Entry(frame_stats, font=("Garamond", 12), state="readonly")
    race_entry.grid(row=17, column=1, padx=10, pady=5)
    class_label = tk.Label(frame_stats, text="Class:", bg=attributes_bg, fg=attributes_fg)
    class_label.grid(row=18, column=0, padx=10, pady=5)
    class_entry = tk.Entry(frame_stats, font=("Garamond", 12), state="readonly")
    class_entry.grid(row=19, column=1, padx=10, pady=5)
    create_button = tk.Button(frame_stats, text="Create", bg="#DF6F18", fg="#2B1605",
                              command=lambda: db.create_character(name_entry.get(), int(strength_entry.get()),
                                                                  int(dexterity_entry.get()),
                                                                  int(constitution_entry.get()),
                                                                  int(intelligence_entry.get()),
                                                                  int(wisdom_entry.get()),
                                                                  int(charisma_entry.get()), int(hp_entry.get()),
                                                                  race_entry.get(), class_entry.get(), id_user))
    create_button.grid(row=21, column=1, padx=10, pady=5)

    # frame for showing a list of all available races and classes
    container = ttk.Frame(window, width=150)
    canvas = tk.Canvas(container, width=150, bg="#3F5C35")
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, width=150, bg="#3F5C35")
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    container.pack(side="left", fill="y", expand=False)
    canvas.pack(side="left", fill="y", expand=False)
    scrollbar.pack(side="right", fill="y", expand=False)

    # frame for displaying information about races/classes
    info_frame = tk.Frame(window, bg="#1D1D21")
    info_frame.pack(expand=True)
    info_text = tk.Frame(info_frame, width=20, height=70, bg="#1D1D21")
    info_text.grid(row=0, column=0, padx=10, pady=10)

    # labels simulating dice
    die_1 = tk.Label(frame, text="Die 1", bg="black", fg="gold", font=("Garamond", 14, "bold"))
    die_1.bind("<Button-1>", lambda _: roll_dice(die_1, 6))
    die_2 = tk.Label(frame, text="Die 2", bg="black", fg="gold", font=("Garamond", 14, "bold"))
    die_2.bind("<Button-1>", lambda _: roll_dice(die_2, 6))
    die_3 = tk.Label(frame, text="Die 3", bg="black", fg="gold", font=("Garamond", 14, "bold"))
    die_3.bind("<Button-1>", lambda _: roll_dice(die_3, 6))
    die_4 = tk.Label(frame, text="Die 4", bg="black", fg="gold", font=("Garamond", 14, "bold"))
    die_4.bind("<Button-1>", lambda _: roll_dice(die_4, 6))

    die_1.grid(row=0, column=0)
    die_2.grid(row=0, column=1)
    die_3.grid(row=0, column=2)
    die_4.grid(row=0, column=3)

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(2, weight=1)
    frame.grid_columnconfigure(3, weight=1)

    frame.pack(side="bottom", fill="x")
    frame_stats.pack(side="right", fill="y")

    # menu for doing different things
    menu = tk.Menu(window, background="#4C3E32", fg="#E0D5C7")
    character_menu = tk.Menu(menu, tearoff=0, background="#4C3E32", fg="#E0D5C7",
                             activebackground="#6C5748",
                             activeforeground="#E0D5C7", bd=0)
    character_menu.configure(font=("Garamond", 12, "bold"))
    character_menu.add_command(label="Choose Race",
                               command=lambda: show_races(scrollable_frame, race_entry, info_frame),
                               font=("Garamond", 12), activebackground="#917A68", background="#4C3E32",
                               activeforeground="#E0D5C7")
    character_menu.add_command(label="Choose Class",
                               command=lambda: show_classes(scrollable_frame, class_entry, info_frame),
                               font=("Garamond", 12), activebackground="#917A68", background="#4C3E32",
                               activeforeground="#E0D5C7")
    character_menu.add_command(label="View Characters", command=lambda: view_characters(window), font=("Garamond", 12),
                               activebackground="#917A68", activeforeground="#E0D5C7", background="#4C3E32")

    die_menu = tk.Menu(menu, tearoff=0, background="#4C3E32", fg="#E0D5C7", activebackground="#6C5748",
                       activeforeground="#E0D5C7", bd=0)
    die_menu.configure(font=("Garamond", 12, "bold"))
    die_menu.add_command(label="Roll Dice", command=lambda: die_window(window), font=("Garamond", 12),
                         activebackground="#917A68", activeforeground="#E0D5C7", background="#4C3E32")

    menu.add_cascade(label="Character", menu=character_menu, background="#4C3E32")
    menu.add_cascade(label="Dice", menu=die_menu, background="#4C3E32")

    # launch the window
    window.config(menu=menu)
    window.mainloop()


def is_valid(username, password, login_frame):
    """
        Validates a username and password combination.

        Args:
            username (str): The username to validate.
            password (str): The password to validate.
            login_frame (tk.Frame): The login frame to destroy.
    """

    f = open("users.txt", "r")
    found = False

    # check if the user has an account
    for i in f:
        i = i.strip()
        if i == username + ":" + password:
            found = True
    if not found:
        messagebox.showerror("Login Error", "Invalid username or password")
    else:  # get the id from database for further use and show the main window
        login_frame.destroy()
        global id_user
        id_user = db.find_user(username)
        show_window()


def register_func(username, password):
    """
       Registers a new user.

       Args:
           username (str): The username to register.
           password (str): The password to register.
    """

    f = open("users.txt", "r")
    found = False

    # check that the username doesn't exist
    for i in f:
        i = i.strip()
        check = i.split(":")
        if check[0] == username:
            found = True
    if found:
        messagebox.showerror("Login Error", "Username already exists")
    else:  # add this new user to the file
        f = open("users.txt", "a")
        f.write(username + ":" + password + "\n")
        db.add_user(username, password)
        messagebox.showinfo("Sweet!", "You're now in the system")


def login_window():
    """
        Creates a login and registration window.
    """

    # initializing the window
    login_window_frame = tk.Tk()
    login_window_frame.geometry("500x500")
    login_window_frame.configure(bg="#37312F")
    login_window_frame.resizable(False, False)
    login_window_frame.title("Login/Register")

    # image upper left corner
    image = tk.PhotoImage(file="fairy.png")
    label_image = tk.Label(login_window_frame, image=image, borderwidth=0, highlightthickness=0)
    label_image.place(x=0, y=0, anchor="nw")

    # image bottom right corner
    image2 = tk.PhotoImage(file="dndDIE.png")
    label_image2 = tk.Label(login_window_frame, image=image2, borderwidth=0, highlightthickness=0)
    label_image2.place(x=300, y=300, anchor="nw")

    # font and color for the words in this window
    new_font = font.Font(family="Garamond", size=18, weight="bold")
    font_labels = font.Font(family="Courier New", size=12)

    # LOGIN
    login_label = tk.Label(login_window_frame, text="LOGIN", font=new_font, bg="#37312F", fg="#857100")
    login_label.pack(pady=10)

    # USERNAME
    username_label = tk.Label(login_window_frame, text="Username", font=font_labels, bg="#F6CE62")
    username_label.pack(pady=5)
    username_entry = tk.Entry(login_window_frame)
    username_entry.pack(pady=5)

    # PASSWORD
    password_label = tk.Label(login_window_frame, text="Password", font=font_labels, bg="#F6CE62")
    password_label.pack(pady=5)
    password_entry = tk.Entry(login_window_frame, show="\U000025CF")
    password_entry.pack(pady=10)

    # LOGIN BUTTON
    login_button = tk.Button(login_window_frame, text="Login", bg="#DF6F18", fg="#2B1605",
                             command=lambda: is_valid(username_entry.get(),
                                                      password_entry.get(),
                                                      login_window_frame))
    login_button.pack(pady=10)

    # REGISTER
    register_label = tk.Label(login_window_frame, text="REGISTER", font=new_font, bg="#37312F", fg="#857100")
    register_label.pack(pady=10)

    # NEW USERNAME
    new_username_label = tk.Label(login_window_frame, text="Username", font=font_labels, bg="#F6CE62")
    new_username_label.pack(pady=5)
    new_username_entry = tk.Entry(login_window_frame)
    new_username_entry.pack(pady=5)

    # NEW PASSWORD
    new_password_label = tk.Label(login_window_frame, text="Password", font=font_labels, bg="#F6CE62")
    new_password_label.pack(pady=5)
    new_password_entry = tk.Entry(login_window_frame, show="\U000025CF")
    new_password_entry.pack(pady=10)

    # REGISTER BUTTON
    new_login_button = tk.Button(login_window_frame, text="Register", bg="#DF6F18", fg="#2B1605",
                                 command=lambda: register_func(
                                     new_username_entry.get(), new_password_entry.get()))
    new_login_button.pack(pady=10)

    # run the window
    login_window_frame.mainloop()
