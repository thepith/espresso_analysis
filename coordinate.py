""" generate overlapp free coordinates """


def pbc(vec, box_l):
    """apply periodic boundary conditions to a distance vector"""
    import numpy as np
    vec_pbc = vec - box_l * np.around(vec / box_l)
    return vec_pbc


def test_overlap(testposition, other_positions, rmin, box_l):
    import numpy
    for other_position in other_positions:
        if numpy.linalg.norm(pbc(testposition - other_position, box_l)) < rmin:
            return True
    return False


def random_pos(N, box_l, rmin, occ_positions=[], maxtry=1000):
    """generate overlap free random positions"""
    import numpy as np
    set_pos = []
    for ipos in range(N):
        itry = 0
        while True:
            pos = (np.random.random(3) - 0.5) * box_l
            if not test_overlap(pos, set_pos + occ_positions, rmin, box_l):
                break
            itry += 1
            if itry >= maxtry:
                raise ValueError("Failed to set random particles")

        set_pos += [pos]
    return set_pos


def self_avoiding_random_chain(N, box_l, rmin, bondl, occ_positions=[], maxtry=1000):
    itry = 0
    set_pos = []
    while len(set_pos) < N:
        set_pos = random_pos(1, box_l, rmin, occ_positions, maxtry)
        for ipos in range(1, N):
            set_part = False
            for jtry in range(maxtry):
                pos = set_pos[ipos - 1] + random_vector_on_sphere()*bondl
                if not test_overlap(pos, set_pos + occ_positions, rmin, box_l):
                    set_part = True
                    break
            if set_part:
                set_pos += [pos]
            else:
                print(set_pos, pos)
                raise ValueError("Failed to set random chain at particle {}".format(ipos))
        itry += 1
        if itry >= maxtry:
            raise ValueError("Failed to set random chain at particle")
    return set_pos


def random_vector_on_sphere():
    import numpy as np
    while True:
        xi = np.random.random(2)
        zeta = 1 - 2 * xi
        zetas = np.sum(np.power(zeta, 2.0))
        if zetas < 1:
            zetasqrt = np.sqrt(1 - zetas)
            return np.array([2.0*zeta[0]*zetasqrt, 2.0*zeta[1]*zetasqrt, 1.0-2.0*zetas])
