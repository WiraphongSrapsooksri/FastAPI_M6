from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from PIL import Image, ImageDraw, ImageFont
import io
import base64
import json
import urllib.parse




app = FastAPI()

# Configure CORS
origins = ["*"]  # You can specify the allowed origins here, e.g., ["http://localhost", "https://example.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
