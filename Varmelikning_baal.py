import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


iterasjonstid = 750

#Konstanter
avstand_fra_baal = 50 #oppgitt i meter
baaltemperatur = 500 #grader Celsius
utetemperatur = 15 #grader Celsius
alpha = 70 * 10**(-6) #Diffusivitet for luft ved 300 grader Celsius
delta_x = 0.1  #Posisjonssteg.
delta_y = delta_x


delta_t = (delta_x ** 2)/(4 * alpha)  #Tidssteg
delta_t = 1
gamma = (alpha * delta_t) / (delta_x ** 2)

# Initisjalbetingelser

u = np.empty((iterasjonstid, avstand_fra_baal, avstand_fra_baal)) #Tomt array for å lagre temperaturverdier

u.fill(utetemperatur) #Fyller arrayet med utetemperatur
u[:, (int(avstand_fra_baal / 2) - 3):(int(avstand_fra_baal / 2) + 3), (int(avstand_fra_baal / 2) - 3):(int(avstand_fra_baal / 2) + 3)] = baaltemperatur #Setter båltemperatur i midten av arrayet

def numerisk_løser(u):  #Bruker finite difference method på varmelikningen
    for k in range(0, iterasjonstid-1, 1):
        for i in range(1, avstand_fra_baal-1, 1):
            for j in range(1, avstand_fra_baal-1, 1):
                if(not (i in range(int(avstand_fra_baal / 2) - 3, int(avstand_fra_baal / 2) + 3) and j in range(int(avstand_fra_baal / 2) - 3, int(avstand_fra_baal / 2) + 3))): #Bålet holder konstant temperatur
                    u[k + 1, i, j] = gamma * (u[k][i+1][j] + u[k][i-1][j] + u[k][i][j+1] + u[k][i][j-1] - 4*u[k][i][j]) + u[k][i][j]
    return u

def plot_av_heatmap(u_t, t): #t er tidssteg
    plt.clf()
    
    plt.pcolormesh(u_t, cmap=plt.cm.jet, vmin=0, vmax=baaltemperatur)
    plt.colorbar(label="Temperatur (Celsius)")

    plt.title(f'Temperatur rundt bål ved tid t = {t*delta_t:.3f} sekunder')
    plt.xlabel('x (dm)')
    plt.ylabel('y (dm)')

    return plt

u = numerisk_løser(u) #Løser varmelikningen

def animasjon(t):
    plot_av_heatmap(u[t], t)

anim = animation.FuncAnimation(plt.figure(), animasjon, interval=1, frames=iterasjonstid, repeat=False)
anim.save("baalsimulasjon.gif")
