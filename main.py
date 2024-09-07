import cv2
import mediapipe as mp
import comandos as cm
from math import sqrt
import time
from comandos import Mao

lastR= 0x25
lastL= 0x25
def reta(x1, x2, y1, y2):
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

video = cv2.VideoCapture(0)
hand = mp.solutions.hands
Hand = hand.Hands(max_num_hands=2)


mpDraw= mp.solutions.drawing_utils

while(True):
    check, img = video.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results =Hand.process(imgRGB)

    handPoints = results.multi_hand_landmarks
    h, w, _ =img.shape
    pontosEsq =[]
    pontosDir = []
    dedos =[4,8,16,20]
    if handPoints:
        for idx,points in enumerate(handPoints):
            hand_label = results.multi_handedness[idx].classification[0].label
            hand_index = "Esquerda" if hand_label == "Left" else "Direita"

            mpDraw.draw_landmarks(img, points, hand.HAND_CONNECTIONS)
            for id, cord in enumerate(points.landmark):
                cx, cy = int(cord.x * w), int(cord.y * h)
                #cv2.putText(img, str(id), (cx, cy+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0),2)
                if hand_index=="Esquerda":
                    pontosEsq.append((cx,cy))
                else:
                    pontosDir.append((cx,cy))    

            maoDir =["","","","",""]
            if len(pontosDir)>=20:
                for x in dedos:
                    polegar = reta(pontosDir[4][0],pontosDir[6][0],pontosDir[4][1],pontosDir[6][1])
                    polegRef =reta(pontosDir[4][0],pontosDir[2][0],pontosDir[4][1],pontosDir[2][1])
                    if polegar>polegRef:
                        maoDir[0]=True
                    else:
                        maoDir[1]=False
                    indicador =reta(pontosDir[0][0],pontosDir[8][0],pontosDir[0][1],pontosDir[8][1])
                    indRef=reta(pontosDir[0][0],pontosDir[6][0],pontosDir[0][1],pontosDir[6][1])
                    if indicador>indRef:
                        maoDir[1]=True
                    else:
                        maoDir[1]=False

                    meio =reta(pontosDir[0][0],pontosDir[12][0],pontosDir[0][1],pontosDir[12][1])
                    meioRef = reta(pontosDir[0][0],pontosDir[10][0],pontosDir[0][1],pontosDir[10][1])
                    if meio>meioRef:
                        maoDir[2]=True
                    else:
                        maoDir[2]=False

                    anelar =reta(pontosDir[0][0],pontosDir[16][0],pontosDir[0][1],pontosDir[16][1])
                    anelRef= reta(pontosDir[0][0],pontosDir[14][0],pontosDir[0][1],pontosDir[14][1])
                    if anelar>anelRef:
                        maoDir[3] =True
                    else:
                        maoDir[3]=False

                    mindin =reta(pontosDir[0][0],pontosDir[20][0],pontosDir[0][1],pontosDir[20][1])
                    minRef= reta(pontosDir[0][0],pontosDir[18][0],pontosDir[0][1],pontosDir[18][1])
                    if mindin>minRef:
                        maoDir[4]=True
                    else:
                        maoDir[4]=False
                    
                    #print(f"Direita: {maoDir}")

            direita = Mao(maoDir, pontosDir, "Dir")

            maoEsq =["","","","",""]
            if len(pontosEsq)>=20:
                maoEsq =[False,False,False, False,False]
                for x in dedos:
                    polegar = reta(pontosEsq[4][0],pontosEsq[6][0],pontosEsq[4][1],pontosEsq[6][1])
                    polegRef =reta(pontosEsq[4][0],pontosEsq[2][0],pontosEsq[4][1],pontosEsq[2][1])
                    if polegar>polegRef:
                        maoEsq[0]=True
                    else:
                        maoEsq[1]=False
                    indicador =reta(pontosEsq[0][0],pontosEsq[8][0],pontosEsq[0][1],pontosEsq[8][1])
                    indRef=reta(pontosEsq[0][0],pontosEsq[6][0],pontosEsq[0][1],pontosEsq[6][1])
                    if indicador>indRef:
                        maoEsq[1]=True
                    else:
                        maoEsq[1]=False

                    meio =reta(pontosEsq[0][0],pontosEsq[12][0],pontosEsq[0][1],pontosEsq[12][1])
                    meioRef = reta(pontosEsq[0][0],pontosEsq[10][0],pontosEsq[0][1],pontosEsq[10][1])
                    if meio>meioRef:
                        maoEsq[2]=True
                    else:
                        maoEsq[2]=False

                    anelar =reta(pontosEsq[0][0],pontosEsq[16][0],pontosEsq[0][1],pontosEsq[16][1])
                    anelRef= reta(pontosEsq[0][0],pontosEsq[14][0],pontosEsq[0][1],pontosEsq[14][1])
                    if anelar>anelRef:
                        maoEsq[3] =True
                    else:
                        maoEsq[3]=False

                    mindin =reta(pontosEsq[0][0],pontosEsq[20][0],pontosEsq[0][1],pontosEsq[20][1])
                    minRef= reta(pontosEsq[0][0],pontosEsq[18][0],pontosEsq[0][1],pontosEsq[18][1])
                    if mindin>minRef:
                        maoEsq[4]=True
                    else:
                        maoEsq[4]=False
                    
                    #print(f"Esquerda: {maoEsq}")
            
            esquerda = Mao(maoEsq, pontosEsq, "Esq")
            
            cm.checa_comandos(esquerda, direita,lastL,lastR)
            lastL= esquerda.comando
            lastR= direita.comando
            #print(f"{direita}\n{esquerda}")
            time.sleep(0.12)

            
    #cv2.imshow("Video", img)
    cv2.waitKey(1)
