from Maze import Maze
import tkinter as tk
import pandas as pd
import time

if __name__ == "__main__":
    sizes = [5, 10, 20, 30, 40]

    data = {
        'Method': [],
        'Time': [],
        'Visited': [],
        'Size': []
    }

    for size in sizes:
        root = None
        path = None
        while path == None:
            if root != None:
                root.destroy()
            root = tk.Tk()
            app = Maze(size, size, root)

            start = time.time()
            path, visited = app.dfs()
            end = time.time()

        data['Method'].append('DFS')
        data['Time'].append(end - start)
        data['Visited'].append(len(visited))
        data['Size'] = size


        start = time.time()
        path, visited = app.bfs()
        end = time.time()

        data['Method'].append('BFS')
        data['Time'].append(end - start)
        data['Visited'].append(len(visited))
        data['Size'] = size
        
        start = time.time()
        path, visited = app.a_star_manhattan()
        end = time.time()

        data['Method'].append('MANHATTAN')
        data['Time'].append(end - start)
        data['Visited'].append(len(visited))
        data['Size'] = size

        start = time.time()
        path, visited = app.a_start_euclidean()
        end = time.time()

        data['Method'].append('EUCLIDEAN')
        data['Time'].append(end - start)
        data['Visited'].append(len(visited))
        data['Size'] = size

    df = pd.DataFrame(data)

    df.to_csv('result.csv', index=False)
