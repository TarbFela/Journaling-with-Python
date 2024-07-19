from os import startfile

class TextFile:
    def __init__(self,filepath):
        self.filepath = filepath
        try:
            with open(filepath) as f:
                self.text = f.read()
        except:
            print("Error: Could not open", filepath)
        finally:
            print()
    def print_to(self, string = "", end = "\n"):
        with open(self.filepath,'a') as f:
            f.write(string)
            f.write(end)
    def tabular_entry(self, elist, write_to_file=True):
        entry = []
        for item in elist:
            entry.append( "{:<25}".format( str(item) ) )
        if write_to_file:
            for item in entry:
                self.print_to(item, end = "")
            self.print_to() #newline
        else:
            ret_string = ""
            for item in entry:
                ret_string += item
            return ret_string
    def clear_contents(self):
        if input("Are you sure you want to clear the contents of this file? (y)") == 'y':
            with open(self.filepath,'w') as f:
                f.write("")
    def __str__(self):
        with open(self.filepath, 'r') as f:
            return f.read()
    @property
    def header(self):
        return str(self).split("\n")[0].split()
    @header.setter
    def header(self, value):
        if type(value) != list: raise TypeError
        with open(self.filepath, 'r+') as f:
            fcopy = f.read()
            #print(fcopy)
            for i, char in enumerate(fcopy):
                if char == "\n": break
            fcopy = fcopy.replace(fcopy[0:i],self.tabular_entry(value,write_to_file=False))
            #print(fcopy)
        with open(self.filepath, 'w') as f:
            f.write(fcopy)
    def remove_line(self,line_n):
        with open(self.filepath, 'r+') as f:
            fcopy = f.read()
            lines = fcopy.split("\n")
            del lines[line_n]
            fcopy = ""
            for line in lines: #put it back together
                fcopy += line + "\n"
            fcopy = fcopy[:-1] #get rid of trailing newline
        with open(self.filepath, 'w') as f:
            f.write(fcopy)  
            
    def editor(self):
        startfile(self.filepath)

class Little_Directory(TextFile):
    def __init__(self, filepath):
        super().__init__(filepath)
        self.update_info()
    def update_info(self):
        self.text = str(self)
        self.header_info = (self.text.split("\n")[0].split()) #list of header strings
        
        try:
            self.file_info = [ # list of dicts
                {i:t for i, t in zip(self.header_info,row.split()) }
                for row in self.text.split("\n")[1:-1]
                ]
        except:
            self.file_info = None
        
    def user_new_notebook(self):
        entry = {}
        for header in self.header_info: #get the user entry...
            if header != "Filepath":
                entry[header] = (input("Input " + header + ":"))
            else:
                entry["Filepath"] = entry["Title"] + ".txt"
        entry_l = list(entry.values())
        try: #make a file...
            f = open(entry['Filepath'],'x')
            f.close()
            tf = Notebook(entry['Filepath'], new=True, info = entry)
            print(tf)
            self.tabular_entry(entry_l)
            self.update_info()
            print("File Created Successfully")
            return tf
        except FileExistsError:
            print("File with given path already exists.")
        
    @property 
    def notebook(self):
        for i, e in enumerate(self.file_info):
            print(f"\t({i})\t {e['Title']}")
        i = input("Choose a number: ")
        return Notebook(self.file_info[int(i)]["Filepath"])
        
  
class Notebook(TextFile):
    def __init__(self, filepath, new=False, info=None):
        super().__init__(filepath)
        if new:
            if info==None: raise ValueError #"New Notebook Needs Info"
            self.tabular_entry(["---NOTEBOOK---", info['Title'],info['Description']])
        self.Title = self.header[1]
    def user_new_note(self):
        entry = {'Title': input("New Note Title: ")}
        entry['Filepath'] = entry['Title'] + '.txt'
        print(entry['Filepath'])
        try: #make a file...
            f = open(entry['Filepath'],'x')
            f.close()
            tf = Note(
                        entry['Filepath'],
                        info = [entry['Title'], "In: " + self.Title],
                        new = True
                        ) #this will wait for entry to be complete
            print(tf)
            print("File Created Successfully")
            self.tabular_entry([ #get the line number
                    "("+str( len( str(self).split("\n") ) - 1 )+")", entry['Title'], entry['Filepath']
                ])
            return tf
        except:
            print("File with given path already exists.")
    @property
    def file_info(self):
        try:
            lines = str(self).split("\n")[1:]
        except:
            print("Notebook is empty: info generation failed")
            return None
        infot = ["Entry Number","Title","Filepath"]
        return [
            {i:t for i, t in zip(infot, line.split()) }
            for line in lines
            ]
    @property
    def note(self):
        for i, e in enumerate(self.file_info[:-1]):
            print(f"\t({i})\t {e['Title']}")
        i = input("Choose a number: ")
        return Note(self.file_info[int(i)]["Filepath"])
            
        
        
        
        
        
class Note(TextFile):
    def __init__(self, filepath, info = None, new = False):
        super().__init__(filepath)
        if new:
            self.tabular_entry(["---NOTE---"] + info)
            self.Title = info[0]
            
        self.editor()
        input("\nSave File and Press Enter to Continue... ")
        print("File Saved as " + self.filepath)

class UI:
    d = Little_Directory("little_dir.txt") #directory
    nb = None #notebook
    n = None #note
    s = 11 #state
    #state numbering system is two digit.
    #First is Level (directory, nb, n)
    #second is action (0 setup, 1 options, 2 new, 3 edit)
    
    def start(self):
        print("IDEA ENTRY PROGRAM")
        print("Welcome")
        while(True):
            self.state_machine()

    def state_machine(self):
        match self.s:
            case 11: #DIRECTORY STATE
                print()
                print("\t\t\t---DIRECTORY---\n")
                print(self.d)
                print()
                self.s = self.display_options(
                    "---DIRECTORY---",["Exit","Choose Notebook","New Notebook","Delete Notebook"],
                    [0, 20, 12, 13] )
            case 12:
                self.nb = self.d.user_new_notebook()
                self.s = 21
                
            case 13:
                return
            case 20:
                self.nb = self.d.notebook # gets user input to choose notebook
                self.s = 21
            case 21:
                print("\t\t\t---NOTEBOOK---\n")
                print(self.nb)
                print()
                self.s = self.display_options(
                    "---NOTEBOOK---",["Exit","Choose Note","New Note","Delete Note", "Back to Directory"],
                    [0, 30, 22, 23, 11] )
            case 30:
                if (self.nb.file_info == None):
                    print("Notebook is empty. Create a note.")
                    self.s = 21
                self.n = self.nb.note # gets user input to choose note
                self.s = 21 
            case 22:
                self.n = self.nb.user_new_note()
                self.s = 21
            case 23:
                print("not yet programmed")
                self.s = 21
            case 0:
                exit()
            case _:
                print(f"INVALID STATE: {self.s}")
                self.s = 0
        
            
    def display_options(self,message,options_l,states_l):
        print(message)
        for i, opt in enumerate(options_l):
            print(f"\t({i})\t {opt}")
        return states_l[int(input("Enter Number: "))]
            

#make a directory if there isn't one...       
try:
    f = open("little_dir.txt",'x')
    f.close()
    fdir = TextFile("little_dir.txt")
    fdir.tabular_entry(["Title","Filepath","Description"])
    print("Created dir file...")
except FileExistsError:
    f = open("little_dir.txt",'r')
    if len(f.read()) == 0:
        fdir = TextFile("little_dir.txt")
        fdir.tabular_entry(["Title","Filepath","Description"])
    print(f.read())
    f.close()
finally:
    print("dir file success.")




loop = UI()
loop.start()


