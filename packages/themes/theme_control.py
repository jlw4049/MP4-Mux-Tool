from configparser import ConfigParser

from packages.config_writer import config_file
from packages.themes import bhd_theme
from packages.themes.system_theme import SystemTheme
from packages.tk_style import GuiStyle


class OpenTheme:
    def __init__(self, main_gui):
        """Opens a theme based off of the user input that has been saved to the config file"""
        self.main_gui = main_gui

        # define parser
        self.config_parser = ConfigParser()
        self.config_parser.read(config_file)

        # run the check theme method
        self.check = self.__check_theme()

        # if check theme returns anything other than None
        if self.check:
            # run the theme method with the returned values from the check theme method
            self.__theme(values=self.check)

            # theme ttk
            self.__theme_ttk()

    def __check_theme(self):
        """define theme parameters based off of config selection"""
        values = None

        if self.config_parser["theme"]["selected_theme"] == "system_default":
            self.colors = SystemTheme(main_gui=self.main_gui)

            self.custom_window_bg_color = self.colors.custom_window_bg_color
            self.custom_button_colors = self.colors.custom_button_colors
            self.custom_entry_colors = self.colors.custom_entry_colors
            self.custom_label_frame_colors = self.colors.custom_label_frame_colors
            self.custom_frame_bg_colors = self.colors.custom_frame_bg_colors
            self.custom_label_colors = self.colors.custom_label_colors
            self.custom_scrolled_text_widget_color = (
                self.colors.custom_scrolled_text_widget_color
            )
            self.custom_listbox_color = self.colors.custom_listbox_color
            self.custom_spinbox_color = self.colors.custom_spinbox_color
            self.custom_text_color = self.colors.custom_text_color

            return values

        else:
            if self.config_parser["theme"]["selected_theme"] == "bhd_theme":
                values = bhd_theme.BHDTheme()

            return values

    def __theme(self, values):
        """set the values for each widget to class variables to be used within the program"""
        self.custom_window_bg_color = values.custom_window_bg_color
        self.custom_button_colors = values.custom_button_colors
        self.custom_entry_colors = values.custom_entry_colors
        self.custom_label_frame_colors = values.custom_label_frame_colors
        self.custom_frame_bg_colors = values.custom_frame_bg_colors
        self.custom_label_colors = values.custom_label_colors
        self.custom_scrolled_text_widget_color = (
            values.custom_scrolled_text_widget_color
        )
        self.custom_listbox_color = values.custom_listbox_color
        self.custom_spinbox_color = values.custom_spinbox_color
        self.custom_text_color = values.custom_text_color

    def __theme_ttk(self):
        """
        Called only if the program is running any theme other than system_default
        This calls the class GuiStyle which themes aspects of the ttk widgets, this
        relies on values extracted from __theme()
        """
        GuiStyle(theme_instance=self)
