from tkinter import *
from tkinter.ttk import * 
from testcsv import *
from tkinter import ttk
import approve
import reject
import os
from approve_and_merge import *

class App(Frame):
    
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.selection = []


        #setup the tree layout for the chart
        self.tree = Treeview(self)
        
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)        

        self.yscrollbar = Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.yscrollbar.set)
        
        
        self.xscrollbar = Scrollbar(self, orient='horizontal', command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.xscrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        self.yscrollbar.grid(row=0, column=1, sticky='ns')
        self.yscrollbar.configure(command=self.tree.yview)
                    
        self.approve = Button(self, text='Approve', command = self.accept_button)
        self.approve.grid(row=2, column = 0, sticky = 'w')
        
        self.reject = Button(self, text='Reject', command = self.reject_button)
        self.reject.grid(row=3, column = 0 , sticky = 'w')

        
        self.row_from = Entry(self,width=10)
        self.row_to = Entry(self,width=10)   
        self.row_from.grid(row=4,column=0,sticky = 'w')
        self.row_to.grid(row=5,column=0,sticky = 'w')

        self.update = Button(self, text='Update', command = self.update_git)
        self.update.grid(row=6, column = 0 , sticky = 'w')
        
        self.close = Button(self, text='Close', command = self.close_button)
        self.close.grid(row=7, column = 0 , sticky = 'w')
    
        self.xscrollbar.grid(row=1, column=0, sticky='ew')
        self.xscrollbar.configure(command=self.tree.xview)      

        self.grid_rowconfigure(0, weight=20)
        self.grid_columnconfigure(0, weight=1)
  
        self.CreateUI('combined.csv')

    # NEW ADDITION -- SELECT RETURNS BACK ALL SELECTED    
    def on_tree_select(self, event):
        self.selection = []
        for item in self.tree.selection():
            item_text = self.tree.item(item,"text")
            self.selection.append(item_text)


    def close_button(self):
        self.destroy()
        exit()
  
    def accept_button(self):
        approve.approve(self.selection, 'combined.csv')
        self.tree.delete(*self.tree.get_children())
        self.CreateUI('combined.csv')

    def reject_button(self):
        reject.reject(self.selection)
        self.tree.delete(*self.tree.get_children())
        self.CreateUI('combined.csv')

    def update_git(self):
        approve_and_merge("https://github.com/OpenExoplanetCatalogue/open_exoplanet_catalogue", "adwen")

    def CreateUI(self,file_name):
        mylist = read_csv(file_name)

        param_name = tuple(mylist[0])

    

        #setup the parameters(heading)
        self.tree['columns'] = param_name
        width_list = [150, 100, 250, 100, 100, 100, 100]
        for i in (range(len(param_name))):
            self.tree.column(param_name[i], anchor='w', width=width_list[i])
            self.tree.heading(param_name[i], text=param_name[i])
        

        self.tree.grid(sticky = (N,S,W,E))

       # mylist = read_csv('formatted.csv')
        mylist.pop(0)
        #(insert the data for each row)
        for i in (range(len(mylist))):
            row_value = tuple(mylist[i])
            
            self.tree.insert('', 'end', text=str(i), values=row_value)


def reduce_cycle():
    '''
    reduces the last column of rejected_updates.csv rows which represent
    daily checks. After 31 checks happen, the file will be deleted from the
    rejected_updates.csv file.
    
    What actually happens: Everytime display.py is opened/ran, it will check
    for the file rejected_updates.csv and if it exists reduce the last column
    of each row except the attribute header row by 1 until it is 0 and the
    function doesn't write it in.
    '''
    cwd = os.getcwd()
    rejected = open(os.path.join(cwd, "rejected_updates.csv"), 'r')
    all_rejected = rejected.read()
    list_reject = all_rejected.split('\n')
    i = 0
    rows = ""
    beginning = list_reject[0] + '\n'
    end = list_reject[-1]
    for string in list_reject[1:-1]:
        if ((int(string[string.rfind(',')+1:]) - 1) > 0):
            rows  = rows + string[:string.rfind(',') + 1] + (str(int(string[string.rfind(',')+1:]) - 1)) + '\n'
    rejected.close()
    rejected = open(os.path.join(cwd, "rejected_updates.csv"), 'w')
    rejected.write(beginning)
    rejected.write(rows)
    rejected.write(end)
    rejected.close()

if __name__ == "__main__":
    cwd = os.getcwd()
    if (os.path.isfile(os.path.join(cwd, "rejected_updates.csv"))):
        reduce_cycle()    
    root = Tk()
    root.title("MyApp")
    app = App(root)
    app.pack(fill="both", expand=True)
    app.mainloop()
    
