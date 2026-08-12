import asyncio
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import edge_tts

W,H=720,1280
BG="#FFFAF4"; PURPLE="#7847D8"; LAVENDER="#F6EDFF"; DARK="#18151B"; MUTED="#665F69"
OUT=Path("day7_build"); OUT.mkdir(exist_ok=True)
VOICE="es-AR-ElenaNeural"; RATE="-5%"

SCENES=[
{"label":"DÍA 7 · 7/30","title":"Los “debería” que gobiernan mi vida","body":"Detectar reglas internas que se sienten obligatorias","speech":"Bienvenida al Día 7 de LUMINA. Ayer observaste de qué está hecha tu autoestima. Hoy vamos a mirar algo que muchas veces dirige nuestras decisiones sin que lo notemos: los debería, los tengo que y los tendría que."},
{"label":"IDEA CENTRAL","title":"Una regla puede sonar como una verdad","body":"“Debería poder con todo” · “Tengo que hacerlo perfecto”","speech":"A veces una idea se repite tantas veces que deja de sentirse como una opinión y empieza a sentirse como una regla. Debería poder con todo. Tengo que hacerlo perfecto. No tendría que necesitar ayuda. Si descanso, estoy perdiendo el tiempo. Estas frases pueden convertirse en exigencias internas muy rígidas."},
{"label":"¿DE DÓNDE VIENEN?","title":"Muchas reglas se aprenden","body":"Familia · cultura · experiencias · comparaciones · expectativas","speech":"Los debería no aparecen de la nada. Algunas reglas se aprenden en la familia, otras en la cultura, en experiencias pasadas, en comparaciones o en expectativas que fuimos incorporando. El objetivo de hoy no es buscar culpables, sino empezar a reconocer qué reglas estás obedeciendo automáticamente."},
{"label":"CUANDO SE VUELVEN RÍGIDOS","title":"El problema no es tener expectativas","body":"El problema es sentir que solo valés si las cumplís","speech":"Tener metas, responsabilidades o expectativas no es el problema. El problema aparece cuando una regla se vuelve absoluta y tu valoración personal empieza a depender de cumplirla. Si no lo hago perfecto, soy un fracaso. Si digo que no, soy mala persona. Si necesito descansar, soy floja."},
{"label":"SEÑAL DE ALERTA","title":"Escuchá estas palabras","body":"debería · tendría que · tengo que · nunca · siempre","speech":"Hoy quiero que prestes atención a ciertas palabras. Debería. Tendría que. Tengo que. Nunca. Siempre. No significa que cada vez que aparezcan haya un problema, pero pueden ser una pista de que se activó una regla rígida."},
{"label":"EJEMPLO","title":"Regla rígida vs. preferencia flexible","body":"“Tengo que hacerlo perfecto” → “Me gustaría hacerlo bien, aunque puedo equivocarme”","speech":"Por ejemplo, una regla rígida podría ser: tengo que hacerlo perfecto. Una alternativa más flexible sería: me gustaría hacerlo bien, voy a esforzarme, y aun así puedo equivocarme. No estamos quitando responsabilidad. Estamos quitando la idea de que solo existe una forma aceptable de ser."},
{"label":"EJERCICIO CENTRAL","title":"Detectá un “debería”","body":"¿Qué frase te repetís como si fuera obligatoria?","speech":"Vamos al ejercicio del Día 7. Pensá en una frase que aparezca seguido y que empiece con debería, tendría que o tengo que. Escribila exactamente como aparece en tu cabeza. Por ejemplo: debería ser más segura, tendría que estar siempre disponible, tengo que poder sola.","pause_after":5},
{"label":"EXPLORÁ LA REGLA","title":"¿Qué pasa si no la cumplo?","body":"¿Qué temo que diga de mí? · ¿Qué emoción aparece?","speech":"Ahora preguntate: qué pasa si no cumplo esa regla. Qué temo que signifique sobre mí. Qué emoción aparece: culpa, vergüenza, ansiedad, miedo a decepcionar. Esta parte ayuda a entender por qué una regla tiene tanto poder.","pause_after":5},
{"label":"PONELA A PRUEBA","title":"¿Es realmente absoluta?","body":"¿Se cumple siempre? · ¿Hay excepciones? · ¿Se la exigiría a alguien que quiero?","speech":"Después ponela a prueba. ¿Esta regla se cumple siempre? ¿Hay situaciones en las que no aplica? ¿Se la exigirías con la misma dureza a alguien que querés? ¿Qué evidencia tenés de que romperla te convierte en una peor persona?"},
{"label":"REFORMULÁ","title":"De obligación a elección","body":"“Tengo que…” → “Me gustaría…” · “Prefiero…” · “Puedo intentar…”","speech":"Ahora reformulá esa frase. No para convencerte de lo contrario, sino para darle más flexibilidad. En lugar de tengo que, probá con me gustaría, prefiero, voy a intentar o sería importante para mí. Esa pequeña diferencia puede cambiar muchísimo el peso emocional de una idea."},
{"label":"REFLEXIÓN","title":"Una regla puede orientarte sin gobernarte","body":"Flexibilidad no es falta de compromiso","speech":"Ser más flexible no significa dejar de tener valores, objetivos o responsabilidades. Significa poder elegir cómo responder sin tratar cada expectativa como una orden. Una regla puede orientarte sin gobernarte."},
{"label":"COMPROMISO · 24 HORAS","title":"Cazá un “debería” en tiempo real","body":"Detectalo · frená · reformulalo con más flexibilidad","speech":"Durante las próximas 24 horas, cada vez que aparezca un debería, frená unos segundos. Preguntate si es una preferencia o una obligación absoluta. Después reformulala con una frase un poco más flexible. No necesitás creerla al cien por ciento todavía. Solo practicar una alternativa."},
{"label":"DÍA 7 COMPLETADO","title":"Hoy empezaste a cuestionar tus reglas internas","body":"7 / 30 · Racha: 7 días 🔥\nMañana: ¿De quién aprendí a hablarme así?","speech":"Completaste el Día 7 de LUMINA. Hoy empezaste a reconocer reglas internas que quizá llevaban mucho tiempo funcionando en automático. Mañana vamos a explorar de dónde aprendiste algunas de esas formas de hablarte y exigirte. Nos vemos en el Día 8."}
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
    d.text((50,1120),"OBSERVÁ · CUESTIONÁ · ELEGÍ",font=font(19,True),fill=PURPLE)
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
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(cf),"-c","copy","LUMINA_Dia7_voz_natural.mp4"],check=True)

if __name__=="__main__": asyncio.run(main())