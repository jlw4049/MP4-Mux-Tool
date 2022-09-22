import pathlib
import threading
from os import PathLike
from queue import Queue, Empty
from tkinter import (
    Toplevel,
    messagebox,
    N,
    S,
    W,
    E,
    ttk,
    HORIZONTAL,
    Label,
    SUNKEN,
    scrolledtext,
    DISABLED,
    NORMAL,
    END,
    WORD,
)
from typing import Union, TYPE_CHECKING

import psutil

if TYPE_CHECKING:
    from mp4_mux_tool import MainGui

from automatic_demuxer import AutoDemuxer

from configparser import ConfigParser
from mp4muxtool.config.config_writer import config_file


class DemuxWindow(Toplevel):
    """Extract selected tracks and show the progress"""

    def __init__(
        self,
        main_gui: "MainGui",
        file_input: Union[str, PathLike],
        track_number: Union[str, int],
        track_type: str,
    ):
        """
        Create variables needed throughout the class as well as the Toplevel window

        :param main_gui: Parent window object.
        :param file_input: File input in the form of a string or Pathlike object.
        :param track_number: Track number in the form of integer or string.
        :param track_type: A lowercase string that can be "video", "audio", "subtitle", or "chapter".
        """

        # Obtain inheritance from Toplevel
        super().__init__()

        # main gui
        self.mp4_win = main_gui

        # config parser info
        self.config_parser = ConfigParser()
        self.config_parser.read(config_file)

        # theme
        self.theme = self.mp4_win.open_theme

        # if custom ttk theme is being used
        if self.theme.enable_ttk:
            self.custom_theme = True
        else:
            self.custom_theme = False

        # file input
        self.file_input = pathlib.Path(file_input)

        # track number
        self.track_number = track_number

        # track type
        self.track_type = track_type

        # start Queue instance
        self.demux_queue = Queue()

        # thread counter
        self.loop_counter = 0

        # job pid
        self.demux_pid = None

        # job status
        self.status = None

        # create demux window
        self.demux_win = self
        self.demux_win.configure(background=self.theme.custom_window_bg_color)
        self.demux_win.title("Demuxer")
        self.demux_win.geometry(
            f'{1000}x{400}+{str(int(self.mp4_win.geometry().split("+")[1]) + 148)}+'
            f'{str(int(self.mp4_win.geometry().split("+")[2]) + 230)}'
        )
        self.demux_win.resizable(False, False)
        self.demux_win.grab_set()
        self.demux_win.wm_transient(self.mp4_win)
        self.demux_win.protocol("WM_DELETE_WINDOW", self._stop_extraction)

        # set window grid configurations
        self.demux_win.grid_rowconfigure(0, weight=1)
        self.demux_win.grid_rowconfigure(1, weight=100)
        self.demux_win.grid_rowconfigure(2, weight=1)
        self.demux_win.grid_columnconfigure(0, weight=1)
        self.demux_win.grid_columnconfigure(1, weight=1)
        self.demux_win.grid_columnconfigure(2, weight=1)

        # video title label
        self.video_title_entry_label = Label(
            self.demux_win,
            text="Extraction Progress:",
            anchor=W,
            bd=0,
            relief=SUNKEN,
            background=self.theme.custom_label_colors["background"],
            fg=self.theme.custom_label_colors["foreground"],
            font=(self.theme.set_font, self.theme.set_font_size + 1),
        )
        self.video_title_entry_label.grid(
            row=0, column=0, padx=10, pady=(6, 0), sticky=W
        )

        # scrolled text widget for output
        self.encode_window_progress = scrolledtext.ScrolledText(
            self.demux_win,
            height=1,
            width=1,
            state=DISABLED,
            bg=self.theme.custom_scrolled_text_widget_color["background"],
            fg=self.theme.custom_scrolled_text_widget_color["foreground"],
            bd=4,
            wrap=WORD,
            font=(self.theme.set_fixed_font, self.theme.set_font_size),
        )
        self.encode_window_progress.grid(
            row=1, column=0, columnspan=3, pady=(10, 0), padx=10, sticky=E + W + N + S
        )

        # progress bar
        self.demux_progress_bar = ttk.Progressbar(
            self.demux_win,
            style="text.Horizontal.TProgressbar",
            orient=HORIZONTAL,
            mode="determinate",
        )
        self.demux_progress_bar.grid(
            row=2, column=0, columnspan=3, pady=(4, 10), padx=10, sticky=E + W
        )

        # thread the method used to extract the file
        self.demux_thread = threading.Thread(target=self._demux_file, daemon=True)
        self.demux_thread.start()

        # start the tkinter safe gui loop to poll the queue
        self._demux_queue_loop()

        # wait for the window to be closed before continuing
        self.demux_win.wait_window()

        # join the queue thread
        self.demux_queue.join()

        # join the extract file thread
        self.demux_thread.join()

    def _demux_file(self):
        """Call AutoDemuxer() to extract based on the track type"""
        self.demux_input = AutoDemuxer()

        # if track type is Video
        if self.track_type == "video":
            self.demux_input.video_demux(
                file_input=self.file_input,
                ffmpeg_path=self.config_parser["ffmpeg_path"]["path"],
                track_number=self.track_number,
                fallback_ext="mp4",
                callback=self._extract_callback,
            )

        # update status variable with AutoDemuxer() returned status
        self.status = self.demux_input.status

    def _extract_callback(self, x):
        """
        Use this callback method to add data to the Queue since it's in a separate thread from the mainloop

        :param x: Callback data from AutoDemuxer()
        """

        # add call back data to the queue
        self.demux_queue.put(x)

        # update job demux PID from call back data
        if not self.demux_pid:
            self.demux_pid = x["job_pid"]

    def _demux_queue_loop(self):
        """
        This is a tkinter safe loop that is non-blocking.
        Here we will handle everything that manipulates the GUI in this loop.
        We do this by taking the Queue data from the threaded method call back
        """

        # if there is data set it to a variables by checking it with the non block get_nowait() method
        try:
            data = self.demux_queue.get_nowait()
        except Empty:
            data = None

        if data:
            # if data == "Terminate":
            #     return

            # if there is video duration data in the input file output the percentage
            if self.demux_input.duration:
                if data["percent"]:
                    # Update progress bar and progress bar text data
                    self.demux_progress_bar["value"] = float(
                        str(data["percent"].replace("%", "").strip())
                    )
                    if self.custom_theme:
                        self.theme.enable_ttk.custom_style.configure(
                            "text.Horizontal.TProgressbar", text=data["percent"]
                        )

                    # Update window title with percent data
                    self.demux_win.title(f"Demuxer - {data['percent']}")

            # if there is no duration update text inside progress bar to let the user know
            elif not self.demux_input.duration:
                if self.custom_theme:
                    self.theme.enable_ttk.custom_style.configure(
                        "text.Horizontal.TProgressbar",
                        text="Video file has no duration, progress bar is disabled",
                    )

                # update title with no duration information
                self.demux_win.title(
                    "Demuxer - No duration detected, progress bar disabled"
                )

            # update window
            self.encode_window_progress.config(state=NORMAL)
            if "size=" in str(data["output"]) and self.loop_counter > 0:
                self.encode_window_progress.delete("end-2l", "end-1l")
                self.encode_window_progress.insert(END, str(data["output"]) + "\n")
            else:
                self.encode_window_progress.insert(END, str(data["output"]) + "\n")
                self.loop_counter += 1
                self.encode_window_progress.see(END)
            self.encode_window_progress.config(state=DISABLED)

            # Everytime data is sent into the queue we must call task_done() to properly close the loop
            self.demux_queue.task_done()

        # Ensure thread is dead and Queue size is == 0 before getting final status and exiting the loop
        if not self.demux_thread.is_alive() and self.demux_queue.qsize() == 0:
            self.encode_window_progress.config(state=NORMAL)
            final_output = (
                f"\n\nExit Code {self.demux_input.status['return_code']} - "
                f"Status: {self.demux_input.status['status']}\n"
                f"Output Filename: {str(self.demux_input.status['output_filename'])}"
            )
            self.encode_window_progress.insert(END, final_output)
            self.encode_window_progress.see(END)
            self.encode_window_progress.config(state=DISABLED)
            return None

        # Constantly call the loop to parse the Queue data
        self.demux_win.after(1, self._demux_queue_loop)

    def _stop_extraction(self):
        """
        If the thread is still alive ask the user if they'd like to close it.
        If they confirm, use psutil to kill all children processes and parent process by PID.
        """
        if self.demux_thread.is_alive():
            cancel_check = messagebox.askyesno(
                parent=self.demux_win,
                title="Are you sure?",
                message="Are you sure you want to cancel extraction?",
            )
            if cancel_check:
                try:
                    parent = psutil.Process(self.demux_pid)
                    for child in parent.children(recursive=True):
                        child.kill()
                    parent.kill()
                except psutil.NoSuchProcess:
                    pass

        # one the thread is dead safely exit the window
        else:
            self.demux_win.destroy()