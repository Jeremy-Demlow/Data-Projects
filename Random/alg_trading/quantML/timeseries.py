import numpy as np
from scipy import linalg as la
from cmath import exp
# import pandas as pd
import datetime as dt
from quantML import scrape
from matplotlib import pyplot as plt


class DMD:

    '''
    This class contains the functions needed for performing a full DMD
    on any given matrix. Depending on functions being used, different
    outputs can be achieved.
    This class also contains functions useful to the analysis of DMD
    results and intermediates.
    '''

    @staticmethod
    def split(Xf, verbose=False):
        '''
        This function will perform a manipulation for DMD
        which is the splitting of a spacial-temporal matrix (Xf) into
        two matrices (X and Xp). The X matrix is the time series for
        1 to n-1 and Xp is the time series of 2 to n where n is the
        number of time intervals (columns of the original Xf).

        input:
        Xf - matrix of full spacial-temporal data

        output:
        X - matrix for times 1 to n-1
        Xp - matrix for times 2 to n

        options:
        verbose - boolean for visualization of splitting
        '''

        if verbose:
            print('Entering the matrix splitting function:')

        if verbose:
            print('Xf =\n', Xf, '\n')

        X = Xf[:, :-1]
        Xp = Xf[:, 1:]

        if verbose:
            print('X =\n', X, '\n')
            print('Xp =\n', Xp, '\n')
        return X, Xp

    @staticmethod
    def decomp(Xf, time, verbose=False, rank_cut=True, esp=1e-2, svd_cut=False,
               num_svd=1, do_SVD=True, given_svd=False):
        '''
        This function performs the basic DMD on a given matrix A.

        inputs:
        X - (mxn) Spacial Temporal Matrix
        time - (nx1) Time vector

        outputs:
        (1) Phi - DMD modes
        (2) omg - discrete time eigenvalues
        (3) lam - continuous time eigenvalues
        (4) b - amplitudes of DMD modes
        (5) Xdmd - reconstructed X matrix from DMD modes
        (6) rank - the rank used in calculations

        *** all contained in a class ***
        ***  see ### (10) ### below  ***

        options:
        verbose - boolean for more information
        svd_cut - boolean for truncation of SVD values of X
        esp - value to truncate singular values lower than
        rank_cut - truncate the SVD of X to the rank of X
        num_svd - number of singular values to use
        do_SVD - tells the program if the svd is provided to it or not
        '''

        if verbose:
            print('Entering Dynamic Mode Decomposition:\n')

        # --- (1) --- #
        # split the Xf matrix
        X, Xp = DMD.split(Xf)
        if verbose:
            print('X = \n', X, '\n')
            print('X` = \n', Xp, '\n')

        ### (2) ###  # noqa:
        # perform a singular value decompostion on X
        if do_SVD:
            if verbose:
                'Performing singular value decomposition...\n'
            U, S, Vh = la.svd(X)
        else:
            if verbose:
                'Singular value decomposition provided...\n'
            U, S, Vh = given_svd

        if verbose:
            print('Singular value decomposition:')
            print('U: \n', U)
            print('S: \n', S)
            print('Vh: \n', Vh)
            print('Reconstruction:')
            S_m = np.zeros(np.shape(X))
            for i in range(len(list(S))):
                S_m[i, i] = S[i]
            recon = np.dot(np.dot(U, S_m), Vh)
            print('X =\n', recon)

        # perform desired truncations of X
        if svd_cut:
            rank_cut = False
        if rank_cut:  # this is the default truncation
            rank = 0
            for i in S:
                if i > esp:
                    rank += 1
            if verbose:
                print('Singular Values of X:', '\n', S, '\n')
                print('Reducing Rank of System...\n')
            Ur = U[:, 0:rank]
            Sr = S[0:rank]
            Vhr = Vh[0:rank, :]
            if verbose:
                recon = np.dot(np.dot(Ur, np.diag(Sr)), Vhr)
                print('Rank Reduced reconstruction:\n', 'X =\n', recon)
        elif svd_cut:
            rank = num_svd
            if verbose:
                print('Singular Values of X:', '\n', S, '\n')
                print('Reducing Rank of System to n =', num_svd, '...\n')
            Ur = U[:, 0:rank]
            Sr = S[0:rank]
            Vhr = Vh[0:rank, :]
            if verbose:
                recon = np.dot(np.dot(Ur, np.diag(Sr)), Vhr)
                print('Rank Reduced reconstruction:\n', 'X =\n', recon)

        # return the condition number to view singularity
        condition = max(Sr) / min(Sr)
        smallest_svd = min(Sr)
        svd_used = np.size(Sr)
        if verbose:
            condition = max(Sr) / min(Sr)
            print('Condition of Rank Converted Matrix X:', '\nK =', condition, '\n')

        # make the singular values a matrix and take the inverse
        Sr_inv = np.diag([i ** -1 for i in Sr])
        Sr = np.diag(Sr)

        ### (3) ###  # noqa:
        # now compute the A_t matrix
        Vr = Vhr.conj().T
        At = Ur.conj().T.dot(Xp)
        At = At.dot(Vr)
        At = At.dot(la.inv(Sr))
        if verbose:
            print('A~ = \n', At, '\n')

        ### (4) ###  # noqa:
        # perform the eigen decomposition of At
        L, W = la.eig(At)
        # also determine the number of positive eigenvalues
        pos_eigs = np.count_nonzero((L > 0))

        ### (5) ###  # noqa:
        # compute the DMD modes
        # phi = Xp @ Vhr.conj().T @ Sr_inv @ W
        phi = np.dot(Xp, Vhr.conj().T)
        phi = np.dot(phi, Sr_inv)
        phi = np.dot(phi, W)

        if verbose:
            print('DMD Mode Matrix:', '\nPhi =\n', phi, '\n')

        ### (6) ###   # noqa:
        # compute the continuous and discrete eigenvalues
        dt = time[1] - time[0]
        lam = L
        omg = np.log(lam) / dt
        if verbose:
            print('Discrete time eigenvalues:\n', 'Lambda =', L, '\n')
            print('Continuous time eigenvalues:\n', 'Omega =', np.log(L) / dt, '\n')
            print('Number of positive eigenvalues: ', pos_eigs, '\n')

        ### (7) ###  # noqa:
        # compute the amplitude vector b by solving the linear system described.
        # note that a least squares solver has to be used in order to approximate
        # the solution to the overdefined problem
        x1 = X[:, 0]
        b = la.lstsq(phi, x1)
        b = b[0]
        if verbose:
            print('b =\n', b, '\n')

        ### (8) ###  # noqa:
        # finally reconstruct the data matrix from the DMD modes
        length = np.size(time)  # number of time measurements
        # initialize the time dynamics
        dynamics = np.zeros((rank, length), dtype=np.complex_)
        for t in range(length):
            omg_p = np.array([exp(i * time[t]) for i in omg])
            dynamics[:, t] = b * omg_p

        if verbose:
            print('Time dynamics:\n', dynamics, '\n')

        # reconstruct the data
        Xdmd = np.dot(phi, dynamics)
        if verbose:
            print('Reconstruction:\n', np.real(Xdmd), '\n')
            print('Original:\n', np.real(Xf), '\n')

        ### (9) ###  # noqa:
        # calculate some residual value
        res = np.real(Xf - Xdmd)
        error = la.norm(res) / la.norm(Xf)
        if verbose:
            print('Reconstruction Error:', round(error * 100, 2), '%')

        ### (10) ###  # noqa:
        # returns a class with all of the results
        class results():
            def __init__(self):
                self.phi = phi
                self.omg = omg
                self.lam = lam
                self.b = b
                self.Xdmd = Xdmd
                self.error = error * 100
                self.rank = rank
                self.svd_used = svd_used
                self.condition = condition
                self.smallest_svd = smallest_svd
                self.pos_eigs = pos_eigs
                self.dynamics = dynamics
                self.svd_used = svd_used

        return results()

    @staticmethod
    def predict(dmd, t):
        '''
        This function will take a DMD decomposition output
        result and a desired time incremint prediction and
        produce a prediction of the system at the given time.

        inputs:
        dmd - class that comes from the function "decomp"
        t - future time for prediction

        outputs:
        x - prediction vector (real part only)
        '''

        # finally reconstruct the data matrix from the DMD modes
        dynamics = np.zeros((dmd.rank, 1), dtype=np.complex_)
        omg_p = np.array([exp(i * t) for i in dmd.omg])
        dynamics = dmd.b * omg_p
        x = np.real(np.dot(dmd.phi, dynamics))

        return x

    @staticmethod
    def predict_vec(dmd, t_vec):
        '''
        vector implementation of "predict"
        '''
        pred = []
        for t in t_vec:
            dynamics = np.zeros((dmd.rank, 1), dtype=np.complex_)
            omg_p = np.array([exp(i * t) for i in dmd.omg])
            dynamics = dmd.b * omg_p
            x = np.real(np.dot(dmd.phi, dynamics))
            pred.append(x)
        return np.array(pred).T

    @staticmethod
    def dmd_specific_svd(Xf):
        '''
        This is a helper function which will split the data and
        perform a singular value decomposition based on whatever the
        input data is and return the outputs for scipy.
        '''

        X, Xp = DMD.split(Xf)
        result = la.svd(X)

        return result

    @staticmethod
    def augment_matrix(x, n):
        '''
        Function to take a vector x and returns an augmented matrix X which
        has n rows.
        '''

        # length of full time series
        num_elements = x.shape[0]

        # length of each row in the X matrix
        len_row = num_elements - n + 1

        # initalize the matrix
        X = []

        # loop over each row
        for row_num in range(n):

            # grab the smaller vector
            small_vec = x[row_num:row_num + len_row]

            # append the vector
            X.append(small_vec)

        return np.array(X)



if __name__ == '__main__':
    ticker = 'MMM'
    days_train = 100
    num_out = 10
    num_svd = 10
    stop = dt.datetime.today().date()
    start = stop - dt.timedelta(days=days_train)

    df = scrape.get_prices([ticker], start, stop,)
    X = DMD.augment_matrix(df.close.to_numpy(), num_out)
    time = np.arange(X.shape[1])
    dmd_res = DMD.decomp(X, time, num_svd=num_svd, verbose=False, svd_cut=True, rank_cut=False)
    pred_time = np.arange(num_out) + 1 + max(time)
    pred = DMD.predict_vec(dmd_res, pred_time)[0]
    print(pred)

    fig, ax = plt.subplots()
    ax.plot(df.close.to_numpy(), label='training')
    ax.plot(pred, label='prediction')
    ax.legend()
    ax.set_title(ticker)
    plt.show()


    print(pred)
