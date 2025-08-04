import json
import base64
from io import BytesIO
from PIL import Image
cold_start = True   

def lambda_handler(event, context):
    global cold_start
    try:
        # Get base64-encoded image from request body
        body = json.loads(event['body'])
        image_data = base64.b64decode(body['image'])

        # Load image
        image = Image.open(BytesIO(image_data))

        # Resize image
        resized_image = image.resize((100, 100))

        # Convert resized image back to base64
        buffer = BytesIO()
        resized_image.save(buffer, format="PNG")
        buffer.seek(0)
        img_b64 = base64.b64encode(buffer.read()).decode('utf-8')
        start_type = "cold" if cold_start else "warm"
        cold_start = False

        return {
            'statusCode': 200,
            'headers': { 'Content-Type': 'application/json' },
            'body': json.dumps({ 'resized_image': img_b64 , 
            'start_type': start_type})

        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({ 'error': str(e) })
        }
