import argparse,json,shutil,subprocess,sys
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parent.parent;FOLDER=ROOT/'graphics/map_tiles'

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--batch',required=True);parser.add_argument('--source',type=Path,required=True);args=parser.parse_args();batch=next(b for b in json.loads((FOLDER/'front_batches/batches.json').read_text()) if b['name']==args.batch);source=Image.open(args.source).convert('RGB');shutil.copyfile(args.source,FOLDER/f"front_batches/{args.batch}_hd.png")
    for item in batch['items']:
        slot=item['slot'];h=source.height/batch['slots'];crop=source.crop((0,round(slot*h),source.width,round((slot+1)*h)));path=FOLDER/f"map_{item['map']}_hd.png";crop.save(path,compress_level=1)
        subprocess.run([sys.executable,'-X','utf8',str(ROOT/'emulator/install_map_art.py'),'--map',str(item['map']),'--source',str(path)],check=True,cwd=ROOT)
    print('Installed',args.batch)

if __name__=='__main__':main()
