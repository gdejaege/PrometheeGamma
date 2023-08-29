from typing import Optional, Tuple, Union
from customtkinter import CTkToplevel, CTkTextbox, CTkLabel
import webbrowser


class AboutView(CTkToplevel):
    """
    A class to display "about" information over the PROMETHEE Gamma GUI application

    Attributes
    ----------
    labelName : CTkLabel
        the label that will contain the application name
    textbox : CTkTexbox
        the textbox that will contain the "about" text
    label1 : CTkLabel
        the label that will contain "Link to the article:" text
    label2 : CTkLabel
        the label that will contain the url of the article
    """

    def __init__(self, about_text, *args, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(*args, fg_color=fg_color, **kwargs)

        self.title("About")
        self.geometry("500x350")
        self.resizable(False, False)
        if fg_color == "white":
            text_color = "black"
        else:
            text_color = "white"

        self.labelName = CTkLabel(self, text="PROMETHEE Gamma GUI", fg_color=fg_color, text_color=text_color, font=("Arial", 16))
        self.textbox = CTkTextbox(self, wrap='word', fg_color=fg_color, text_color=text_color, width=420)
        self.textbox.insert("end", about_text)
        self.textbox.configure(state="disabled")

        self.label1 = CTkLabel(self, text="Link to the article:", fg_color=fg_color, text_color=text_color)
        self.label2 = CTkLabel(self, text="https://doi.org/10.1002/mcda.1805", text_color="blue", cursor="hand2", fg_color=fg_color)

        self.label2.bind("<Button-1>", lambda e:self.callback("https://doi.org/10.1002/mcda.1805"))

        self.labelName.pack(pady = (30,10))
        self.textbox.pack()
        self.label1.pack()
        self.label2.pack()


    def callback(self, url:str):
        """Open the url in a new tab in a browser

        Parameters
        ----------
        url : str
            the url that will be opened
        """
        webbrowser.open_new_tab(url)



