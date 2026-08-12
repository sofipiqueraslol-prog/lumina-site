import asyncio
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import edge_tts

W,H=720,1280
BG="#FFFAF4"; PURPLE="#7847D8"; LAVENDER="#F6EDFF"; DARK="#18151B"; MUTED="#665F69"
OUT=Path("day8_build"); OUT.mkdir(exist_ok=True)
VOICE="es-AR-ElenaNeural"; RATE="-5%"

SCENES=[
{"label":"DÍA 8 · 8/30","title":"¿De quién aprendí a hablarme así?","body":"Reconocer el origen de algunas voces internas","speech":"Bienvenida al Día 8 de LUMINA. Ayer observaste algunos de los debería que pueden gobernar tu vida sin que los cuestiones. Hoy vamos a ir un paso más atrás y mirar algo importante: de dónde aprendiste algunas de las formas en las que hoy te hablás, te exigís o te evaluás."},
{"label":"IDEA CENTRAL","title":"Tu diálogo interno tiene historia","body":"Muchas frases actuales fueron aprendidas, repetidas o incorporadas","speech":"La manera en que te hablás no apareció de un día para el otro. A lo largo de la vida vamos recibiendo mensajes sobre lo que está bien, lo que está mal, cómo deberíamos comportarnos, qué merece aprobación y qué puede generar rechazo. Algunos de esos mensajes terminan convirtiéndose en parte de nuestra voz interna."},
{"label":"¿DE DÓNDE PUEDE VENIR?","title":"No hay una sola fuente","body":"Familia · escuela · vínculos · cultura · experiencias · comparaciones","speech":"Esas voces pueden venir de muchos lugares. De la familia, de la escuela, de amistades, parejas, experiencias difíciles, comentarios repetidos, la cultura o las comparaciones. A veces alguien lo dijo directamente. Otras veces lo aprendiste observando qué cosas recibían aprobación y cuáles no."},
{"label":"NO BUSCAMOS CULPABLES","title":"Comprender no es acusar","body":"El objetivo es reconocer qué aprendiste y decidir qué querés conservar","speech":"Este ejercicio no busca señalar culpables ni reducir toda tu historia a una persona. Las personas también transmiten lo que aprendieron. Lo que buscamos es algo diferente: reconocer qué mensajes incorporaste y preguntarte cuáles todavía tienen sentido para la persona que sos hoy."},
{"label":"UNA VOZ APRENDIDA","title":"A veces suena como si fuera totalmente tuya","body":"“No seas débil” · “Tenés que poder sola” · “No molestes” · “Hacelo perfecto”","speech":"Una frase aprendida puede repetirse tanto que termina sonando como si siempre hubiera sido tuya. No seas débil. Tenés que poder sola. No molestes a los demás. Hacelo perfecto. Tenés que verte de determinada manera. Cuando aparece automáticamente, quizá ni siquiera te preguntás de dónde salió."},
{"label":"EJEMPLO","title":"Del mensaje externo a la regla interna","body":"“No llores” → “Mostrar lo que siento es una debilidad”","speech":"Imaginá que durante mucho tiempo escuchaste que llorar era exagerar o ser débil. Con los años, ese mensaje podría transformarse en una regla interna: no debería mostrar lo que siento. Lo importante es notar que entre lo que alguna vez aprendiste y lo que hoy elegís creer puede existir una diferencia."},
{"label":"EJERCICIO CENTRAL","title":"Elegí una frase que te repetís","body":"¿Qué te decís cuando fallás, necesitás ayuda o sentís que no alcanzás?","speech":"Vamos al ejercicio del Día 8. Elegí una frase que te repetís cuando algo sale mal, cuando necesitás ayuda o cuando sentís que no estás cumpliendo. Escribila exactamente como aparece. Puede ser: soy demasiado sensible, tengo que poder sola, si digo que no voy a decepcionar, nunca hago suficiente.","pause_after":5},
{"label":"RASTREÁ SU HISTORIA","title":"¿Cuándo empezaste a escuchar algo parecido?","body":"¿Quién lo decía? · ¿Dónde lo aprendiste? · ¿Qué situaciones lo reforzaron?","speech":"Ahora rastreá su historia con curiosidad. ¿Recordás cuándo empezaste a escuchar algo parecido? ¿Había alguien que se hablara así o que te hablara de esa manera? ¿Qué experiencias pudieron reforzar esa idea? No necesitás encontrar un origen exacto. A veces alcanza con reconocer un contexto o una etapa." ,"pause_after":5},
{"label":"PREGUNTA CLAVE","title":"¿Esta voz todavía me representa?","body":"¿Me ayuda hoy? · ¿Es justa? · ¿La elegiría conscientemente?","speech":"Después hacete una pregunta central: esta voz todavía me representa. ¿Me ayuda hoy? ¿Es justa conmigo? ¿La elegiría conscientemente si pudiera decidir cómo quiero acompañarme? Que una idea sea antigua o familiar no significa que tenga que seguir dirigiendo tu vida."},
{"label":"CONSTRUÍ TU PROPIA VOZ","title":"Podés conservar, modificar o soltar","body":"No todo lo aprendido merece seguir intacto","speech":"Tal vez algunas enseñanzas sí querés conservar. Otras necesitan ser actualizadas. Y otras quizá ya no te sirven. Madurar también implica revisar mensajes heredados y construir una voz más propia, más consciente y más acorde a tus valores actuales."},
{"label":"REFLEXIÓN","title":"Entender el origen cambia la relación con la frase","body":"“Lo aprendí” no es lo mismo que “es una verdad sobre mí”","speech":"Cuando reconocés que una frase fue aprendida, puede empezar a perder parte de su poder. Lo aprendí no significa es una verdad sobre mí. Podés entender de dónde vino una forma de tratarte y, al mismo tiempo, decidir que hoy querés relacionarte con vos de otra manera."},
{"label":"MICROACCIÓN · 24 HORAS","title":"Preguntate: ¿de quién es esta voz?","body":"Detectá una frase · ubicá su posible origen · elegí cómo querés responderte hoy","speech":"Durante las próximas 24 horas, cuando aparezca una frase dura o exigente, probá preguntarte: ¿de quién aprendí a hablarme así? Después agregá una segunda pregunta: ¿cómo quiero hablarme yo hoy? No hace falta borrar la voz anterior. Solo empezar a diferenciarla de tu propia elección."},
{"label":"DÍA 8 COMPLETADO","title":"Hoy empezaste a reconocer qué voces llevás adentro","body":"8 / 30 · Racha: 8 días 🔥\nMañana: Expectativas ajenas vs. expectativas propias","speech":"Completaste el Día 8 de LUMINA. Hoy empezaste a reconocer que algunas voces internas tienen historia y que comprender su origen puede darte más libertad para elegir. Mañana vamos a diferenciar expectativas ajenas de expectativas propias. Nos vemos en el Día 9."}
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
    d.text((50,1120),"RECONOCÉ · COMPRENDÉ · ELEGÍ",font=font(19,True),fill=PURPLE)
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
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(cf),"-c","copy","LUMINA_Dia8_voz_natural.mp4"],check=True)

if __name__=="__main__": asyncio.run(main())
