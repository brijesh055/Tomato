import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json
import urllib.request
import io

class SmileyGame:
    def __init__(self, root, player_name):

        self.root = root
        self.root.title("Tomato Game")
        self.root.geometry("800x600+350+100")
        self.root.resizable(False, False)

        self.name = player_name
        self.score = 0
        self.imagelab = tk.Label(root)
        self.imagelab.place(x=70, y=100)

        logout = tk.Button(root, text="Quit", command=self.logout, cursor="hand2", font=(
            "Helvetica 15 underline"), bg="#d77337", fg="Black", activebackground="blue")
        logout.place(x=600, y=20, width=120)

        welcome_text = f'WELCOME {self.name}'
        title = tk.Label(root, text=welcome_text, font=("Impact", 36, "bold"), bg='#FDE8E3', fg="blue")
        title.place(x=220, y=10)

        self.answer = tk.Entry(root, font=("times new Roman", 14), bg="lightgray")
        self.answer.place(x=300, y=520, width=200, height=50)

        result = tk.Button(root, text="Submit", cursor="hand2", command=lambda: self.check_answer(),
                           font=("times new Roman", 14), bg="#d05d20", fg="white")
        result.place(x=100, y=525, width=120)

        self.score_res = tk.Label(root, font=("times new Roman", 22))
        self.score_res.place(x=600, y=525)
        self.score_res.config(text=f'Score: {str(self.score)}')

        self.photo = None

        self.show_image()

    def show_image(self):
        self.ques, self.soln = SmileyGame.get_image()
        with urllib.request.urlopen(self.ques) as u:
            raw_data = u.read()
        image = Image.open(io.BytesIO(raw_data))
        self.photo = ImageTk.PhotoImage(image)
        self.imagelab.config(image=self.photo)
        self.imagelab.image = self.photo
        self.imagelab.update()

    def logout(self):
        if messagebox.askyesno("Log Out", "Are you sure you want to log out?", parent=self.root):
            self.root.destroy()
            login_page()

    @staticmethod
    def get_image():
        api_url = "http://marcconrad.com/uob/tomato/api.php"
        response = urllib.request.urlopen(api_url)
        smile_json = json.loads(response.read())
        question = smile_json['question']
        solution = smile_json['solution']
        return question, str(solution)

    def check_answer(self):
        user_answer = self.answer.get()

        if user_answer.lower() == self.soln.lower():
            self.score += 1
            self.score_res.config(text=f'Score: {str(self.score)}')
            self.show_image()
            self.answer.delete(0, tk.END)
        else:
            messagebox.showinfo("Incorrect", "Sorry, that's not the correct answer. Try again!")

def login_page():
    login = tk.Tk()
    login.title("Login Page")
    login.geometry("400x200+500+200")

    frame = ttk.Frame(login, padding="10")
    frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)

    name_label = ttk.Label(frame, text="Enter your name:")
    name_label.grid(column=0, row=0, sticky=tk.W, pady=10)
    name_entry = ttk.Entry(frame, font=("times new Roman", 14), width=20)
    name_entry.grid(column=1, row=0, sticky=tk.W, pady=10)

    start_game_button = ttk.Button(frame, text="play ", command=lambda: start_game(login, name_entry.get()))
    start_game_button.grid(column=1, row=1, sticky=tk.W, pady=10)

    login.mainloop()

def start_game(login, name):
    if not name:
        messagebox.showinfo("Error", "Please enter your name.")
    else:
        login.destroy()
        root = tk.Tk()
        root.title("Tomato Game")
        root.geometry("800x600+350+100")
        root.resizable(False, False)

        game = SmileyGame(root, name)
        root.mainloop()

login_page()