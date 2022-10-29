from pathlib import Path

import qrcode
from PIL import Image
from aiogram.utils.deep_linking import get_start_link
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer


async def generate_qrcode(user_id: int, deep_link: str = None):
    if not deep_link:
        deep_link = await get_start_link(f'userId_{user_id}')
    img_path = Path('data', f'imq-qrcode-{user_id}.png')
    logo_path = Path('data', 'logo.jpg')
    qr = qrcode.QRCode(box_size=20)
    qr.add_data(deep_link)
    qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer()).save(img_path)
    watermark_image(
        input_image_path=img_path,
        watermark_image_path=logo_path
    )
    return img_path


def watermark_image(input_image_path, watermark_image_path):
    background: Image.Image = Image.open(input_image_path).convert('RGBA')
    width, height = background.size
    half_width = int(width/2)
    half_height = int(height/2)
    logo_positions = (
        (0, 0),
        (0, half_height),
        (half_width, 0),
        (half_width, half_height)
    )
    transparent = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    foreground: Image.Image = Image.open(watermark_image_path).convert('RGBA').resize((half_width, half_height))
    for position in logo_positions:
        transparent.paste(foreground, box=position, mask=foreground)
    Image.blend(background, transparent, alpha=0.2).save(input_image_path)
