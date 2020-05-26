#note that this scripts only solves sudoku grid that admit only one solution and doesn't care about those that don't
from random import randint
class Grid():
    #base constructor, 
    def __init__(self,cols=9,g=[]):
        super().__init__()
        if(g):
            self._cols=len(g)
            self.g=list(g)
        else:
            self._cols=cols
            self.g=[[0 for i in range(self._cols)] for j in range(self._cols)]
    #method used to draw the grid if the script is executed on a console
    def draw_grid(self):
        for i in self.g:
            for j in i:
                print(j,end=" ")
            print()
        print("\n\n\n\n")
    #copying the data in the grid to another list 
    def store_grid_values(self,*storage):
        for storage_list in storage:
            storage_list.clear()
        for i in self.g:
                temporary=[]
                for j in i:
                    temporary.append(j)
                for storage_list in storage:
                    storage_list.append(temporary)
    #loading data from a list to our current Grid instance's g
    def get_grid_values(self,origin):
        self.g.clear()
        for i in origin:
            temporary=[]
            for j in i:
                temporary.append(j)
            self.g.append(temporary)
    #grid getter
    def get_g(self):
        return self.g
    def get_cell(self,x,y):
        return self.g[x][y]
    #not quite the right place for this method but I wasn't able to put this method in the controller file
    #I used it to generate a new grid each time the user clicks on generate to generate a new grid
    def generate(self):
        self.fill_grid()
        self.strip_values(20)
        return self.g
    #the core method for filling the grid, we use this method for filling each square of the grid
    def fill_square(self,coord,count=9):
        #if we are filling the top left square ,central square, or bottom right one
        #we only verify wether the number we are entering in a certain cell is not in that square already
        #we do this verification using the method missing,that returns a list of numbers that are missing
        #in that square ,then we pick a random number from one of those.
        if coord[0]==coord[1]:
           for i in range(3):
               for j in range(3):
                    available_position=self.missing(self.square(coord[0]*3,coord[1]*3))
                    try:
                        self.g[(coord[0]-1)*3+i][(coord[1]-1)*3+j]=available_position[randint(0,len(available_position)-1)]
                    except ValueError:
                        self.g[(coord[0]-1)*3+i][(coord[1]-1)*3+j]=available_position[0]
        # if it's one of the other squares we construct a list containing all availble numbers for
        #for each cell that isn't filled yet.
        #this method is a recursive function that is executed as many time as the number of the square's  cells
        else:
            if count>0:
                allpositions=[]
                for i in range(3):
                    for j in range(3):
                        if self.g[(coord[0]-1)*3+i][(coord[1]-1)*3+j]==0:
                            square_available=self.missing(self.square(coord[0]*3,coord[1]*3))
                            line_availabale=self.missing(self.line((coord[0]-1)*3+i+1,(coord[1]-1)*3+j+1))
                            column_available=self.missing(self.column((coord[0]-1)*3+i+1,(coord[1]-1)*3+j+1))
                            available_position=[a for a in square_available if a in line_availabale and a in column_available]
                            allpositions.append((available_position,(coord[0]-1)*3+i,(coord[1]-1)*3+j))
                #we then proceed to the search of the elements of the list that contain the least number of choices
                #to minimize the number of errors that our program may do
                #since our program may do error each time it has to pick a number randomly( the error that may be done is 
                #that our square by the end of this function may still contain 0s)
                suitable=[i for i in allpositions if len(i[0])==min([len(i[0]) for i in allpositions])]
                #we check this to avoid the value error exception.
                if len(suitable)-1:
                    available_position,x,y=suitable[randint(0,len(suitable)-1)]
                else:
                    available_position,x,y=suitable[0]
                if len(available_position)-1:
                    self.g[x][y]=available_position[randint(0,len(available_position)-1)]
                else:
                    self.g[x][y]=available_position[0]
                self.fill_square(coord,count-1)
    # before diving in this function I want to clarify that the solution emplemented here isn't not the only solution
    # and I very much doubt that it's the most efficient one ,this only consist in an effort to construct a sudoku_grid generator
    def fill_grid(self):
        self.g=[[0 for i in range(self._cols)] for j in range(self._cols)]
        self.fill_square((1,1))
        self.fill_square((2,2))
        self.fill_square((3,3))
        try:
            self.fill_square((1,2))
            self.fill_square((1,3))
            self.fill_square((2,1))
            self.fill_square((3,1))
            self.fill_square((3,2))
            self.fill_square((2,3))
        except ValueError:
            self.g=[[0 for i in range(self._cols)] for j in range(self._cols)]
            self.fill_grid()
    #after having a filled grid ,we need to strip it from a certain number of its values
    #we do that through mirror striping (see mirror strip)
    #after each mirror strip we perform we have to check if the grid has a unique solution or not
    #we do that by calling the solve function
    #if the function can't solve it that means the solution is not unique
    #we do this until the we get a grid striped from 2*n of its values with a unique solution
    def strip_values(self,lvl):    
        copy_lvl=lvl
        g1,g2=list(),list()
        self.store_grid_values(g1,g2)
        while(g1==self.g and lvl>0):
            self.get_grid_values(g2)
            self.mirror_strip((randint(1,9),randint(1,9)))
            self.store_grid_values(g2)
            try:
                self.solve()
                lvl-=1
            except RecursionError:
                break
        if lvl:
            self.get_grid_values(g1)
            self.strip_values(copy_lvl)
        else:
            self.get_grid_values(g2)
    #this method performs a mirror strip on the grid ,mirror striping in removing an element and its
    # mirror element on the grid 
    def mirror_strip(self,coord):
        self.g[coord[0]-1][coord[1]-1]=0
        self.g[(self._cols-1)-(coord[0]-1)][(self._cols-1)-(coord[1]-1)]=0
    #method that returns the square(list of elements that are in the square) to which a certain given point belongs
    def square(self,x,y):
        line=((x-1)//3)*3
        column=((y-1)//3)*3
        temporary=[]
        for i in range(line,line+3):
            for j in range(column,column+3):
                 temporary.append(self.g[i][j])
        return temporary
    #method that returns the line(list of elements that are in the line) to which a certain given point belongs
    def line(self,x,y):
        return [i for i in self.g[x-1]]
    #method that returns the column(list of elements that are in the column) to which a certain given point belongs
    def column(self,x,y):
        return [i[y-1] for i in self.g]
    def missing(*lists):
        numbers=[1,2,3,4,5,6,7,8,9]
        for current_l in lists[1:]:    
            nb=[]
            for i in range(len(numbers)):
                if numbers[i] in current_l:
                    nb.append(numbers[i])
            numbers=[i for i in numbers if i not in nb]
        return numbers
    #the solver function , we operate in this function using the fact that each grid has only a unique solution
    #following this reasoning we find that at each state of the grid there's at least one cell that can only have one value
    #(if at a giben state of the grid there's no cell that accepts only one value, that means that this grid accepts more than one solution)
    def solve(self):
        #we emplement this logic by loopinfg through the cells of the grid and looking for the ones that admit only one solution
        for i in range(len(self.g)):
            for j in range(len(self.g)):
                if not self.g[i][j]:
                    options=self.missing(self.line(i+1,j+1),self.column(i+1,j+1),self.square(i+1,j+1))
                    if len(options)==1:
                        self.g[i][j]=options[0]
        #after that , we check if the grid still contains blank elements(0) , if so we call the solve function another time ,if not then we have a solved grid
        for i in range(len(self.g)):
            for j in range(len(self.g)):
                if not self.g[i][j]:
                    self.solve()
if __name__=="__main__":
    import pdb
    while True:
        pdb.set_trace()
        g=Grid()
        g.draw_grid()
        print()
        g.fill_grid()
        print("\n\n\n\n\n\nstrip values")
        g.strip_values(20)
        g.draw_grid()
        print("\n\n\n\n\n\nsovlved")
        g.solve()
        g.draw_grid()
