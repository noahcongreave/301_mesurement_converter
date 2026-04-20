from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import date
import all_constants as c
import os
import subprocess
import sys


# ==========================================
# Main Converter Class
# ==========================================
class Converter:

    def __init__(self, root):

        self.root = root
        root.title("Temperature Converter")

        self.all_calculations_list = []


        # convertion dictionary
        self.conversions = {
    "Meters → Kilometers": {
        "func": lambda x: x / 1000,
        "from": "m",
        "to": "km"
    },
    "Kilometers → Meters": {
        "func": lambda x: x * 1000,
        "from": "km",
        "to": "m"
    },
    "Grams → Kilograms": {
        "func": lambda x: x / 1000,
        "from": "g",
        "to": "kg"
    },
    "Kilograms → Grams": {
        "func": lambda x: x * 1000,
        "from": "kg",
        "to": "g"
    }
        }



        self.temp_frame = Frame(root, padx=10, pady=10)
        self.temp_frame.grid()

        # Heading
        Label(
            self.temp_frame,
            text="mesurement converter ",
            font=("Arial", 16, "bold")
        ).grid(row=0)

        # Instructions
        instructions = (
            "Enter a mesurement and choose a conversion "
            "(Kilograms → Grams)."
        )

        Label(
            self.temp_frame,
            text=instructions,
            wraplength=250,
            justify="left"
        ).grid(row=1)

        # Entry
        self.temp_entry = Entry(
            self.temp_frame,
            font=("Arial", 14, "bold")
        )
        self.temp_entry.grid(row=2, pady=10)

        # Output
        self.answer_error = Label(self.temp_frame, fg="#004C99")
        self.answer_error.grid(row=3)

        # Dropdown
        self.conversion_choice = StringVar()

        self.dropdown = ttk.Combobox(
            self.temp_frame,
            textvariable=self.conversion_choice,
            state="readonly",
            values=list(self.conversions.keys())
        )
        self.dropdown.current(0)
        self.dropdown.grid(row=4, pady=5)

        # -------------------------------
        # Buttons (ALL same size)
        # -------------------------------
        self.button_frame = Frame(self.temp_frame)
        self.button_frame.grid(row=5)

        button_details_list = [
            ["Convert", "#0066CC", self.run_conversion, 0, 0],
            ["Clear", "#666666", self.clear, 0, 1],
            ["History / Export", "#CC6600", self.open_history, 1, 0],
            ["Help / Info", "#CC6600", self.to_help, 1, 1]
        ]

        self.button_ref_list = []

        for item in button_details_list:
            btn = Button(
                self.button_frame,
                text=item[0],
                bg=item[1],
                fg="white",
                font=("Arial", 12, "bold"),
                width=16,
                command=item[2]
            )
            btn.grid(row=item[3], column=item[4], padx=5, pady=5)
            self.button_ref_list.append(btn)

        # Button references
        self.history_button = self.button_ref_list[2]
        self.to_help_button = self.button_ref_list[3]

        # Disable history initially
        self.history_button.config(state=DISABLED)

    # ==========================================
    # Help window
    # ==========================================
    def to_help(self):
        DisplayHelp(self)

    # ==========================================
    # Run conversion
    # changed the conversion to run from the list
    # rather than being hard coded
    # ==========================================
    def run_conversion(self):

        choice = self.conversion_choice.get()
        to_convert = self.temp_entry.get()

        self.answer_error.config(fg="#004C99", font=("Arial", 13, "bold"))
        self.temp_entry.config(bg="white")

        try:
            value = float(to_convert)
            #min and max vaule
            if value >= 10000000:
                self.answer_error.config(
                    text="Number must be less than 10,000,000",
                    fg="#9C0000"
                )
                self.temp_entry.config(bg="#F4CCCC")
                return
            if value <= 0:
                self.answer_error.config(
                    text="Number must be more than 0",
                    fg="#9C0000"
                )
                self.temp_entry.config(bg="#F4CCCC")
                return

            # ⭐ NEW: use dictionary instead of if statements
            conversion = self.conversions[choice]

            from_unit = conversion["from"]
            to_unit = conversion["to"]

            answer = conversion["func"](value)

            calculation = f"{value} {from_unit} = {round(answer, 3)} {to_unit}"
            self.answer_error.config(text=calculation)

            self.all_calculations_list.append(calculation)
            self.history_button.config(state=NORMAL)
            self.temp_entry.config(bg="#88E788")

        except ValueError:
            self.answer_error.config(
                text="Enter a valid number",
                fg="#9C0000"
            )
            self.temp_entry.config(bg="#F4CCCC")
            self.temp_entry.delete(0, END)



    # Clear
    def clear(self):
        self.temp_entry.delete(0, END)
        self.answer_error.config(text="")

        #reset backround coulor
        self.temp_entry.config(bg="white")

        # Clear history list
        self.all_calculations_list.clear()

        # Disable history button again
        self.history_button.config(state=DISABLED)

    # Open history
    def open_history(self):

        if len(self.all_calculations_list) == 0:
            messagebox.showinfo("History", "No calculations yet.")
            return

        HistoryWindow(self, self.all_calculations_list)


# ==========================================
# Help Window
# ==========================================
class DisplayHelp:

    def __init__(self, partner):

        self.partner = partner
        background = "#ffe6cc"

        self.help_box = Toplevel()

        # Disable help button
        self.partner.to_help_button.config(state=DISABLED)

        self.help_box.protocol('WM_DELETE_WINDOW', self.close_help)

        self.help_frame = Frame(self.help_box, padx=20, pady=20, bg=background)
        self.help_frame.grid()

        help_text = (
            "This program converts mesurements .\n\n"
            "Steps:\n"
            "1. Enter a number\n"
            "2. Choose conversion type\n"
            "3. Click Convert\n\n"
            "Use History to view and export results."
            " you can uses the clear button to clear your history"
        )

        Label(
            self.help_frame,
            text="Help / Info",
            font=("Arial", 14, "bold"),
            bg=background
        ).grid(row=0, pady=10)

        Label(
            self.help_frame,
            text=help_text,
            wraplength=300,
            justify="left",
            bg=background
        ).grid(row=1)

        Button(
            self.help_frame,
            text="Dismiss",
            font=("Arial", 12, "bold"),
            bg="#CC6600",
            fg="white",
            command=self.close_help
        ).grid(row=2, pady=10)

    def close_help(self):
        self.partner.to_help_button.config(state=NORMAL)
        self.help_box.destroy()


# ==========================================
# History Window (unchanged)
# ==========================================
class HistoryWindow:

    def __init__(self, partner, calculations):

        self.partner = partner
        self.calculations = calculations

        self.partner.history_button.config(state=DISABLED)

        self.window = Toplevel()
        self.window.title("History / Export")
        self.window.protocol('WM_DELETE_WINDOW', self.close_window)

        self.frame = Frame(self.window, bg="#ffe6cc", padx=20, pady=20)
        self.frame.grid()

        Label(
            self.frame,
            text="History / Export",
            font=("Arial", 14, "bold"),
            bg="#ffe6cc"
        ).grid(row=0, columnspan=2)

        if len(calculations) <= c.MAX_CALCS:
            calc_back = "#D5E8D4"
            calc_amount = "Showing all calculations"
        else:
            calc_back = "#F4CCCC"
            calc_amount = f"Showing {c.MAX_CALCS} of {len(calculations)}"

        Label(
            self.frame,
            text=calc_amount,
            bg="#ffe6cc"
        ).grid(row=1, columnspan=2)

        calc_text = "\n".join(calculations[:c.MAX_CALCS])

        # Frame to hold text + scrollbar
        text_frame = Frame(self.frame)
        text_frame.grid(row=2, columnspan=2, pady=10)


        # Text widget
        self.history_text = Text(
            text_frame,
            width=50,
            height=14,
            wrap="none",
            bg=calc_back,
            fg="black",  # ensures readability
            font=("Courier", 14)
        )

        self.history_text.pack(side=LEFT, fill=BOTH)

      
        #  NOW insert text (AFTER widget exists)
        for item in calculations[:c.MAX_CALCS]:
            self.history_text.insert(END, item + "\n")

        # Optional: make read-only
        self.history_text.config(state=DISABLED)

        self.export_filename_label = Label(self.frame, bg="#ffe6cc")
        self.export_filename_label.grid(row=3, columnspan=2)

        Button(
            self.frame,
            text="Export",
            bg="#CC6600",
            fg="white",
            width=12,
            command=self.export_data
        ).grid(row=4, column=0, pady=10)

        Button(
            self.frame,
            text="Close",
            width=12,
            command=self.close_window
        ).grid(row=4, column=1)

    def export_data(self):

        today = date.today()
        day = today.strftime("%d")
        month = today.strftime("%m")
        year = today.strftime("%Y")

        file_name = f"measurement_{year}_{month}_{day}.txt"

        with open(file_name, "w", encoding="utf-8") as text_file:
            text_file.write("****** Measurement Calculations ******\n")
            text_file.write(f"Generated: {day}/{month}/{year}\n\n")

            for item in self.calculations:
                text_file.write(item + "\n")

        # Cross-platform open
        if sys.platform == "win32":
            os.startfile(file_name)
        elif sys.platform == "darwin":
            subprocess.call(["open", file_name])
        else:
            subprocess.call(["xdg-open", file_name])

        messagebox.showinfo("Export", "History exported and opened!")
    def close_window(self):
        self.partner.history_button.config(state=NORMAL)
        self.window.destroy()


# ==========================================
# Main
# ==========================================
if __name__ == "__main__":

    root = Tk()
    Converter(root)
    root.mainloop()