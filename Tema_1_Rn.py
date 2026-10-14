import pathlib

def load_system(path: pathlib.Path) -> tuple[list[list[float]], list[float]]:
    A: list[list[float]] = []
    B: list[float] = []

    with open(path, "r") as f:
        for line in f:
            if "=" not in line:
                continue
            # separam stanga si dreapta de egal
            st, dr = line.split("=")
            B.append(float(dr))

            linie = []
            semn = 1.0
            # luam pe rand fiecare termen
            for token in st.split():
                if token == "+":
                    semn = 1.0
                elif token == "-":
                    semn = -1.0
                else:
                    val_str = token[:-1]
                    # daca litera nu are cifra in fata, e 1
                    if val_str == "":
                        val = 1.0
                    else:
                        val = float(val_str)
                    linie.append(val * semn)
            A.append(linie)
    return A, B

def determinant(matrix: list[list[float]]) -> float:
    # despachetam liniile
    a11, a12, a13 = matrix[0]
    a21, a22, a23 = matrix[1]
    a31, a32, a33 = matrix[2]
    # formula clasica pt 3x3
    det = a11*(a22*a33 - a23*a32) - a12*(a21*a33 - a23*a31) + a13*(a21*a32 - a22*a31)
    return float(det)

def trace(matrix: list[list[float]]) -> float:
    # adunam de pe diagonala
    tr = matrix[0][0] + matrix[1][1] + matrix[2][2]
    return float(tr)

def norm(vector: list[float]) -> float:
    # radical din suma patratelor
    norma = vector[0]**2 + vector[1]**2 + vector[2]**2
    return float(norma**0.5)

def transpose(matrix: list[list[float]]) -> list[list[float]]:
    n = len(matrix)
    rez = []
    # inversam i cu j
    for i in range(n):
        linie_noua = []
        for j in range(n):
            linie_noua.append(matrix[j][i])
        rez.append(linie_noua)
    return rez

def multiply(matrix: list[list[float]], vector: list[float]) -> list[float]:
    m = []
    n = len(matrix)
    # inmultim matricea cu vectorul
    for i in range(n):
        val = matrix[i][0]*vector[0] + matrix[i][1]*vector[1] + matrix[i][2]*vector[2]
        m.append(val)
    return m

def solve_cramer(matrix: list[list[float]], vector: list[float]) -> list[float]:
    det_A = determinant(matrix)
    
    # inlocuim col 1 cu vectorul termenilor liberi
    A_x = [[vector[0], matrix[0][1], matrix[0][2]],
           [vector[1], matrix[1][1], matrix[1][2]],
           [vector[2], matrix[2][1], matrix[2][2]]]
           
    # inlocuim col 2
    A_y = [[matrix[0][0], vector[0], matrix[0][2]],
           [matrix[1][0], vector[1], matrix[1][2]],
           [matrix[2][0], vector[2], matrix[2][2]]]
           
    # inlocuim col 3
    A_z = [[matrix[0][0], matrix[0][1], vector[0]],
           [matrix[1][0], matrix[1][1], vector[1]],
           [matrix[2][0], matrix[2][1], vector[2]]]
           
    x = determinant(A_x) / det_A
    y = determinant(A_y) / det_A
    z = determinant(A_z) / det_A
    return [x, y, z]

def minor(matrix: list[list[float]], i: int, j: int) -> list[list[float]]:
    min_matrix = []
    n = len(matrix)
    for i1 in range(n):
        # sarim peste linia curenta
        if i1 == i:
            continue
        linie = []
        for j1 in range(n):
            # sarim si peste coloana
            if j1 == j:
                continue
            linie.append(matrix[i1][j1])
        min_matrix.append(linie)
    return min_matrix

def cofactor(matrix: list[list[float]]) -> list[list[float]]:
    n = len(matrix)
    A_ij = []
    for i in range(n):
        linie = []
        for j in range(n):
            m = minor(matrix, i, j)
            # det pt 2x2
            det = m[0][0]*m[1][1] - m[0][1]*m[1][0]
            # regula semnelor
            linie.append(((-1)**(i+j)) * det)
        A_ij.append(linie)
    return A_ij

def adjoint(matrix: list[list[float]]) -> list[list[float]]:
    # adjuncta e transpusa matricii cofactorilor
    cof = cofactor(matrix)
    adj = transpose(cof)
    return adj

def solve(matrix: list[list[float]], vector: list[float]) -> list[float]:
    det_A = determinant(matrix)
    adj_A = adjoint(matrix)
    n = len(matrix)
    inv_A = []
    
    # inmultim fiecare element din adjuncta cu 1 pe det
    for i in range(n):
        linie = []
        for j in range(n):
            linie.append((1 / det_A) * adj_A[i][j])
        inv_A.append(linie)

    # la final inmultim inversa cu vectorul b
    X = multiply(inv_A, vector)
    return X