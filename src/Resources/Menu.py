import tkinter
from typing import Callable, Optional, Tuple, Union
from customtkinter import CTkOptionMenu, Variable
from customtkinter.windows.widgets.font import CTkFont

class Menu(CTkOptionMenu):
    def __init__(self, master: any, text:str="Menu", 
                 width: int = 140, height: int = 28, corner_radius: int | None = None, 
                 bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, 
                 button_color: str | Tuple[str, str] | None = None, button_hover_color: str | Tuple[str, str] | None = None, 
                 text_color: str | Tuple[str, str] | None = None, text_color_disabled: str | Tuple[str, str] | None = None, 
                 dropdown_fg_color: str | Tuple[str, str] | None = None, dropdown_hover_color: str | Tuple[str, str] | None = None, 
                 dropdown_text_color: str | Tuple[str, str] | None = None, font: tuple | CTkFont | None = None, 
                 dropdown_font: tuple | CTkFont | None = None, values: list | None = None, variable: Variable | None = None, 
                 state: str = tkinter.NORMAL, hover: bool = True, command: Callable[[str], None] | None = None, 
                 dynamic_resizing: bool = True, anchor: str = "w", **kwargs):
        
        if text is None or text == "":
            self._text = "Menu"
        else:
            self._text = text

        super().__init__(master, width, height, corner_radius, bg_color, fg_color, button_color, button_hover_color, text_color, 
                         text_color_disabled, dropdown_fg_color, dropdown_hover_color, dropdown_text_color, font, dropdown_font, values, 
                         variable, state, hover, command, dynamic_resizing, anchor, **kwargs)

        self._text_label = tkinter.Label(master=self,
                                         font=self._apply_font_scaling(self._font),
                                         anchor=anchor,
                                         padx=0,
                                         pady=0,
                                         borderwidth=1,
                                         text=self._text)
        
    
    def configure(self, require_redraw=False, text:str=None, **kwargs):
        if text is not None:
            self._text = text
        self._text_label.configure(text=self._text)
        
        if "variable" in kwargs:
            if self._variable is not None:  # remove old callback
                self._variable.trace_remove("write", self._variable_callback_name)

            self._variable = kwargs.pop("variable")

            if self._variable is not None and self._variable != "":
                self._variable_callback_name = self._variable.trace_add("write", self._variable_callback)
                self._current_value = self._variable.get()
            else:
                self._variable = None
        super().configure(require_redraw, **kwargs)



    def _variable_callback(self, var_name, index, mode):
        if not self._variable_callback_blocked:
            self._current_value = self._variable.get()


    def _dropdown_callback(self, value: str):
        self._current_value = value

        if self._variable is not None:
            self._variable_callback_blocked = True
            self._variable.set(self._current_value)
            self._variable_callback_blocked = False

        if self._command is not None:
            self._command(self._current_value)


    def set(self, value: str):
        self._current_value = value

        if self._variable is not None:
            self._variable_callback_blocked = True
            self._variable.set(self._current_value)
            self._variable_callback_blocked = False