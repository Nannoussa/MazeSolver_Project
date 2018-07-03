import sys
import png
# import imageResize
from PIL import Image
import numpy as np
import pydip as dip
#from scipy import ndimage
#from scipy.ndimage import label
from skimage.measure import label, regionprops

def start_goal_positions():
# Starting with your `path_pixels` image:
    path_image = Image.open(sys.argv[1])
    #img =  np.array(path_pixels)   # convert to NumPy array by copy (so we don't modify original)
    copy_image = path_image.copy()
    # img = Image(img)         # convert to PyDIP image (no copy made)
    img = copy_image == 255              # binarize, path is True/1
    #img = ndimage.Any(img, process=[False,False,True]) # if this is a color image, remove color dimension
    greyscale_image = copy_image.convert('L') # if this is a color image, convert it to grey scale image(black and white)
    greyscale_image.show()
    greyscale_image[1:-2,1:-2] = 0            # set image interior to 0, leaving only outer path
    label_image = label(greyscale_image)          # do connected component analysis -- should result in two regions
    centroid_image = regionprops(label_image) # find centroids for regions
    #m = dip.MeasurementTool.Measure(img,features=['Center']) # find centroids for regions
    start = m[1]['Center']      # randomly pick first region as start point
    goal = m[2] ['Center']    # ... and second region as goal point
    return start,goal

def AStar(start, goal, neighbor_nodes, distance, cost_estimate):
    def reconstruct_path(came_from, current_node):
        path = []
        while current_node is not None:
            path.append(current_node)
            current_node = came_from[current_node]
        return list(reversed(path))
    g_score = {start: 0}
    f_score = {start: g_score[start] + cost_estimate(start, goal)}
    openset = {start}
    closedset = set()
    came_from = {start: None}
    while openset:
        current = min(openset, key=lambda x: f_score[x])
        if current == goal:
            return reconstruct_path(came_from, goal)
        openset.remove(current)
        closedset.add(current)
        for neighbor in neighbor_nodes(current):
            if neighbor in closedset:
                continue
            if neighbor not in openset:
                openset.add(neighbor)
            tentative_g_score = g_score[current] + distance(current, neighbor)
            if tentative_g_score >= g_score.get(neighbor, float('inf')):
                continue
            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            f_score[neighbor] = tentative_g_score + cost_estimate(neighbor, goal)
    return []
def is_blocked(p):
    x,y = p
    pixel = path_pixels[x,y]
    if any(c < 225 for c in pixel):
        return True
def von_neumann_neighbors(p):
    x, y = p
    neighbors = [(x-1, y), (x, y-1), (x+1, y), (x, y+1)]
    return [p for p in neighbors if not is_blocked(p)]
def manhattan(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])
def squared_euclidean(p1, p2):
    return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2
# start = (400, 984)
# goal = (398, 25)



start = start_goal_positions().start
goal = start_goal_positions().goal

path_img = Image.open(sys.argv[1])
path_pixels = path_img.load()
distance = manhattan
heuristic = manhattan
path = AStar(start, goal, von_neumann_neighbors, distance, heuristic)
for position in path:
    x,y = position
    path_pixels[x,y] = (255,0,0) # the solution color path is red
path_img.save(sys.argv[2])