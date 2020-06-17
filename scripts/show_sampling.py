#! /usr/bin/env python3
import argparse
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
import numpy as np
import euphonic.sampling

choices_2d = {'golden-square', 'regular-square'}
choices_3d = {'golden-sphere', 'sphere-from-square-grid',
              'spherical-polar-grid', 'spherical-polar-improved',
              'random-sphere'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('npts', type=int)
    parser.add_argument('sampling', type=str,
                        choices=(choices_2d | choices_3d))
    parser.add_argument('--jitter', action='store_true',
                        help='Apply local random displacements to points')
    args = parser.parse_args()

    if args.sampling in choices_2d:
        fig, ax = plt.subplots()
    else:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

    if args.sampling == 'golden-square':
        ax.plot(*zip(*euphonic.sampling.golden_square(args.npts,
                                                      jitter=args.jitter)),
                'o')
    elif args.sampling == 'regular-square':
        n_rows = int(np.ceil(np.sqrt(args.npts)))
        npts = n_rows**2

        if npts != args.npts:
            print("Requested npts ∉ {x^2, x ∈ Z, x > 1}; "
                  f"rounding up to {npts}.")
        ax.plot(*zip(*euphonic.sampling.regular_square(n_rows, n_rows,
                                                       jitter=args.jitter)),
                'o')

    elif args.sampling == 'golden-sphere':
        ax.scatter(*zip(*euphonic.sampling.golden_sphere(args.npts,
                                                         jitter=args.jitter)),
                   marker='x')
    elif args.sampling == 'spherical-polar-grid':
        n_theta = int(np.ceil(np.sqrt(args.npts / 2)))
        npts = n_theta**2 * 2

        if npts != args.npts:
            print("Requested npts ∉ {2x^2, x ∈ Z, x > 1}; "
                  f"rounding up to {npts}.")

        ax.scatter(*zip(
            *euphonic.sampling.spherical_polar_grid(n_theta * 2, n_theta,
                                                    jitter=args.jitter)),
                   marker='x')

    elif args.sampling == 'sphere-from-square-grid':
        n_theta = int(np.ceil(np.sqrt(args.npts / 2)))
        npts = n_theta**2 * 2

        if npts != args.npts:
            print("Requested npts ∉ {2x^2, x ∈ Z, x > 1}; "
                  f"rounding up to {npts}.")

        ax.scatter(*zip(
            *euphonic.sampling.sphere_from_square_grid(n_theta * 2, n_theta,
                                                       jitter=args.jitter)),
                   marker='x')

    elif args.sampling == 'spherical-polar-improved':
        ax.scatter(
            *zip(*euphonic.sampling.spherical_polar_improved(
                args.npts, jitter=args.jitter)),
            marker='x')
    elif args.sampling == 'random-sphere':
        ax.scatter(
            *zip(*euphonic.sampling.random_sphere(args.npts)),
            marker='x')
    else:
        raise ValueError("Sampling type f{args.sampling} is not implemented.")

    plt.show()


if __name__ == '__main__':
    main()