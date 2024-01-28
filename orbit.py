import numpy as np
import datetime as dt
import math as m

# Earth orbit parameters
mu = 398600.4418
r = 6400 #6781
D = 24*0.997269

# Maths for getting orbit paths from tles
# https://python.plainenglish.io/plot-satellites-real-time-orbits-with-python-s-matplotlib-3c7ccd737638
def get_orbit(data):
    orbit_data = {'x': [], 'y': [], 'z': []}
    for i in range(len(data)//2):
        if data[i*2][0] != "1":
            print("Wrong TLE format at line "+str(i*2)+". Lines ignored.")
            continue
        if int(data[i*2][18:20]) > int(dt.date.today().year%100):
            orb = {"t":dt.datetime.strptime("19"+data[i*2][18:20]+" "+data[i*2][20:23]+" "+str(int(24*float(data[i*2][23:33])//1))+" "+str(int(((24*float(data[i*2][23:33])%1)*60)//1))+" "+str(int((((24*float(data[i*2][23:33])%1)*60)%1)//1)), "%Y %j %H %M %S")}
        else:
            orb = {"t":dt.datetime.strptime("20"+data[i*2][18:20]+" "+data[i*2][20:23]+" "+str(int(24*float(data[i*2][23:33])//1))+" "+str(int(((24*float(data[i*2][23:33])%1)*60)//1))+" "+str(int((((24*float(data[i*2][23:33])%1)*60)%1)//1)), "%Y %j %H %M %S")}
            orb.update({"name":data[i*2+1][2:7],"e":float("."+data[i*2+1][26:34]),"a":(mu/((2*m.pi*float(data[i*2+1][52:63])/(D*3600))**2))**(1./3),"i":float(data[i*2+1][9:17])*m.pi/180,"RAAN":float(data[i*2+1][17:26])*m.pi/180,"omega":float(data[i*2+1][34:43])*m.pi/180})
            orb.update({"b":orb["a"]*m.sqrt(1-orb["e"]**2),"c":orb["a"]*orb["e"]})
            R = np.matmul(np.array([[m.cos(orb["RAAN"]),-m.sin(orb["RAAN"]),0],[m.sin(orb["RAAN"]),m.cos(orb["RAAN"]),0],[0,0,1]]),(np.array([[1,0,0],[0,m.cos(orb["i"]),-m.sin(orb["i"])],[0,m.sin(orb["i"]),m.cos(orb["i"])]])))
            R = np.matmul(R,np.array([[m.cos(orb["omega"]),-m.sin(orb["omega"]),0],[m.sin(orb["omega"]),m.cos(orb["omega"]),0],[0,0,1]]))
        for i in np.linspace(0,2*m.pi,100):
            P = np.matmul(R,np.array([[orb["a"]*m.cos(i)],[orb["b"]*m.sin(i)],[0]]))-np.matmul(R,np.array([[orb["c"]],[0],[0]]))
            orbit_data['x'].append(P[0][0])
            orbit_data['y'].append(P[1][0])
            orbit_data['z'].append(P[2][0])
    return orbit_data

def plot_earth(fig):
    uu, vv = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    xx = r * np.cos(uu) * np.sin(vv)
    yy = r * np.sin(uu) * np.sin(vv)
    zz = r * np.cos(vv)

    fig.add_surface(x=xx, y=yy, z=zz, showscale=False)
    fig.update(layout_coloraxis_showscale=False)