import numpy as np
from collections import Counter
import os

def levenstein_alignment(ref, hyp):
    # create a matrix of size (len(ref)+1) x (len(hyp)+1)
    # the first row and the first column are filled with 0, 1, 2, 3, ...
    # the rest of the matrix is filled with -1
    matrix = np.zeros((len(ref)+1, len(hyp)+1))
    for i in range(1, len(ref)+1):
        matrix[i, 0] = i
    for j in range(1, len(hyp)+1):
        matrix[0, j] = j
    for i in range(1, len(ref)+1):
        for j in range(1, len(hyp)+1):
            matrix[i, j] = -1

    # fill the matrix with the correct values
    for i in range(1, len(ref)+1):
        for j in range(1, len(hyp)+1):
            if ref[i-1] == hyp[j-1]:
                matrix[i, j] = matrix[i-1, j-1]
            else:
                matrix[i, j] = min(matrix[i-1, j-1], matrix[i-1, j], matrix[i, j-1]) + 1

    # create two lists of words with a <epsilon> token for insertion and deletion
    ref_aligned = []
    hyp_aligned = []
    i = len(ref)
    j = len(hyp)
    while i > 0 or j > 0:
        if i > 0 and j > 0 and ref[i-1] == hyp[j-1]:
            ref_aligned.append(ref[i-1])
            hyp_aligned.append(hyp[j-1])
            i -= 1
            j -= 1
        elif i > 0 and matrix[i, j] == matrix[i-1, j] + 1:
            ref_aligned.append(ref[i-1])
            hyp_aligned.append("<epsilon>")
            i -= 1
        elif j > 0 and matrix[i, j] == matrix[i, j-1] + 1:
            ref_aligned.append("<epsilon>")
            hyp_aligned.append(hyp[j-1])
            j -= 1
        else:
            ref_aligned.append(ref[i-1])
            hyp_aligned.append(hyp[j-1])
            i -= 1
            j -= 1

    refa, hypa = ref_aligned[::-1], hyp_aligned[::-1]
    binary_list = [int(r == h) for r, h in zip(refa, hypa)]
    return refa, hypa, binary_list


# write a function that return the n most frequent elmements in a list
def most_frequent(lst, n):
    return Counter(lst).most_common(n)




if __name__ == "__main__":
    #filename = "KD_woR.txt"
    filename = "ex1.txt"

    refs = []
    hyps = []
    binary_lists = []
    with open("data/" + filename, "r", encoding="utf8") as f:
        for line in f:
            line = line.split("\t")
            ref = line[1].split(" ")
            hyp = line[2].split(" ")
            ref_aligned, hyp_aligned, binary_list = levenstein_alignment(ref, hyp)
            refs.append(ref_aligned)
            hyps.append(hyp_aligned)
            binary_lists.append(binary_list)

            
    # given the reference and hypothesis in two lists using the levenstein_alignment function, align the reference and hypothesis so we can print the top substitutions and deletions and insertions

    substitutions = []
    deletions = []
    insertions = []
    for i, binary_list in enumerate(binary_lists):
        for j, binary in enumerate(binary_list):
            if binary == 0:
                if hyps[i][j] == "<epsilon>":
                    deletions.append(refs[i][j])
                elif refs[i][j] == "<epsilon>":
                    insertions.append(hyps[i][j])
                else:
                    substitutions.append((refs[i][j], hyps[i][j]))


    n = 6

    print("Substitutions:")
    for substitution in most_frequent(substitutions, n):
        print(substitution)
    print("Deletions:")
    for deletion in most_frequent(deletions, n):
        print(deletion)
    print("Insertions:")
    for insertion in most_frequent(insertions, n):
        print(insertion)

    if os.path.isdir("results/" + filename[:-4]) == False:
        os.mkdir("results/" + filename[:-4])

    with open("results/" + filename[:-4] + "/substitutions.txt", "w", encoding="utf8") as f:
        for substitution in most_frequent(substitutions, len(substitutions)):
            f.write(substitution[0][0] + "\t" + substitution[0][1] + "\t" + str(substitution[1]) + "\n")
    with open("results/" + filename[:-4] + "/deletions.txt", "w", encoding="utf8") as f:
        for deletion in most_frequent(deletions, len(deletions)):
            f.write(deletion[0] + "\t" + str(deletion[1]) + "\n")
    with open("results/" + filename[:-4] + "/insertions.txt", "w", encoding="utf8") as f:
        for insertion in most_frequent(insertions, len(insertions)):
            f.write(insertion[0] + "\t" + str(insertion[1]) + "\n")