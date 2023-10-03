from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse,FileResponse
import datetime
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import json
import urllib.parse
import requests
import random



app = FastAPI()

# Configure CORS
origins = ["*"]  # You can specify the allowed origins here, e.g., ["http://localhost", "https://example.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],  
    # allow_origins=["https://web-m6-v2.vercel.app/"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

global A
global B
global ARR1
global ARR2
global ARR3


def draw_name(draw,pos,name,text_color,font,aligb,stroke_width,stroke_fill):
    draw.text(pos,name,fill=text_color, font=font, align=aligb, stroke_width=stroke_width, stroke_fill=stroke_fill)
    

def draw_line_name(draw,x,y,text_width,text_height,line_color,widths):
    line_start = (x-20, y + text_height)  
    line_end = (x + text_width+20, y + text_height) 
    draw.line([line_start, line_end], fill=line_color, width=widths)

def get_random_number(min_value, max_value, previous=None):
    num = random.randint(min_value, max_value)
    while num == previous:
        num = random.randint(min_value, max_value)
    return num

def get_random_numbers_with_exclusion(number, num2):
    num = int(number)
    result = []
    all_numbers = list(range(1, 10))  # 1-9

    # Remove num2 and num from available numbers
    available_numbers = [n for n in all_numbers if n != int(num2) and n != int(number)]

    shuffled_numbers = random.sample(available_numbers, 3)  # Shuffle and take first 2

    result = [str(num * 10 + n).zfill(2) for n in shuffled_numbers]

    return result


def array3index(num1, num2, arr1, arr2):
    result = []
    ran = random.randint(0, 2)
    number_index = get_random_unique_number(num1, num2)
    num_index_one = str(number_index)
    num_main = str(num1) + str(num2)
    
    if ran == 0:
        temp1 = random.randint(0, 2)
        ins = get_random_unique_number_oune(temp1)
        result = [
            num_index_one + arr1[ins],
            num_index_one + arr1[temp1],
            num_index_one + num_main
        ]
    elif ran == 1:
        temp1 = random.randint(0, 2)
        ins = get_random_unique_number_oune(temp1)
        result = [
            num_index_one + arr2[temp1],
            num_index_one + arr2[ins],
            num_index_one + num_main
        ]
    else:
        temp1 = random.randint(0, 2)
        ins = get_random_unique_number_oune(temp1)
        result = [
            num_index_one + arr2[random.randint(0, 2)],
            num_index_one + arr1[ins],
            num_index_one + num_main
        ]
    
    return result

def get_random_unique_number(first_number, second_number):
    available_numbers = list(range(10))  # สร้างรายการ [0, 1, ..., 9]
    available_numbers.remove(first_number)
    available_numbers.remove(second_number)
    random_unique_number = random.choice(available_numbers)
    return random_unique_number

def get_random_unique_number_oune(input_number):
    available_numbers = [0, 1, 2]
    available_numbers.remove(input_number)
    random_unique_number = random.choice(available_numbers)
    return random_unique_number


def RANDOMNUMBER():
    
    global A,B,ARR1,ARR2,ARR3
    random_num1 = get_random_number(0, 9)
    random_num2 = get_random_number(0, 9, random_num1)

    arr1 = get_random_numbers_with_exclusion(random_num1, random_num2)
    arr2 = get_random_numbers_with_exclusion(random_num2, random_num1)
    arr3 = array3index(random_num1, random_num2, arr1, arr2)
    A = random_num1
    B = random_num2
    ARR1 = arr1
    ARR2 = arr2
    ARR3 = arr3

# ===================================================
@app.post("/draw_user1_listname")
async def draw_image(json_data: dict):
    try:
        number = json_data["number"]
        listname = json_data["listname"]

        with open('Datausers.json', mode='r') as my_file:
            data = json.load(my_file)

        found = False 

        for user_data in data:
            if int(number) == int(user_data['cid']):
                found = True
                break 
        listsputname = []
        listsputname = listname.split(",")
        
        if not found:
            print(False)
        else:
            listbase64  = []    
            for elemennamet in listsputname:
                
                img = Image.open(user_data['imglocal'])
                draw = ImageDraw.Draw(img)
                
                current_date = datetime.datetime.now()
                formatted_date = current_date.strftime("%d/%m/%Y")

                RANDOMNUMBER()
                fontname = ImageFont.truetype(user_data['font1'], size=70)  
                fonttime = ImageFont.truetype(user_data['font1'], size=45)
                fontNUMMAIN = ImageFont.truetype(user_data['font1'], size=150)  
                fontARR1 = ImageFont.truetype(user_data['font1'], size=90)  
                fontARR3 = ImageFont.truetype(user_data['font1'], size=54)  


                def create_image(message, font):
                    _, _, w, h = draw.textbbox((0, 0), message, font=font)
                    return w,h
                
                text_width, text_height = create_image(elemennamet, fontname)
                time_width, time_height = create_image(formatted_date, fonttime)

                line_color = (255, 255, 255) 

                positionname = ((img.width - text_width) // 2, 75)
                positiontime = ((img.width - time_width) // 2, 185)

                draw_name(draw,positionname,elemennamet,(253, 205, 0),fontname,"center",5,(0, 0, 0))
                draw_line_name(draw,((img.width - text_width) // 2),50,text_width,text_height,line_color,5)
                
                draw_name(draw,positiontime,formatted_date,(255, 255, 255),fonttime,"center",3,(0, 0, 0))

                draw.text((200,380),str(A)+"-"+str(B),fill=(255, 255, 255) , font=fontNUMMAIN, align="center", stroke_width=10, stroke_fill=(0,0,0))

                for index, element in enumerate(ARR1):
                    draw.text((610,(280+(index*130))),str(element),fill=(255, 255, 255) , font=fontARR1, align="center", stroke_width=5, stroke_fill=(0,0,0))
                
                for index, element in enumerate(ARR2):
                    draw.text((820,(280+(index*130))),str(element),fill=(255, 255, 255) , font=fontARR1, align="center", stroke_width=5, stroke_fill=(0,0,0))

                for index, element in enumerate(ARR3):
                    draw.text((120+(index*140),650),str(element),fill=(255, 255, 255) , font=fontARR3, align="center", stroke_width=5, stroke_fill=(0,0,0))
                
                buffer = io.BytesIO()
                img.save(buffer, format="PNG")
                base64_image = base64.b64encode(buffer.getvalue()).decode()
                result = {"name":elemennamet,"base64_image":base64_image}
                listbase64.append(result)            
            
            return JSONResponse(content={"listbase64": listbase64})
        
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid JSON data. 'number' and 'nameH' fields are required.")
    


 
# ========================================  user1 Katen    ======================================================================================
@app.post("/draw_user1")
async def draw_image(json_data: dict):
    try:
        number = json_data["number"]
        nameH = json_data["nameH"]

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

            RANDOMNUMBER()
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
            draw_line_name(draw,((img.width - text_width) // 2),50,text_width,text_height,line_color,5)
            
            draw_name(draw,positiontime,formatted_date,(255, 255, 255),fonttime,"center",3,(0, 0, 0))

            draw.text((200,380),str(A)+"-"+str(B),fill=(255, 255, 255) , font=fontNUMMAIN, align="center", stroke_width=10, stroke_fill=(0,0,0))

            for index, element in enumerate(ARR1):
                draw.text((610,(280+(index*130))),str(element),fill=(255, 255, 255) , font=fontARR1, align="center", stroke_width=5, stroke_fill=(0,0,0))
            
            for index, element in enumerate(ARR2):
                draw.text((820,(280+(index*130))),str(element),fill=(255, 255, 255) , font=fontARR1, align="center", stroke_width=5, stroke_fill=(0,0,0))

            for index, element in enumerate(ARR3):
                draw.text((120+(index*140),650),str(element),fill=(255, 255, 255) , font=fontARR3, align="center", stroke_width=5, stroke_fill=(0,0,0))
    
            # img.show()

            
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            base64_image = base64.b64encode(buffer.getvalue()).decode()

            return {"base64_image": base64_image}
        
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid JSON data. 'number' and 'nameH' fields are required.")
    


# ==============================================================================================================================


@app.post("/draw_image")
async def draw_image(json_data: dict):
    try:
        number = json_data["number"]
        nameH = json_data["nameH"]

        with open('datauser.json', mode='r') as my_file:
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

            font = ImageFont.truetype(user_data['font'], size=76)  
            # Text to be drawn
            # txt = urllib.parse.quote(nameH)
            

            def create_image(message, font):
                _, _, w, h = draw.textbbox((0, 0), message, font=font)
                return w,h
            text_width, text_height = create_image(nameH, font)
            
            # Position to draw the text
            position = ((img.width - text_width) // 2, 100)

            # Fill color for the text (black in this example)
            fill_color = (0, 0, 0)

            # Draw the text with the specified font and size
            draw.text(position, nameH, fill=fill_color, font=font)

            # Save the image
            # img.save('graph.png')

            # Show the image
            # img.show()

            # Convert the image to a base64 string
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            base64_image = base64.b64encode(buffer.getvalue()).decode()

            return {"base64_image": base64_image}
        
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid JSON data. 'number' and 'nameH' fields are required.")
    

@app.get("/draw_image/{number}/{nameH}")
async def draw_image(number: str,nameH:str):
    with open('datauser.json', mode='r') as my_file:
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

        font = ImageFont.truetype(user_data['font'], size=76)  
        # Text to be drawn
        txt = urllib.parse.quote(nameH)
        

        def create_image(message, font):
            _, _, w, h = draw.textbbox((0, 0), message, font=font)
            return w,h
        text_width, text_height = create_image(txt, font)
        
        # Position to draw the text
        position = ((img.width - text_width) // 2, 100)

        # Fill color for the text (black in this example)
        fill_color = (0, 0, 0)

        # Draw the text with the specified font and size
        draw.text(position, txt, fill=fill_color, font=font)

        # Save the image
        # img.save('graph.png')

        # Show the image
        # img.show()

        # Convert the image to a base64 string
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        base64_image = base64.b64encode(buffer.getvalue()).decode()

        return {"base64_image": base64_image}

@app.get("/download_image/{number}/{nameH}")
async def download_image(number: str, nameH: str):
    # สร้างรูปภาพด้วยฟังก์ชัน draw_image
    image_data = await draw_image(number, nameH)

    # สร้างไฟล์ชั่วคราวจากข้อมูลรูปภาพ
    with open("temp_image.png", "wb") as temp_image_file:
        temp_image_file.write(base64.b64decode(image_data["base64_image"]))

    # ใช้ FileResponse เพื่อสร้างการตอบสนองสำหรับการดาวน์โหลดไฟล์
    return FileResponse("temp_image.png", headers={"Content-Disposition": f"attachment; filename=temp_image.png"})
