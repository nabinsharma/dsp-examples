# Digital Signal Processing by Paolo Prandoni and Martin Vetterli
# Coursera/EPFL

# Nabin Sharma
# Oct 19, 2013

from mpl_toolkits.mplot3d import proj3d
from matplotlib.patches import FancyArrowPatch
import matplotlib.pyplot as plt
import numpy


def gs_orthonormalization(V):
    """
    V is a matrix where each column contains the vectors spanning
    the space of which we want to compute the orthonormal base E
    is a matrix where each column contains an ortho-normal vector
    of the base of the space.
    """

    V = numpy.asmatrix(V)

    # Projection of vector v onto the line spanned by vector u.
    # Note that u and v must be single column matrix.
    proj_uv = lambda u, v: numpy.squeeze(numpy.asarray(v.T * u / (u.T * u))) * u

    # Matrix containing the orthogonal vectors (non normalized).
    U = numpy.asmatrix(numpy.zeros(V.shape))

    # Matrix containing the orthogonal vectors.
    E = numpy.asmatrix(numpy.zeros(V.shape))
    
    for c in range(V.shape[1]):
        U[:, c] = V[:, c]
        R = numpy.asmatrix(numpy.zeros(V.shape[0])).T
        for k in range(0, c):
            R = R + proj_uv(U[:, k], V[:, c])
        U[:, c] = U[:, c] -  R
        E[:, c] = U[:, c] / numpy.linalg.norm(U[:, c])
    return E


def example():
    # A set of orthonormal vectors.
    ex = numpy.matrix([1, 0, 0]).T
    ey = numpy.matrix([0, 1, 0]).T
    ez = numpy.matrix([0, 0, 1]).T
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection='3d')
    ax1.view_init(elev=20, azim=-135)
    _draw_vector(ex, ax1)
    _draw_vector(ey, ax1)
    _draw_vector(ez, ax1, True)

    # Rotate the vectors so that they become non orthonormal.
    Rx, Ry, Rz = _rotation_matrices(numpy.pi/3, numpy.pi/4, numpy.pi/6)
    v1 = Rz * ex
    v2 = Rx * ey
    v3 = Ry * ez
    V = numpy.matrix([numpy.squeeze(numpy.asarray(v1)),
                      numpy.squeeze(numpy.asarray(v2)),
                      numpy.squeeze(numpy.asarray(v3))]).T
    fig = plt.figure()
    ax2 = fig.add_subplot(111, projection='3d')
    ax2.view_init(elev=20, azim=-135)
    _draw_vector(v1, ax2)
    _draw_vector(v2, ax2)
    _draw_vector(v3, ax2, True)

    # Use Gram-Schmidt orthonormalizatiion on V to make
    # it a set of orthonormal vectors.
    E = gs_orthonormalization(V)
    fig = plt.figure()
    ax3 = fig.add_subplot(111, projection='3d')
    ax3.view_init(elev=20, azim=-135)
    _draw_vector(E[:, 0], ax3)
    _draw_vector(E[:, 1], ax3)
    _draw_vector(E[:, 2], ax3, True)
    plt.show()


def exercise():
    V = numpy.matrix([[0.86, 0.5, 0],
                      [0, 0.5, 0.86],
                      [1.732, 3, 3.464]]).T
    E = gs_orthonormalization(V)
    print("Solution to Exercise")
    print("E represents a set of orthonormal vectors as E\'*E = I:")
    print(E.T*E)


## Utilities.

# The arrow drawing class is taken from
# https://github.com/wealth/magnetic/blob/master/black-field.py
class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)


def _vec3d_to_arrow(p1, p0=numpy.matrix([0, 0, 0]).T):
    p1 = numpy.squeeze(numpy.asarray(p1.T))
    p0 = numpy.squeeze(numpy.asarray(p0.T))
    return Arrow3D([p0[0], p1[0]], [p0[1], p1[1]], [p0[2] ,p1[2]],
                   mutation_scale=20, lw=1,
                   arrowstyle="-|>", color="k")


def _draw_vector(v, ax, finalize=False):
    ax.add_artist(_vec3d_to_arrow(v))
    if finalize:
        ax.set_xlim(-0.2, 1.2)
        ax.set_ylim(-0.2, 1.2)
        ax.set_zlim(0, 0.8)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')


def _rotation_matrices(theta, alpha, beta):
    Rx = numpy.matrix([[1, 0, 0],
                       [0, numpy.cos(theta), -numpy.sin(theta)],
                       [0, numpy.sin(theta), numpy.cos(theta)]])
    Ry = numpy.matrix([[numpy.cos(alpha), 0, numpy.sin(alpha)],
                       [0, 1, 0],
                       [-numpy.sin(alpha), 0, numpy.cos(alpha)]])
    Rz = numpy.matrix([[numpy.cos(beta), -numpy.sin(beta), 0],
                       [numpy.sin(beta), numpy.cos(beta), 0],
                       [0, 0, 1]])
    return Rx, Ry, Rz


if __name__ == "__main__":
    example()
    exercise()
