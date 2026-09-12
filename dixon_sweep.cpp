// Dixon-Coles soccer 1X2 + BTTS, sweep rho from -0.15 to 0.
// Independent Poisson joint, then tau on the four low-score cells.
// Marginals P(H=0) and P(A=0) stay Poisson; BTTS and draw move with rho.

#include <iostream>
#include <cmath>
using namespace std;

const int z0 = 31;              // goals 0 .. 30
const double db = 0.00000001;   // snap rho to 0 after float drift

class Tup {
public:
    double v[3];
    void start() { v[0] = v[1] = v[2] = 0; }
};

// Kill tiny residuals so (rho == 0) is reachable after += 0.005.
double klean(double x) {
    if (x < db && x > -db) x = 0;
    return x;
}

class Mat {
public:
    double m[z0][z0];

    // Build P(H=i, A=j) = Poisson(i; muH) Poisson(j; muA) * tau(i,j).
    void set(double muH, double muA, double rho) {
        int i, j;
        double h[z0], a[z0];
        h[0] = exp(-muH);
        a[0] = exp(-muA);
        for (i = 1; i < z0; i++) {
            h[i] = h[i - 1] * muH / (double)i;
            a[i] = a[i - 1] * muA / (double)i;
        }
        for (i = 0; i < z0; i++)
            for (j = 0; j < z0; j++)
                m[i][j] = h[i] * a[j];

        // Dixon-Coles tau. Valid rho:
        // max(-1/muH, -1/muA) <= rho <= min(1, 1/(muH*muA))
        m[0][0] *= (1 - rho * muH * muA);
        m[0][1] *= (1 + rho * muH);
        m[1][0] *= (1 + rho * muA);
        m[1][1] *= (1 - rho);
    }

    // v[0] home (H>A), v[1] draw, v[2] away.
    Tup hda() {
        Tup T;
        T.start();
        int i, j;
        for (i = 0; i < z0; i++)
            for (j = 0; j < z0; j++) {
                if (i > j)  T.v[0] += m[i][j];
                if (i == j) T.v[1] += m[i][j];
                if (i < j)  T.v[2] += m[i][j];
            }
        return T;
    }

    // v[0] home scores, v[1] away scores, v[2] BTTS.
    // First two are almost invariant in rho; BTTS is not.
    Tup score() {
        Tup T;
        T.start();
        int i, j;
        for (i = 0; i < z0; i++)
            for (j = 0; j < z0; j++) {
                if (i != 0)                 T.v[0] += m[i][j];
                if (j != 0)                 T.v[1] += m[i][j];
                if (i != 0 && j != 0)       T.v[2] += m[i][j];
            }
        return T;
    }
};

int main() {
    cout << "\n\n";
    double muH, muA, rho;
    Mat M;
    Tup X, Y;

    cout << "Soccer Dixon-Coles Calculator\n\nenter home mean: ";
    cin >> muH;
    cout << "\nenter away mean: ";
    cin >> muA;
    cout << "\n";

    rho = -0.15;
    while (rho <= 0) {
        M.set(muH, muA, rho);
        X = M.hda();
        Y = M.score();
        cout << "rho = " << rho;
        if (rho == 0) cout << "\t";
        cout << "\thome: " << X.v[0]
             << "\tdraw: " << X.v[1]
             << "\taway: " << X.v[2]
             << "\tbtts: " << Y.v[2] << "\n";
        rho += 0.005;
        rho = klean(rho);
    }
    cout << "\n\n";
    return 0;
}
