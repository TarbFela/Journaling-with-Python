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
            del tf
            self.tabular_entry(entry_l)
            self.update_info()
            print("File Created Successfully")
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
        except:
            print("File with given path already exists.")
    @property
    def file_info(self):
        try:
            lines = str(self).split("\n")[1:]
        except:
            print("Notebook is empty: info generation failed")
            return
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
        print("File Saved as" + self.filepath)
        
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



d = Little_Directory("little_dir.txt")
print(d)
#d.user_new_notebook()


