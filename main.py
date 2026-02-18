#Imports
import customtkinter as ct

#Initializations
ct.set_appearance_mode("dark")

#OOP
class App(ct.CTk):
    def __init__(self):
        super().__init__()
        self.app_width = 586
        self.app_height = 325
        self.geometry(f"{self.app_width}x{self.app_height}")       
        
        #Textbox
        self.textbox_width = 570
        self.textbox_height = 43
        self.line_height = 15
        self.chatbox()

    def messages(self,event=None):
        contents = self.textbox.get("0.0","end-1c")
        self.textbox.delete("0.0", "end-1c")
        self.chatbox_resize()
        return "break"

    def chatbox_resize(self,event=None):

        try:
            lines = int(self.textbox._textbox.tk.call(
                self.textbox._textbox._w, "count", "-displaylines", "1.0", "end-1c"
            ))
        except:
            lines = 1

        #For Textbox size 
        max_height = 88
        new_height = self.textbox_height + (lines)*self.line_height
        self.textbox.configure(height=min(new_height,max_height))

        #For Window size
        max_window_height = 370    
        new_window = self.app_height +(lines)*self.line_height
        final_window = min(new_window,max_window_height)
        self.geometry(f"{self.app_width}x{final_window}")

    
    def add_placeholder(self,event=None):
        if not self.textbox.get("0.0", "end-1c"):
            self.textbox.insert("0.0",self.placeholder)
            self.textbox.configure(text_color="gray")     
    
    def remove_placeholder(self,event=None):
        if self.textbox.get("0.0", "end-1c") == self.placeholder:
            self.textbox.delete("0.0", "end")
            self.textbox.configure(text_color="white")

    def chatbox(self):
        
        self.textbox = ct.CTkTextbox(master=self, 
                                     width=self.textbox_width,
                                     height=self.textbox_height,
                                     corner_radius=5, 
                                     border_width=1,
                                     border_spacing=12,
                                     wrap="word",
                                     text_color="gray")
        self.textbox.pack()
        self.textbox.place(x=7,y=270)

        self.textbox.bind("<Return>",self.messages)
        self.textbox.bind("<Shift-Return>",lambda e: "break")
        self.textbox.bind("<KeyPress>", self.chatbox_resize)

        self.placeholder = "Enter your message"
        self.textbox.insert("0.0",self.placeholder)
        self.textbox.bind("<FocusOut>", self.add_placeholder)
        self.textbox.bind("<FocusIn>",self.remove_placeholder)




app = App()

app.mainloop()