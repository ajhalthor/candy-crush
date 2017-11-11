import copy
import signal
import time

class V:
    """The value of a node

    A node consists of 2 values:
        - value (int): score of obtained till end of game
        - move (tuple): the candy crushed
    """
    def __init__(self, player):
        if player == 'min':
            self.value = 1000000
            self.move = ()
        else:
            self.value = -1000000
            self.move = ()
            
            
class Node:
    """Nodes of the Tree that represent MAX and MIN players"""

    def __init__(self, player, board, alpha, beta):
        """Node Constructor

        Args:
            - player (str): MAX or MIN
            - board (list of list of `str`): NxN board of candies.
            - alpha (int): Best end score of MAX 
            - beta (int): Best end score of MIN  

        Node:
            value of node `v` consists of 2 components shown in class `V`.

        """
        self.player = player
        self.board = board

        self.alpha = alpha
        self.beta = beta
        self.v = V(player) 

        self.visited = False #Node has not been traversed

class Graph:
    """Graph spcifically for crushing candies

    Graph is used for board manipulation and determining possible moves.
    """
 
    def __init__(self, N, p, g):
        """Graph Constructor
- 
        Args:
            - N (int): Board Dimension
            - p (int): Number of unique candies
            - g (list of list of `str`): Instance of input board

        """
        self.nrows = N
        self.ncols = N
        self.graph = g
        self.p = p

        self.p_arr = []

 
    def isSafe(self, i, j, visited, l):
        """A function to check if a given cell (row, col) can be included in DFS

        Args:
            - i (int): row of candy
            - j (int): column of candy
            - visited(list of list of `boolean`): True if cell has been checked

        Returns:
            boolean: whether to include a cell in the next DFS iteration.
        """

        # row number is in range, column number is in range and value is 1 and not yet visited
        return (i >= 0 and i < self.nrows and
                j >= 0 and j < self.ncols and
                not visited[i][j] and self.graph[i][j]==l)
             
    
    def DFS(self, i, j, visited, current_score, l, safe_path):
        """A utility function to do DFS for a 2D boolean matrix. It only considers the 4 neighbours as adjacent vertices.

        Args:
            - i (int): cell row
            - j (int): cell column
            - visited (list of list of boolean): Each cell determines if cell has been visited
            - current_score(int): Number of candies crused from the move
            - l (int): Candy number
            - safe_path (list of tuples): List of crushed candies from the move.

        Returns:
            Tuple: (current_score, safe_path) as described above.

        """
 
        # These arrays are used to get row and column numbers of 4 neighbours of a given cell
        rowNbr = [-1, 0, 0, 1];
        colNbr = [0 ,-1, 1, 0];
         
        # Mark this cell as visited
        visited[i][j] = True

        current_score+=1

        #See what other nodes became points
        safe_path.append((i, j))
 
        # Recur for all connected neighbours
        for k in range(0, 4):
            if self.isSafe(i + rowNbr[k], j + colNbr[k], visited, l):
                current_score, safe_path = self.DFS(i + rowNbr[k], j + colNbr[k], visited, current_score, l, safe_path)

        return (current_score, safe_path)
 
 
    
    def countIslands(self):
        """The main function that returns the number of possible moves on a board"""

        # Initialize count as 0 and travese through the all cells of given matrix
        count = 0

        for l in range(0, 10):
            # Make - a bool array to mark visited cells. Initially all cells are unvisited
            visited = [[False for j in range(self.ncols)]for i in range(self.nrows)]

            for i in range(self.nrows):
                for j in range(self.ncols):
                    # If a cell with value 1 is not visited yet, then new island found
                    if self.graph[i][j] == str(l) and visited[i][j] == False:

                        current_score = 0
                        safe_path = []

                        # Visit all cells in this island and increment island count
                        current_score, safe_path = self.DFS(i, j, visited, current_score, str(l), safe_path)
                        count += 1

                        self.p_arr.append((str(l), current_score, (i,j), safe_path))

 
        return count

    def make_move(self, row, col):
        """Select a candy and crush similar adjacent candies to make a move.

        Args:
            - row (int): row of selected candy
            - col (int): Column of selected candy

        Returns:
            - current_score (int): Number of candies crushed
            - safe_path (list of tuples): The `current_score` candies crushed.

        """
        current_score = 0
        safe_path = []
        visited = [[False for j in range(self.ncols)]for i in range(self.nrows)]
        l = self.graph[row][col]

        # Visit all cells in this island and increment island count
        current_score, safe_path = self.DFS(row, col, visited, current_score, l, safe_path)

        return (current_score, safe_path)



def crush_candies(board, path):
    """Once a move is made, the crushed candies are replaced with `*`s. This function flushes the candies down and bubbles up the *s to the top of every column

    Args:
        - board (list of list of str): board for which the move is determined but hasnt been applied.
        - path (list of tuples): List of candies to be crushed

    Returns:
        Board with crushed candies and *s have bubbled up.

    """
    # Let '*' represent crushed candies 
    for i, j in path:
        board[i][j] = '*'

    #Transpose because python doesn't work like an array.
    #Transform list of rows to list of columns
    board_T = list(map(list, zip(*board)))

    #Move candies down every column
    for col in range(0, N):
        for row in range(0, N):
            if board_T[col][row] == '*':
                # Move star up
                board_T[col] = [board_T[col][row]] + [board_T[col][:row]] + [board_T[col][row+1:]]
                
                # Flatten to list from list of lists
                board_T[col] = [item for sublist in board_T[col] for item in sublist]
                        

    # Transpose back to get the original board
    board = list(map(list, zip(*board_T)))
    
    return board



def next_turn(iboard, player, alpha, beta, m=None, depth=None):
    """Performs the ab pruning

    This recursively called function is the core that contains the ab pruning logic.

    Args:
        - iboard (list of list of str): Input board for node.
        - player (str): MAX/MIN node
        - alpha (int): Best end score for MAX 
        - beta (int): Best end score for MIN
        - m (tuple, optional): Move made for current node
        - depth (int, optional): Current depth of node in ab tree

    Returns:
        Tuple to the parent consisting of:
            - :obj:v.move: the optimal move
            - :obj:v.value: optimal end score.

    Note:
        1. Current score of board is the square of number of candies crushed.
            Eg. If 5 candies are crushed by MAX, he gets 25 points.

        2. Value of node = (Sum of MAX children scores) - (Sum of MIN children scores)
            E.g. If We have a board with the following scores for subsequent moves:
                MAX : 25
                MIN : 36
                MAX : 16
                MIN : 4
                MAX : 25

            Then the value of the parent = 25 - 36 + 16 - 4 + 25 = 26.

    """
    global max_depth_touched 

    #Create current node
    node = Node(board=iboard, player=player, alpha=alpha, beta=beta)
    node.depth = depth

    g = Graph(N, p, iboard[:])
 
    moves = g.countIslands()

    #Check if any moves can be made
    if moves == 0:
        return (m ,0)

    # Sort paths in descending number of candies crushed. This will help early pruning
    new_sorted = sorted(g.p_arr, reverse=True, key=lambda x: x[1]) 

    #For every g, make the move
    for candy, score, move ,path in new_sorted:

        board = crush_candies(copy.deepcopy(g.graph), path)

        if (node.depth >= max_turns): #or moves == 0:            
            max_depth_touched = True

            if player=='min':
                return (move, -score*score)
            return (move, score*score)

        else:
            node.visited = True

            new_player = 'max'

            if player == 'max':
                new_player = 'min'

            v_move, v_value = next_turn(board, new_player, node.alpha, node.beta, move, node.depth+1)

            if player == 'max':
                if node.v.value < v_value+score*score:
                    node.v.value = v_value+score*score
                    node.v.move = move
        
                if node.v.value >= node.beta:
                    return (move, node.v.value)

                node.alpha = max(node.alpha, node.v.value)
        
            else:

                if node.v.value > v_value-score*score:            
                    node.v.value = v_value-score*score
                    node.v.move = move
        
                if node.v.value <= node.alpha:
                    return (move, node.v.value)

                node.beta = min(node.beta, node.v.value)
        
    return (node.v.move, node.v.value)


def handler(signum, frame):
    """SIGALRM handler

    Once the time alloted for the move has passed, the ab pruning stops and this function is called. It takes the best move computed thus far and writes it to an output file. 
    """

    #print("Optimal End score : ", max_score)

     # Columns are alphabets
    alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alpha_dict = {i: alphabets[i-1] for i in range(1, N+1)}

    g = Graph(N, p, input_board)
    score, path = g.make_move(best_move[0], best_move[1])
    board = crush_candies(input_board, path)

    #Write to output file
    with open('output.txt','w+') as out:
        #Take the first node of the path as the selected candy
        row = best_move[0]+1
        col = alpha_dict[best_move[1]+1]

        #Row is int, convert to str to write to file
        out.write(col+str(row)+"\n")
        for r in range(0, N):
            for c in range(0, N):
                out.write(str(board[r][c]))
            out.write("\n")
    exit()



if __name__ == '__main__':
    start_time = time.time()
    lines = tuple(open("input.txt", 'r'))
    lines = [l.strip() for l in lines]
    N = int(lines[0])
    p = int(lines[1])
    time_left = float(lines[2])

    input_board = []
    for i in range(0,N):
        row = list(lines[3+i]) #[int(l) for l in list(lines[3+i])]
        input_board.append(row)

    # Redundancy to know time
    g = Graph(N, p, input_board[:])
    moves = g.countIslands()

    time_per_move = int(time_left/moves)

    max_turns = 2
    best_move, max_score = next_turn(player='max', iboard=input_board, alpha=-1000000, beta=1000000, depth=1)

    signal.signal(signal.SIGALRM, handler)
    signal.alarm(time_per_move+1)

    global max_depth_touched

    while True:
        max_turns += 1
        max_depth_touched = False

        best_move, max_score = next_turn(player='max', iboard=input_board, alpha=-1000000, beta=1000000, depth=1)

        # If the maximum depth hasn't been explored, then we've completed DFS.
        if max_depth_touched == False:
            handler(0,0)

   