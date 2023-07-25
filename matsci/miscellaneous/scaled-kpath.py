G = (0,0,0)
M = (1/2, 0, 0)
K = (1/3, 1/3, 0)
detect = False
steps = [G,M,K,G]
invcell = read('inse/plotdata/monolayer/unit.xyz').cell.array
npointstotal=400
nunit= len(read('inse/plotdata/monolayer/unit.xyz'))

# Generate x values
distances = np.array([np.linalg.norm(np.matmul(invcell, np.subtract(np.roll(steps, -1, axis=0)[i], steps[i])))
        for i in range(len(steps)-1)])
total_distance = np.sum(distances)
scaled_distances = distances / total_distance
label_distances = [np.sum(scaled_distances[:i]) for i in range(len(scaled_distances))] + [1]

path = np.zeros((npointstotal, 3))
current_point = 0
for i, step in enumerate(steps[:-1]):
    n_points=int(np.round(scaled_distances[i]*npointstotal, 0))
    new_point = current_point+n_points
    path[current_point:new_point] = np.linspace(step, steps[i+1], n_points)
    current_point += n_points

np.savetxt('kpts', path[:-1, :])
