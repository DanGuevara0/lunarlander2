# Lunar Lander
import math
from pygame import image, Color
import time
import subprocess,ast
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
start_time = time.time()
backgroundImage = image.load('images/background.png')
lander = Actor('lander',(400,45))
firsty = lander.y
lander.angle = lander.direction = 0
lander.thrust = 0
lander.thrustx = lander.thrusty = 0
gravity = 1.62
masanave = 0
lander.burn = speedDown = speedSide = gameState = gameTime = option = autom = 0
proba=0
counter = 0
lock = 0
dt= 0
pushforce=0
alt=3000

def fuzzycreate():
    global acceling
    altura = ctrl.Antecedent(np.arange(0, 3000, 1), 'altura')
    velocidad = ctrl.Antecedent(np.arange(0, 60, 1), 'velocidad')
    empuje = ctrl.Consequent(np.arange(0, 30000, 1), 'empuje')

    #altura
    altura['amp'] = fuzz.trapmf(altura.universe, [0,0,100,300])
    altura['ap'] = fuzz.trimf(altura.universe, [100, 300, 600])
    altura['am'] = fuzz.trimf(altura.universe, [300, 600, 1000 ])
    altura['ag'] = fuzz.trimf(altura.universe, [600, 1000, 2000])
    altura['amg'] = fuzz.trapmf(altura.universe, [1000, 2500, 3000,3000])
    #velocidad
    velocidad['vmp'] = fuzz.trapmf(velocidad.universe, [0,0,5,15])
    velocidad['vp'] = fuzz.trimf(velocidad.universe, [5, 15, 25])
    velocidad['vm'] = fuzz.trimf(velocidad.universe, [15, 25, 40])
    velocidad['vg'] = fuzz.trimf(velocidad.universe, [25, 40, 55])
    velocidad['vmg'] = fuzz.trapmf(velocidad.universe, [40, 55, 60,60])
    #empuje
    empuje['acmmp'] = fuzz.trimf(empuje.universe, [0,0,0])
    empuje['acmp'] = fuzz.trimf(empuje.universe, [0,5000,10000])
    empuje['acp'] = fuzz.trimf(empuje.universe, [5000, 10000, 15000])
    empuje['acm'] = fuzz.trimf(empuje.universe, [10000, 15000, 20000])
    empuje['acg'] = fuzz.trimf(empuje.universe, [15000, 20000, 25000])
    empuje['acmg'] = fuzz.trimf(empuje.universe, [20000,25000,30000])
    empuje['acmmg'] = fuzz.trimf(empuje.universe, [30000,30000,30000])

    rule1 = ctrl.Rule(altura['amg'] & velocidad['vmg'], empuje['acmmp'])
    rule2 = ctrl.Rule(altura['amg'] & velocidad['vg'], empuje['acmmp'])
    rule3 = ctrl.Rule(altura['amg'] & velocidad['vm'], empuje['acmmp'])
    rule4 = ctrl.Rule(altura['amg'] & velocidad['vp'], empuje['acmmp'])
    rule5 = ctrl.Rule(altura['amg'] & velocidad['vmp'], empuje['acmmp'])

    rule6 = ctrl.Rule(altura['ag'] & velocidad['vmg'], empuje['acmmp'])
    rule7 = ctrl.Rule(altura['ag'] & velocidad['vg'], empuje['acmmp'])
    rule8 = ctrl.Rule(altura['ag'] & velocidad['vm'], empuje['acmmp'])
    rule9 = ctrl.Rule(altura['ag'] & velocidad['vp'], empuje['acmmp'])
    rule10 = ctrl.Rule(altura['ag'] & velocidad['vmp'], empuje['acmmp'])

    rule11 = ctrl.Rule(altura['am'] & velocidad['vmg'], empuje['acg'])
    rule12 = ctrl.Rule(altura['am'] & velocidad['vg'], empuje['acm'])
    rule13 = ctrl.Rule(altura['am'] & velocidad['vm'], empuje['acm'])
    rule14 = ctrl.Rule(altura['am'] & velocidad['vp'], empuje['acm'])
    rule15 = ctrl.Rule(altura['am'] & velocidad['vmp'], empuje['acmmp'])

    rule16 = ctrl.Rule(altura['ap'] & velocidad['vmg'], empuje['acg'])
    rule17 = ctrl.Rule(altura['ap'] & velocidad['vg'], empuje['acg'])
    rule18 = ctrl.Rule(altura['ap'] & velocidad['vm'], empuje['acg'])
    rule19 = ctrl.Rule(altura['ap'] & velocidad['vp'], empuje['acm'])
    rule20 = ctrl.Rule(altura['ap'] & velocidad['vmp'], empuje['acmmp'])

    rule21 = ctrl.Rule(altura['amp'] & velocidad['vmg'], empuje['acmmg'])
    rule22 = ctrl.Rule(altura['amp'] & velocidad['vg'], empuje['acmg'])
    rule23 = ctrl.Rule(altura['amp'] & velocidad['vm'], empuje['acg'])
    rule24 = ctrl.Rule(altura['amp'] & velocidad['vp'], empuje['acm'])
    rule25 = ctrl.Rule(altura['amp'] & velocidad['vmp'], empuje['acmmp'])

    accel_ctrl = ctrl.ControlSystem([rule1, rule2, rule3,rule4,rule5,rule6,rule7,rule8,rule9,rule10,rule11,rule12,
                                 rule13,rule14,rule15,rule16,rule17,rule18,rule19,rule20,rule21,rule22,rule23,
                                 rule24,rule25])

    acceling = ctrl.ControlSystemSimulation(accel_ctrl)

fuzzycreate()

def draw():
    global gameTime
    if gameState == 0:
        screen.blit('background',(0,0))
        screen.blit('space',(0,0))
        screen.blit('title',(200,120))
        screen.draw.text("Flechas arriba y abajo para cambiar opcion", topleft=(10, 560), owidth=0.5, ocolor=(255,0,0), color=(255,255,0) , fontsize=25)
        screen.draw.text("Tecla A para seleccionar opcion", topleft=(10, 580), owidth=0.5, ocolor=(255,0,0), color=(255,255,0) , fontsize=25)
        if option==0:
            screen.draw.text("Inicio", topleft=(400, 300), owidth=0.5, ocolor=(255,255,0), color=(255,255,0) , fontsize=25)
            screen.draw.text("Salir", topleft=(400, 330), owidth=0.5, ocolor=(255,0,0), color=(255,255,0) , fontsize=25)
        if option==1:
            screen.draw.text("Inicio", topleft=(400, 300), owidth=0.5, ocolor=(255,0,0), color=(255,255,0) , fontsize=25)
            screen.draw.text("Salir", topleft=(400, 330), owidth=0.5, ocolor=(255,255,0), color=(255,255,0) , fontsize=25)    
    elif gameState == 5:
        screen.blit('background',(0,0))
        screen.blit('space',(0,0))
        screen.blit('title',(200,120))
        screen.draw.text("Flechas arriba y abajo para cambiar opcion", topleft=(10, 560), owidth=0.5, ocolor=(255,0,0), color=(255,255,0) , fontsize=25)
        screen.draw.text("Tecla A para seleccionar opcion", topleft=(10, 580), owidth=0.5, ocolor=(255,0,0), color=(255,255,0) , fontsize=25)
        if option==0:
            screen.draw.text("Manual", topleft=(400, 300), owidth=0.5, ocolor=(255,255,0), color=(255,255,0) , fontsize=25)
            screen.draw.text("Automatico", topleft=(400, 330), owidth=0.5, ocolor=(255,0,0), color=(255,255,0) , fontsize=25)
        if option==1:
            screen.draw.text("Manual", topleft=(400, 300), owidth=0.5, ocolor=(255,0,0), color=(255,255,0) , fontsize=25)
            screen.draw.text("Automatico", topleft=(400, 330), owidth=0.5, ocolor=(255,255,0), color=(255,255,0) , fontsize=25)
    elif gameState == 6:
        screen.draw.text("Flechas arriba y abajo para cambiar opcion", topleft=(10, 540), owidth=0.5, ocolor=(255,0,0), color=(255,255,0) , fontsize=25)
        screen.draw.text("Tecla A para seleccionar opcion", topleft=(10, 560), owidth=0.5, ocolor=(255,0,0), color=(255,255,0) , fontsize=25)
        if option==0:
            screen.draw.text("Continuar", topleft=(400, 300), owidth=0.5, ocolor=(255,255,0), color=(255,255,0) , fontsize=25)
            screen.draw.text("Volver al menu inicial", topleft=(400, 330), owidth=0.5, ocolor=(255,0,0), color=(255,255,0) , fontsize=25)
        if option==1:
            screen.draw.text("Continuar", topleft=(400, 300), owidth=0.5, ocolor=(255,0,0), color=(255,255,0) , fontsize=25)
            screen.draw.text("Volver al menu inicial", topleft=(400, 330), owidth=0.5, ocolor=(255,255,0), color=(255,255,0) , fontsize=25)        
    else:
        screen.blit('background',(0,0))
        screen.blit('space',(0,0))
        r = lander.angle
        if(lander.burn > 0):
            lander.image = "landerburn"
        else:
            lander.image = "lander"
        lander.angle = r
        lander.draw()
        screen.draw.text("Altitud : "+ str(round(alt))+ " m", topleft=(650, 10), owidth=0.5, ocolor=(255,0,0), color=(255,255,0) , fontsize=25)
        screen.draw.text("Tiempo : "+ str(round(gameTime,2))+" s", topleft=(10, 10), owidth=0.5, ocolor=(255,0,0), color=(255,255,0) , fontsize=25)
        screen.draw.text("Vel. Bajada : "+ str(round(speedDown,2))+ " m/s", topleft=(10,30), owidth=0.5, ocolor=(255,0,0), color=(255,255,0) , fontsize=25)
        screen.draw.text("Acel. empuje: "+ str(round(proba,2))+ " m/s", topleft=(10, 50), owidth=0.5, ocolor=(255,0,0), color=(255,255,0) , fontsize=25)
        screen.draw.text("masanave : "+ str(round(masanave,2))+ " Kg", topleft=(10, 70), owidth=0.5, ocolor=(255,0,0), color=(255,255,0) , fontsize=25)
        screen.draw.text("Empuje : "+ str(round(pushforce,2))+ " N", topleft=(10, 90), owidth=0.5, ocolor=(255,0,0), color=(255,255,0) , fontsize=25)
        screen.draw.text( "presione P para menu de pausa :", topleft=(10, 580), owidth=0.5, ocolor=(255,0,0), color=(255,255,0) , fontsize=25)
        if autom == 0:
            screen.draw.text("presione flechas izq y der para variar empuje ", topleft=(10, 540), owidth=0.5, ocolor=(255,0,0), color=(255,255,0) , fontsize=25)
            screen.draw.text("presione flecha arriba para aplicar empuje ", topleft=(10, 560), owidth=0.5, ocolor=(255,0,0), color=(255,255,0) , fontsize=25)
        if gameState == 1:
            gameTime=gameTime
        if gameState == 2:
            screen.draw.text("Felicitaciones \nLa nave ha alunizado con exito", center=(400, 50), owidth=0.5, ocolor=(255,0,0), color=(255,255,0) , fontsize=35)
            screen.draw.text("Presione p\npara volver al menu principal", center=(400, 100), owidth=0.5, ocolor=(255,0,0), color=(255,255,0) , fontsize=35)        
        if gameState == 3:
            screen.draw.text("La nave se ha estrellado", center=(400, 50), owidth=0.5, ocolor=(255,0,0), color=(255,255,0) , fontsize=35)
            screen.draw.text("Presione p\npara volver al menu principal", center=(400, 100), owidth=0.5, ocolor=(255,0,0), color=(255,255,0) , fontsize=35)
        if gameState == 4:
            screen.draw.text("La nave se fue a la deriva", center=(400, 50), owidth=0.5, ocolor=(255,0,0), color=(255,255,0) , fontsize=35)    
            screen.draw.text("Presione p\npara volver al menu principal", center=(400, 100), owidth=0.5, ocolor=(255,0,0), color=(255,255,0) , fontsize=35)

def update(dt):
    global gameState, speedDown, speedSide, option, counter, lock, proba, autom, gameTime,masanave, pushforce,alt
    proba= lander.thrust
    if gameState == 0: # menu principal
        if counter > 0.4:
            counter = 0
            lock = 0
        counter += dt
        if keyboard.up:
            if option == 0 and lock==0:
                option = 1
                lock = 1
            elif option == 1 and lock==0:
                option = 0
                lock = 1
        if keyboard.down:
            if option == 0 and lock==0:
                option = 1
                lock = 1
            elif option == 1 and lock==0:
                option = 0
                lock = 1
        if keyboard.a:
            if option == 0 and lock==0: 
                counter=0
                lock=1
                lander.x = 400
                lander.y = 45
                masanave = 3900
                speedDown= 0
                alt = (getAlt()) 
                gameState = 5
            elif option == 1 and lock==0:
                quit()
    if gameState == 5: # automatico o manual
        if counter > 0.4:
            counter = 0
            lock = 0
        counter += dt
        if keyboard.up:
            if option == 0 and lock==0:
                option = 1
                lock = 1
            elif option == 1 and lock==0:
                option = 0
                lock = 1
        if keyboard.down:
            if option == 0 and lock==0:
                option = 1
                lock = 1
            elif option == 1 and lock==0:
                option = 0
                lock = 1
        if keyboard.a and lock==0:
            if option == 0:
                gameTime=0
                autom = 0 
                gameState = 1
            elif option == 1:
                gameTime=0
                autom = 1 
                gameState = 1
    if gameState == 6: # menu pausa
        if counter > 0.4:
            counter = 0
            lock = 0
        counter += dt
        if keyboard.up:
            if option == 0 and lock==0:
                option = 1
                lock = 1
            elif option == 1 and lock==0:
                option = 0
                lock = 1
        if keyboard.down:
            if option == 0 and lock==0:
                option = 1
                lock = 1
            elif option == 1 and lock==0:
                option = 0
                lock = 1
        if keyboard.a and lock==0:
            if option == 0: 
                gameState = 1
            elif option == 1:
                counter=0
                lock=1
                gameState = 0
    if gameState == 3 or gameState == 2 or gameState == 4:
        if keyboard.p:
            gameState = 0
    if gameState == 1:
        gameTime += dt
        if autom == 1:
            if masanave>3899:
                pushforce = fuzzyControl(alt, round(speedDown,2))
                lander.thrust = pushforce / masanave
            else: 
                lander.thrust = 0    
            if lander.thrust > 0:
                lander.burn = 1
            else:
                lander.burn = 0    
        else:
            if keyboard.up:
                if masanave>3899 and pushforce>0:
                    lander.thrust = pushforce/masanave
                    lander.burn = 1
                else:
                    lander.thrust = 0
                    lander.burn = 0 
            else: 
                lander.thrust = 0
                lander.burn = 0
            if keyboard.left:
                if pushforce>0:
                    pushforce -= 1000
                else:
                    pushforce = pushforce     
            if keyboard.right:
                if pushforce<30000:
                    pushforce += 1000
                else:
                    pushforce = pushforce    
        if keyboard.p:
            gameState = 6
        lander.thrustx = lander.thrust*math.cos(math.radians(90-lander.direction))
        lander.thrusty = lander.thrust*math.sin(math.radians(90-lander.direction)) 
        speedSide -= ((lander.thrustx))*dt
        lander.x += speedSide*dt/10  # factor de conversion 1 pixel son 10 metros 
        speedDown += ((gravity-lander.thrusty))*dt
        lander.y += speedDown*dt/10  # factor de conversion 1 pixel son 10 metros
        alt -= speedDown*dt
        if speedDown < 6 and getAlt() == 0:
            lander.thrust = 0
            lander.burn = 0
            gameState = 2
        elif getAlt() == 0:
            gameState = 3
        elif lander.center[0]>800 or lander.center[0]<0 or lander.center[1]>600 or lander.center[1]<0:
            gameState = 4      

def getAlt():
    testY = lander.y+8
    height = 0
    while testPixel((int(lander.x),int(testY))) == Color('black') and height < 6000:
        testY += 1
        height += 10
    return height

def testPixel(xy):
    if xy[0] >= 0 and xy[0] < 800 and xy[1] >= 0 and xy[1] < 600:
        return backgroundImage.get_at(xy)
    else:
        return Color('black')

def fuzzyControl(height, speed):
    acceling.input['altura'] = height
    acceling.input['velocidad'] = speed
    acceling.compute()
    return float(acceling.output['empuje'])
