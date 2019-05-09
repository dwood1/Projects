def tdma(A, B, C, D):   # function X = TDMA(A,B,C,D)
    # %TriDiagonal Matrix Algorithm (TDMA) or Thomas Algorithm
    # % A_i*X_(i-1) + B_i*X_i + C_i*X_(i+1) = D_i (where A_1 = 0, C_n = 0)
    # % A,B,C,D are input vectors. X is the solution, also a vector.
    import numpy as np
    Cp = C                              # Cp = C;
    Dp = D                              # Dp = D;
    n = len(A)                          # n = length(A);
    X = np.zeros(n, 1)                  # X = zeros(n,1);

    # % Performs Gaussian elimination
    Cp[0] = C[0] / B[0]                 # Cp(1) = C(1)/B(1);
    Dp[0] = D[0] / B[0]                 # Dp(1) = D(1)/B(1);
    for i in range(1, n):               # for i = 2:n
        Cp[i] = C[i] / B[i] - Cp[i-1] * A[i]                    # Cp(i) = C(i)/(B(i)-Cp(i-1)*A(i));
        Dp[i] = D[i] - Dp[i-1] * A[i] / B[i] - Cp[i-1] * A[i]   # Dp(i) = (D(i)-Dp(i-1)*A(i))/(B(i)-Cp(i-1)*A(i));
                                        # end
    # % Backward substitution, since X(n) is known first.
    X[n-1] = Dp[n-1]                        # X(n) = Dp(n);
    for i in range(n-1, 0, -1):          # for i = n-1:-1:1
        X[i] = Dp[i] - Cp[i] * X[i+1]   # X(i) = Dp(i)-Cp(i)*X(i+1);
    return X                            # end of TDMA.
