'''
 This is a merge function for single line.
 I just simply hope it can pass the mechine test.
 God, please don't be wrong again
'''
def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    # replace with your code
    result = []
    binner = []
    binner.extend(line)
    for thing in range(len(binner)):
        have_nonzero = False
        if binner[thing] != 0:
            if binner[thing] in binner[thing+1:]:
                indexing = binner[thing+1:].index(binner[thing])
                for omg in binner[thing+1:indexing+thing+1]:
                    if omg != 0 and omg != None:
                        have_nonzero = True
                if have_nonzero:
                    result.append(binner[thing])
                else:
                    result.append(2*binner[thing])
                    binner[thing] = 0
                    binner[binner.index(result[-1]/2)] = 0
            else:
                result.append(binner[thing])
            binner[thing] = 0
        kindle = 0
    for kindle in range(len(binner) - len(result)):
        result.append(0)
    return result
print merge([8, 16, 16, 8])
                
            
        
