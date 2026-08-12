import asyncio
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import edge_tts

W, H = 720, 1280
BG = "#FFFAF4"
PURPLE = "#7847D8"
LAVENDER = "#F6EDFF"
DARK = "#18151B"
MUTED = "#665F69"
OUT = Path("day6_build")
OUT.mkdir(exist_ok=True)
VOICE = "es-AR-ElenaNeural"
RATE = "-5%"

SCENES = [
{"label":"DÍA 6 · 6/30","title":"El triángulo de mi autoestima","body":"Cómo me pienso · cómo me trato · cómo actúo conmigo","speech":"Bienvenida al Día 6 de LUMINA. En los primeros días empezaste a mirar cómo te tratás, cómo te definís, qué querés para tu vida y qué partes de vos no siempre se ven. Hoy vamos a ordenar todo eso con una idea muy simple: el triángulo de tu autoestima."},
{"label":"IDEA CENTRAL","title":"La autoestima no depende de una sola cosa","body":"Pensamiento · trato · acción","speech":"Muchas veces pensamos que la autoestima depende solamente de lo que sentimos por nosotras mismas. Pero en realidad se construye desde varias dimensiones. Hoy quiero que imagines un triángulo con tres partes: cómo me pienso, cómo me trato y cómo actúo conmigo. Cuando una de esas partes está muy debilitada, la autoestima se resiente."},
{"label":"PRIMER LADO","title":"Cómo me pienso","body":"Lo que creo sobre mí · cómo me describo · qué historia me cuento","speech":"La primera parte es cómo me pienso. Tiene que ver con lo que creo sobre mí, cómo me describo y qué historia me cuento sobre quién soy. Si constantemente me pienso desde la crítica, la comparación o la insuficiencia, mi autoestima se debilita."},
{"label":"SEGUNDO LADO","title":"Cómo me trato","body":"El tono con el que me acompaño también construye autoestima","speech":"La segunda parte es cómo me trato. No alcanza con tener pensamientos lindos de vez en cuando si después me hablo mal, me exijo sin descanso o invalido lo que siento. La autoestima también se nota en el tono con el que me acompaño."},
{"label":"TERCER LADO","title":"Cómo actúo conmigo","body":"Límites · descanso · decisiones · cuidado · prioridades","speech":"Y la tercera parte es cómo actúo conmigo. Esto incluye las decisiones que tomo, los límites que pongo, el descanso que me permito, las cosas que sostengo por mí y la forma en que priorizo mi bienestar. Porque a veces digo que me valoro, pero actúo como si mis necesidades no importaran."},
{"label":"EL TRIÁNGULO","title":"Pensamiento + trato + acción","body":"Las tres dimensiones se influyen entre sí","speech":"Por eso, una autoestima más sana no se construye solo pensando distinto. También necesita un trato más compasivo y acciones más coherentes. Pensamiento, trato y acción se influyen entre sí. Ese es tu triángulo."},
{"label":"EJERCICIO CENTRAL","title":"¿Cómo me pienso?","body":"¿Cuál es la frase que más repito sobre mí?","speech":"Vamos al ejercicio del Día 6. Primero preguntate: cómo me pienso. Cuál es la frase que más repito sobre mí. Qué palabras uso para describirme cuando algo sale mal. Escribilo sin corregirte todavía.","pause_after":5},
{"label":"EJERCICIO CENTRAL","title":"¿Cómo me trato?","body":"¿Me acompaño o me exijo de forma cruel?","speech":"Después preguntate: cómo me trato. Cuando algo me cuesta, me acompaño o me exijo de forma cruel. Me permito equivocarme o convierto el error en una condena personal.","pause_after":5},
{"label":"EJERCICIO CENTRAL","title":"¿Cómo actúo conmigo?","body":"¿Mis decisiones reflejan cuidado y valor personal?","speech":"Y ahora: cómo actúo conmigo. Mis decisiones reflejan cuidado y valor personal. Pongo límites cuando los necesito. Respeto mi descanso. Hago lugar para lo que me importa.","pause_after":5},
{"label":"PREGUNTA CLAVE","title":"¿Qué lado está hoy más debilitado?","body":"No para juzgarte. Para saber por dónde empezar.","speech":"Ahora elegí cuál de las tres partes sentís hoy más debilitada. No para juzgarte, sino para saber por dónde empezar. A veces el primer paso es cambiar una frase. Otras veces, hablarte con más respeto. Y otras, tomar una decisión distinta."},
{"label":"REFLEXIÓN","title":"Coherencia, no perfección","body":"Una autoestima más sana se construye con pequeños cambios sostenidos","speech":"No hace falta tener un triángulo perfecto. Lo importante es reconocer en qué parte necesitás más trabajo hoy. Una autoestima más sana necesita coherencia, no perfección. Pequeños cambios sostenidos pueden empezar a modificar la relación que tenés con vos."},
{"label":"COMPROMISO · 24 HORAS","title":"Fortalecé un lado con una acción pequeña","body":"Pensamiento · trato · acción","speech":"Para cerrar el Día 6, elegí una de las tres partes del triángulo y hacé hoy una acción pequeña para fortalecerla. Puede ser cambiar una frase, tratarte con más respeto o tomar una decisión más coherente con vos. Observá qué cambia cuando empezás a actuar desde el cuidado."},
{"label":"DÍA 6 COMPLETADO","title":"Hoy entendiste mejor de qué está hecha tu autoestima","body":"6 / 30 · Racha: 6 días 🔥\nMañana: Los debería que gobiernan mi vida","speech":"Completaste el Día 6 de LUMINA. Hoy entendiste mejor de qué está hecha tu autoestima y por dónde podés empezar a fortalecerla. Mañana vamos a observar algo que muchas veces dirige nuestra vida sin que lo notemos: los debería. Nos vemos en el Día 7."}
]

def font(size,bold=False):
    p="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(p,size)

def wrap_px(draw,text,fnt,max_width):
    out=[]
    for para in text.split("\n"):
        words=para.split()
        if not words: out.append(""); continue
        cur=words[0]
        for w in words[1:]:
            t=cur+" "+w
            if draw.textbbox((0,0),t,font=fnt)[2] <= max_width: cur=t
            else: out.append(cur); cur=w
        out.append(cur)
    return out

def draw_multiline(draw,x,y,lines,fnt,fill,spacing=12):
    for line in lines:
        draw.text((x,y),line,font=fnt,fill=fill)
        b=draw.textbbox((x,y),line if line else "Ag",font=fnt)
        y += (b[3]-b[1])+spacing
    return y

def make_slide(scene,idx):
    img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)
    d.text((50,55),"LUMINA",font=font(28,True),fill=PURPLE)
    d.rounded_rectangle((560,45,670,90),radius=22,fill=LAVENDER)
    d.text((615,67),f"{idx+1}/13",font=font(18,True),fill=PURPLE,anchor="mm")
    d.rounded_rectangle((50,112,670,122),radius=5,fill="#E9DDF8")
    d.rounded_rectangle((50,112,50+max(30,int(620*(idx+1)/13)),122),radius=5,fill=PURPLE)
    d.text((50,170),scene["label"],font=font(22,True),fill=PURPLE)
    tf=font(48 if len(scene["title"])<48 else 42,True)
    y=draw_multiline(d,50,225,wrap_px(d,scene["title"],tf,620),tf,DARK,12)+35
    bf=font(29); lines=wrap_px(d,scene["body"],bf,540); card_h=max(210,80+len(lines)*42)
    if y+card_h>1030: card_h=1030-y
    d.rounded_rectangle((50,y,670,y+card_h),radius=32,fill=LAVENDER)
    by=y+42
    for line in lines:
        d.text((90,by),line,font=bf,fill=DARK); by+=42
    d.text((50,1120),"OBSERVÁ · ESCRIBÍ · ELEGÍ",font=font(19,True),fill=PURPLE)
    d.text((50,1165),"LUMINA · 30 días para volver a vos",font=font(17),fill=MUTED)
    return img

async def synth(text,out_mp3):
    await edge_tts.Communicate(text=text,voice=VOICE,rate=RATE).save(str(out_mp3))

def duration(path):
    r=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",str(path)],capture_output=True,text=True,check=True)
    return float(r.stdout.strip())

def make_segment(img_path,audio_path,out_path):
    dur=duration(audio_path)
    subprocess.run(["ffmpeg","-y","-loop","1","-framerate","30","-i",str(img_path),"-i",str(audio_path),"-vf","scale=720:1280,format=yuv420p","-c:v","libx264","-preset","veryfast","-tune","stillimage","-c:a","aac","-b:a","160k","-ar","48000","-ac","2","-t",f"{dur:.3f}","-shortest",str(out_path)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

def add_pause(img_path,seconds,out_path):
    subprocess.run(["ffmpeg","-y","-loop","1","-framerate","30","-i",str(img_path),"-f","lavfi","-i","anullsrc=r=48000:cl=stereo","-vf","scale=720:1280,format=yuv420p","-c:v","libx264","-preset","veryfast","-tune","stillimage","-c:a","aac","-b:a","160k","-t",str(seconds),"-shortest",str(out_path)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

async def main():
    entries=[]
    for i,s in enumerate(SCENES):
        img=OUT/f"slide_{i:02d}.png"; aud=OUT/f"voice_{i:02d}.mp3"; seg=OUT/f"seg_{i:02d}.mp4"
        make_slide(s,i).save(img); await synth(s["speech"],aud); make_segment(img,aud,seg); entries.append(seg)
        if s.get("pause_after"):
            p=OUT/f"pause_{i:02d}.mp4"; add_pause(img,s["pause_after"],p); entries.append(p)
    cf=OUT/"concat.txt"; cf.write_text("\n".join(f"file '{p.resolve()}'" for p in entries),encoding="utf-8")
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(cf),"-c","copy","LUMINA_Dia6_voz_natural.mp4"],check=True)

if __name__=="__main__": asyncio.run(main())