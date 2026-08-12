import asyncio
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import edge_tts

W,H=720,1280
BG="#FFFAF4"; PURPLE="#7847D8"; LAVENDER="#F6EDFF"; DARK="#18151B"; MUTED="#665F69"
OUT=Path("day9_build"); OUT.mkdir(exist_ok=True)
VOICE="es-AR-ElenaNeural"; RATE="-5%"

SCENES=[
{"label":"DÍA 9 · 9/30","title":"Expectativas ajenas vs. expectativas propias","body":"Distinguir lo que esperás vos de lo que aprendiste a esperar para otros","speech":"Bienvenida al Día 9 de LUMINA. Ayer observaste que algunas formas de hablarte tienen una historia. Hoy vamos a mirar otra pieza importante: las expectativas. Especialmente, la diferencia entre lo que realmente querés para vos y lo que sentís que deberías querer para cumplir con lo que otros esperan."},
{"label":"IDEA CENTRAL","title":"No toda expectativa nace de vos","body":"A veces perseguimos metas que nunca elegimos conscientemente","speech":"Las expectativas son ideas sobre cómo deberían salir las cosas, cómo deberíamos ser o qué tendríamos que alcanzar. Algunas son propias y están conectadas con nuestros valores. Otras fueron absorbidas del entorno y pueden seguir guiándonos incluso cuando ya no representan lo que queremos."},
{"label":"EXPECTATIVAS AJENAS","title":"Lo que siento que otros esperan de mí","body":"Familia · pareja · amistades · trabajo · cultura · redes","speech":"Una expectativa ajena puede aparecer como: tengo que ser exitosa a cierta edad, debería estar en pareja, tengo que ser siempre fuerte, tendría que verme de determinada manera, no puedo decepcionar a mi familia. A veces nadie lo está diciendo hoy, pero la expectativa quedó instalada."},
{"label":"EXPECTATIVAS PROPIAS","title":"Lo que yo elijo construir","body":"Deseos, valores, necesidades y objetivos que tienen sentido para vos","speech":"Una expectativa propia no es simplemente hacer lo contrario de lo que otros quieren. Es preguntarte qué tiene sentido para vos. Qué tipo de vida querés construir, qué valores querés cuidar, qué ritmo necesitás y qué objetivos elegirías aunque nadie estuviera mirando."},
{"label":"PREGUNTA CLAVE","title":"¿Esto lo quiero o quiero ser aprobada?","body":"A veces ambas cosas conviven. El objetivo es distinguirlas","speech":"No siempre es fácil separar una cosa de la otra. Podés querer algo genuinamente y, al mismo tiempo, disfrutar de la aprobación que genera. Por eso la pregunta no busca respuestas perfectas. Busca darte más claridad: ¿esto lo quiero yo, o siento que necesito cumplirlo para sentir que valgo o que no voy a decepcionar?"},
{"label":"EJEMPLO","title":"La misma meta puede tener motivos distintos","body":"“Quiero crecer profesionalmente” puede ser elección, presión o una mezcla","speech":"Imaginá dos personas con la misma meta: crecer profesionalmente. Una puede hacerlo porque disfruta aprender y quiere desarrollar un proyecto. Otra puede sentir que si no alcanza cierto nivel decepciona a su familia. Desde afuera la meta parece igual. Por dentro, la experiencia puede ser muy diferente."},
{"label":"SEÑALES DE PRESIÓN EXTERNA","title":"Prestá atención a ciertas frases","body":"“A esta edad ya debería…” · “Qué van a pensar” · “No puedo fallarles”","speech":"Algunas señales pueden ayudarte a detectar expectativas ajenas. Por ejemplo: a esta edad ya debería haber logrado esto. Qué van a pensar si cambio de idea. No puedo fallarles. Todos esperan que yo pueda. Estas frases no prueban por sí solas que una meta sea ajena, pero pueden mostrar que hay presión externa mezclada."},
{"label":"EJERCICIO CENTRAL","title":"Dividí una hoja en dos columnas","body":"EXPECTATIVAS AJENAS / EXPECTATIVAS PROPIAS","speech":"Vamos al ejercicio del Día 9. Dividí una hoja en dos columnas. En la primera escribí expectativas que sentís que otras personas, tu entorno o la cultura ponen sobre vos. En la segunda, escribí lo que vos realmente querés cuidar, construir o experimentar en esta etapa de tu vida.","pause_after":5},
{"label":"MIRÁ LAS DIFERENCIAS","title":"¿Dónde aparecen tensión y alivio?","body":"¿Qué expectativa pesa? · ¿Cuál te entusiasma? · ¿Cuál ya no te representa?","speech":"Después mirá ambas columnas y observá qué pasa en vos. ¿Qué expectativa se siente pesada? ¿Cuál te genera ansiedad o culpa? ¿Cuál, en cambio, te da energía o sentido? ¿Hay algo que seguís persiguiendo aunque ya no te represente? No hace falta decidir nada todavía. Primero buscamos claridad.","pause_after":5},
{"label":"NO ES EGOÍSMO","title":"Elegir lo propio no implica ignorar a los demás","body":"Podés considerar a otros sin abandonar tu criterio","speech":"Diferenciar expectativas propias de ajenas no significa vivir sin considerar a nadie. En los vínculos también hacemos acuerdos, cuidamos consecuencias y negociamos necesidades. La diferencia está en no convertir la aprobación externa en la única brújula de tu vida."},
{"label":"REFLEXIÓN","title":"Tu valor no depende de cumplir un guion","body":"Podés revisar metas, ritmos y decisiones sin que eso defina tu valor","speech":"Tal vez creciste con una idea bastante clara de cómo debía verse una vida correcta. Pero revisar un guion no significa fracasar. Cambiar de dirección, elegir otro ritmo o descubrir que querés algo diferente no dice que valgas menos. Dice que estás escuchando con más atención qué vida querés construir."},
{"label":"MICROACCIÓN · 24 HORAS","title":"Antes de decidir, preguntate: ¿para quién?","body":"¿Lo quiero? · ¿Lo necesito? · ¿Lo elegiría si nadie opinara?","speech":"Durante las próximas 24 horas, cuando aparezca un debería relacionado con una meta, una decisión o tu imagen, probá preguntarte: ¿para quién estoy intentando cumplir esto? Después sumá: ¿qué elegiría yo si no tuviera que demostrar nada en este momento? No necesitás actuar de inmediato. Solo escuchar la diferencia."},
{"label":"DÍA 9 COMPLETADO","title":"Hoy empezaste a separar deseo de presión","body":"9 / 30 · Racha: 9 días 🔥\nMañana: Lo que puedo controlar y lo que no","speech":"Completaste el Día 9 de LUMINA. Hoy empezaste a distinguir expectativas ajenas de expectativas propias y a reconocer cuándo la aprobación externa puede estar influyendo en tus decisiones. Mañana vamos a trabajar con algo que puede aliviar mucha carga mental: diferenciar lo que podés controlar de lo que no. Nos vemos en el Día 10."}
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
    tf=font(48 if len(scene["title"])<45 else 40,True)
    y=draw_multiline(d,50,225,wrap_px(d,scene["title"],tf,620),tf,DARK,12)+35
    bf=font(28); lines=wrap_px(d,scene["body"],bf,540); card_h=max(210,80+len(lines)*42)
    if y+card_h>1030: card_h=1030-y
    d.rounded_rectangle((50,y,670,y+card_h),radius=32,fill=LAVENDER)
    by=y+42
    for line in lines:
        d.text((90,by),line,font=bf,fill=DARK); by+=42
    d.text((50,1120),"DISTINGUÍ · ELEGÍ · CONSTRUÍ",font=font(19,True),fill=PURPLE)
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
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(cf),"-c","copy","LUMINA_Dia9_voz_natural.mp4"],check=True)

if __name__=="__main__": asyncio.run(main())
