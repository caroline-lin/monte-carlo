from merge import * 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


# copied from the plotting file

np.random.seed(0)

if __name__ == '__main__':
    Ns = [40]
    nsamples_list = [10]


    for N in Ns:
        for nsamples in nsamples_list:
            print(N,nsamples)
            boundary_func = lambda x: x[0]*x[0] + x[1]*x[1] - 1
            #boundary_func = squiggly_domain(0.45)
            h = 2/N
            grid_to_vec, vec_to_grid, boundary, grid_to_point = grid_gen(boundary_func, np.array([-1.0,-1.0]), np.array([1.0,1.0]), np.array([N+1,N+1]))
            #grid_to_vec, vec_to_grid, boundary, grid_to_point = grid_gen(boundary_func, np.array([-1.5,-1.5]), np.array([1.5,1.5]), np.array([N+1,N+1]))

            domain = SetWithCartesianBoundary(boundary, grid_to_point, boundary_func, h)
            
            f = lambda x: x[0]**3 + x[1]**3 - 3*x[0]*x[0]*x[1] - 3*x[0]*x[1]*x[1] + 1
            g = lambda x: 0
            # f = lambda x: x[0]**2 + x[1]**2
            # g = lambda x: -4

            simulator = MonteCarloSimulator(domain, nsamples,
                lambda x, y: x ** 3 + y ** 3 - 3 * x ** 2 * y -3 * y ** 2 * x + 1
            )

            #for i, el in enumerate(zip(domain.bdry_X, domain.bdry_Y)):
            #    plt.scatter(el[0], el[1], c=np.array([ i / len(domain.bdry_X), i / len(domain.bdry_X), i / len(domain.bdry_X)]).reshape(1, -1))
            #
            #plt.scatter(domain.bdry_X[0], domain.bdry_Y[0], c='r')
            #plt.show()
            '''
            print("Simulating a few points.")
            my_point = domain.bdry_X[-20], domain.bdry_Y[-20]

            figs, axes = plt.subplots(1, 2, figsize=(6, 3))
            simulator.simulate_point(my_point, plotting=True, ax=axes[0])
            simulator.simulate_point(my_point, plotting=True, coupling=True, ax=axes[1])

            axes[0].set_title(f"No coupling, 10 Walks")
            axes[1].set_title(f"Coupling, 10 Walks from {tuple(map(lambda s: round(s, 2), my_point))}")
            
            plt.savefig('./figures/random-walks.png')
            exit(0)
            '''
            
            simulator.simulate()
            u = simulator.solve_coupling()

            # solve on the interior
            def find_val(p):
                return u[domain.bdry_dict[p]]
            L, b = gen_L(find_val, g, grid_to_vec, vec_to_grid, boundary, grid_to_point, h)
            x = sppl.spsolve(L, b)
            x_true = np.vectorize(lambda x: f(grid_to_point(x)), signature='(n)->()')(np.array(vec_to_grid))


            points = [grid_to_point( vec_to_grid[i] ) for i in range(len(vec_to_grid))]
            X = np.array( list(map( lambda x: x[0], points )) )
            Y = np.array( list(map( lambda x: x[1], points )) )


            fig, ax = plt.subplots(1, 3, subplot_kw={'projection': '3d'}, figsize=(9, 3))
            ax[0].set_xlabel('X')
            ax[0].set_ylabel('Y')
            ax[0].set_zlabel('U')

            ax[0].scatter(X, Y, x)
            ax[1].scatter(X, Y, x, c='r')
            
            ax[2].scatter(X, Y, x)
            ax[2].scatter(X, Y, x, c='r')

            plt.savefig('./figures/results-circle.png')
            
            print('Carolinesim -- exiting early')
            exit(0)

            # Okay, now I should make some plots of my solution.


        


            def find_val(p):
                return u[domain.bdry_dict[p]]

            L, b = gen_L(find_val, g, grid_to_vec, vec_to_grid, boundary, grid_to_point, h)

            x = sppl.spsolve(L, b)
            x_true = np.vectorize(lambda x: f(grid_to_point(x)), signature='(n)->()')(np.array(vec_to_grid))
            
            print(np.max(np.abs(x-x_true)))
            print(np.max(np.abs(x-x_true)/x_true))
            print(np.mean(np.abs(x-x_true)/x_true))


            find_val_exact = lambda x: f(grid_to_point(x))
            for k in boundary:
                boundary[k] = None

            L, b = gen_L(find_val_exact, g, grid_to_vec, vec_to_grid, boundary, grid_to_point, h)

            x = sppl.spsolve(L, b)
            x_true = np.vectorize(lambda x: f(grid_to_point(x)), signature='(n)->()')(np.array(vec_to_grid))
            print(np.max(np.abs(x-x_true)))
            # print(np.max(np.abs(x-x_true)/x_true))
            # print(np.mean(np.abs(x-x_true)/x_true))
