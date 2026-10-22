"""
Práctica 2: Sistema cardiovascular

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Mildred Angel Torales
Número de control: 23212731
Correo institucional: L23212731@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""

# Instalar librerias en consola
# pip install numpy control matplotlib

# Librerías
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import control as ctrl
import pandas as pd

# Datos de simulación
x0,t0,tend,dt,w,h = 0,0,15,1E-3,7,3.5
n = round((tend-t0)/dt)+1
t = np.linspace(t0,tend,n)

# Señal de entrada
from pathlib import Path
carpeta = Path(__file__).resolve().parent
u = np.array(pd.read_excel('C:/Users/Angel Torales/Documents/MATLAB/signal.xlsx',header=None))
u = np.reshape(signal.resample(u,len(t)),-1)

# Función de transferencia
def cardio(Z,C,R,L):
    num = [L*R,R*Z]
    den = [C*L*R*Z,L*R+L*Z,R*Z]
    sys = ctrl.tf(num,den)
    return sys

# Normotenso
Z,L,R,C = 0.010,0.001,1.00,1.500
sysnormo = cardio(Z,C,R,L)
print('Normotenso:',sysnormo)

# Hipotenso
Z,L,R,C = 0.010,0.001,1.00,3.500
syshipo = cardio(Z,C,R,L)
print('Hipotenso:',syshipo)

# Hipertenso
Z,L,R,C = 0.010,0.001,1.00,1.000
syshiper = cardio(Z,C,R,L)
print('Hipertenso:',syshiper)

# Respuestas en lazo abierto
_,PpN = ctrl.forced_response(sysnormo,t,u,x0)
_,PpL = ctrl.forced_response(syshipo,t,PpN,x0)
_,PpH = ctrl.forced_response(syshiper,t,PpN,x0)

# Colores
clr1 = np.array([247, 214, 208])/255
clr2 = np.array([226, 180, 189])/255
clr3 = np.array([62, 88, 121])/255

# Gráfica 1: Lazo abierto
fg1 = plt.figure(figsize=(w,h))
plt.plot(t,PpN,color=clr1,label='Normotenso')
plt.plot(t,PpL,color=clr2,label='Hipotenso')
plt.plot(t,PpH,color=clr3,label='Hipertenso')
plt.xlim(0,15)
plt.ylim(-0.6,1.4)
plt.xticks(np.arange(0,16,2))
plt.yticks(np.arange(-0.6,1.41,0.2))
plt.xlabel('t [s]')
plt.ylabel('Pp(t) [V]')
plt.legend(loc='upper center',bbox_to_anchor=(0.5,-0.10),ncol=3)
plt.tight_layout()
fg1.savefig(carpeta / 'individuos.png', dpi=300,bbox_inches='tight')

# Controlador PI
def controlador(kP,kI,kD,sys):
    Cr = 1E-6
    Re = 1/(kI*Cr)
    Rr = kP*Re
    numPI = [Rr*Cr,1]
    denPI = [Re*Cr,0]
    PI = ctrl.tf(numPI,denPI)
    X = ctrl.series(PI,sys)
    sysPI = ctrl.feedback(X,1)
    return sysPI

# Controladores
hipoPID = controlador(458.483,1112094.736,0.00627,syshipo)
print(f'Función de transferencia del hipotenso lazo cerrado: {hipoPID}')
hiperPID = controlador(126.595,293327.703,0.00140,syshiper)
print(f'Función de transferencia del hipertenso lazo cerrado: {hiperPID}')

# Respuestas con controlador
_,Pp3 = ctrl.forced_response(hipoPID,t,PpN,x0)
_,Pp4 = ctrl.forced_response(hiperPID,t,PpH,x0)

# Gráfica 2: Hipotenso con controlador
fg2 = plt.figure(figsize=(w,h))
plt.plot(t,PpN,color=clr1,label='Normotenso')
plt.plot(t,PpL,color=clr2,label='Hipotenso')
plt.plot(t,Pp3,':',color=clr3,label='PID: Hipotenso')
plt.xlim(0,15)
plt.ylim(-0.6,1.4)
plt.xticks(np.arange(0,16,2))
plt.yticks(np.arange(-0.6,1.41,0.2))
plt.xlabel('t [s]')
plt.ylabel('Pp(t) [V]')
plt.legend(loc='upper center',bbox_to_anchor=(0.5,-0.10),ncol=3)
plt.tight_layout()
fg2.savefig(carpeta / 'hipotenso.png',
            dpi=300,bbox_inches='tight')

# Gráfica 3: Hipertenso con controlador
fg3 = plt.figure(figsize=(w,h))
plt.plot(t,PpN,color=clr1,label='Normotenso')
plt.plot(t,PpH,color=clr2,label='Hipertenso')
plt.plot(t,Pp4,':',color=clr3,label='PID: Hipertenso')
plt.xlim(0,15)
plt.ylim(-0.6,1.4)
plt.xticks(np.arange(0,16,2))
plt.yticks(np.arange(-0.6,1.41,0.2))
plt.xlabel('t [s]')
plt.ylabel('Pp(t) [V]')
plt.legend(loc='upper center',bbox_to_anchor=(0.5,-0.10),ncol=3)
plt.tight_layout()
fg3.savefig(carpeta / 'hipertenso.png',
            dpi=300,bbox_inches='tight')

# Mostrar gráficas
plt.show()