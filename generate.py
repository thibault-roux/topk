import numpy as np


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





if __name__ == "__main__":
    #filename = "KD_woR.txt"
    filename = "ex1.txt"

    refs = []
    hyps = []
    binary_lists = []
    with open("data/" + filename, "r", encoding="utf8") as f:
        for line in file:
            line = line.split("\t")
            ref = line[1]
            hyp = line[2]
            ref_aligned, hyp_aligned, binary_list = levenstein_alignment(ref, hyp)
            refs.append(ref_aligned)
            hyps.append(hyp_aligned)
            binary_lists.append(binary_list)

            
    # given the reference and hypothesis in two lists using the levenstein_alignment function, align the reference and hypothesis so we can print the top substitutions and deletions and insertions
    # print the top 5 substitutions, deletions and insertions

    substitutions = []
    deletions = []
    insertions = []
    for binary_list in binary_lists:
        for i, binary in enumerate(binary_list):
            if binary == 0:
                if hyps[i] == "<epsilon>":
                    deletions.append(refs[i])
                elif refs[i] == "<epsilon>":
                    insertions.append(hyps[i])
                else:
                    substitutions.append((refs[i], hyps[i]))

    print("Substitutions:")
    for substitution in sorted(substitutions, key=lambda x: substitutions.count(x), reverse=True)[:5]:
        print(substitution, substitutions.count(substitution))
    print("Deletions:")
    for deletion in sorted(deletions, key=lambda x: deletions.count(x), reverse=True)[:5]:
        print(deletion, deletions.count(deletion))
    print("Insertions:")
    for insertion in sorted(insertions, key=lambda x: insertions.count(x), reverse=True)[:5]:
        print(insertion, insertions.count(insertion))