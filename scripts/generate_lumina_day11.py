import asyncio
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import edge_tts

W,H=720,1280
BG="#FFFAF4"; PURPLE="#7847D8"; LAVENDER="#F6EDFF"; DARK="#18151B"; MUTED="#665F69"
OUT=Path("day11_build"); OUT.mkdir(exist_ok=True)
VOICE="es-AR-ElenaNeural"; RATE="-5%"

SCENES=[
{"label":"DÍA 11 · 11/30","title":"Pensar algo no lo convierte en verdad","body":"Empezar a observar tus pensamientos sin tratarlos automáticamente como hechos","speech":"Bienvenida al Día 11 de LUMINA. Ayer trabajaste en distinguir lo que depende de vos de lo que no. Hoy empezamos una nueva etapa: mirar más de cerca cómo funciona tu mente. Y vamos a partir de una idea fundamental: pensar algo no lo convierte automáticamente en verdad."},
{"label":"IDEA CENTRAL","title":"Un pensamiento es una interpretación","body":"Puede aparecer rápido, sentirse convincente y aun así necesitar ser revisado","speech":"Los pensamientos aparecen muchas veces de forma automática. Algunos describen hechos, pero otros son interpretaciones, conclusiones o predicciones. Que un pensamiento aparezca con fuerza, se repita o genere una emoción intensa no significa, por sí solo, que sea una descripción exacta de la realidad."},
{"label":"PENSAMIENTO Y EMOCIÓN","title":"Lo que pensás influye en cómo te sentís","body":"Situación · pensamiento · emoción · conducta","speech":"Una idea central del enfoque cognitivo es que la manera en que interpretamos una situación influye en cómo nos sentimos y en lo que hacemos. Dos personas pueden vivir una situación parecida y reaccionar distinto porque la interpretan de manera diferente. Por eso observar el pensamiento es tan importante."},
{"label":"EJEMPLO","title":"Un mensaje sin respuesta","body":"Hecho: todavía no respondió · Pensamiento: “seguro hice algo mal”","speech":"Imaginá que mandás un mensaje y todavía no recibís respuesta. El hecho es ese: no respondió todavía. Pero tu mente puede agregar: seguro hice algo mal, está enojado conmigo o ya no le importo. Esas frases pueden sentirse verdaderas, pero siguen siendo interpretaciones hasta que exista información que las confirme."},
{"label":"POR QUÉ SE SIENTE TAN REAL","title":"La intensidad no es evidencia","body":"Miedo, inseguridad y experiencias previas pueden aumentar la sensación de certeza","speech":"A veces creemos más un pensamiento porque viene acompañado de una emoción fuerte. Si sentís miedo, la idea puede parecer más peligrosa. Si sentís vergüenza, puede parecer más cierta una crítica hacia vos. Pero la intensidad emocional no funciona como prueba. Sentir algo con mucha fuerza no demuestra que la interpretación sea correcta."},
{"label":"SEÑAL DE ALERTA","title":"Palabras que suenan a certeza total","body":"“Seguro…” · “Obviamente…” · “Nunca…” · “Siempre…” · “Ya sé lo que piensa”","speech":"Algunas palabras pueden ayudarte a detectar cuándo una interpretación se está presentando como si fuera un hecho. Seguro, obviamente, nunca, siempre, ya sé lo que piensa. No significa que esas frases sean siempre falsas, pero sí que vale la pena detenerte antes de aceptarlas sin revisión."},
{"label":"PRIMER PASO","title":"Nombrá el pensamiento","body":"En vez de “soy un fracaso” → “estoy pensando que soy un fracaso”","speech":"Una forma sencilla de crear un poco de distancia es nombrar lo que está ocurriendo. En vez de decir soy un fracaso, podés decir estoy pensando que soy un fracaso. El contenido todavía está ahí, pero ahora aparece como un pensamiento que podés observar, no como una identidad o una verdad indiscutible."},
{"label":"EJERCICIO CENTRAL","title":"Pensamiento o hecho","body":"Elegí una situación reciente y separá qué pasó de lo que tu mente interpretó","speech":"Vamos al ejercicio del Día 11. Elegí una situación reciente que haya generado malestar. Primero escribí solamente lo observable: qué ocurrió, qué se dijo, qué datos tenés. Después, en otra línea, escribí qué pensaste sobre eso. El objetivo no es decidir todavía si el pensamiento es verdadero o falso. Solo aprender a diferenciar el hecho de la interpretación.","pause_after":5},
{"label":"PREGUNTA CLAVE","title":"¿Qué sé y qué estoy suponiendo?","body":"Separar datos de conclusiones te da más espacio para pensar","speech":"Ahora mirá lo que escribiste y preguntate: ¿qué sé realmente y qué estoy suponiendo? Puede haber partes muy claras y otras inciertas. No necesitás encontrar una respuesta perfecta. Lo importante es empezar a notar cuándo tu mente completa información que todavía no tiene.","pause_after":5},
{"label":"NO ES PENSAR POSITIVO","title":"Cuestionar no significa negar","body":"No buscamos reemplazar todo por frases lindas, sino mirar con más precisión","speech":"Este trabajo no consiste en obligarte a pensar positivo ni en negar emociones. Si algo duele, duele. Si una situación es difícil, merece ser reconocida. Lo que buscamos es evitar que una interpretación automática se convierta en una sentencia sin haberla examinado."},
{"label":"REFLEXIÓN","title":"Podés escuchar tu mente sin obedecerla de inmediato","body":"Pensar algo y actuar como si fuera cierto son dos cosas diferentes","speech":"Tu mente produce pensamientos todo el tiempo. Algunos te ayudan y otros pueden estar influidos por miedo, experiencias previas o hábitos. Aprender a observarlos te permite crear un pequeño espacio entre lo que aparece en tu cabeza y la forma en que elegís responder."},
{"label":"MICROACCIÓN · 24 HORAS","title":"Agregá una frase de distancia","body":"“Estoy teniendo el pensamiento de que…”","speech":"Durante las próximas 24 horas, cuando aparezca un pensamiento que aumente tu malestar, probá agregar una frase antes: estoy teniendo el pensamiento de que. Después preguntate: ¿qué parte de esto sé y qué parte estoy interpretando? No hace falta resolverlo en ese momento. Solo practicar la diferencia."},
{"label":"DÍA 11 COMPLETADO","title":"Hoy empezaste a mirar tus pensamientos con más distancia","body":"11 / 30 · Racha: 11 días 🔥\nMañana: Las trampas de mi mente","speech":"Completaste el Día 11 de LUMINA. Hoy empezaste a separar pensamientos de hechos y a observar tus interpretaciones con un poco más de distancia. Mañana vamos a avanzar un paso más y conocer algunas trampas frecuentes de la mente, también llamadas distorsiones cognitivas. Nos vemos en el Día 12."}
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
    d.text((50,1120),"OBSERVÁ · DISTINGUÍ · CUESTIONÁ",font=font(19,True),fill=PURPLE)
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
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(cf),"-c","copy","LUMINA_Dia11_voz_natural.mp4"],check=True)

if __name__=="__main__": asyncio.run(main())
