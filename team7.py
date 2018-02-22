from __future__ import print_function
import copy
import random
import datetime

INFINITY = 1e10

class Team7:
    def __init__(self):
        self.termVal = INFINITY
        self.limit = 5
        self.count = 0
        self.weight = [2,4,4,2,4,3,3,4,4,3,3,4,2,4,4,2]
        self.dict = {'x':1,'o':-1,'-':0,'d':0}
        self.trans = {}
        self.timeLimit = datetime.timedelta(seconds = 14)
        self.begin = INFINITY
        self.limitReach = 0

    def evaluate(self,board,blx,bly,tmpBlock):
        # print("Calculating for block ",blx, " " , bly)
        # mark = board.block_status[blx][bly]
        # if(mark=='x' or mark=='o' or mark=='d'):
        #     return 0

        val = 0
        rowCnt = [3,3,3,3]
        colCnt = [3,3,3,3]
        for i in xrange(4):
            for j in xrange(4):
                mark = board.board_status[4*blx+i][4*bly+j]
                # print("hi")
                dictVal = self.dict[mark]
                if(dictVal!=0):
                    val+=dictVal*self.weight[4*i+j]
                    if (rowCnt[i]==3):
                        rowCnt[i] = dictVal*5
                    elif(dictVal*rowCnt[i]<0):
                        rowCnt[i] = 0
                    rowCnt[i]=rowCnt[i]*16
                    if (colCnt[j]==3):
                        colCnt[j] = dictVal*5
                    elif(dictVal*colCnt[j]<0):
                        colCnt[j] = 0
                    colCnt[j]=colCnt[j]*16
        # print(rowCnt,colCnt)

        xx = [0,-1,0,1]
        yy = [-1,0,1,0]
        diam1,diam2,diam3,diam4 = 3,3,3,3
        for i in xrange(4):
            mark = board.board_status[4*blx + 1 + xx[i]][4*bly + 1 + yy[i]]
            dictVal = self.dict[mark]
            if(dictVal):
                if(diam1 == 3):
                    diam1 = dictVal*5
                elif(dictVal*diam1 < 0):
                    diam1 = 0
                diam1 *= 16
            mark = board.board_status[4*blx + 1 + xx[i]][4*bly + 2 + yy[i]]
            dictVal = self.dict[mark]
            if(dictVal):
                if(diam2 == 3):
                    diam2 = dictVal*5
                elif(dictVal*diam2<0):
                    diam2 = 0
                diam2 *= 16
            mark = board.board_status[4*blx + 2 + xx[i]][4*bly + 1 + yy[i]]
            dictVal = self.dict[mark]
            if(dictVal!=0):
                if(diam3==3):
                    diam3 = dictVal * 5
                elif(dictVal*diam3 < 0):
                    diam3 = 0
                diam3 *= 16
            mark = board.board_status[4*blx + 2 + xx[i]][4*bly + 2 + yy[i]]
            dictVal = self.dict[mark]
            if(dictVal!=0):
                if(diam4 == 3):
                    diam4 = dictVal * 5
                elif(dictVal*diam4 < 0):
                    diam4 = 0
                diam4 *= 16

        #commented out coz u know
        # diag1,diag2 = 3,3
        # for i in xrange(4):
        #         mark = board.board_status[4*blx+i][4*bly+i]
        #         dictVal = self.dict[mark]
        #         if(dictVal!=0):
        #             if(diag1==3):
        #                 diag1 = dictVal*5
        #             elif(dictVal*diag1<0):
        #                 diag1 = 0
        #             diag1=diag1*16
        #         mark = board.board_status[4*blx+i][4*bly+3-i]
        #         dictVal = self.dict[mark]
        #         if(dictVal!=0):
        #             if(diag2==3):
        #                 diag2 = dictVal*5
        #             elif(dictVal*diag2<0):
        #                 diag2 = 0
        #             diag2=diag2*16

        #commented out coz u know
        # draw = 10
        # for i in xrange(4):
        #     if(rowCnt[i]==0):
        #         draw-=1
        #     if(colCnt[i]==0):
        #         draw-=1
        # if(diag1==0):
        #     draw-=1
        # if(diag2==0):
        #     draw-=1
        # if(draw==0):
        #     # print("because of draw for block ",blx,bly)
        #     # board.print_board()
        #     tmpBlock[blx][bly] = 'd'
        #     return 0

        #commented out coz u know
        # for i in xrange(4):
        #     if(rowCnt[i]!=3):
        #         val+=rowCnt[i]
        #     if(colCnt[i]!=3):
        #         val+=colCnt[i]

        #commented out coz u know
        # if(diag1!=3):
        #     val+=diag1
        # if(diag2!=3):
        #     val+=diag2

        draw = 12
        for i in xrange(4):
            if(rowCnt[i]==0):
                draw-=1
            if(colCnt[i]==0):
                draw-=1
        if(diam1==0):
            draw-=1
        if(diam2==0):
            draw-=1
        if(diam3==0):
            draw-=1
        if(diam4==0):
            draw-=1

        if(draw==0):
            # print("because of draw for block ",blx,bly)
            # board.print_board()
            tmpBlock[blx][bly] = 'd'
            return 0

        for i in xrange(4):
            if(rowCnt[i]!=3):
                val+=rowCnt[i]
            if(colCnt[i]!=3):
                val+=colCnt[i]

        if(diam1!=3):
            val+=diam1
        if(diam2!=3):
            val+=diam2
        if(diam3!=3):
            val+=diam3
        if(diam4!=3):
            val+=diam4

        return val

    def blockEval(self,board,tmpBlock):
        val = 0
        rowCnt = [3,3,3,3]
        colCnt = [3,3,3,3]
        for i in xrange(4):
            for j in xrange(4):
                mark = tmpBlock[i][j]
                dictVal = self.dict[mark]
                if(mark!='-'):
                    # print("Heuristic involves block ",i,j)
                    val+=dictVal*self.weight[4*i+j]
                    if (rowCnt[i]==3):
                        rowCnt[i] = dictVal*5
                    elif(dictVal*rowCnt[i]<=0):
                        rowCnt[i] = 0
                    rowCnt[i]=rowCnt[i]*16
                    if (colCnt[j]==3):
                        colCnt[j] = dictVal*5
                    elif(dictVal*colCnt[j]<=0):
                        colCnt[j] = 0
                    colCnt[j]=colCnt[j]*16

        diam = [3,3,3,3]
        x1   = [1,1,2,2]
        y1   = [1,2,1,2]
        xx = [0,-1,0,1]
        yy = [-1,0,1,0]

        for i in xrange(4):
            for j in xrange(4):
                mark = tmpBlock[ x1[j]+xx[i] ][ y1[j]+yy[i] ]
                if(mark!='-'):
                    dictVal = self.dict[mark]
                    if(diam[j] == 3):
                        diam[j] = dictVal*5
                    elif(diam[j]*dictVal <= 0):
                        diam[j] = 0
                    diam[j] *= 16 * dictVal * dictVal

        #commented coz u know
        # diag1,diag2 = 3,3
        # for i in xrange(4):
        #         mark = tmpBlock[i][i]
        #         if(mark!='-'):
        #             dictVal = self.dict[mark]
        #             if(diag1==3):
        #                 diag1 = dictVal*5
        #             elif(dictVal*diag1<=0):
        #                 diag1 = 0
        #             diag1=diag1*16*dictVal*dictVal
        #         mark = tmpBlock[i][3-i]
        #         if(mark!='-'):
        #             dictVal = self.dict[mark]
        #             if(diag2==3):
        #                 diag2 = dictVal*5
        #             elif(dictVal*diag2<=0):
        #                 diag2 = 0
        #             diag2=diag2*16*dictVal*dictVal

        for i in xrange(4):
            if(rowCnt[i]!=3):
                val += rowCnt[i]
            if(colCnt[i]!=3):
                val += colCnt[i]
            if(diam[i] != 3):
                val += diam[i]
        # draw = 10
        # for i in xrange(4):
        #     if(rowCnt[i]==0):
        #         draw-=1
        #     if(colCnt[i]==0):
        #         draw-=1
        # if(diag1==0):
        #     draw-=1
        # if(diag2==0):
        #     draw-=1
        #
        # if(draw==0):
        #     print("because of draw for game ")
        #     board.print_board()
        #     if()
            # return 0

        #commented out coz u know
        # if(diag1!=3):
        #     val+=diag1
        # if(diag2!=3):
        #     val+=diag2

        # print("val is ",val)
        return val

    def heuristic(self, board):
        tmpBlock = copy.deepcopy(board.block_status)
        final = 0
        # print("Calculating heur")
        for i in xrange(4):
            for j in xrange(4):
                aaja = self.evaluate(board,i,j,tmpBlock)
                # print(aaja,i,j)
                final += aaja
        final += self.blockEval(board,tmpBlock)*120
        del(tmpBlock)
        # return (50, old_move)
        # print("final is ",final)
        return final

    def alphaBeta(self, board, old_move, flag, depth, alpha, beta):
        # Assuming 'x' to be the maximising player

        # print("old move is ",old_move)

        hashval = hash(str(board.board_status))
        if(self.trans.has_key(hashval)):
            # print("hash exists")
            bounds = self.trans[hashval]
            if(bounds[0] >= beta):
                return bounds[0],old_move
            if(bounds[1] <= alpha):
                return bounds[1],old_move
            # print("also returning")
            alpha = max(alpha,bounds[0])
            beta = min(beta,bounds[1])

        # print(len(cells), ": length of cells")
        # print("old move is ",old_move,hashval)
        # nodeVal = 0,cells[0]
        # beta = b
        # alpha = a
        #
        # if(board.find_terminal_state()[0] == 'x'):
        #     nodeVal = self.termVal, old_move
        #
        # elif(board.find_terminal_state()[0] == 'o'):
        #     nodeVal = -1*self.termVal, old_move
        #
        # elif(self.trans.has_key(hashval)):
        #     bounds = self.trans[hashval]
        #     if(bounds[0] >= b):
        #         return bounds[0]
        #     if(bounds[1] <= a):
        #         return bounds[1]
        #     a = max(a,bounds[0])
        #     b = min(b,bounds[1])

        # if(board.find_terminal_state()[0] == 'NONE' or depth > self.limit):
        #     print("while returning heur")
        #     # board.print_board()
        #     heurVal = self.heuristic(board)
        #     print("final returned as ",heurVal)
        #     nodeVal = heurVal,old_move
        #     print("hello")

        # random.shuffle(cells)
        # print(cells)

        cells = board.find_valid_move_cells(old_move)
        random.shuffle(cells)
        # print(len(cells), ": length of cells")
        if (flag == 'x'):
            nodeVal = -INFINITY, cells[0]
            new = 'o'
            tmp = copy.deepcopy(board.block_status)
            a = alpha

            for chosen in cells :
                if datetime.datetime.utcnow() - self.begin >= self.timeLimit :
                    # print("breaking at depth ",depth)
                    self.limitReach = 1
                    break
                board.update(old_move, chosen, flag)
                # print("chosen ",chosen)
                if (board.find_terminal_state()[0] == 'x'):
                    board.board_status[chosen[0]][chosen[1]] = '-'
                    board.block_status = copy.deepcopy(tmp)
                    nodeVal = self.termVal,chosen
                    break
                elif (board.find_terminal_state()[0] == 'o'):
                    board.board_status[chosen[0]][chosen[1]] = '-'
                    board.block_status = copy.deepcopy(tmp)
                    continue
                elif(board.find_terminal_state()[0] == 'NONE'):
                    x = 0
                    d = 0
                    o = 0
                    tmp1 = 0
                    for i2 in xrange(4):
                        for j2 in xrange(4):
                            if(board.block_status[i2][j2] == 'x'):
                                x += 1
                            if(board.block_status[i2][j2] == 'o'):
                                o += 1
                            if(board.block_status[i2][j2] == 'd'):
                                d += 1
                    if(x==o):
                        tmp1 = 0
                    elif(x>o):
                        tmp1 = INFINITY/2 + 10*(x-o)
                    else:
                        tmp1 = -INFINITY/2 - 10*(o-x)
                    # print(tmp1)
                elif( depth >= self.limit):
                    tmp1 = self.heuristic(board)
                    # print("Heuristic value for ",chosen," is ",tmp1)
                else:
                    tmp1 = self.alphaBeta(board, chosen, new, depth+1, a, beta)[0]

                board.board_status[chosen[0]][chosen[1]] = '-'
                board.block_status = copy.deepcopy(tmp)
                if(nodeVal[0] < tmp1):
                    nodeVal = tmp1,chosen
                # print("hi nodeval ",nodeVal)
                a = max(a, tmp1)
                if beta <= nodeVal[0] :
                    break
            del(tmp)

        if (flag == 'o'):
            nodeVal = INFINITY, cells[0]
            new = 'x'
            tmp = copy.deepcopy(board.block_status)
            b = beta

            for chosen in cells :
                if datetime.datetime.utcnow() - self.begin >= self.timeLimit :
                    self.limitReach = 1
                    break
                board.update(old_move, chosen, flag)
                # print("chosen ",chosen)
                if(board.find_terminal_state()[0] == 'o'):
                    board.board_status[chosen[0]][chosen[1]] = '-'
                    board.block_status = copy.deepcopy(tmp)
                    nodeVal = -1*self.termVal,chosen
                    break
                elif(board.find_terminal_state()[0] == 'x'):
                    board.board_status[chosen[0]][chosen[1]] = '-'
                    board.block_status = copy.deepcopy(tmp)
                    continue
                elif(board.find_terminal_state()[0] == 'NONE'):
                    x = 0
                    d = 0
                    o = 0
                    tmp1 = 0
                    for i2 in range(4):
                        for j2 in range(4):
                            if board.block_status[i2][j2] == 'x':
                                x += 1
                            if board.block_status[i2][j2] == 'o':
                                o += 1
                            if board.block_status[i2][j2] == 'd':
                                d += 1
                    if(x==o):
                        tmp1 = 0
                    elif(x>o):
                        tmp1 = INFINITY/2 + 10*(x-o)
                    else:
                        tmp1 = -INFINITY/2 - 10*(o-x)
                    # print(tmp1)
                elif(depth >= self.limit):
                    tmp1 = self.heuristic(board)
                    # print("Heuristic value for ",chosen," is ",tmp1)
                else:
                    tmp1 = self.alphaBeta(board, chosen, new, depth+1, alpha, b)[0]
                board.board_status[chosen[0]][chosen[1]] = '-'
                board.block_status = copy.deepcopy(tmp)
                if(nodeVal[0] > tmp1):
                    nodeVal = tmp1,chosen
                b = min(b, tmp1)
                if alpha >= nodeVal[0] :
                    break
            del(tmp)

        # print("return value is ",nodeVal)
        if(nodeVal[0] <= alpha):
            self.trans[hashval] = [-INFINITY,nodeVal[0]]
        if(nodeVal[0] > alpha and nodeVal[0] < beta):
            self.trans[hashval] = [nodeVal[0],nodeVal[0]]
        if(nodeVal[0]>=beta):
            self.trans[hashval] = [nodeVal[0],INFINITY]
        # print(self.trans.items())
        return nodeVal

    def mtd(self,board,old_move,flag,depth,f):
        g = f
        upperbound = INFINITY
        lowerbound = -INFINITY
        while(lowerbound<upperbound):
            # print("new mtd ",lowerbound,upperbound)
            b = max(g,lowerbound+1)
            tmp = self.alphaBeta(board,old_move,flag,depth,b-1,b)
            if datetime.datetime.utcnow() - self.begin >= self.timeLimit :
                self.limitReach = 1
                break
            g = tmp[0]
            if(g<b):
                upperbound = g
            else:
                lowerbound = g
        return tmp

    def move(self, board, old_move, flag):
        self.begin = datetime.datetime.utcnow()
        self.count += 1
        self.limitReach = 0
        self.trans.clear()
        # print(self.trans.items())
        # print("entering the move for ", self.count)
        toret = board.find_valid_move_cells(old_move)[0]
        for i in xrange(3,100):
            self.trans.clear()
            self.limit = i
            # print("in depth ",i)
            blah = self.alphaBeta(board, old_move, flag, 1, -INFINITY, INFINITY)
            getval = blah[1]
            # print("returned from depth ",i)
            # print("Returning finally ",blah[0])
            if(self.limitReach == 0):
                toret = getval
            else:
                break
        # toret = self.alphaBeta(board, old_move, flag, 1, -10000000, 10000000)[1]
        # print("toret",toret)
        return toret[0], toret[1]
