#Imports
import customtkinter as ct
from customtkinter import DrawEngine
import time

#Initializations
ct.set_appearance_mode("dark")
DrawEngine.preferred_drawing_method = "polygon_shapes"
#OOP
class App(ct.CTk):
    def __init__(self):
        super().__init__()

        #App configurations
        self.transparency_after = 5 #In seconds
        self.transparency_countingID = None
        self.time1 = time.perf_counter()
        self.title("LC Chat")
        self.app_width = 500
        self.app_height = 280
        self.geometry(f"{self.app_width}x{self.app_height}")  
        self.borders_visible = False
        self.main_transparent = "gray32"
        self.configure(fg_color=self.main_transparent)
        self.attributes("-transparentcolor",self.main_transparent)
        self.background_transparency = 0.65
        self.attributes('-alpha',self.background_transparency)
        self.attributes("-topmost", True)
        self.main_frame = ct.CTkFrame(
            master=self,
            corner_radius=10,        
            fg_color="gray12",       
            bg_color=self.main_transparent 
        )
        self.main_frame.pack(fill="both", expand=True)
        self.resizable(False, False)

        #Transparency alter
        self.bind("<FocusOut>", self.focusedout)
        self.bind("<FocusIn>", self.focusedin)
        

        #User Profile
        self.user = "LoLCraft2"
        self.color= "red"
        

        #Widgets/UI layer
        self.ui_layer = ct.CTkToplevel(self)
        self.ui_layer.overrideredirect(True)
        self.transparent_color = "#000001"
        self.ui_layer.configure(fg_color=self.transparent_color)
        self.ui_layer.attributes("-transparentcolor",self.transparent_color) 
        self.ui_layer.geometry(f"{self.app_width}x{self.app_height}") 
        self.bind("<Configure>", self.sync_windows)
        self.ui_transparency = 0.9
        self.ui_layer.lift()
        self.ui_layer.attributes("-topmost", True)
        self.ui_layer.attributes("-alpha",self.ui_transparency)
        self.bind("<Unmap>", self.on_minimize)
        self.bind("<Map>", self.on_restore)

        #Commands
        self.commands = {
            "alter_border" : self.alter_border,
            "exit" : self.destroy,
            "set_user": self.set_user,
        }

        #Textbox
        self.textbox_width = self.app_width-15
        self.textbox_height = 43
        self.line_height = 15
        self.chatbox()

        #Messagebox
        self.messages_window()
        self.message_box.tag_config("red", foreground="red")


        #Always keep the App on screen
        for window in [self, self.ui_layer]:
             window.attributes("-topmost", True)
             window.attributes("-toolwindow", True) 
        

        
    
    #Commands
    def alter_border(self):
        self.borders_visible = False if self.borders_visible else True
        self.overrideredirect(self.borders_visible)

    def set_user(self, username=None):
        if username == None:
            pass
        self.user = " ".join(username)


    #App
    def alter_transparency(self):
        time2 =  time.perf_counter()
        if time2 - self.time1>self.transparency_after:
            self.attributes("-alpha",self.background_transparency-0.3)
            self.ui_layer.attributes("-alpha",self.ui_transparency-0.3)
        self.transparency_countingID = None

    def focusedin(self, event=None):
        self.time1 = time.perf_counter()
        dimmed = self.ui_transparency - 0.3
        if dimmed == self.ui_layer.attributes("-alpha"):
            self.attributes('-alpha',self.background_transparency)
            self.ui_layer.attributes("-alpha",self.ui_transparency)

    def focusedout(self,event=None):
        if self.transparency_countingID == None:
            self.transparency_counting = self.after(5000,self.alter_transparency)
        else:
            self.after_cancel(self.transparency_countingID)
            self.transparency_counting = self.after(5000,self.alter_transparency)

    def keep_on_top(self):
        self.lift()
        self.ui_layer.lift()
        self.after(1000, self.keep_on_top)

    def on_minimize(self, event):
        if event.widget == self:
            self.ui_layer.withdraw()

    def on_restore(self, event):
        if event.widget == self:
            self.ui_layer.deiconify()
            self.ui_layer.lift() 

    def sync_windows(self, event=None):
        x = self.winfo_x()
        y = self.winfo_y()
        fix= [7,0]
        if not self.borders_visible:
            fix = [18,37]
        self.ui_layer.geometry(f"+{x+fix[0]}+{y+fix[1]}")
        
        if self.state() == 'iconic':
            self.ui_layer.withdraw()
        else:
            self.ui_layer.deiconify()

    def messages_window(self):
        self.message_box = ct.CTkTextbox(master=self.ui_layer, 
                                     width=self.textbox_width,
                                     height=self.app_height-self.textbox_height-10, 
                                     border_spacing=10,
                                     wrap="word",
                                     fg_color=self.transparent_color,
                                     bg_color=self.transparent_color)
        self.message_box.insert("0.0","Type .c to run commands!")
        self.message_box.configure(state="disabled")    
        self.message_box.place(x=0,y=0)
    
    def send_message(self, message):
        self.message_box.configure(state="normal")
        self.message_box.insert("end",f"\n{self.user}", "red")


        self.message_box.insert("end", f": {message}")

        

        self.message_box.configure(state="disabled")

    def run_commands(self,contents):
        
        check_command = contents.split(".c ")[1]
        full_command = check_command.split(" ")
        command = full_command[0]

        if command not in self.commands:
            return "break" 

        command_variables = full_command[1::]

        if not command_variables:
                self.commands[command]()
                return "break"
        self.commands[command](command_variables)
     
    def messages(self,event=None):
        contents = self.textbox.get("0.0","end-1c")

        if not contents:
            return "break"        
            
        self.textbox.delete("0.0", "end-1c")
        self.chatbox_resize()

        #Check for commands
        length_of_contents = len(contents)
        if length_of_contents < 3:
            self.send_message(contents)
            return "break"
        
        if "".join([contents[0],contents[1]]) == ".c":
            self.run_commands(contents)
        else:
            self.send_message(contents)
            return "break"
            

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
        max_window_height = 325    
        new_window = self.app_height +(lines)*self.line_height
        final_window = min(new_window,max_window_height)
        self.geometry(f"{self.app_width}x{final_window}")
        self.ui_layer.geometry(f"{self.app_width}x{final_window}")

    def select_all(self,event=None):
        event.widget.tag_add("sel", "0.0", "end-1c")
        return "break"
    
    def add_placeholder(self,event=None):
        self.focusedout()
        if not self.textbox.get("0.0", "end-1c"):
            self.textbox.insert("0.0",self.placeholder)
            self.textbox.configure(text_color="gray")     
    
    def remove_placeholder(self,event=None):
        self.focusedin()
        if self.textbox.get("0.0", "end-1c") == self.placeholder:
            self.textbox.delete("0.0", "end")
            self.textbox.configure(text_color="white")

    def chatbox(self):
        
        self.textbox = ct.CTkTextbox(master=self.ui_layer, 
                                     width=self.textbox_width,
                                     height=self.textbox_height,
                                     corner_radius=5, 
                                     border_width=1,
                                     border_spacing=12,
                                     wrap="word",
                                     text_color="gray",
                                     fg_color="gray15")
        self.textbox.place(x=0,y=self.app_height-self.textbox_height-10)

        #Hotkeys
        self.textbox.bind("<Control-A>", self.select_all)
        self.textbox.bind("<Control-a>", self.select_all)
        self.textbox.bind("<Double-Button-1>", self.select_all)
        self.textbox.bind("<Return>",self.messages)
        self.textbox.bind("<Shift-Return>",lambda e: "break")
        self.textbox.bind("<KeyPress>", self.chatbox_resize)

        #Add placeholder text
        self.placeholder = "Enter your message"
        self.textbox.insert("0.0",self.placeholder)
        self.textbox.bind("<FocusOut>", self.add_placeholder)
        self.textbox.bind("<FocusIn>",self.remove_placeholder)

        
        
app = App()
app.mainloop()