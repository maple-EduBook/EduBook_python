import os
from typing import Dict
from PIL import Image
from fastapi import UploadFile, File, HTTPException


async def upload_image(file: UploadFile | None = File(None)) -> Dict[str, str]:
    print("upload_image 실행")
    if not file:
        return {"detail": "이미지 없음"}
    file = await validate_image_type(file)
    # 이미지 파일을 메모리에서 PIL 이미지 객체로 변환
    image = Image.open(file.file)
    # 이미지 저장 경로 설정 (예: 현재 디렉토리의 'uploads' 폴더)
    save_path = f"./uploads/{file.filename}"
    # 이미지 저장
    await save_image(image, save_path)
    return {"detail": "이미지 업로드 성공"}

async def validate_image_type(file : UploadFile) -> UploadFile:
    if file.filename.split(".")[-1].lower() not in ["jpg", "jpeg", "png"]:
        raise HTTPException(detail="업로드 불가능한 확장자")
    if not file.content_type.startswith("image"):
        raise  HTTPException(detail="이미지 파일만 업로드 가능")
    return file
async def save_image(image: Image.Image, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    image.save(path)