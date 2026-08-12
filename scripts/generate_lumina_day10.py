import asyncio
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import edge_tts

W,H=720,1280
BG="#FFFAF4"; PURPLE="#7847D8"; LAVENDER="#F6EDFF"; DARK="#18151B"; MUTED="#665F69"
OUT=Path("day10_build"); OUT.mkdir(exist_ok=True)
VOICE="es-AR-ElenaNeural"; RATE="-5%"

SCENES=[
{"label":"DÍA 10 · 10/30","title":"Lo que puedo controlar y lo que no","body":"Distinguir dónde poner tu energía y dónde empezar a soltar","speech":"Bienvenida al Día 10 de LUMINA. Ayer trabajaste en diferenciar expectativas ajenas de expectativas propias. Hoy vamos a mirar algo que puede aliviar mucha carga mental: distinguir qué cosas dependen de vos, cuáles podés influir y cuáles están fuera de tu control."},
{"label":"IDEA CENTRAL","title":"No todo merece la misma cantidad de energía","body":"Preocuparte por algo no significa que puedas controlarlo","speech":"Cuando algo nos importa, es fácil sentir que pensar más, anticipar más o revisar una situación una y otra vez nos va a dar más control. Pero preocupación y control no son lo mismo. A veces gastamos muchísima energía intentando resolver algo que, en realidad, no depende de nosotras."},
{"label":"SÍ DEPENDE DE VOS","title":"Tus decisiones y tus acciones","body":"Lo que decís · lo que hacés · tus límites · tu esfuerzo · dónde ponés tu atención","speech":"Hay cosas que sí están mucho más cerca de tu control: lo que elegís decir, lo que hacés con la información que tenés, los límites que ponés, cómo pedís algo, cuánto esfuerzo decidís invertir y a qué volvés a dirigir tu atención cuando notás que tu mente se engancha."},
{"label":"NO DEPENDE DE VOS","title":"La respuesta final de otras personas o de la realidad","body":"Opiniones · reacciones · decisiones ajenas · el pasado · resultados exactos","speech":"Y hay otras cosas que no podés controlar directamente: lo que otra persona piense de vos, cómo reaccione a un límite, si alguien cambia, decisiones que no te pertenecen, lo que ya pasó o el resultado exacto de algo aunque hayas hecho todo lo posible."},
{"label":"ENTRE MEDIO","title":"También existe la influencia","body":"Podés hacer tu parte sin garantizar el resultado","speech":"Entre controlar y no controlar existe una zona intermedia: la influencia. Podés prepararte para una conversación, comunicarte con claridad, pedir ayuda o entrenar para un objetivo. Todo eso puede aumentar ciertas posibilidades, pero no garantiza lo que va a pasar. Reconocer esa diferencia evita confundir responsabilidad con omnipotencia."},
{"label":"EJEMPLO","title":"Un mensaje sin respuesta","body":"Control: cómo escribís y qué hacés después · No control: cuándo o cómo responde la otra persona","speech":"Imaginá que mandás un mensaje importante y la otra persona tarda en responder. Podés controlar si escribís con claridad, si decidís esperar, si hacés otra actividad o si más tarde preguntás directamente. No podés controlar cuándo responde, qué siente ni qué interpretación hace. Intentar adivinarlo no aumenta tu control; suele aumentar tu ansiedad."},
{"label":"SEÑAL DE ALERTA","title":"¿Estoy intentando controlar lo incontrolable?","body":"“Necesito saber qué piensa” · “Tengo que lograr que entienda” · “No puedo permitir que salga mal”","speech":"Algunas frases pueden avisarte que estás intentando controlar demasiado: necesito saber exactamente qué piensa, tengo que lograr que entienda, no puedo permitir que esto salga mal, necesito que todos estén de acuerdo. Cuando aparezcan, preguntate si estás frente a una acción posible o frente a un resultado que depende también de otras variables."},
{"label":"EJERCICIO CENTRAL","title":"Dividí una hoja en tres zonas","body":"PUEDO CONTROLAR · PUEDO INFLUIR · NO PUEDO CONTROLAR","speech":"Vamos al ejercicio del Día 10. Pensá en una situación que hoy te esté ocupando mucha energía. Dividí una hoja en tres zonas. En la primera escribí lo que sí podés controlar. En la segunda, aquello sobre lo que podés influir pero no garantizar. En la tercera, lo que no depende de vos.","pause_after":5},
{"label":"LLEVÁLO A UNA ACCIÓN","title":"Elegí una sola cosa de la primera zona","body":"¿Qué acción concreta, pequeña y realista podés hacer hoy?","speech":"Ahora mirá solamente la primera zona y elegí una acción concreta. Algo pequeño y realizable. Puede ser mandar un correo, pedir una conversación, poner un límite, descansar antes de decidir, preparar información o dejar de revisar algo por una hora. El objetivo es mover energía desde la preocupación hacia una acción posible.","pause_after":5},
{"label":"SOLTAR NO ES DESENTENDERSE","title":"Aceptar un límite no significa que no te importe","body":"Podés cuidar algo sin controlar cada resultado","speech":"Soltar lo que no controlás no significa volverte indiferente. Podés amar a alguien y no controlar sus decisiones. Podés prepararte mucho y no controlar una evaluación exacta. Podés expresar una necesidad y no controlar la respuesta. Aceptar esos límites puede ayudarte a cuidar mejor la parte que sí te corresponde."},
{"label":"REFLEXIÓN","title":"Responsabilidad no es control total","body":"Hacer tu parte es diferente de garantizar el desenlace","speech":"A veces la autoexigencia nos hace sentir responsables incluso de reacciones ajenas o resultados imprevisibles. Pero responsabilidad no significa control total. Tu tarea puede ser actuar de acuerdo con tus valores, reparar cuando corresponde y aprender de lo que pasa. El resto no siempre depende de vos."},
{"label":"MICROACCIÓN · 24 HORAS","title":"Preguntate: ¿esto me corresponde?","body":"Si sí: una acción · Si puedo influir: hacé tu parte · Si no: volvé a lo que sí depende de vos","speech":"Durante las próximas 24 horas, cuando notes que estás rumiando una situación, probá preguntarte: ¿esto depende de mí, puedo influir o está fuera de mi control? Si depende de vos, elegí una acción. Si podés influir, hacé tu parte sin exigir garantía. Y si no depende de vos, intentá volver tu atención a algo que sí esté en tus manos."},
{"label":"DÍA 10 COMPLETADO","title":"Hoy empezaste a elegir mejor dónde poner tu energía","body":"10 / 30 · Racha: 10 días 🔥\nMañana: Pensar algo no lo convierte en verdad","speech":"Completaste el Día 10 de LUMINA. Hoy practicaste distinguir control, influencia y aquello que no depende de vos. Esta diferencia puede ayudarte a bajar exigencia y a actuar con más claridad. Mañana empezamos una nueva etapa: vamos a trabajar con una idea fundamental, pensar algo no lo convierte en verdad. Nos vemos en el Día 11."}
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
    d.text((50,1120),"DISTINGUÍ · ACTUÁ · SOLTÁ",font=font(19,True),fill=PURPLE)
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
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(cf),"-c","copy","LUMINA_Dia10_voz_natural.mp4"],check=True)

if __name__=="__main__": asyncio.run(main())
