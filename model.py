from random import randint
import time

# First i fixed PEP warnings with Pycharm, you'll notice a difference

# Here, You don't need the parentheses after the class name*


class Grid:
    """
    It is good to have your classes and methods documented in this way.
    It allows to automatically generate beautiful documentation web pages.
    And also it has nice features for the methods... you'll see
    """
    # So from now on, i'll use this form of comments just for my remarks
    # In the g argument, it's not good to have a default parameter as an empty array.
    # The warning says "default argument value is mutable"
    # This article explains in more details
    # https://florimond.dev/blog/articles/2018/08/python-mutable-defaults-are-the-source-of-all-evil/
    # So i advice you to replace it with a None, and then check the None if the method
    # & Then replace with an empty array if needed
    def __init__(self, cols=9, g=None):
        """
        Like this you can define documentation for methoods.
        Explain what they do, & what the variables mean, in this way
        :param cols: I couldn't guess up to this point, below (in the code) i can indicate the expected type
        :type cols: int
        :param: g: the content of the grid i guess
        :type g: list
        """
        super().__init__()
        if g is None:
            # But i guess in this case you can just replace if (g) with if g is not None
            g = []
        # No need for parentheses around g
        # You are marking cols as a private attribute & g not as a private attribute
        # If there's a good reason for that then it's okay
        # Otherwise you should really have a uniform naming
        if g:
            self._cols = len(g)
            self.g = list(g)
        else:
            self._cols = cols
            self.g = [[0 for i in range(self._cols)] for j in range(self._cols)]

    def compare_to_grid(self, obj):
        """
        another documentation for another method
        :param obj: a grid i guess
        :type obj: list
        :rtype: bool
        """
        for i in range(len(self.g)):
            for j in range(len(self.g[i])):
                if self.g[i][j] != obj[i][j]:
                    return False
        return True

    def solved(self):
        for i in self.g:
            for j in i:
                if not j:
                    return False
        return True

    def draw_grid(self):
        """
        This method is used to draw the grid if the script is executed on a console
        """
        for i in self.g:
            # You can also replace this loop with print(" ".join(i))
            # Or even the two loops with print("\n".join([i for i in self.g]))
            for j in i:
                print(j, end=" ")
            print()
        print("\n\n\n\n")

    # copying the data in the grid to another list
    # I'm not sure the *storage is used well, there are no pointers in python
    def store_grid_values(self, *storage):
        for storage_list in storage:
            storage_list.clear()
        for i in self.g:
            temporary = []
            for j in i:
                temporary.append(j)
            for storage_list in storage:
                storage_list.append(temporary)

    # loading data from a list to our current Grid instance's g
    def get_grid_values(self, origin):
        self.g.clear()
        for i in origin:
            temporary = []
            for j in i:
                temporary.append(j)
            self.g.append(temporary)

    # grid getter
    # as it is right now, you don't need the getter since the attribute is set public
    def get_g(self):
        return self.g

    def get_cell(self, x, y):
        return self.g[x][y]

    # not quite the right place for this method but I wasn't able to put this method in the controller file
    # I used it to generate a new grid each time the user clicks on generate to generate a new grid
    # You could have a static method, or have this one called in the constructor
    def generate(self):
        self.fill_grid()
        self.strip_values(35)
        return self.g

    # the core method for filling the grid, we use this method for filling each square of the grid
    def fill_square(self, coord, count=9):
        # if we are filling the top left square ,central square, or bottom right one
        # we only verify wether the number we are entering in a certain cell is not in that square already
        # we do this verification using the method missing,that returns a list of numbers that are missing
        # in that square ,then we pick a random number from one of those.
        if coord[0] == coord[1]:
            for i in range(3):
                for j in range(3):
                    available_position = self.missing(self.square(coord[0] * 3, coord[1] * 3))
                    try:
                        self.g[(coord[0] - 1) * 3 + i][(coord[1] - 1) * 3 + j] = available_position[
                            randint(0, len(available_position) - 1)]
                    except ValueError:
                        self.g[(coord[0] - 1) * 3 + i][(coord[1] - 1) * 3 + j] = available_position[0]
        # if it's one of the other squares we construct a list containing all availble numbers for
        # for each cell that isn't filled yet.
        # this method is a recursive function that is executed as many time as the number of the square's  cells
        else:
            if count > 0:
                allpositions = []
                for i in range(3):
                    for j in range(3):
                        if self.g[(coord[0] - 1) * 3 + i][(coord[1] - 1) * 3 + j] == 0:
                            square_available = self.missing(self.square(coord[0] * 3, coord[1] * 3))
                            line_availabale = self.missing(
                                self.line((coord[0] - 1) * 3 + i + 1, (coord[1] - 1) * 3 + j + 1))
                            column_available = self.missing(
                                self.column((coord[0] - 1) * 3 + i + 1, (coord[1] - 1) * 3 + j + 1))
                            available_position = [a for a in square_available if
                                                  a in line_availabale and a in column_available]
                            allpositions.append((available_position, (coord[0] - 1) * 3 + i, (coord[1] - 1) * 3 + j))
                # we then proceed to the search of the elements of the list that contain the least number of choices
                # to minimize the number of errors that our program may do
                # since our program may do error each time it has to pick a number randomly( the error that may be done is
                # that our square by the end of this function may still contain 0s)
                suitable = [i for i in allpositions if len(i[0]) == min([len(i[0]) for i in allpositions])]
                # we check this to avoid the value error exception.
                if len(suitable) - 1:
                    available_position, x, y = suitable[randint(0, len(suitable) - 1)]
                else:
                    available_position, x, y = suitable[0]
                if len(available_position) - 1:
                    self.g[x][y] = available_position[randint(0, len(available_position) - 1)]
                else:
                    self.g[x][y] = available_position[0]
                self.fill_square(coord, count - 1)

    # before diving in this function I want to clarify that the solution emplemented here isn't not the only solution
    # and I very much doubt that it's the most efficient one ,this only consist in an effort to construct a sudoku_grid generator
    def fill_grid(self):
        self.g = [[0 for i in range(self._cols)] for j in range(self._cols)]
        self.fill_square((1, 1))
        self.fill_square((2, 2))
        self.fill_square((3, 3))
        try:
            self.fill_square((1, 2))
            self.fill_square((1, 3))
            self.fill_square((2, 1))
            self.fill_square((3, 1))
            self.fill_square((3, 2))
            self.fill_square((2, 3))
        except ValueError:
            self.g = [[0 for i in range(self._cols)] for j in range(self._cols)]
            self.fill_grid()

    # after having a filled grid ,we need to strip it from a certain number of its values
    # we do that through mirror striping (see mirror strip)
    # after each mirror strip we perform we have to check if the grid has a unique solution or not
    # we do that by calling the solve function
    # if the function can't solve it that means the solution is not unique
    # we do this until the we get a grid striped from 2*n of its values with a unique solution
    def strip_values(self, lvl):
        copy_lvl = lvl
        g1, g2 = list(), list()
        self.store_grid_values(g1, g2)
        while (g1 == self.g and lvl >= 0):
            self.get_grid_values(g2)
            self.mirror_strip((randint(1, 9), randint(1, 9)))
            self.store_grid_values(g2)
            self.solve()
            lvl -= 1
        if lvl:
            self.get_grid_values(g1)
            self.strip_values(copy_lvl)
        else:
            self.get_grid_values(g2)

    # this method performs a mirror strip on the grid ,mirror striping in removing an element and its
    # mirror element on the grid 
    def mirror_strip(self, coord):
        self.g[coord[0] - 1][coord[1] - 1] = 0
        self.g[(self._cols - 1) - (coord[0] - 1)][(self._cols - 1) - (coord[1] - 1)] = 0

    def square(self, x, y):
        line = ((x - 1) // 3) * 3
        column = ((y - 1) // 3) * 3
        temporary = []
        for i in range(line, line + 3):
            for j in range(column, column + 3):
                temporary.append(self.g[i][j])
        return temporary

    def line(self, x, y):
        return [i for i in self.g[x - 1]]

    def column(self, x, y):
        return [i[y - 1] for i in self.g]

    def my_missing(self, *lists):
        numbers = set([i+1 for i in range(self._cols)])
        return list(numbers.difference(*lists))
        # i could even do it in one line return(set([i+1 for i in range(self._cols)]).difference(*lists))

    def missing(*lists):
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for current_l in lists[1:]:
            nb = []
            for i in range(len(numbers)):
                if numbers[i] in current_l:
                    nb.append(numbers[i])
            numbers = [i for i in numbers if i not in nb]
        return numbers

    def solve(self):
        copy = []
        self.store_grid_values(copy)
        done = True
        while (done):
            done = False
            for i in range(len(self.g)):
                for j in range(len(self.g)):
                    if not self.g[i][j]:
                        options = self.missing(self.line(i + 1, j + 1), self.column(i + 1, j + 1),
                                               self.square(i + 1, j + 1))
                        if len(options) == 1:
                            self.g[i][j] = options[0]
                            done = True
            g1 = Grid()
            index = 0
            while (not g1.solved()):
                self.solve_backtrack((0, 0), index, g1)
                index += 1
            self.get_grid_values(g1.g)

    def solve_backtrack(self, position, index, resptacle):
        self.g[position[0]][position[1]] = 0
        if len(self.missing(self.line(position[0] + 1, position[1] + 1), self.column(position[0] + 1, position[1] + 1),
                            self.square(position[0] + 1, position[1] + 1))) > 0:
            self.g[position[0]][position[1]] = \
            self.missing(self.line(position[0] + 1, position[1] + 1), self.column(position[0] + 1, position[1] + 1),
                         self.square(position[0] + 1, position[1] + 1))[index]
            for i in range(len(self.g)):
                for j in range(len(self.g)):
                    if not self.g[i][j]:
                        break
                if not self.g[i][j]:
                    break
            new_position = (i, j)
            if len(self.missing(self.line(new_position[0] + 1, new_position[1] + 1),
                                self.column(new_position[0] + 1, new_position[1] + 1),
                                self.square(new_position[0] + 1, new_position[1] + 1))):
                for index in range(len(self.missing(self.line(new_position[0] + 1, new_position[1] + 1),
                                                    self.column(new_position[0] + 1, new_position[1] + 1),
                                                    self.square(new_position[0] + 1, new_position[1] + 1)))):
                    self.solve_backtrack(new_position, index, resptacle)
                    self.g[new_position[0]][new_position[1]] = 0
            if self.solved():
                l = []
                self.store_grid_values(l)
                resptacle.g = l


if __name__ == "__main__":
    g2 = Grid(g=[[0, 0, 6, 0, 4, 0, 3, 0, 0], [7, 8, 3, 0, 0, 0, 1, 4, 5], [0, 0, 4, 0, 8, 0, 2, 0, 0],
                 [0, 0, 0, 1, 0, 2, 0, 0, 0], [1, 6, 0, 0, 0, 0, 0, 9, 2],
                 [0, 0, 0, 4, 0, 8, 0, 0, 0], [0, 0, 1, 0, 5, 0, 9, 0, 0], [6, 3, 7, 0, 0, 0, 5, 8, 4],
                 [0, 0, 9, 0, 7, 0, 6, 0, 0]])
    g2.draw_grid()
    print("\n\n\n\n\n\nsolved")
    g1 = Grid(g=[[0, 0, 6, 0, 4, 0, 3, 0, 0], [7, 8, 3, 0, 0, 0, 1, 4, 5], [0, 0, 4, 0, 8, 0, 2, 0, 0],
                 [0, 0, 0, 1, 0, 2, 0, 0, 0], [1, 6, 0, 0, 0, 0, 0, 9, 2],
                 [0, 0, 0, 4, 0, 8, 0, 0, 0], [0, 0, 1, 0, 5, 0, 9, 0, 0], [6, 3, 7, 0, 0, 0, 5, 8, 4],
                 [0, 0, 9, 0, 7, 0, 6, 0, 0]])
    index = 0
    start = time.time()
    while (not g1.solved()):
        g2.solve_backtrack((0, 0), index, g1)
        index += 1
    g1.draw_grid()
    end = time.time()
    print(end - start)
    g2 = Grid(g=[[0, 0, 6, 0, 4, 0, 3, 0, 0], [7, 8, 3, 0, 0, 0, 1, 4, 5], [0, 0, 4, 0, 8, 0, 2, 0, 0],
                 [0, 0, 0, 1, 0, 2, 0, 0, 0], [1, 6, 0, 0, 0, 0, 0, 9, 2],
                 [0, 0, 0, 4, 0, 8, 0, 0, 0], [0, 0, 1, 0, 5, 0, 9, 0, 0], [6, 3, 7, 0, 0, 0, 5, 8, 4],
                 [0, 0, 9, 0, 7, 0, 6, 0, 0]])
    g2.draw_grid()
    print("\n\n\n\n\n\nsolved")
    start = time.time()
    g2.solve()
    end = time.time()
    print(end - start)
    g2.draw_grid()
    g3 = Grid()
    g3.fill_grid()
    g3.strip_values(28)
    g3.draw_grid()
    g3.solve()
    g3.draw_grid()
