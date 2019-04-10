import random, datetime, copy

INFINITY = 1e10

class Team7:
    def __init__(self):
        self.termVal = INFINITY

        self.weight = [2,3,3,2,3,4,4,3,3,4,4,3,2,3,3,2]
        self.blocknormal = 120
        self.limit = 5
        self.dict = {'x':1,'o':-1,'-':0,'d':0}
        self.trans = {}
        self.normalize = 5
        self.timeLimit = datetime.timedelta(seconds = 15)
        self.begin = INFINITY
        self.limitReach = 0
        self.tle = 0

    
    def elemEval(self, board, blx, bly, tmpBlock, blkFlg):
        elemVal = 0                                         # storing the calculated value of that element
        
         # initial value of each of the patters possible

        # nulVal = 0
        stdVal = 3

        rowVals = []
        colVals = []
        diam = []

        for i in xrange(4):
            rowVals.append(stdVal)
            colVals.append(stdVal)
            diam.append(stdVal)
            
        
        diamNXPos   = [1,1,2,2]                                 # setting position of the 4 diamond patterns and the blocks in each
        diamNYPos   = [1,2,1,2]
        diamBXPos   = [0,-1,0,1]
        diamBYPos   = [-1,0,1,0]

        for i in xrange(4):                                     # checking with patterns in rows and columns
            for j in xrange(4):
                if(blkFlg):
                    elem = tmpBlock[i][j]
                else:
                    elem = board.board_status[4*blx+i][4*bly+j] # reading the mark which is at the position (i,j), and each block is checked
                dictVal = self.dict[elem]                       # the value of that mark is stored locally (-1 or +1 or 0)
                if(dictVal != 0):                               # if the block is a 'o' or 'x'
                    elemVal += dictVal * self.weight[4*i + j]   # add the weight of that position to the value after multiplying it with the respective value of that mark (-1 or 1)
                    if (rowVals[i] == 3):                       # if this is the first 'o' or 'x' in that row
                        rowVals[i] = dictVal*self.normalize                  # change the row pattern value
                    elif(dictVal * rowVals[i] < 0):             # if the mark is a 'o'
                        rowVals[i] = 0                          # set row value to zero
                    rowVals[i] *= 16                            # multiply the value for that row pattern

                    if (colVals[j] == 3):                       # if this is the first 'o' or 'x' in that column
                        colVals[j] = dictVal * self.normalize                # change the column value
                    elif(dictVal * colVals[j] < 0):             # if the mark is 'o'
                        colVals[j] = 0                          # set column to zero
                    colVals[j] *= 16
                    
                    # if (dictVal == -1):
                    #     enemRow[i]  += 1
                    #     enemCol[j]  += 1
                    # else:
                    #     unitRow[i] += 1
                    #     unitCol[j] += 1
                # checking for the diamond patterns now
                if(blkFlg):
                    elem = tmpBlock[ diamNXPos[j] + diamBXPos[i] ][ diamNYPos[j] + diamBYPos[i] ]
                else:
                    elem = board.board_status[4*blx + diamNXPos[j] + diamBXPos[i]][4*bly + diamNYPos[j] + diamBYPos[i]]
                dictVal = self.dict[elem]                       # get the value of the required element
                if(dictVal):
                    if(diam[j] == 3):                           # if its the first element in that pattern, set the value high
                        diam[j] = dictVal * self.normalize
                    elif(diam[j]*dictVal < 0):                  # if there's another element in that pattern, set it to zero (d or enemy mark)
                        diam[j] = 0
                    diam[j] *= 16                               # if the value if non zero, the value of that element gets higher
                    
                    # if(dictVal == -1):
                    #     enemDiam[j] += 1
                    # else:
                    #     unitDiam[j] += 1

        if(blkFlg == 0):
            checkDraw = 12
            for itr in xrange(4):                       # check for the draws in each pattern
                if(colVals[itr] == 0):
                    checkDraw -= 1
                if(rowVals[itr] == 0):
                    checkDraw -= 1
                if(diam[itr] == 0):
                    checkDraw -= 1

            if(checkDraw == 0):
                tmpBlock[blx][bly] = 'd'                # if draw, set tmpBlock, thats a deepcopy of the boardstatus from the heuristic function, to 'd'
                return 0


        for itr in xrange(4):
            if(rowVals[itr] != 3):
                elemVal += rowVals[itr]
            if(colVals[itr] != 3):
                elemVal += colVals[itr]
            if(diam[itr] != 3):
                elemVal += diam[itr]

        return elemVal

    def heuristic(self, board):
        val = 0
        tempBlock = copy.deepcopy(board.block_status)
        
        for i in xrange(4):
            for j in xrange(4):
                val += self.elemEval(board,i,j,tempBlock,0)
        
        val += self.elemEval(board,0,0,tempBlock,1)*self.blocknormal
        del(tempBlock)
        
        return val

    def alphaBeta(self, board, old_move, flag, depth, alpha, beta):
        hashval = hash(str(board.board_status)) # check exists in transition table
        if(self.trans.has_key(hashval)):
            bounds = self.trans[hashval]
            if(beta <= bounds[0]):
                return bounds[0],old_move
            if(alpha >= bounds[1]):
                return bounds[1],old_move
            alpha = max(alpha,bounds[0])
            beta = min(beta,bounds[1])

        cells = board.find_valid_move_cells(old_move)
        random.shuffle(cells)

        p = self.dict[flag]
        if (p):
            nodeVal = -1*p*INFINITY,cells[0]
            new = ''
            a,b = 0,0
            emp = 'NONE'
            tmp = copy.deepcopy(board.block_status)

            if (p == 1):
                new = 'o'
                a = alpha
                
            elif (p == -1):
                new = 'x'
                b = beta

            for chosen in cells :
                if datetime.datetime.utcnow() - self.begin >= self.timeLimit :
                    self.limitReach = 1
                    break
                board.update(old_move, chosen, flag)
                if (board.find_terminal_state()[0] == flag):
                    board.board_status[chosen[0]][chosen[1]] = '-'
                    board.block_status = copy.deepcopy(tmp)
                    nodeVal = p*self.termVal,chosen
                    break
                elif (board.find_terminal_state()[0] == new):
                    board.board_status[chosen[0]][chosen[1]] = '-'
                    board.block_status = copy.deepcopy(tmp)
                    continue
                elif(board.find_terminal_state()[0] == emp):
                    x,o,d = 0,0,0
                    tmp1 = 0

                    for col in board.block_status:
                        for el in col:
                            if (el == 'x'):
                                x += 1
                            
                            if (el == 'o'):
                                o += 1
                            
                            if (el == 'd'):
                                d += 1

                    if(x==o):
                        tmp1 = 0
                    elif(x>o):
                        tmp1 = INFINITY/2 + 10*(x-o)
                    else:
                        tmp1 = -INFINITY/2 - 10*(o-x)
 
                elif( depth >= self.limit):
                    tmp1 = self.heuristic(board)

                else:
                    if (p==1):
                        tmp1 = self.alphaBeta(board, chosen, new, depth+1, a, beta)[0]

                    elif (p==-1):
                        tmp1 = self.alphaBeta(board, chosen, new, depth+1, alpha, b)[0]

                board.board_status[chosen[0]][chosen[1]] = '-'
                board.block_status = copy.deepcopy(tmp)
                
                if (p == 1):
                    if(nodeVal[0] < tmp1):
                        nodeVal = tmp1,chosen

                    a = max(a, tmp1)
                    if beta <= nodeVal[0] :
                        break

                if (p == -1):
                    if(tmp1 < nodeVal[0]):
                        nodeVal = tmp1,chosen
                    
                    b = min(b, tmp1)
                    if nodeVal[0] <= alpha:
                        break

            del(tmp)

        if(alpha >= nodeVal[0]):
            self.trans[hashval] = [-INFINITY,nodeVal[0]]
        
        if(alpha < nodeVal[0] and beta > nodeVal[0]):
            self.trans[hashval] = [nodeVal[0],nodeVal[0]]
        
        if(beta <= nodeVal[0]):
            self.trans[hashval] = [nodeVal[0],INFINITY]

        return nodeVal

    def transReset(self):
        resetVal = 1
        self.trans.clear()

    def move(self, board, old_move, flag):
        self.begin = datetime.datetime.utcnow()
        self.limitReach = 0
        self.transReset()

        toret = board.find_valid_move_cells(old_move)[0]

        for i in xrange(3,100):
            self.transReset()
            self.limit = i
            root = 1
            prune = self.alphaBeta(board, old_move, flag, root, -INFINITY, INFINITY)
            getval = prune[1]
            if(self.limitReach == root - 1):
                toret = getval
            else:
                break
        # print (i)
        # print("toret",toret)
        return toret[0], toret[1]
