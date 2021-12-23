# Imports--------------------------------------------------------------------
from tkinter import *
from tkinter import filedialog, StringVar, ttk, messagebox
import subprocess
import tkinter as tk
import pathlib
import tkinter.scrolledtext as scrolledtextwidget
from TkinterDnD2 import *
from ISO_639_2 import *


# Main Gui & Windows --------------------------------------------------------
def mp4_root_exit_function():
    confirm_exit = messagebox.askyesno(title='Prompt', message="Are you sure you want to exit the program?\n\n"
                                                               "     Note: This will end all current tasks!",
                                       parent=mp4_root)
    if confirm_exit:
        try:
            subprocess.Popen(f"TASKKILL /F /im MP4-Mux-Tool.exe /T", creationflags=subprocess.CREATE_NO_WINDOW)
            mp4_root.destroy()
        except (Exception,):
            mp4_root.destroy()


mp4_root = TkinterDnD.Tk()
mp4_root.title("MP4-Mux-Tool Beta v1.0")
# mp4_root.iconphoto(True, PhotoImage(file="Runtime/Images/topbar.png"))
mp4_root.configure(background="#434547")
window_height = 720
window_width = 630
screen_width = mp4_root.winfo_screenwidth()
screen_height = mp4_root.winfo_screenheight()
x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))
mp4_root.geometry(f'{window_width}x{window_height}+{x_coordinate}+{y_coordinate}')
mp4_root.protocol('WM_DELETE_WINDOW', mp4_root_exit_function)


# Themes --------------------------------------------------------------------------------------------------------------
# Combobox Theme-----------------------------------------
custom_menu_theme = ttk.Style()
custom_menu_theme.theme_create('combostyle', parent='alt', settings={'TCombobox':
                                                                         {'configure': {'selectbackground': '#23272A',
                                                                                        'fieldbackground': '#23272A',
                                                                                        'background': 'white',
                                                                                        'foreground': 'white'}}})
custom_menu_theme.theme_use('combostyle')
mp4_root.option_add('*TCombobox*Listbox*Background', '#404040')
mp4_root.option_add('*TCombobox*Listbox*Foreground', '#FFFFFF')
mp4_root.option_add('*TCombobox*Listbox*selectBackground', '#FFFFFF')
mp4_root.option_add('*TCombobox*Listbox*selectForeground', '#404040')
custom_menu_theme.map('TCombobox', foreground=[('hover', 'white')], background=[('hover', 'grey')])


# ------------------------------------------ Combobox Theme

# Hover over button theme ---------------------------------
class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground


# -------------------------------- Hover over button theme
# -------------------------------------------------------------------------------------------------------------- Themes


# root.grid_columnconfigure(0, weight=1)
# root.grid_columnconfigure(1, weight=1)
# root.grid_columnconfigure(2, weight=1)
# root.grid_columnconfigure(3, weight=1)
# root.grid_rowconfigure(0, weight=1)
# root.grid_rowconfigure(1, weight=1)
# root.grid_rowconfigure(2, weight=1)
# root.grid_rowconfigure(3, weight=1)

# Bundled Apps --------------------------------------------------------------------------------------------------------
mp4box = '"Apps/mp4box/MP4Box.exe"'

# -------------------------------------------------------------------------------------------------------- Bundled Apps

# Frames --------------------------------------------------------------------------------------------------------------
# Video Frame -------------------------------------------------------------------------------------------
video_frame = LabelFrame(mp4_root, text=' Video ')
video_frame.grid(row=0, columnspan=4, sticky=E + W + N + S, padx=20, pady=(10, 10))
video_frame.configure(fg="white", bg="#434547", bd=4)

video_frame.rowconfigure(1, weight=1)
video_frame.columnconfigure(0, weight=1)
video_frame.columnconfigure(1, weight=1)


# Entry Box for Video Title -----------------------------------------------------------------------------
def video_title(*args):
    global video_title_cmd_input
    if video_title_cmd.get() == (''):
        video_title_cmd_input = ('')
    else:
        cstmcmd = video_title_cmd.get()
        video_title_cmd_input = cstmcmd + ' '


video_title_cmd = StringVar()
video_title_entrybox_label = Label(video_frame, text='Video Title:', anchor=W, background='#434547', foreground='white')
video_title_entrybox_label.grid(row=1, column=0, columnspan=1, padx=10, pady=(0, 0), sticky=N + S + W + E)
video_title_entrybox = Entry(video_frame, textvariable=video_title_cmd, borderwidth=4, background='#CACACA')
video_title_entrybox.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 15), sticky=W + E)
video_title_cmd.trace('w', video_title)
video_title_cmd.set('')
# ------------------------------------------------------------------------------------- Video Title Line

# Video FPS Selection ----------------------------------------------------------------------------------
video_fps = StringVar()
video_fps_choices = {'Automatic': '',
                     '23.976': '-fps 23.976',
                     '24': '-fps 24',
                     '25': '-fps 25',
                     '29.97': '-fps 29.97',
                     '30': '-fps 30',
                     '50': '-fps 50',
                     '59.94': '-fps 59.94',
                     '60': '-fps 60'}
video_fps_menu_label = Label(video_frame, text='Framerate (FPS):', background="#434547", foreground="white")
video_fps_menu_label.grid(row=1, column=3, columnspan=1, padx=10, pady=(0, 0), sticky=W)
combo_fps = ttk.Combobox(video_frame, values=list(video_fps_choices.keys()), justify="center",
                         textvariable=video_fps)
combo_fps.grid(row=2, column=3, columnspan=1, padx=10, pady=(0, 10), sticky=N + S + W + E)
combo_fps['state'] = 'readonly'
combo_fps.current(0)

# ------------------------------------------------------------------------------------------------ Video FPS

# Video Language Selection ----------------------------------------------------------------------------------
video_language = StringVar()
video_language_menu_label = Label(video_frame, text='Language:', background="#434547", foreground="white")
video_language_menu_label.grid(row=1, column=2, columnspan=1, padx=10, pady=(0, 0), sticky=W)
combo_language = ttk.Combobox(video_frame, values=list(iso_639_2_codes_dictionary.keys()), justify="center",
                              textvariable=video_language)
combo_language.grid(row=2, column=2, columnspan=1, padx=10, pady=(0, 10), sticky=N + S + W + E)
combo_language['state'] = 'readonly'
combo_language.current(0)


# print(iso_639_2_codes_dictionary[video_language.get()])
# video_language_menu = OptionMenu(video_frame, video_language, *iso_639_2_codes_dictionary.keys())
# video_language_menu.config(background="#23272A", foreground="white", highlightthickness=1, width=12)
# video_language_menu.grid(row=2, column=2, columnspan=1, padx=10, pady=(0, 10), sticky=N + S + W + E)
# video_language.set('')
# # video_language.set(config_profile['FFMPEG AC3 - SETTINGS']['tempo'])
# video_language_menu["menu"].configure(activebackground="dim grey")
# ------------------------------------------------------------------------------------------------ Video Language

def input_button_commands():
    global VideoInput, autosavefilename, autofilesave_dir_path, VideoInputQuoted, VideoOutput
    video_extensions = ('.avi', '.mp4', '.m1v', '.m2v', '.m4v', '.264', '.h264', '.hevc', '.h265')
    VideoInput = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                            filetypes=[("Supported Formats", video_extensions)])
    if VideoInput:
        input_entry.configure(state=NORMAL)
        input_entry.delete(0, END)
        if VideoInput.endswith(video_extensions):
            autofilesave_file_path = pathlib.Path(VideoInput)  # Command to get file input location
            autofilesave_dir_path = autofilesave_file_path.parents[0]  # Final command to get only the directory
            VideoInputQuoted = '"' + str(pathlib.Path(VideoInput)) + '"'
            input_entry.insert(0, str(pathlib.Path(VideoInput)))
            filename = pathlib.Path(VideoInput)
            VideoOut = filename.with_suffix('')
            autosavefilename = VideoOut.name
            VideoOutput = str(pathlib.Path(r'' + str(VideoOut)))
            input_entry.configure(state=DISABLED)

            # output_entry.configure(state=NORMAL)
            # output_entry.delete(0, END)
            # output_entry.configure(state=DISABLED)
            # output_entry.configure(state=NORMAL)
            # output_entry.insert(0, str(VideoOut))
            # output_entry.configure(state=DISABLED)
            # output_button.configure(state=NORMAL)
            # check_for_hdr()
        else:
            messagebox.showinfo(title='Input Not Supported',
                                message="Try Again With a Supported File Type!\n\nIf this is a "
                                        "file that should be supported, please let me know.\n\n"
                                        + 'Unsupported file extension "' + str(pathlib.Path(VideoInput).suffix) + '"')
    # if not VideoInput:
    #     input_entry.configure(state=NORMAL)
    #     input_entry.delete(0, END)
    #     input_entry.configure(state=DISABLED)
    #     output_entry.configure(state=NORMAL)
    #     output_entry.delete(0, END)
    #     output_entry.configure(state=DISABLED)
    #     output_button.config(state=DISABLED)
    #     start_button.configure(state=DISABLED)


# ---------------------------------------------------------------------------------------------- Input Functions Button

# Drag and Drop Functions ---------------------------------------------------------------------------------------------
def drop_input(event):
    input_dnd.set(event.data)


def update_file_input(*args):
    global VideoInput, autofilesave_dir_path, VideoInputQuoted, VideoOutput, autosavefilename
    input_entry.configure(state=NORMAL)
    input_entry.delete(0, END)
    VideoInput = str(input_dnd.get()).replace("{", "").replace("}", "")
    video_extensions = ('.avi', '.mp4', '.m1v', '.m2v', '.m4v', '.264', '.h264', '.hevc', '.h265')
    if VideoInput.endswith(video_extensions):
        autofilesave_file_path = pathlib.Path(VideoInput)  # Command to get file input location
        autofilesave_dir_path = autofilesave_file_path.parents[0]  # Final command to get only the directory
        VideoInputQuoted = '"' + str(pathlib.Path(VideoInput)) + '"'
        input_entry.insert(0, str(input_dnd.get()).replace("{", "").replace("}", ""))
        filename = pathlib.Path(VideoInput)
        VideoOut = filename.with_suffix('')
        autosavefilename = VideoOut.name
        VideoOutput = str(pathlib.Path(r'' + str(VideoOut)))
        input_entry.configure(state=DISABLED)
        # output_entry.configure(state=NORMAL)
        # output_entry.delete(0, END)
        # output_entry.configure(state=DISABLED)
        # output_entry.configure(state=NORMAL)
        # output_entry.insert(0, str(VideoOut))
        # output_entry.configure(state=DISABLED)
        # output_button.configure(state=NORMAL)
        # check_for_hdr()
    else:
        messagebox.showinfo(title='Input Not Supported',
                            message="Try Again With a Supported File Type!\n\nIf this is a "
                                    "file that should be supported, please let me know.\n\n"
                                    + 'Unsupported file extension "' + str(pathlib.Path(VideoInput).suffix) + '"')


# --------------------------------------------------------------------------------------------- Drag and Drop Functions


# Buttons ------------------------------------------------------------------------------------
input_dnd = StringVar()
input_dnd.trace('w', update_file_input)
input_button = HoverButton(video_frame, text='Open File', command=input_button_commands, foreground='white',
                           background='#23272A', borderwidth='3', activebackground='grey')
input_button.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky=N + S + E + W)
input_button.drop_target_register(DND_FILES)
input_button.dnd_bind('<<Drop>>', drop_input)

input_entry = Entry(video_frame, width=48, borderwidth=4, background='#CACACA', state=DISABLED)
input_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky=W)
input_entry.drop_target_register(DND_FILES)
input_entry.dnd_bind('<<Drop>>', drop_input)

delete_input_button = HoverButton(video_frame, text='X', command=input_button_commands, foreground='white',
                           background='#23272A', borderwidth='3', activebackground='grey', width=2)
delete_input_button.grid(row=0, column=3, columnspan=1, padx=10, pady=5, sticky=E)

# ------------------------------------------------------------------------------------------ Buttons
# -------------------------------------------------------------------------------------------- Video Frame

# Audio Frame -------------------------------------------------------------------------------------------
# audio_frame = LabelFrame(mp4_root, text=' Audio ')
# audio_frame.grid(row=1, columnspan=4, sticky=E + W + N + S, padx=20, pady=(10,10))
# audio_frame.configure(fg="white", bg="#434547", bd=3)
#
# audio_frame.rowconfigure(1, weight=1)
# audio_frame.columnconfigure(0, weight=1)
# audio_frame.columnconfigure(1, weight=1)

# # Notebook Frame ------------------------------------------------------------------------------------------------------
# tabs = ttk.Notebook(mp4_root, height=170)
# tabs.grid(row=1, column=0, columnspan=4, sticky=E + W + N + S, padx=20, pady=(0, 0))
# audio_frame = Frame(tabs, background="#434547")
# # video_frame = Frame(tabs, background="#434547")
# # audio_frame = Frame(tabs, background="#434547")
# tabs.add(audio_frame, text='Audio')
# # tabs.add(video_frame, text='  Video Settings  ')
# # tabs.add(audio_frame, text='  Audio Settings  ')
# audio_frame.rowconfigure(1, weight=1)
# audio_frame.columnconfigure(0, weight=1)
# audio_frame.columnconfigure(1, weight=1)
#
#
# # ------------------------------------------------------------------------------------------------------ Notebook Frame

# # Entry Box for Audio Title -----------------------------------------------------------------------------
# def audio_title(*args):
#     global audio_title_cmd_input
#     if audio_title_cmd.get() == (''):
#         audio_title_cmd_input = ('')
#     else:
#         cstmcmd = audio_title_cmd.get()
#         audio_title_cmd_input = cstmcmd + ' '
#
#
# audio_title_cmd = StringVar()
# audio_title_entrybox_label = Label(audio_frame, text='Audio Title:', anchor=W, background='#434547',
#                                    foreground='white')
# audio_title_entrybox_label.grid(row=1, column=0, columnspan=1, padx=10, pady=(0, 0), sticky=N + S + W + E)
# audio_title_entrybox = Entry(audio_frame, textvariable=audio_title_cmd, borderwidth=4, background='#CACACA')
# audio_title_entrybox.grid(row=2, column=0, columnspan=2, padx=10, pady=(1, 1), sticky=W + E)
# audio_title_cmd.trace('w', audio_title)
# audio_title_cmd.set('')
# # ------------------------------------------------------------------------------------- Audio Title Line

# Audio Atempo Selection ----------------------------------------------------------------------------------
# audio_language = StringVar()
# audio_language_choices = {'Automatic': '',}
# audio_language_menu_label = Label(audio_frame, text='Frame Rate:', background="#434547", foreground="white")
# audio_language_menu_label.grid(row=1, column=2, columnspan=1, padx=10, pady=(0, 0), sticky=W)
# audio_language_menu = OptionMenu(audio_frame, audio_language, *audio_language_choices.keys())
# audio_language_menu.config(background="#23272A", foreground="white", highlightthickness=1, width=12)
# audio_language_menu.grid(row=2, column=2, columnspan=1, padx=10, pady=(1), sticky=N + S + W + E)
# audio_language.set('Automatic')
# audio_language.set(config_profile['FFMPEG AC3 - SETTINGS']['tempo'])
# audio_language_menu["menu"].configure(activebackground="dim grey")
# audio_language_menu.bind("<Enter>", audio_language_menu_hover)
# audio_language_menu.bind("<Leave>", audio_language_menu_hover_leave)
# ------------------------------------------------------------------------------------------------ Audio Atempo

# # Audio Gain Selection ----------------------------------------------------------------------------------------
# audio_delay = StringVar()
# audio_delay_label = Label(audio_frame, text="Delay:", background="#434547", foreground="white")
# audio_delay_label.grid(row=3, column=0, columnspan=1, padx=10, pady=1, sticky=W)
# audio_delay_spinbox = Spinbox(audio_frame, from_=-1000, to=1000, increment=1.0, justify=CENTER,
#                               wrap=True, textvariable=audio_delay)
# audio_delay_spinbox.configure(background="#23272A", foreground="white", highlightthickness=1,
#                               buttonbackground="black", width=15, readonlybackground="#23272A")
# audio_delay_spinbox.grid(row=4, column=0, columnspan=1, padx=10, pady=(1, 8), sticky=N + S + E + W)
# # audio_delay.set(int(config_profile['FFMPEG AAC - SETTINGS']['audio_delay']))
# audio_delay.set(0)
#
#
# # -------------------------------------------------------------------------------------------------------- Gain

# def drop_input(event):
#     input_dnd.set(event.data)
#
#
# def update_file_input(*args):
#     global audioInput
#     global track_count
#     global autofilesave_dir_path
#     global audioInputQuoted
#     input_entry.configure(state=NORMAL)
#     input_entry.delete(0, END)
#     audioInput = str(input_dnd.get()).replace("{", "").replace("}", "")
#     # file_extension = pathlib.Path(VideoInput).suffix
#
#
# # Buttons -------------------------------------------------------------------------------------------------------------
# def input_button_hover(e):
#     input_button["bg"] = "grey"
#
#
# def input_button_hover_leave(e):
#     input_button["bg"] = "#23272A"
#
#
# input_dnd = StringVar()
# input_dnd.trace('w', update_file_input)
# input_button = tk.Button(audio_frame, text='Open File', command=input_button_commands, foreground='white',
#                          background='#23272A', borderwidth='3')
# input_button.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky=N + S + E + W)
# input_button.drop_target_register(DND_FILES)
# input_button.dnd_bind('<<Drop>>', drop_input)
# input_button.bind("<Enter>", input_button_hover)
# input_button.bind("<Leave>", input_button_hover_leave)
#
# input_entry = Entry(audio_frame, width=40, borderwidth=4, background='#CACACA', state=DISABLED)
# input_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky=S + E + W)
# input_entry.drop_target_register(DND_FILES)
# input_entry.dnd_bind('<<Drop>>', drop_input)
#
# # -------------------------------------------------------------------------------------------- Audio Frame

# Subtitle Frame -------------------------------------------------------------------------------------------
# subtitle_frame = LabelFrame(mp4_root, text=' Subtitle ')
# subtitle_frame.grid(row=2, columnspan=4, sticky=E + W + N + S, padx=20, pady=(10,10))
# subtitle_frame.configure(fg="white", bg="#434547", bd=3)


# # Notebook Frame ------------------------------------------------------------------------------------------------------
# subtitle_tabs = ttk.Notebook(mp4_root, height=120)
# subtitle_tabs.grid(row=2, column=0, columnspan=4, sticky=E + W + N + S, padx=20, pady=(10, 0))
# subtitle_frame = Frame(subtitle_tabs, background="#434547")
# # video_frame = Frame(subtitle_tabs, background="#434547")
# # audio_frame = Frame(subtitle_tabs, background="#434547")
# subtitle_tabs.add(subtitle_frame, text='Subtitle')
# # subtitle_tabs.add(video_frame, text='  Video Settings  ')
# # subtitle_tabs.add(audio_frame, text='  Audio Settings  ')
# subtitle_frame.rowconfigure(1, weight=1)
# subtitle_frame.columnconfigure(0, weight=1)
# subtitle_frame.columnconfigure(1, weight=1)
#
# # ------------------------------------------------------------------------------------------------------ Notebook Frame

# subtitle_frame.rowconfigure(1, weight=1)
# subtitle_frame.columnconfigure(0, weight=1)
# subtitle_frame.columnconfigure(1, weight=1)
#
#
# # Entry Box for subtitle Title -----------------------------------------------------------------------------
# def subtitle_title(*args):
#     global subtitle_title_cmd_input
#     if subtitle_title_cmd.get() == (''):
#         subtitle_title_cmd_input = ('')
#     else:
#         cstmcmd = subtitle_title_cmd.get()
#         subtitle_title_cmd_input = cstmcmd + ' '
#
#
# subtitle_title_cmd = StringVar()
# subtitle_title_entrybox_label = Label(subtitle_frame, text='Subtitle Title:', anchor=W, background='#434547',
#                                       foreground='white')
# subtitle_title_entrybox_label.grid(row=1, column=0, columnspan=1, padx=10, pady=(0, 0), sticky=N + S + W + E)
# subtitle_title_entrybox = Entry(subtitle_frame, textvariable=subtitle_title_cmd, borderwidth=4, background='#CACACA')
# subtitle_title_entrybox.grid(row=2, column=0, columnspan=2, padx=10, pady=(1, 8), sticky=W + E)
# subtitle_title_cmd.trace('w', subtitle_title)
# subtitle_title_cmd.set('')
#
#
# # ------------------------------------------------------------------------------------- subtitle Title Line

# subtitle Language Selection ----------------------------------------------------------------------------------
# subtitle_language = StringVar()
# subtitle_language_choices = {'Automatic': '',}
# subtitle_language_menu_label = Label(subtitle_frame, text='Frame Rate:', background="#434547", foreground="white")
# subtitle_language_menu_label.grid(row=1, column=2, columnspan=1, padx=10, pady=(0, 0), sticky=W)
# subtitle_language_menu = OptionMenu(subtitle_frame, subtitle_language, *subtitle_language_choices.keys())
# subtitle_language_menu.config(background="#23272A", foreground="white", highlightthickness=1, width=12)
# subtitle_language_menu.grid(row=2, column=2, columnspan=1, padx=10, pady=(1,8), sticky=N + S + W + E)
# subtitle_language.set('Automatic')
# subtitle_language.set(config_profile['FFMPEG AC3 - SETTINGS']['tempo'])
# subtitle_language_menu["menu"].configure(activebackground="dim grey")
# subtitle_language_menu.bind("<Enter>", subtitle_language_menu_hover)
# subtitle_language_menu.bind("<Leave>", subtitle_language_menu_hover_leave)
# # ------------------------------------------------------------------------------------------------ Subtitle Langage
#
# def drop_input(event):
#     input_dnd.set(event.data)
#
#
# def update_file_input(*args):
#     global subtitleInput
#     global track_count
#     global autofilesave_dir_path
#     global subtitleInputQuoted
#     input_entry.configure(state=NORMAL)
#     input_entry.delete(0, END)
#     subtitleInput = str(input_dnd.get()).replace("{", "").replace("}", "")
#     # file_extension = pathlib.Path(VideoInput).suffix
#
#
# # Buttons -------------------------------------------------------------------------------------------------------------
# def input_button_hover(e):
#     input_button["bg"] = "grey"
#
#
# def input_button_hover_leave(e):
#     input_button["bg"] = "#23272A"
#
#
# input_dnd = StringVar()
# input_dnd.trace('w', update_file_input)
# input_button = tk.Button(subtitle_frame, text='Open File', command=input_button_commands, foreground='white',
#                          background='#23272A', borderwidth='3')
# input_button.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky=N + S + E + W)
# input_button.drop_target_register(DND_FILES)
# input_button.dnd_bind('<<Drop>>', drop_input)
# input_button.bind("<Enter>", input_button_hover)
# input_button.bind("<Leave>", input_button_hover_leave)
#
# input_entry = Entry(subtitle_frame, width=40, borderwidth=4, background='#CACACA', state=DISABLED)
# input_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky=S + E + W)
# input_entry.drop_target_register(DND_FILES)
# input_entry.dnd_bind('<<Drop>>', drop_input)
#
# # -------------------------------------------------------------------------------------------- Subtitle Frame


# # chapter Frame -------------------------------------------------------------------------------------------
# chapter_frame = LabelFrame(mp4_root, text=' Chapter ')
# chapter_frame.grid(row=3, columnspan=4, sticky=E + W + N + S, padx=20, pady=(10, 10))
# chapter_frame.configure(fg="white", bg="#434547", bd=3)
#
# chapter_frame.rowconfigure(1, weight=1)
# chapter_frame.columnconfigure(0, weight=1)
# chapter_frame.columnconfigure(1, weight=1)
# chapter_frame.columnconfigure(2, weight=1)
#
# clear_button = Button(chapter_frame, text='X', command=input_button_commands, foreground='white',
#                       background='#23272A', borderwidth='3')
# clear_button.grid(row=0, column=3, columnspan=1, padx=5, pady=5, sticky=N + S + E + W)
#
#
# def drop_input(event):
#     input_dnd.set(event.data)
#
#
# def update_file_input(*args):
#     global chapterInput
#     global track_count
#     global autofilesave_dir_path
#     global chapterInputQuoted
#     input_entry.configure(state=NORMAL)
#     input_entry.delete(0, END)
#     chapterInput = str(input_dnd.get()).replace("{", "").replace("}", "")
#     # file_extension = pathlib.Path(VideoInput).suffix
#
#
# # # Buttons -------------------------------------------------------------------------------------------------------------
# def input_button_hover(e):
#     input_button["bg"] = "grey"
#
#
# def input_button_hover_leave(e):
#     input_button["bg"] = "#23272A"
#
#
# input_dnd = StringVar()
# input_dnd.trace('w', update_file_input)
# input_button = tk.Button(chapter_frame, text='Open File', command=input_button_commands, foreground='white',
#                          background='#23272A', borderwidth='3')
# input_button.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky=N + S + E + W)
# input_button.drop_target_register(DND_FILES)
# input_button.dnd_bind('<<Drop>>', drop_input)
# input_button.bind("<Enter>", input_button_hover)
# input_button.bind("<Leave>", input_button_hover_leave)
#
# input_entry = Entry(chapter_frame, width=40, borderwidth=4, background='#CACACA', state=DISABLED)
# input_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=8, sticky=S + E + W)
# input_entry.drop_target_register(DND_FILES)
# input_entry.dnd_bind('<<Drop>>', drop_input)
#
# # -------------------------------------------------------------------------------------------- chapter Frame


# -------------------------------------------------------------------------------------------------------------- Frames


# End Loop ------------------------------------------------------------------------------------------------------------
mp4_root.mainloop()
