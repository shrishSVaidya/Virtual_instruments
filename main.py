import cv2
import matplotlib.pyplot as plt
import numpy as np
from pygame import mixer

c_note_top=[88, 163]
c_note_btm=[144, 236]

d_note_top=[88, 240]
d_note_btm=[144, 313]

e_note_top=[88, 318]
e_note_btm=[144, 390]

f_note_top=[88, 392]
f_note_btm=[144, 468]

g_note_top=[88, 470]
g_note_btm=[144, 545]

a_note_top=[88, 548]
a_note_btm=[144, 619]

b_note_top=[88, 624]
b_note_btm=[144, 696]


csharp_note_top=[0, 211]
csharp_note_btm=[85, 260]

dsharp_note_top=[0, 287]
dsharp_note_btm=[85, 335]

fsharp_note_top=[0, 441]
fsharp_note_btm=[85, 492]

gsharp_note_top=[0, 519]
gsharp_note_btm=[85, 568]

asharp_note_top=[0, 594]
asharp_note_btm=[85, 645]



drum_top=[145, 730]
drum_btm=[245, 830]

hat_top=[145, 30]
hat_btm=[245, 130]

cap=cv2.VideoCapture(0)
cap.set(3, 750)

y=100

mixer.init()
csharp=mixer.Sound('./notes/c#.mp3')
dsharp=mixer.Sound('./notes/d#.mp3')
fsharp=mixer.Sound('./notes/f#.mp3')
gsharp=mixer.Sound('./notes/g#.mp3')
asharp=mixer.Sound('./notes/a#.mp3')

c=mixer.Sound('./notes/c.mp3')
d=mixer.Sound('./notes/d.mp3')
e=mixer.Sound('./notes/e.mp3')
f=mixer.Sound('./notes/f.mp3')
g=mixer.Sound('./notes/g.mp3')
a=mixer.Sound('./notes/a.mp3')
b=mixer.Sound('./notes/b.mp3')

drum=mixer.Sound('./notes/drum.mp3')
hat=mixer.Sound('./notes/hat.mp3')

sounds=[csharp, dsharp, fsharp, gsharp, asharp, c, d, e, f, g, a, b, drum, hat]
# c_note = mixer.Sound('./sounds/high_hat_1.ogg')
# c_note.play()

def divide_region(frame):
    c_region=frame[c_note_top[0]:c_note_btm[0], c_note_top[1]:c_note_btm[1]]
    d_region=frame[d_note_top[0]:d_note_btm[0], d_note_top[1]:d_note_btm[1]]
    e_region=frame[e_note_top[0]:e_note_btm[0], e_note_top[1]:e_note_btm[1]]
    f_region=frame[f_note_top[0]:f_note_btm[0], f_note_top[1]:f_note_btm[1]]
    g_region=frame[g_note_top[0]:g_note_btm[0], g_note_top[1]:g_note_btm[1]]
    a_region=frame[a_note_top[0]:a_note_btm[0], a_note_top[1]:a_note_btm[1]]
    b_region=frame[b_note_top[0]:b_note_btm[0], b_note_top[1]:b_note_btm[1]]

    #index=5
    csharp_region=frame[csharp_note_top[0]:csharp_note_btm[0], csharp_note_top[1]:csharp_note_btm[1]]
    dsharp_region=frame[dsharp_note_top[0]:dsharp_note_btm[0], dsharp_note_top[1]:dsharp_note_btm[1]]
    fsharp_region=frame[fsharp_note_top[0]:fsharp_note_btm[0], fsharp_note_top[1]:fsharp_note_btm[1]]
    gsharp_region=frame[gsharp_note_top[0]:gsharp_note_btm[0], gsharp_note_top[1]:gsharp_note_btm[1]]
    asharp_region=frame[asharp_note_top[0]:asharp_note_btm[0], asharp_note_top[1]:asharp_note_btm[1]]

    drum_region=frame[drum_top[0]:drum_btm[0], drum_top[1]:drum_btm[1]]
    hat_region=frame[hat_top[0]:hat_btm[0], hat_top[1]:hat_btm[1]]

    regions=[csharp_region, dsharp_region, fsharp_region, gsharp_region, asharp_region, c_region, d_region, e_region, f_region, g_region, a_region, b_region, drum_region, hat_region]
    region_sum=[]
    for region in regions:
        hsvim=cv2.cvtColor(region, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsvim, np.array([2,0,20]), np.array([20, 255, 255]))

        kernel=np.ones((5,5))

        dilate=cv2.dilate(mask, kernel, iterations=1)
        erode=cv2.erode(dilate, kernel, iterations=1)

        skiney=np.sum(erode)//10000
        region_sum.append(skiney)
    
    return region_sum



def detect_n_play_note(frame):
    reg_sum=divide_region(frame)
    i=0
    global y
    c=0
    N=len(reg_sum)
    for i in range(N-2):
        if reg_sum[i]>25:
            if y!=i:
                sounds[i].play()
                y=i
        if reg_sum[N-2]>20:
            sounds[N-2].play()
        if reg_sum[N-1]>20:
            sounds[N-1].play()
            

img= cv2.imread("keyboard.jpeg")
img=cv2.resize(img, (540, 150), interpolation=cv2.INTER_AREA)

img_drum=cv2.imread("drum.jpg")
img_drum=cv2.resize(img_drum, (100, 100), interpolation=cv2.INTER_AREA)

img_hat=cv2.imread("hat.jpg")
img_hat=cv2.resize(img_hat, (100, 100), interpolation=cv2.INTER_AREA)

while True:
    rt, frame=cap.read()
    imgexp=frame.copy()
   
    imgexp[0:150, 160:700]=img
    imgexp[145:245, 30:130]=img_hat
    imgexp[145:245, 730:830]=img_drum

    detect_n_play_note(frame)

    cv2.imshow("output", imgexp)
    

    if cv2.waitKey(1)==13:
        break

cap.release()
cv2.destroyAllWindows()