from PIL import Image, ImageDraw, ImageFont
import json
import datetime

number = 1
nameH = "ฮานอยกาชาด"

A=5
B=3
ARR1 = [51,58,52]
ARR2 = [39,31,36]
ARR3 = [431,451,453]

def draw_name(draw,pos,name,text_color,font,aligb,stroke_width,stroke_fill):
    draw.text(pos,name,fill=text_color, font=font, align=aligb, stroke_width=stroke_width, stroke_fill=stroke_fill)
    

def draw_line_name(x,y,text_width,text_height,line_color,widths):
    line_start = (x-20, y + text_height)  
    line_end = (x + text_width+20, y + text_height) 
    draw.line([line_start, line_end], fill=line_color, width=widths)



with open('Datausers.json', mode='r') as my_file:
    data = json.load(my_file)

found = False 

for user_data in data:
    if int(number) == int(user_data['cid']):
        found = True
        break 

if not found:
    print(False)
else:
    img = Image.open(user_data['imglocal'])
    draw = ImageDraw.Draw(img)
    
    current_date = datetime.datetime.now()
    formatted_date = current_date.strftime("%d/%m/%Y")
    
    fontname = ImageFont.truetype(user_data['font1'], size=70)  
    fonttime = ImageFont.truetype(user_data['font1'], size=45)
    fontNUMMAIN = ImageFont.truetype(user_data['font1'], size=150)  
    fontARR1 = ImageFont.truetype(user_data['font1'], size=90)  
    fontARR3 = ImageFont.truetype(user_data['font1'], size=54)  


    def create_image(message, font):
        _, _, w, h = draw.textbbox((0, 0), message, font=font)
        return w,h
    
    text_width, text_height = create_image(nameH, fontname)
    time_width, time_height = create_image(formatted_date, fonttime)

    text_color = (253, 205, 0)
    outline_color = (0, 0, 0)    
    line_color = (255, 255, 255) 

    positionname = ((img.width - text_width) // 2, 75)
    positiontime = ((img.width - time_width) // 2, 185)

    draw_name(draw,positionname,nameH,(253, 205, 0),fontname,"center",5,(0, 0, 0))
    draw_line_name(((img.width - text_width) // 2),50,text_width,text_height,line_color,5)
    
    draw_name(draw,positiontime,formatted_date,(255, 255, 255),fonttime,"center",3,(0, 0, 0))

    draw.text((200,380),str(A)+"-"+str(B),fill=(255, 255, 255) , font=fontNUMMAIN, align="center", stroke_width=10, stroke_fill=(0,0,0))

    for index, element in enumerate(ARR1):
        draw.text((610,(280+(index*130))),str(element),fill=(255, 255, 255) , font=fontARR1, align="center", stroke_width=5, stroke_fill=(0,0,0))
    
    for index, element in enumerate(ARR2):
        draw.text((820,(280+(index*130))),str(element),fill=(255, 255, 255) , font=fontARR1, align="center", stroke_width=5, stroke_fill=(0,0,0))

    for index, element in enumerate(ARR3):
        draw.text((120+(index*140),650),str(element),fill=(255, 255, 255) , font=fontARR3, align="center", stroke_width=5, stroke_fill=(0,0,0))
    



    img.show()



