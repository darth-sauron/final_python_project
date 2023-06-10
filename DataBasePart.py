import json
from tkinter import messagebox

import sqlalchemy
import tkinter as tk
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

# initializing the database
engine = create_engine('sqlite:///projectDatabase.db')
connection = engine.connect()
Base = sqlalchemy.orm.declarative_base()


# creating tables
class Race(Base):
    __tablename__ = 'races'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    ability_scores = Column(String(50))
    traits = Column(String(100))
    subraces = Column(String(100))
    suggested_classes = Column(String(150))
    size = Column(String(20))
    speed = Column(String(100))


class Class(Base):
    __tablename__ = 'classes'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    party_role = Column(String(50))
    primary_ability = Column(String(100))
    saving_throws = Column(String(100))
    hit_dice = Column(String(150))
    hp = Column(String(20))
    best_races = Column(String(100))


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    user_name = Column(String(50))
    password = Column(String(50))


class Character(Base):
    __tablename__ = 'characters'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    strength = Column(Integer)
    dexterity = Column(Integer)
    constitution = Column(Integer)
    intelligence = Column(Integer)
    wisdom = Column(Integer)
    charisma = Column(Integer)
    hp = Column(Integer)
    race_id = Column(Integer, ForeignKey('races.id'))
    class_id = Column(Integer, ForeignKey('classes.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    race = relationship('Race')
    class_ = relationship('Class')
    user = relationship('User')


Base.metadata.create_all(engine)


def populate_races():
    """
       Populate the race table, as well as the class table with data from the races.json file and class.json file.
    """

    session = sessionmaker(bind=engine)
    session = session()
    session.execute(Race.__table__.delete())
    session.execute(Class.__table__.delete())
    session.commit()
    f = open("races.json", "r")
    j_data = json.load(f)

    # races
    for i in j_data:
        suggested_classes = j_data[i].get('Suggested classes', '')
        session.add(
            Race(name=i, ability_scores=j_data[i]['Ability scores'], traits=j_data[i]['Traits'],
                 subraces=j_data[i]['Subraces'],
                 suggested_classes=suggested_classes, size=j_data[i]['Size'], speed=j_data[i]['Speed'])
        )
        session.commit()
    f.close()

    # classes
    f2 = open("classes.json")
    j_data2 = json.load(f2)
    for i in j_data2:
        session.add(
            Class(name=i, party_role=j_data2[i]['Party role'], primary_ability=j_data2[i]['Primary ability'],
                  saving_throws=j_data2[i]['Saving throws'],
                  hit_dice=j_data2[i]['Hit dice'], hp=j_data2[i]['HP at 1st level'],
                  best_races=j_data2[i]['Best races'])
        )
        session.commit()
    f2.close()


def display_traits(attribute, name, frame):
    """
    Display the traits of a specific race or class.

    Args:
        attribute (str): The attribute to display traits for ('race' or 'class').
        name (str): The name of the race or class.
        frame (tk.Frame): The frame to display the traits in.
    """

    session = sessionmaker(bind=engine)
    session = session()
    if attribute == "class":
        f = Class
    else:
        f = Race
    char = session.query(f).filter(f.name == name).first()
    for child in frame.winfo_children():
        if isinstance(child, tk.Label):
            child.destroy()
    for field, value in char.__dict__.items():
        if not field == "id" and not field == "_sa_instance_state":  # don't display id and the field that shows up in
            # the
            # beginning
            label = tk.Label(frame, text=f"{field}:\n {value}\n", bg="#1D1D21", fg="gold")
            label.grid(padx=5, pady=5)


def create_character(name, strength, dexterity, constitution, intelligence, wisdom, charisma, hp, race, class_, user):
    """
        Create a new character and add it to the characters table.

        Args:
            name (str): The name of the character.
            strength (int): The strength attribute of the character.
            dexterity (int): The dexterity attribute of the character.
            constitution (int): The constitution attribute of the character.
            intelligence (int): The intelligence attribute of the character.
            wisdom (int): The wisdom attribute of the character.
            charisma (int): The charisma attribute of the character.
            hp (int): The hit points of the character.
            race (str): The name of the race of the character.
            class_ (str): The name of the class of the character.
            user (int): The ID of the user creating the character.
    """

    session = sessionmaker(bind=engine)
    session = session()
    race_ = session.query(Race).filter(Race.name == race).first()
    race_id = race_.id
    _class_ = session.query(Class).filter(Class.name == class_).first()
    class_id = _class_.id
    try:
        session.add(
            Character(
                name=name,
                strength=strength,
                dexterity=dexterity,
                constitution=constitution,
                intelligence=intelligence,
                wisdom=wisdom,
                charisma=charisma,
                hp=hp,
                race_id=race_id,
                class_id=class_id,
                user_id=user
            )
        )
        session.commit()
        messagebox.showinfo("Sweet!", "The character is created!")
        session.close()
    except TypeError:  # shouldn't really happen since it's taken care of in the entries
        print("Incorrect values")


def show_list(frame, attr, frame2):
    """
       Show a list of races or classes in a frame.

       Args:
           frame (tk.Frame): The frame to display the list in.
           attr (str): The attribute to show the list for ('race' or 'class').
           frame2 (tk.Frame): The frame to display traits when a race or class is selected.

       Returns:
           tk.StringVar: The selected race or class.
       """

    session = sessionmaker(bind=engine)
    session = session()
    if attr == "class":
        f = Class
    else:
        f = Race
    selected = tk.StringVar()
    for child in frame.winfo_children():
        child.destroy()
    chars = session.query(f).all()

    # create selectable buttons with all the available races/classes
    for i in chars:
        checkbox = tk.Radiobutton(frame, text=f"{i.name}", variable=selected, value=i.name,
                                  command=lambda i=i: display_traits(attr, i.name, frame2),
                                  font=("Garamond", 12, "bold"), bg="#4C3E32", fg="#E0D5C7",
                                  activebackground="#6C5748", activeforeground="#E0D5C7", relief=tk.FLAT)
        checkbox.pack(padx=5, pady=5)
    return selected


def find_user(user_name):
    """
       Find a user by their username.

       Args:
           user_name (str): The username of the user.

       Returns:
           User: The user object if found, None otherwise.
       """

    session = sessionmaker(bind=engine)
    session = session()
    user = session.query(User).filter(User.user_name == user_name).first()
    return user.id  # shouldn't be a None because it happen only after the user is found in the dedicated file


def add_user(user_name, password):
    """
        Adds a new user to the database.

        Args:
            user_name (str): The username of the user.
            password (str): The password of the user.
    """
    session = sessionmaker(bind=engine)
    session = session()
    session.add(User(user_name=user_name, password=password))
    session.commit()


def show_all_characters(user_id, list_box):
    """
       Displays all characters belonging to a specific user in a list box.

       Args:
           user_id (int): The ID of the user.
           list_box (tkinter.Listbox): The Tkinter Listbox widget to display the characters.
    """

    session = sessionmaker(bind=engine)
    session = session()
    characters = session.query(Character).filter(Character.user_id == user_id).all()
    for char in characters:
        list_box.insert(tk.END, f"{char.id} : {char.name}")


def show_char_stats(frame, char_id):
    """
       Displays the statistics of a character in a given frame.

       Args:
           frame (tkinter.Frame): The Tkinter Frame widget to display the character statistics.
           char_id (int): The ID of the character.
    """

    def is_int(_value):
        """
                Validates if a value is an integer.

                Args:
                    _value (str): The value to be validated.

                Returns:
                    bool: True if the value is a valid integer, False otherwise.
        """

        if _value.isdigit() or _value == '' or (_value == '-' and len(entry.get()) == 1):
            return True
        else:
            return False

    session = sessionmaker(bind=engine)
    session = session()
    for child in frame.winfo_children():
        if not isinstance(child, tk.Button):
            child.destroy()
    character = session.query(Character).filter(Character.id == char_id).first()

    # making the labels with the entries so that the user can modify some (but not all) stats
    i = 0
    for field, value in character.__dict__.items():
        if not field == "id" and not field == "_sa_instance_state" and not field == "user_id":
            label = tk.Label(frame, text=f"{field}:", bg="#AA3907", fg="#F5F6C8")
            label.grid(row=i, column=0, padx=10, pady=5)
            if field not in ["name", "race_id", "class_id"]:
                entry = tk.Entry(frame, validate="key", validatecommand=(frame.register(is_int), "%P"))
            else:
                entry = tk.Entry(frame)
            if field == "race_id" or field == "class_id":
                if field == "race_id":
                    the_race = session.query(Race).filter(Race.id == value).first()
                    the_name = the_race.name
                else:
                    the_class = session.query(Class).filter(Class.id == value).first()
                    the_name = the_class.name
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.config(state=tk.NORMAL)
                entry.insert(0, the_name)
                entry.config(state="readonly")
            else:
                entry.grid(row=i, column=1)
                entry.insert(0, f"{value}")
            i += 1


def change_character(char_id, name, strength, dexterity, constitution, intelligence, wisdom, charisma, hp):
    """
       Updates the attributes of a character with the provided values.

       Args:
           char_id (int): The ID of the character to be updated.
           name (str): The new name of the character.
           strength (int): The new strength attribute of the character.
           dexterity (int): The new dexterity attribute of the character.
           constitution (int): The new constitution attribute of the character.
           intelligence (int): The new intelligence attribute of the character.
           wisdom (int): The new wisdom attribute of the character.
           charisma (int): The new charisma attribute of the character.
           hp (int): The new hit points attribute of the character.
       """

    session = sessionmaker(bind=engine)
    session = session()
    character = session.query(Character).get(char_id)

    character.name = name
    character.strength = strength
    character.dexterity = dexterity
    character.constitution = constitution
    character.intelligence = intelligence
    character.wisdom = wisdom
    character.charisma = charisma
    character.hp = hp

    session.commit()
    messagebox.showinfo("Sweet!", "The character is updated!")
    session.close()
