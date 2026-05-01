import os
import shutil
import re
from app import create_app, db
from app.models import Labs
from bs4 import BeautifulSoup

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def import_labs():
    app = create_app('default')
    
    # Default to a folder next to the script or a specific path
    possible_roots = [
        r"c:\Users\Defender\Desktop\Programs\Virtual laboratoriyalar",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "Virtual laboratoriyalar"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Virtual laboratoriyalar")
    ]
    
    source_root = None
    for path in possible_roots:
        if os.path.exists(path):
            source_root = path
            break
            
    if not source_root:
        print("Warning: 'Virtual laboratoriyalar' folder not found. Skipping file copy.")
        return
    
    dest_root = os.path.join(app.static_folder, "labs")
    pics_root = os.path.join(app.static_folder, "pics")
    
    if not os.path.exists(dest_root):
        os.makedirs(dest_root)
        
    if not os.path.exists(pics_root):
        os.makedirs(pics_root)

    lab_folders = [
        ("1. Yoritilganlik", "yoritilganlik"),
        ("2. Transformator", "transformator"),
        ("3. O‘ZAKSIZ G‘ALTAKNING INDUKTIV QARSHILIGINI ANIQLASH", "induktiv-qarshilik"),
        ("4. Sindirish ko'rsatkichi", "sindirish-korsatkichi")
    ]

    with app.app_context():
        count = 0
        for folder_name, slug in lab_folders:
            src_path = os.path.join(source_root, folder_name)
            if not os.path.exists(src_path):
                print(f"Skipping {folder_name}: Not found")
                continue

            # 1. Copy files
            dest_path = os.path.join(dest_root, slug)
            if os.path.exists(dest_path):
                shutil.rmtree(dest_path)
            shutil.copytree(src_path, dest_path)
            print(f"Copied {folder_name} to {dest_path}")

            # 2. Get Title from index.html
            index_path = os.path.join(dest_path, "index.html")
            title = folder_name
            if os.path.exists(index_path):
                try:
                    with open(index_path, 'r', encoding='utf-8') as f:
                        soup = BeautifulSoup(f.read(), 'html.parser')
                        if soup.title:
                            title = soup.title.string.strip()
                except UnicodeDecodeError:
                     # Fallback for other encodings
                    try:
                        with open(index_path, 'r', encoding='windows-1251') as f:
                            soup = BeautifulSoup(f.read(), 'html.parser')
                            if soup.title:
                                title = soup.title.string.strip()
                    except:
                        pass
            
            # 3. Handle Image
            pic_path = ""
            images_dir = os.path.join(dest_path, "images")
            if os.path.exists(images_dir):
                images = [f for f in os.listdir(images_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                if images:
                    # Try to find a good image, otherwise take the first one
                    # Specific overrides for better thumbnails if needed, or just take first
                    img_name = images[0]
                    # Specific mapping based on inspection could go here
                    if "istochnik.png" in images: img_name = "istochnik.png" # Example from 1. Yoritilganlik
                    
                    src_img = os.path.join(images_dir, img_name)
                    dest_img_name = f"{slug}.png"
                    dest_img = os.path.join(pics_root, dest_img_name)
                    shutil.copy2(src_img, dest_img)
                    pic_path = f"pics/{dest_img_name}"

            # 4. Add to DB
            # Check if exists
            existing = Labs.query.filter_by(link=f"/static/labs/{slug}/index.html").first()
            if existing:
                print(f"Update existing lab: {title}")
                existing.name = title
                existing.pic_path = pic_path or existing.pic_path
                existing.about = "Virtual laboratoriya"
            else:
                print(f"Creating new lab: {title}")
                lab = Labs(
                    name=title,
                    about="Virtual laboratoriya",
                    pic_path=pic_path,
                    link=f"/static/labs/{slug}/index.html"
                )
                db.session.add(lab)
            count += 1
        
        db.session.commit()
        print(f"Successfully imported {count} labs.")

if __name__ == "__main__":
    import_labs()
