#!/usr/bin/env python
# coding: utf-8

import sys

def constructRangeTree(data):
    '''
    Constructs the range tree.
    Allocates space and then constructs by calling function constructRangeTree1D()
    Assumption: sxdata is sorted 
    '''
    global rangeTree,sxdata

    sxdata = data
    # Allocate space for range tree
    c=len(sxdata).bit_length()
    if c <=3:                 # no need of a range tree if data length is < 8.
        return None
    if 2**(c-1)==len(sxdata): # else allocate space
        rangeTree = [None for _ in range(2*len(sxdata))]
    else:
        rangeTree = [None for _ in range(2**(c+1))]
        
    # Construct range tree
    constructRangeTree2D(0,len(sxdata)-1,1)
    return rangeTree

def constructRangeTree2D(low_id,high_id,cur_id):
    '''
    Constructs the range tree recursively
    '''
    global sxdata, rangeTree
    
    if low_id == high_id:
        rangeTree[cur_id] = [sxdata[low_id],[sxdata[low_id]]]   # single node with no child
        return
    mid_id = (low_id + high_id)//2
    node_data = constructRangeTreeSecondary(sxdata[low_id:high_id+1],1) # construct 1D range tree with y coordinates
    rangeTree[cur_id] = [sxdata[mid_id],node_data]
    constructRangeTree2D(low_id,mid_id,2*cur_id)
    constructRangeTree2D(mid_id+1,high_id,2*cur_id+1)
    return   


def constructRangeTree1D(data,low_id,high_id,cur_id):
    '''
    Constructs the range tree recursively
    '''
    global tree
    
    if low_id == high_id:
        tree[cur_id] = [data[low_id],[data[low_id]]]   # single node with no child
        return
    mid_id = (low_id + high_id)//2
    tree[cur_id] = [data[mid_id],data[low_id:high_id+1]]
    constructRangeTree1D(data,low_id,mid_id,2*cur_id)
    constructRangeTree1D(data,mid_id+1,high_id,2*cur_id+1)
    return    

def constructRangeTreeSecondary(data,index):
    '''
    Constructs the range tree for data, with key as index
    '''
    global tree

    if len(data) == 0:
        return []
    if len(data[0]) <= index:
        sys.exit('Inconsistent values passed to constructRangeTreeSecondary.')
    data.sort(key=lambda x: x[index])

    # Allocate space for range tree
    c=len(data).bit_length()
    if 2**(c-1)==len(data): 
        tree = [None for _ in range(2*len(data))]
    else:
        tree = [None for _ in range(2**(c+1))]

    # Construct range tree
    constructRangeTree1D(data,0,len(data)-1,1)
    return tree    


def findSplitNode2D(xmin,xmax):
    '''
    Returns the index of the split node for a range search in the tree.
    '''    
    global rangeTree
    
    node_id = 1                              # If tree, search for split node.
    while ((node_id < len(rangeTree)) and (rangeTree[node_id] is not None)):
        if xmin <= rangeTree[node_id][0][0] <= xmax: # found split node
            break
        else:                                # travel down the tree
            splitNode_id_cur = node_id
            node_id *= 2
            if rangeTree[splitNode_id_cur][0][0] < xmin:
                node_id += 1                 # travel right sub tree
    else:
        return None
    return node_id


def findSplitNode(ymin,ymax,tree):
    '''
    Returns the index of the split node for a range search in the tree.
    '''    
    node_id = 1                              # If tree, search for split node.
    while ((node_id < len(tree)) and (tree[node_id] is not None)):
        if ymin <= tree[node_id][0][1] <= ymax: # found split node
            break
        else:                                # travel down the tree
            node_id_cur = node_id
            node_id *= 2
            if tree[node_id_cur][0][1] < ymin:
                node_id += 1                 # travel right sub tree
    else:
        return None
    return node_id

def childExists2D(cur_id,left=True):
    '''
    Checks if a right or left child exists for the current node.
    Inputs: cur_id : the index of the current node in range tree
            left   : True if left child to be checked. 
                     False if right child to be checked
    Output: True if child exists. 
            False otherwise. 
    '''
    global rangeTree
    
    if left == True:                      # Return true if left child exists
        left_cur_id = cur_id*2
        if left_cur_id >= len(rangeTree):
            return False
        elif rangeTree[left_cur_id] is None:
            return False
        else:
            return True
    else:                                 # Return true if right child exists
        right_cur_id = cur_id*2 + 1
        if right_cur_id >= len(rangeTree):
            return False
        elif rangeTree[right_cur_id] is None:
            return False
        else:
            return True        

def childExists(cur_id,tree, left=True):
    '''
    Checks if a right or left child exists for the current node.
    Inputs: cur_id : the index of the current node in range tree
            left   : True if left child to be checked. 
                     False if right child to be checked
    Output: True if child exists. 
            False otherwise. 
    '''
    if tree is None:
        return False
   
    if left == True:                      # Return true if left child exists
        left_cur_id = cur_id*2
        if left_cur_id >= len(tree):
            return False
        elif tree[left_cur_id] is None:
            return False
        else:
            return True
    else:                                 # Return true if right child exists
        right_cur_id = cur_id*2 + 1
        if right_cur_id >= len(tree):
            return False
        elif tree[right_cur_id] is None:
            return False
        else:
            return True        


def addResult(result,cur_id, tree,left=True):
    '''
    Reports elements from child subtrees. Concatenates to the existing result set.
    Inputs : result: existing result set with which current result set will be concatenated
             cur_id: index of the current node
             left  : True if left subtree is to be concatenated to result
                     False if right subtree to be concatenated 
    Outputs: result: elements from the subtree concatenated with the prior result
    '''   
    if left == True:          # Add left child elements if not none
        if childExists(cur_id,tree):
            return result + tree[cur_id*2][1]
        else:
            return result + [tree[cur_id][0]]
    else:                     # Add right child elements if not none
        if childExists(cur_id,tree,False):
            return tree[cur_id*2 + 1][1] + result
        else:
            return result


def fetchRightSubtrees(ymin,cur_id,tree):
    '''
    Search for xmin (minimum value of search query range) and travel left subtree of the split node and 
    report all right subtrees along the way. (All these elements are >= xmin).
    '''
    result=[]
    while tree[cur_id] is not None:
        if tree[cur_id][0][1] > ymin:   # report elements of right children while travelling left
            result = addResult(result,cur_id,tree,False)
            if childExists(cur_id,tree)==True:
                cur_id *= 2
            else:
                result = [tree[cur_id][0]] + result
                break
        elif tree[cur_id][0][1] == ymin:  # report xmin as it is in range
            result = [tree[cur_id][0]] + addResult(result,cur_id,tree,False)
            break
        else:                               # xmin is in the right tree of current node
            if childExists(cur_id,tree,False)==True:
                cur_id *= 2
                cur_id += 1
            else:
                break
    return result


def fetchLeftSubtrees(ymax,cur_id,tree):
    '''
    Search for xmax (maximum element of the search query range) in the right subtree of the split node
    and report all elements in the left subtrees along the way. These elements are <= xmax.
    '''            
    result = []
    while tree[cur_id] is not None:
        if tree[cur_id][0][1] <= ymax:     # report elements of left children while travelling right
            result = addResult(result,cur_id,tree)
            if childExists(cur_id, tree, False)==True:
                cur_id *= 2
                cur_id += 1
            else:
                break
        else:                               # xmax is in the left tree of current node
            if childExists(cur_id,tree)==True:
                cur_id *= 2
            else:
                break
    return result

def searchRangeTree1D(y1,y2,tree):
    '''
    Search and report all elements from a range tree within a given range.
    '''    
    ymax = max(y1,y2)
    ymin = min(y1,y2)
    if len(tree) == 0:   # Empty tree
        return []
    elif len(tree) == 1: # Single node. Not a tree.  
        if ymin <= tree[0][1] <= ymax:
            return [tree[0]]

    ysplitNode_id = findSplitNode(ymin,ymax,tree)
    if ysplitNode_id is None:  # split node not found
        print('No data for the given range')
        return []
    result = []

    # Report right trees while searching for xmin
    if childExists(ysplitNode_id,tree,True)==False:  # if left child of split node does not exist, then report the split node
        result += [tree[ysplitNode_id][0]]
    else:
        result += fetchRightSubtrees(ymin,ysplitNode_id*2,tree)
 
    # Report left trees while searching for xmax
    if childExists(ysplitNode_id,tree,False)==False: # if right child of split node does not exist, then skip
        return result
    else:
        result += fetchLeftSubtrees(ymax,ysplitNode_id*2 + 1,tree)
    return result


def addResult2D(result,cur_id,y1,y2,left=True):
    '''
    Reports elements from child subtrees. Concatenates to the existing result set.
    Inputs : result: existing result set with which current result set will be concatenated
             cur_id: index of the current node
             left  : True if left subtree is to be concatenated to result
                     False if right subtree to be concatenated 
    Outputs: result: elements from the subtree concatenated with the prior result
    '''    
    global rangeTree
    if left == True:          # Add left child elements if not none
        if childExists2D(cur_id):
            return result + searchRangeTree1D(y1,y2,rangeTree[cur_id*2][1])
        else:
            if (y1 <= rangeTree[cur_id][0][1] <= y2) or (y2 <= rangeTree[cur_id][0][1] <= y1):
                result += [rangeTree[cur_id][0]]
            return result
    else:                     # Add right child elements if not none
        if childExists2D(cur_id,False):
            searchRangeTree1D(y1,y2,rangeTree[cur_id*2 + 1][1])
            return searchRangeTree1D(y1,y2,rangeTree[cur_id*2 + 1][1]) + result
 
        else:
            return result


def fetchRightSubtrees2D(xmin,y1,y2,cur_id):
    '''
    Search for xmin (minimum value of search query range) and travel left subtree of the split node and 
    report all right subtrees along the way. (All these elements are >= xmin).
    '''
    global rangeTree

    result=[]
    while rangeTree[cur_id] is not None:
        if rangeTree[cur_id][0][0] > xmin:   # report elements of right children while travelling left
            result = addResult2D(result,cur_id,y1,y2,False)

            if childExists2D(cur_id)==True:
                cur_id *= 2
            else:
                if (y1 <= rangeTree[cur_id][0][1] <= y2) or (y2 <= rangeTree[cur_id][0][1] <= y1):
                    result = [rangeTree[cur_id][0]] + result
                break
        elif rangeTree[cur_id][0][0] == xmin:  # report xmin as it is in range
            if (y1 <= rangeTree[cur_id][0][1] <= y2) or (y2 <= rangeTree[cur_id][0][1] <= y1):
                result = [rangeTree[cur_id][0]] + addResult2D(result,cur_id,y1,y2,False)
            else:
                result = addResult2D(result,cur_id,y1,y2,False)
            break
        else:                               # xmin is in the right tree of current node
            if childExists2D(cur_id, False)==True:
                cur_id *= 2
                cur_id += 1
            else:
                break
    return result


def fetchLeftSubtrees2D(xmax,y1,y2,cur_id):
    '''
    Search for xmax (maximum element of the search query range) in the right subtree of the split node
    and report all elements in the left subtrees along the way. These elements are <= xmax.
    '''            
    global rangeTree

    result=[]
    while rangeTree[cur_id] is not None:
        if rangeTree[cur_id][0][0] <= xmax:     # report elements of left children while travelling right
            result = addResult2D(result,cur_id,y1,y2)
            if childExists2D(cur_id, False)==True:                
                cur_id *= 2
                cur_id += 1
            else:
                break
        else:                               # xmax is in the left tree of current node
            if childExists2D(cur_id)==True:
                cur_id *= 2
            else:
                break
    return result


def searchRangeTree2D(xy1,xy2,tree):
    '''
    Search and report all elements from a range tree within a given range of x and y coordinates.
    '''    
    global rangeTree

    rangeTree = tree
    
    x1,y1 = xy1
    x2,y2 = xy2
    xmax = max(x1,x2)
    xmin = min(x1,x2)

    splitNode_id = findSplitNode2D(xmin,xmax)
    if splitNode_id is None:  # split node not found
        print('No data for the given range')
        return None
 
    result = []

    # Report right trees while searching for xmin
    if childExists2D(splitNode_id)==False:  # if left child of split node does not exist, then report the split node
        result += searchRangeTree1D(y1,y2,rangeTree[splitNode_id][1])
    else:
        result += fetchRightSubtrees2D(xmin,y1,y2,splitNode_id*2)
   
    # Report left trees while searching for xmax
    if childExists2D(splitNode_id,False)==False: # if right child of split node does not exist, then skip
        return result
    else:
        result += fetchLeftSubtrees2D(xmax,y1,y2,splitNode_id*2 + 1)
    return result


if __name__=='__main__':
    '''
    This is the main program. It first created a range tree from a sorted data, and then queries on a range.
    '''
    sxdata=[[6,2,3],[15,3,4],[17,5,6],[21,7,8],[24,9,13],[33,12,13],[42,14,15],[51,16,17],[52,18,19],[57,20,23],[65,21,32],[73,22,30],[78,2,3]]
    tree=[]
    rangeTree = constructRangeTree(sxdata)
#    print('rangeTree[5] node ',rangeTree[5][0],' tree=',rangeTree[5][1])
    if rangeTree is None:
        # Do binary search on x and serial search on y
        print("Better do serial search, too small list.")
        pass
    else:
        # Use rangeTree for x and y search
        xy1=(51,1)
        xy2=(74,22)
        fiteredData = searchRangeTree2D(xy1,xy2,rangeTree)
        if fiteredData == []:
            print('No data for range ',xy1,', ',xy2)
        else:
            print('Data in range ',xy1,', ',xy2, ' are : ',fiteredData)