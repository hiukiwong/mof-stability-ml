import numpy as np
import matplotlib.pyplot as plt

def readcontour(input_dat_file): 
    #top and bottom surface dats
    fh = open(input_dat_file)
    lines = fh.readlines()
    fh.close()

    val = 0

# Create 3D space and fill it with zeros
# Find min and max x,y values, plus spacing
    zdata = []
    xmin = +999.0
    xmax = -999.0
    ymin = +999.0
    ymax = -999.0
    for i in range(len(lines)):
        fields = lines[i].split()
        if len(fields) == 3:
           zdata.append(float(fields[2]))
           val = val+1
           if float(fields[0])<xmin:
              xmin = float(fields[0])
           if float(fields[0])>xmax:
              xmax = float(fields[0])
           if float(fields[1])<ymin:
              ymin = float(fields[1])
           if float(fields[1])>ymax:
              ymax = float(fields[1])
    d = int(np.sqrt(val))
    x = np.zeros(d, float)
    y = np.zeros(d, float)
    z = np.zeros((d,d), float)
    grid_mesh = float((xmax-xmin)/(d-1))

#Setting grid mesh values here 
    for i in range(0, d, 1):
        x[i]= xmin+i*grid_mesh
        y[i]= ymin+i*grid_mesh
    c = 0
    for i in range(0, d, 1):
        for j in range(0, d, 1):
            z[j,i] = zdata[c]
            c = c+1

    return(x, y, z, xmin, xmax)

# Main program below

# Read z(x,y) file and  fill the levels
(cx, cy, cz, xmin, xmax) = readcontour("py2sambvca_input-TopSurface.dat")
spacing = 0.25
levels = np.arange(xmin, xmax+0.001, spacing)

plt.figure()
cset1 = plt.contourf(cx, cy, cz, levels, cmap=plt.get_cmap('jet', len(levels)-1),)
cset2 = plt.contour(cx, cy, cz, cset1.levels, colors = 'k', hold='on')
for c in cset2.collections:
    c.set_linestyle('solid')

plt.colorbar(cset1)
plt.show()

out_filename="coloured_plt"
plt.savefig(out_filename+".jpg")

print(f"Info: PNG map image in file {out_filename}.jpg")