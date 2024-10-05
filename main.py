import tkinter.messagebox
from tkinter import *
from random import randint
import time
import threading
# importing tkinter, random, time and threading modules

# please note that images are integral to this program
# the program can function without them, but it greatly hinders the aesthetics and beauty of the gui
# image sprites are created by me, with this model being the standard template from which all deviations stem:
# https://www.turbosquid.com/de/3d-models/human-male/370689

# most of the information about different widget options and methods used in this project
# is sourced from Tkinter 8.5 Reference: a GUI for python
# https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/index.html

# global variables that will hold current race/class/weapon images
# for the purpose of nor being deleted with garbage collector
global char_race, char_class, char_weapon

# main dictionary that will hold all characters, their attributes and stats
char_dict = dict()
# dictionary which holds current character's attributes
curr_dict = {'race': 'default', 'class': 'blank', 'weapon': 'blank'}
# dictionary which holds information about classes, displayed on screen
class_dict = dict()
# dictionary which holds information about races, displayed on screen
race_dict = dict()
# dictionary which holds current generated stats of a character
stat_dict = {'STR': '', 'CON': '', 'DEX': '', 'INT': '', 'WIS': '', 'CHA': ''}
# dictionary which holds information about racial bonuses to stats
race_bonus = {'dragonborn': ['2', '0', '0', '0', '0', '2'], 'human': ['0', '2', '0', '2', '0', '0'],
              'elf': ['0', '0', '2', '0', '2', '0'], 'tiefling': ['0', '0', '0', '2', '0', '2']}
# dictionary which holds information about weapon stats, their damage, type and proficiency bonus
weapon_stat = {'sword': '1d8, Heavy Blade, +3', 'warhammer': '1d10, Hammer, +2',
               'staff': '1d6, Mace, +2', 'dagger': '1d4, Light Blade, +3'}
color_dict = {'dragonborn': 'blue', 'tiefling': 'dark red', 'human': 'grey', 'elf': 'green', 'cleric': 'dark blue',
              'paladin': 'black', 'wizard': 'magenta', 'rogue': 'dark grey', 'sword': 'grey', 'warhammer': 'gold',
              'staff': 'brown', 'dagger': 'black', 'blank': 'white'}


# ---------------------------------------- Function are defined in next section ----------------------------------------


def import_chars():
    """
    this function opens a save file and transfers characters and their attributes from save file to char_dict
    :return:
    """
    # if there is FileNotFoundError, a messagebox pops up with a warning. the app can function without save file,
    # since creating and saving new characters will create a saving file anew
    try:
        save_file = open("store_char.txt", 'r')
        in_list = save_file.readlines()
    except FileNotFoundError:
        tkinter.messagebox.showerror(title='File Error', message='Save file not found, please check files',
                                     default='ok', icon='warning')
    else:
        # if there is a save file, characters from it are written into char_dict
        # for each line = for each character
        for i in range(len(in_list)):
            x = in_list[i].rstrip('\n')
            x = x.split(' - ')
            char_dict[x[0]] = {'class': x[1], 'race': x[2], 'weapon': x[3], 'STR': x[4], 'CON': x[5], 'DEX': x[6],
                   'INT': x[7], 'WIS': x[8], 'CHA': x[9]}

            # each character is stored in a string, where all attributes are separated by ' - '. Attributes are:
            # Name - class - race - weapon - strength score - constitution score - dexterity score
            # - intelligence score - wisdom score - charisma score

        save_file.close()


def export_chars():
    """
    this function opens a save file and transfers characters and their attributes from char_dict to save file
    :return:
    """

    save_file = open("store_char.txt", 'w')
    upl = ''

    # for each character the attributes are joined with ' - ' as separator,
    # all lines are joined with '\n', and the save file is rewritten.

    for i in char_dict:
        tmp = i + ' - ' + ' - '.join(list(char_dict[i].values()))
        upl += tmp + '\n'
    save_file.write(upl)
    save_file.close()


def import_class():
    """
    this function opens files with information about classes and puts that information in class_dict,
    with class names serving as keys and text blocks as values
    :return:
    """
    lst = ['paladin', 'cleric', 'rogue', 'wizard']
    # if there is FileNotFoundError - message pops up and app terminates, since class information cannot be displayed
    try:
        for i in lst:
            info_class = open('class_info/' + i + '_info.txt', 'r')
            class_dict[i] = info_class.read()
            info_class.close()
    except FileNotFoundError:
        tkinter.messagebox.showerror(title='File Error', message='Class information files not found, please check '
                                                                 'files, app terminated', default='ok', icon='error')
        quit()


def import_race():
    """
    this function opens files with information about races and puts that information in race_dict,
    with race names serving as keys and text blocks as values
    :return:
    """
    lst = ['dragonborn', 'human', 'tiefling', 'elf']
    # if there is FileNotFoundError - message pops up and app terminates, since race information cannot be displayed
    try:
        for i in lst:
            info_race = open('race_info/' + i + '_info.txt', 'r')
            race_dict[i] = info_race.read()
            info_race.close()
    except FileNotFoundError:
        tkinter.messagebox.showerror(title='File Error', message='Race information files not found, please check '
                                                                 'files, app terminated', default='ok', icon='error')
        quit()


def update_layers(images_present):
    """
    this function is called every time displayed character attribute is changed.
    this function uses global variables and redraws character in correct layer order
    if there are no images, function draws placeholder squares
    :return:
    """
    global char_race, char_class, char_weapon
    if images_present:
        race_layer = C.create_image(600, 0, image=char_race, anchor='n')
        class_layer = C.create_image(600, 0, image=char_class, anchor='n')
        weapon_layer = C.create_image(600, 0, image=char_weapon, anchor='n')
    else:
        race_layer = C.create_rectangle(450, 40, 750, 180, fill=color_dict[curr_dict['race']])
        C.create_text(600, 110, fill='white', text=curr_dict['race'])
        class_layer = C.create_rectangle(450, 180, 750, 320, fill=color_dict[curr_dict['class']])
        C.create_text(600, 250, fill='white', text=curr_dict['class'])
        weapon_layer = C.create_rectangle(450, 320, 750, 460, fill=color_dict[curr_dict['weapon']])
        C.create_text(600, 390, fill='white', text=curr_dict['weapon'])


def spawn_char(name):
    """
    this function sets selected character to be the current one displayed
    :param name:
    :return:
    """
    global char_race, char_class, char_weapon

    # Character's name is displayed in entry field
    entry_var.set(name)

    # each stat in stat_dict is assigned a corresponding value from char_dict[name]
    for i in stat_dict:
        stat_dict[i] = char_dict[name][i]
    # stats are displayed
    assign_stats(stat_dict)
    # final scores are calculated and displayed
    set_final_scores()

    # current character's race, class and weapon are set with set_race, set_class and set_weapon respectively
    set_race(char_dict[name]['race'])
    set_class(char_dict[name]['class'])
    set_weapon(char_dict[name]['weapon'])


def set_race(race_name):
    """
    this function updates current character's race to be race_name
    :param race_name:
    :return:
    """
    global char_race, char_class, char_weapon, images_present
    # curr_dict['race'] is updated to be selected race
    curr_dict['race'] = race_name
    images_present = True
    # if the image file cannot be found - app terminates, since image sprites are central to this app
    try:
        # global char_race is updated with corresponding image
        char_race = PhotoImage(file='images/sprites/' + race_name + '.png')
    except:
        images_present = False
    finally:
        # information variable is updated with corresponding text
        race_info_var.set(race_dict[race_name])

        # racial modifiers are updated according to race_bonus dictionary, final scores are calculated and displayed
        str_rmod_var.set('+' + race_bonus[race_name][0])
        con_rmod_var.set('+' + race_bonus[race_name][1])
        dex_rmod_var.set('+' + race_bonus[race_name][2])
        int_rmod_var.set('+' + race_bonus[race_name][3])
        wis_rmod_var.set('+' + race_bonus[race_name][4])
        cha_rmod_var.set('+' + race_bonus[race_name][5])
        set_final_scores()

        # finally, layers are redrawn in order
        update_layers(images_present)


def set_class(class_name):
    """
    this function updates current character's class to be class_name
    :param class_name:
    :return:
    """
    global char_race, char_class, char_weapon, images_present
    # curr_dict['class'] is updated to be selected class
    curr_dict['class'] = class_name
    images_present = True
    # if the image file cannot be found - app terminates, since image sprites are central to this app
    try:
        # global char_class is updated with corresponding image
        char_class = PhotoImage(file='images/sprites/' + class_name + '.png')
    except:
        images_present = False
    finally:
        # info box is updated with corresponding class information text
        change_info()
        # since not all classes can use same weapons, weapon menu is updated with weapons corresponding to class
        update_weapon_menu(class_name)
        # if a weapon was set previously, it is now set to blank image
        set_weapon('blank')
        # finally, layers are redrawn in order
        update_layers(images_present)


def set_weapon(weapon_name):
    """
    this function updates current character's weapon to be weapon_name
    :param weapon_name:
    :return:
    """
    global char_race, char_class, char_weapon, images_present
    # curr_dict['weapon'] is updated to be selected weapon
    curr_dict['weapon'] = weapon_name
    images_present = True
    # if the image file cannot be found - app terminates, since image sprites are central to this app
    try:
        # global char_weapon is updated with corresponding image
        char_weapon = PhotoImage(file='images/sprites/' + weapon_name + '.png')
    except:
        images_present = False
    finally:
        # if weapon is not blank, display info about this weapon, according to weapon_stat[weapon_name]
        if weapon_name != 'blank':
            weapon_info_var.set(weapon_name.capitalize() + "\nDamage, weapon type, proficiency "
                                                           "bonus:\n" + weapon_stat[weapon_name])
        else:
            weapon_info_var.set('')
        # finally, layers are redrawn in order
        update_layers(images_present)


def update_weapon_menu(class_name):
    """
    since not all classes can use same weapons, each time class is updated the weapon selection menu also has to be.
    this function updates weapon selection menu according to chosen class
    :param class_name:
    :return:
    """
    # this dictionary holds 'class to weapons' correspondence
    c_to_w = {'paladin': ('Sword', 'Warhammer'), 'rogue': ('Sword', 'Dagger'),
              'cleric': ('Staff', 'Warhammer'), 'wizard': ('Staff', 'Dagger')}
    # this is a list of all available weapons
    all_weapon = ['Sword', 'Warhammer', 'Dagger', 'Staff']
    # all weapons currently in menu are deleted
    m_weapon.menu.delete(0, 2)
    # all weapons are added again as radio buttons with set_weapon as command
    # When pressed, button calls set_weapon with weapon corresponding to button pressed
    m_weapon.menu.add_radiobutton(label="Sword", variable=weaponVar, value='sword',
                                  command=lambda: set_weapon(weaponVar.get()))
    m_weapon.menu.add_radiobutton(label="Warhammer", variable=weaponVar, value='warhammer',
                                  command=lambda: set_weapon(weaponVar.get()))
    m_weapon.menu.add_radiobutton(label="Staff", variable=weaponVar, value='staff',
                                  command=lambda: set_weapon(weaponVar.get()))
    m_weapon.menu.add_radiobutton(label="Dagger", variable=weaponVar, value='dagger',
                                  command=lambda: set_weapon(weaponVar.get()))
    # all weapons, not corresponding to this class, are deleted
    for i in all_weapon:
        if i not in c_to_w[class_name]:
            m_weapon.menu.delete(i)


def merge(lst1, lst2, lst3):
    """
    function merge takes in three lists. it then merges first two lists into the third one
    :param lst1:
    :param lst2:
    :param lst3:
    :return:
    """
    # i1, i2, i3 are created for iteration through lists
    i1, i2, i3 = 0, 0, 0
    # n1 and n2 are lengths of lst1 and lst2 respectively
    n1, n2 = len(lst1), len(lst2)
    # while lst1 and lst2 have not been iterated through fully
    while i1 < n1 and i2 < n2:
        # if current element of lst1 is less than current element of lst2, write it to lst3, i1++
        if lst1[i1] < lst2[i2]:
            lst3[i3] = lst1[i1]
            i1 += 1
        # otherwise write element of lst2 to lst3, i2++
        else:
            lst3[i3] = lst2[i2]
            i2 += 1
        # i3 is also iterated up
        i3 += 1
    while i1 < n1:
        # if any elements of lst1 are left - finish putting them in lst3
        lst3[i3] = lst1[i1]
        i1 += 1
        i3 += 1
    while i2 < n2:
        # if any elements of lst2 are left - finish putting them in lst3
        lst3[i3] = lst2[i2]
        i2 += 1
        i3 += 1


def sort_m(lst_inp):
    """
    sort_m is a merge sort algorithm that recursively calls itself to sort a list
    :param lst_inp:
    :return:
    """
    n = len(lst_inp)
    if n > 1:
        # if length of a list is more than one - list is split in 2,
        # each part is passed through merge sort, and then merged
        m = n//2
        lst_1, lst_2 = lst_inp[:m], lst_inp[m:]
        sort_m(lst_1)
        sort_m(lst_2)
        merge(lst_1, lst_2, lst_inp)


def assign_stats(dct):
    """
    this function configures labels in 1st column with corresponding stats from input dictionary dct
    :param dct:
    :return:
    """
    l_str_score.configure(text=dct['STR'])
    l_con_score.configure(text=dct['CON'])
    l_dex_score.configure(text=dct['DEX'])
    l_int_score.configure(text=dct['INT'])
    l_wis_score.configure(text=dct['WIS'])
    l_cha_score.configure(text=dct['CHA'])


def roll_stats():
    """
    this function uses classic 'roll 4d6 drop lowest' algorithm to generate stats for the character
    :return:
    """
    # temporary list to hold generated stats
    arr = []
    global stat_dict
    # 6 times, for each stat in str, con, dex, int, wis, cha, happens following:
    for i in range(6):
        # temporary list to hold individual dice rolls
        roll = []
        # 4 times a random number from 1 to 6 is generated, 'a d6 die is rolled', and appended into roll
        for j in range(4):
            roll.append(randint(1, 6))
        # roll is sorted with merge sort, so that lowest number is 0th element
        sort_m(roll)
        # all generated numbers apart from lowest (0th) are added together to get a value and assigned to arr
        arr.append(roll[1]+roll[2]+roll[3])
    # all values are converted to strings
    arr = [str(el) for el in arr]
    # iterating through stat_dict, each stat is assigned a value in order
    i = 0
    for j in stat_dict:
        stat_dict[j] = arr[i]
        i += 1
    # stats are displayed
    assign_stats(stat_dict)
    # final scores are calculated and displayed
    set_final_scores()
    return arr


def set_final_scores():
    """
    final scores are calculated taking in consideration racial modifiers and displayed
    ability modifiers are calculated from final scores and displayed
    :return:
    """
    # if stat_dict is not empty
    if stat_dict['STR']:
        # for each stat variable: generated score from stat_dict is converted to integer,
        # racial modifier is stripped of '+', converted to integer, they are added together and converted to string.
        # stat variable is set to this new value.
        str_var.set(str(int(stat_dict['STR']) + int(str_rmod_var.get().strip('+'))))
        con_var.set(str(int(stat_dict['CON']) + int(con_rmod_var.get().strip('+'))))
        dex_var.set(str(int(stat_dict['DEX']) + int(dex_rmod_var.get().strip('+'))))
        int_var.set(str(int(stat_dict['INT']) + int(int_rmod_var.get().strip('+'))))
        wis_var.set(str(int(stat_dict['WIS']) + int(wis_rmod_var.get().strip('+'))))
        cha_var.set(str(int(stat_dict['CHA']) + int(cha_rmod_var.get().strip('+'))))

        # for each ability modifier:
        # modifier is calculated with formula '(score-10)/2 round down' and temporarily stored in tmp
        # corresponding ability modifier variable is set to this value, which is modified depending on its sign:
        # If the nuber is negative, i.e. it already has a '-' sign - nothing changes
        # If it's positive, i.e. has no sign in front of it - '+' sign is added
        tmp = str((int(str_var.get())-10)//2)
        l_str_mod.configure(text=('+' + tmp if '-' not in tmp else '' + tmp))
        tmp = str((int(con_var.get()) - 10) // 2)
        l_con_mod.configure(text=('+' + tmp if '-' not in tmp else '' + tmp))
        tmp = str((int(dex_var.get()) - 10) // 2)
        l_dex_mod.configure(text=('+' + tmp if '-' not in tmp else '' + tmp))
        tmp = str((int(int_var.get()) - 10) // 2)
        l_int_mod.configure(text=('+' + tmp if '-' not in tmp else '' + tmp))
        tmp = str((int(wis_var.get()) - 10) // 2)
        l_wis_mod.configure(text=('+' + tmp if '-' not in tmp else '' + tmp))
        tmp = str((int(cha_var.get()) - 10) // 2)
        l_cha_mod.configure(text=('+' + tmp if '-' not in tmp else '' + tmp))

        # if class is not 'blank', the info box is updated, because it uses stats and modifiers for AC and HP
        if curr_dict['class'] != 'blank':
            change_info()


def change_info():
    """
    info box is updated with information text corresponding to current class
    :return:
    """
    # class_name is set to current class
    class_name = curr_dict['class']
    # dictionary which holds hp values corresponding to classes
    hp_dict = {'cleric': 12, 'paladin': 15, 'rogue': 12, 'wizard': 10}

    # if stat_dict is not empty, i.e. stats are known - ac and hp calculated normally
    if stat_dict['STR']:
        # hit points are calculated with hp values from hp_dict and constitution score from con_var, turned to strings
        hp = str(hp_dict[class_name] + int(con_var.get()))
        # armor class, based on class is either set or calculated by formula '10 + greater of int and dex modifiers'
        if class_name == 'cleric':
            ac = '16'
        elif class_name == 'paladin':
            ac = '18'
        else:
            ac = str(10 + max((int(int_var.get()) - 10) // 2, (int(dex_var.get()) - 10) // 2))
    # otherwise, message 'Determined by ability scores' is displayed
    else:
        hp = 'Determined by ability scores'
        ac = 'Determined by ability scores'

    # text_hp is updated with hp and ac values
    text_hp = 'Hit Points on first level: ' + str(hp) + '\nArmor Class on first level: ' + str(ac) + '\n\n'
    # info_var is updated with text_hp and information corresponding to class from class_dict
    info_var.set(text_hp + class_dict[class_name])


def add_new_char():
    """
    this function saves current character to char_dict.
    :return:
    """
    # name is set to value in entry_var
    name = entry_var.get()
    # if character is not ready (see char_ready())
    if char_ready()[0]:
        # exist is a flag that gets raised if a character with that name already exists in char_dict
        exist = False
        if name in char_dict.keys():
            exist = True
        # char_dict is updated with name as a key and a dictionary as value
        # In the nested dictionary, class, race and weapon are set to corresponding values from curr_dict
        char_dict[name] = {'class': curr_dict['class'], 'race': curr_dict['race'], 'weapon': curr_dict['weapon']}
        # iterating through stat_dict, stats in char_dict[name] are assigned corresponding values from stat_dict
        for j in stat_dict:
            char_dict[name][j] = stat_dict[j]
        # char_dict is exported to save file
        export_chars()
        # if the character did not exist, a button is created for them
        if not exist:
            # "lambda name=name:" as well as all subsequent lambda variable=variable type solutions are adapted from
            # https://stackoverflow.com/questions/10865116/tkinter-creating-buttons-in-for-loop-passing-command-arguments
            b_char = Button(frame_char_sel, text=name, relief=GROOVE, command=lambda name=name: spawn_char(name),
                            bg='black', fg='white')
            b_char.pack(fill='x', anchor='w')

    # regardless of readiness, message in l_error is changed to be a message delivered by char_ready()
    l_error.configure(text=char_ready()[1])

    # Define function for waiting 3 seconds and then removing error message
    def clear_error_message():
        time.sleep(3)  # Wait for 3 seconds
        l_error.configure(text='')

    # thread is started once error or success message is set, and clear_error_message is ran.
    # threading is needed, because otherwise sleep is freezing the whole app
    # the threading solution is adapted from:
    # https://stackoverflow.com/questions/55551007/how-to-make-a-timer-in-python-without-freezing-up-the-entire-code
    threading.Thread(target=clear_error_message).start()


def char_ready():
    """
    this functions checks is the character has his class, race, weapon, name and stats selected
    :return:
    """
    # by default character is ready and message is 'Success!'
    ans = (True, 'Success!')
    # if stat_dict['STR'] is empty == if stats are not generated, character set to not ready and error message added
    if not stat_dict['STR']:
        ans = (False, 'Error: please generate stats')
    # if curr_dict['weapon'] is empty or set to blank, character set to not ready and error message added
    if not curr_dict['weapon'] or curr_dict['weapon'] == 'blank':
        ans = (False, 'Error: please select weapon')
    # if curr_dict['class'] is empty or set to blank, character set to not ready and error message added
    if not curr_dict['class'] or curr_dict['class'] == 'blank':
        ans = (False, 'Error: please select class')
    # if curr_dict['race'] is empty or set to default, character set to not ready and error message added
    if not curr_dict['race'] or curr_dict['race'] == 'default':
        ans = (False, 'Error: please select race')
    # if entry_var is empty - name is not set, character set to not ready and error message added
    if not entry_var.get():
        ans = (False, 'Error: please select name')

    return ans


# ---------------------------------------- Functions definition area is finished ---------------------------------------


# window is created, given name, size. Set to non-resizable

top = Tk()
top.title('Character Creator')
top.geometry('1200x750')
top.resizable(width=False, height=False)

# variables that will hold final scores and racial modifiers are created for each stat: str, con, dex, int, wis, cha

str_var = StringVar()
con_var = StringVar()
dex_var = StringVar()
int_var = StringVar()
wis_var = StringVar()
cha_var = StringVar()
str_rmod_var = StringVar()
con_rmod_var = StringVar()
dex_rmod_var = StringVar()
int_rmod_var = StringVar()
wis_rmod_var = StringVar()
cha_rmod_var = StringVar()

# canvas is created

C = Canvas(top, height=750, width=1200, bg='black')
C.pack(fill='both', expand=True)

# if parchment.png is found, background is set.
# otherwise, background is set to an approximate colour and warning message pops up
try:
    bg = PhotoImage(file='images/parchment.png')
    C.create_image(0, 0, image=bg, anchor='nw')
except:
    C.configure(bg='#e3c076')

# if frame.png is found, frame is set.
# otherwise, a makeshift frame is created from a rectangle and warning message pops up
try:
    frame_img = PhotoImage(file='images/frame.png')
    C.create_image(600, 0, image=frame_img, anchor='n')
except:
    C.create_rectangle(440, 10, 760, 490, outline='black', width=5, stipple='gray25', fill='black')


# frames and windows on Canvas are created:

# frame_rcw_sel is for selection of race, class, weapon, name input/display, and display of race info and weapon info
frame_rcw_sel = LabelFrame(C, padx=10, pady=10, bg='black', bd=2)
frame_rcw_sel.pack(padx=20, pady=20, anchor='nw')
C.create_window(215, 140, window=frame_rcw_sel, height=240, width=390)

# frame_stat holds table with information about generated stats, racial modifiers, final stats and ability modifiers,
# as well as a button which generates stats
frame_stat = LabelFrame(C, pady=10, padx=10, bg='black', bd=2)
frame_stat.pack(padx=20, pady=20, anchor='w')
# creates rectangle for design purposes
C.create_rectangle(20, 280, 410, 730, fill='black', stipple='gray75')
C.create_window(215, 505, window=frame_stat, height=450, width=270)

# frame_char_info is for class information, abilities, hit points and armor class, displayed below character images
frame_char_info = LabelFrame(C, pady=10, bg='black', bd=2)
frame_char_info.pack(padx=20, pady=20, anchor='w')
C.create_window(600, 625, window=frame_char_info, height=210, width=320)

# frame_char_sel holds all characters that can be selected and 'spawned', as well as a button to save current character
frame_char_sel = LabelFrame(C, padx=10, pady=10, bg='black', bd=2)
frame_char_sel.pack(padx=20, pady=20, anchor='nw')
C.create_window(975, 190, window=frame_char_sel, height=340, width=390)

# frame instruct holds instructions and advice on using this program
frame_instruct = LabelFrame(C, pady=10, padx=10, bg='black', bd=2)
frame_instruct.pack(padx=20, pady=20, anchor='w')
C.create_window(975, 555, window=frame_instruct, height=350, width=390)

# character are imported into char_dict. Class and race information texts are also imported
import_chars()
import_class()
import_race()

# label with instruction
l_load = Label(frame_char_sel, text='Select a character to load in or save the current one:',
               bg='black', fg='white', justify='center')
l_load.pack()
# for each character in char_dict, a button is created. this button calls spawn_char(character)
for char in char_dict:
    b_char = Button(frame_char_sel, text=char, relief=GROOVE, command=lambda char=char: spawn_char(char),
                    bg='black', fg='white')
    b_char.pack(fill='x', anchor='w')
# a button at the bottom side is created which calls add_new_char()
b_new_char = Button(frame_char_sel, text='Save Character', relief=GROOVE, bg='black', fg='white', command=add_new_char)
b_new_char.pack(side='bottom', anchor='sw')
# label for error message, modified by add_new_char()
l_error = Label(frame_char_sel, text='', bg='black', fg='white')
l_error.pack(side='bottom', anchor='se')


# label with instructions
l_name_text = Label(frame_rcw_sel, text='Please enter name of the character, select race, class and weapon: ',
                    bg='black', fg='white')
l_name_text.grid(row=0, column=0, columnspan=4)
# entry field to enter name, entry_var to store it. when character is loaded - their name is displayed there too
entry_var = StringVar()
e_name = Entry(frame_rcw_sel, textvariable=entry_var, bd=5, bg='black', fg='white')
e_name.grid(row=1, column=0)

# menu for races is created. for each race a radiobutton is created, each button calls set_race(chosen race)

m_race = Menubutton(frame_rcw_sel, text="Select race:", relief=RAISED, bg='black', fg='white')
m_race.grid(row=1, column=1)  # most widgets here are packed in a grid
m_race.menu = Menu(m_race, tearoff=0)
m_race["menu"] = m_race.menu
raceVar = StringVar()
m_race.menu.add_radiobutton(label="Dragonborn", variable=raceVar, value='dragonborn',
                            command=lambda: set_race(raceVar.get()))
m_race.menu.add_radiobutton(label="Human", variable=raceVar, value='human',
                            command=lambda: set_race(raceVar.get()))
m_race.menu.add_radiobutton(label="Tiefling", variable=raceVar, value='tiefling',
                            command=lambda: set_race(raceVar.get()))
m_race.menu.add_radiobutton(label="Elf", variable=raceVar, value='elf',
                            command=lambda: set_race(raceVar.get()))

# menu for classes is created. for each class a radiobutton is created, each button calls set_class(chosen class)

m_class = Menubutton(frame_rcw_sel, text="Select class:", relief=RAISED, bg='black', fg='white')
m_class.grid(row=1, column=2)
m_class.menu = Menu(m_class, tearoff=0)
m_class["menu"] = m_class.menu
classVar = StringVar()
m_class.menu.add_radiobutton(label="Paladin", variable=classVar, value='paladin',
                             command=lambda: set_class(classVar.get()))
m_class.menu.add_radiobutton(label="Cleric", variable=classVar, value='cleric',
                             command=lambda: set_class(classVar.get()))
m_class.menu.add_radiobutton(label="Rogue", variable=classVar, value='rogue',
                             command=lambda: set_class(classVar.get()))
m_class.menu.add_radiobutton(label="Wizard", variable=classVar, value='wizard',
                             command=lambda: set_class(classVar.get()))

# menu for weapons is created. a radiobutton for no weapons is created.

m_weapon = Menubutton(frame_rcw_sel, text="Select weapon:", relief=RAISED, bg='black', fg='white')
m_weapon.grid(row=1, column=3)
m_weapon.menu = Menu(m_weapon, tearoff=0)
m_weapon["menu"] = m_weapon.menu
weaponVar = StringVar()
m_weapon.menu.add_radiobutton(label="No weapon", variable=weaponVar, value='blank',
                              command=lambda: set_weapon(weaponVar.get()))

# this label is located under menus and entry field. once race is selected,
# race_info_var is set to information about race by set_race. rowconfigure adds padding between rows in grid
race_info_var = StringVar()
l_race_info = Label(frame_rcw_sel, textvariable=race_info_var, bg='black', fg='white')
l_race_info.grid(row=2, column=0, columnspan=4)
frame_rcw_sel.rowconfigure(2, pad=15)

# this label is located under racial info variable. once weapon is selected,
# weapon_info_var is set to information about weapon by set_weapon
weapon_info_var = StringVar()
l_weapon_info = Label(frame_rcw_sel, textvariable=weapon_info_var, bg='black', fg='white')
l_weapon_info.grid(row=3, column=0, columnspan=4)


# this is top row of a table that contains ability scores. it has names for every column.
# zeroth column is the name of the ability, first column is for score generated with roll_stats and stored in stat_dict
# second column is for racial modifiers, set when race is selected. third column is for final ability scores
# final column is for ability modifier, which is calculated from final ability scores
l_stat_1 = Label(frame_stat, text='Ability\nname', bg='black', fg='white', relief=RAISED)
l_stat_1.grid(row=0, column=0)
l_stat_2 = Label(frame_stat, text='Generated\nscore', bg='black', fg='white', relief=RAISED)
l_stat_2.grid(row=0, column=1)
l_stat_3 = Label(frame_stat, text='Racial\nmodifier', bg='black', fg='white', relief=RAISED)
l_stat_3.grid(row=0, column=2)
l_stat_4 = Label(frame_stat, text='Ability\nscore', bg='black', fg='white', relief=RAISED)
l_stat_4.grid(row=0, column=3)
l_stat_5 = Label(frame_stat, text='Ability\nmodifier', bg='black', fg='white', relief=RAISED)
l_stat_5.grid(row=0, column=4)

# this is the strength (STR) row of ability score table, all columns are set the way they are described above
l_str = Label(frame_stat, text=' STR ', bg='black', fg='white', relief=RAISED)
l_str.grid(row=1, column=0)
l_str_score = Label(frame_stat, text='', bg='black', fg='white')
l_str_score.grid(row=1, column=1)
l_str_race = Label(frame_stat, textvariable=str_rmod_var, bg='black', fg='white')
str_rmod_var.set('+0') # racial modifier  is set to +0 by default
l_str_race.grid(row=1, column=2)
l_str_f_score = Label(frame_stat, textvariable=str_var, bg='black', fg='white')
l_str_f_score.grid(row=1, column=3)
l_str_mod = Label(frame_stat, text='', bg='black', fg='white')
l_str_mod.grid(row=1, column=4)

# this is the constitution (CON) row of ability score table
l_con = Label(frame_stat, text=' CON ', bg='black', fg='white', relief=RAISED)
l_con.grid(row=2, column=0)
l_con_score = Label(frame_stat, text='', bg='black', fg='white')
l_con_score.grid(row=2, column=1)
l_con_race = Label(frame_stat, textvariable=con_rmod_var, bg='black', fg='white')
con_rmod_var.set('+0')
l_con_race.grid(row=2, column=2)
l_con_f_score = Label(frame_stat, textvariable=con_var, bg='black', fg='white')
l_con_f_score.grid(row=2, column=3)
l_con_mod = Label(frame_stat, text='', bg='black', fg='white')
l_con_mod.grid(row=2, column=4)

# this is the dexterity (DEX) row of ability score table
l_dex = Label(frame_stat, text=' DEX ', bg='black', fg='white', relief=RAISED)
l_dex.grid(row=3, column=0)
l_dex_score = Label(frame_stat, text='', bg='black', fg='white')
l_dex_score.grid(row=3, column=1)
l_dex_race = Label(frame_stat, textvariable=dex_rmod_var, bg='black', fg='white')
dex_rmod_var.set('+0')
l_dex_race.grid(row=3, column=2)
l_dex_f_score = Label(frame_stat, textvariable=dex_var, bg='black', fg='white')
l_dex_f_score.grid(row=3, column=3)
l_dex_mod = Label(frame_stat, text='', bg='black', fg='white')
l_dex_mod.grid(row=3, column=4)

# this is the intelligence (INT) row of ability score table
l_int = Label(frame_stat, text=' INT ', bg='black', fg='white', relief=RAISED)
l_int.grid(row=4, column=0)
l_int_score = Label(frame_stat, text='', bg='black', fg='white')
l_int_score.grid(row=4, column=1)
l_int_race = Label(frame_stat, textvariable=int_rmod_var, bg='black', fg='white')
int_rmod_var.set('+0')
l_int_race.grid(row=4, column=2)
l_int_f_score = Label(frame_stat, textvariable=int_var, bg='black', fg='white')
l_int_f_score.grid(row=4, column=3)
l_int_mod = Label(frame_stat, text='', bg='black', fg='white')
l_int_mod.grid(row=4, column=4)

# this is the wisdom (WIS) row of ability score table
l_wis = Label(frame_stat, text=' WIS ', bg='black', fg='white', relief=RAISED)
l_wis.grid(row=5, column=0)
l_wis_score = Label(frame_stat, text='', bg='black', fg='white')
l_wis_score.grid(row=5, column=1)
l_wis_race = Label(frame_stat, textvariable=wis_rmod_var, bg='black', fg='white')
wis_rmod_var.set('+0')
l_wis_race.grid(row=5, column=2)
l_wis_f_score = Label(frame_stat, textvariable=wis_var, bg='black', fg='white')
l_wis_f_score.grid(row=5, column=3)
l_wis_mod = Label(frame_stat, text='', bg='black', fg='white')
l_wis_mod.grid(row=5, column=4)

# this is the charisma (CHA) row of ability score table
l_cha = Label(frame_stat, text=' CHA ', bg='black', fg='white', relief=RAISED)
l_cha.grid(row=6, column=0)
l_cha_score = Label(frame_stat, text='', bg='black', fg='white')
l_cha_score.grid(row=6, column=1)
l_cha_race = Label(frame_stat, textvariable=cha_rmod_var, bg='black', fg='white')
cha_rmod_var.set('+0')
l_cha_race.grid(row=6, column=2)
l_cha_f_score = Label(frame_stat, textvariable=cha_var, bg='black', fg='white')
l_cha_f_score.grid(row=6, column=3)
l_cha_mod = Label(frame_stat, text='', bg='black', fg='white')
l_cha_mod.grid(row=6, column=4)

# this button is at the bottom of the table, it calls roll_stats() to generate stats when pressed
b_roll = Button(frame_stat, text='Press to generate\nability scores', relief=RAISED, bg='black', fg='white',
                command=lambda: roll_stats())
b_roll.grid(row=7, column=0, columnspan=2)

# rowconfigure adds vertical padding to each row in a table
for i in range(0, 7):
    frame_stat.rowconfigure(i, pad=30)


# this variable is updated by change_info() when either class is changed or ability scores are changed
info_var = StringVar()
l_info = Label(frame_char_info, textvariable=info_var, bg='black', fg='white')
l_info.pack()

# app tries to get text for the text widget from file. if the file is not found, a shorter message is inserted instead
# finally means that a text widget is created anyway
try:
    file = open('instruct.txt', 'r')
    txt = file.read()
except FileNotFoundError:
    tkinter.messagebox.showerror(title='File Error', message='Instructions failed to load, please check files',
                                 default='ok', icon='warning')
    txt = 'Welcome to a Character Creator app, inspired by Dungeons & Dragons 4th Edition!'
finally:
    t_instruct_all = Text(frame_instruct, bg='black', fg='white', font='Times', bd=0, wrap=WORD)
    t_instruct_all.insert(2.0, txt)
    t_instruct_all.configure(state=DISABLED)
    t_instruct_all.pack(anchor='n')

# when program is first run, the character on screen is a placeholder,
# where body is default.png, and class and weapon images are blank (blank.png)
# program attempts to load them, if not possible - terminates
# update layers is run to make sure they are in order
try:
    char_race = PhotoImage(file='images/sprites/default.png')
    char_class = PhotoImage(file='images/sprites/blank.png')
    char_weapon = PhotoImage(file='images/sprites/blank.png')
    images_present = True
    update_layers(images_present)
except:
    images_present = False


top.mainloop()
