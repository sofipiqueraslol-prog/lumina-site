import asyncio
import os
import subprocess
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import edge_tts

W, H = 720, 1280
BG = "#FFFAF4"
PURPLE = "#7847D8"
LAVENDER = "#F6EDFF"
DARK = "#18151B"
MUTED = "#665F69"
WHITE = "#FFFFFF"
OUT = Path("day2_build")
OUT.mkdir(exist_ok=True)

VOICE = "es-AR-ElenaNeural"
RATE = "-5%"

SCENES = [
    {
        "label": "DÍA 2 · 2/30",
        "title": "¿Quién soy cuando dejo de definirme por los demás?",
        "body": "Hoy vamos a separar quién sos de las etiquetas, roles y opiniones que aprendiste a cargar.",
        "speech": "Bienvenida al Día 2 de LUMINA. Ayer empezamos a observar cómo te tratás. Hoy vamos a mirar algo igual de importante: cómo te definís. Muchas veces creemos que sabemos quiénes somos, pero en realidad repetimos ideas, etiquetas o miradas que fuimos recibiendo con el tiempo. Y si queremos construir una autoestima más sana, primero necesitamos distinguir quién sos vos de todo lo que aprendiste a creer sobre vos."
    },
    {
        "label": "AUTOCONCEPTO",
        "title": "La imagen que construís sobre vos",
        "body": "Cómo me veo · Cómo me describo · Qué creo que soy",
        "speech": "Todos construimos una imagen de nosotros mismos. A esa imagen la llamamos autoconcepto. Es la manera en que te describís, cómo pensás quién sos, cómo te ves en tus vínculos, en tu trabajo o estudio, en tu cuerpo y en tus emociones. Es como un mapa interno que usamos para explicarnos quiénes somos. Y ese mapa influye en cómo interpretamos lo que nos pasa."
    },
    {
        "label": "¿CÓMO SE FORMA?",
        "title": "Tu mirada no nació en el vacío",
        "body": "Experiencias + vínculos + mensajes recibidos + expectativas",
        "speech": "Ese mapa no se construye solamente con lo que vos descubrís de vos misma. También se forma con experiencias, vínculos, mensajes recibidos y expectativas. Familia, escuela, amistades, parejas, redes y cultura nos devuelven miradas. Algunas nos ayudan a conocernos. Otras pueden convertirse en etiquetas que repetimos durante años. A veces una frase ajena se instala tanto que dejamos de preguntarnos si realmente nos representa."
    },
    {
        "label": "ETIQUETAS",
        "title": "Cuando una frase empieza a sentirse como verdad",
        "body": "“Sos sensible” · “Sos complicada” · “Sos intensa” · “Sos insegura”",
        "speech": "Quizás alguna vez escuchaste frases como: sos demasiado sensible, sos complicada, nunca terminás nada, sos intensa, sos insegura. Cuando una frase aparece muchas veces, puede empezar a sentirse como una verdad. Pero que una idea se repita no significa que describa toda tu identidad. Una mirada puede contener algo de información y, al mismo tiempo, ser incompleta, exagerada o estar atravesada por la historia de quien la dijo."
    },
    {
        "label": "HECHO ≠ IDENTIDAD",
        "title": "“Me equivoqué” no es lo mismo que “soy un desastre”",
        "body": "Una conducta puntual no tiene que convertirse en una definición total de vos.",
        "speech": "Imaginá una situación cotidiana. Cometés un error pequeño, te olvidás de responder algo, llegás tarde o dejás algo sin terminar. Y aparece automáticamente la frase: soy un desastre. Fijate qué pasó. No dijiste: hoy me equivoqué. Dijiste: soy un desastre. Una conducta puntual se transformó en identidad. Y cuando hacemos eso una y otra vez, terminamos usando momentos aislados como pruebas de quién creemos que somos."
    },
    {
        "label": "OBSERVÁ EL PATRÓN",
        "title": "La etiqueta empieza a buscar pruebas",
        "body": "HECHO → ETIQUETA → FILTRO → MÁS “PRUEBAS”",
        "speech": "Esto es importante porque cuando convertimos hechos en etiquetas absolutas, empezamos a interpretar muchas situaciones desde esa etiqueta. Si pienso que soy incapaz, cada error parece demostrarlo. Si pienso que soy complicada, cualquier conflicto puede convertirse en otra prueba. El problema no es observar una dificultad. El problema es reducir toda nuestra identidad a ella. Una dificultad puede ser real sin convertirse en una sentencia sobre tu valor."
    },
    {
        "label": "PREGUNTA DEL DÍA",
        "title": "¿Qué cosas creés de vos porque realmente las sentís?",
        "body": "¿Y cuáles porque las escuchaste demasiadas veces?",
        "speech": "Por eso quiero que te hagas esta pregunta: ¿qué cosas creés de vos porque realmente las sentís y cuáles porque las escuchaste demasiadas veces? No respondas rápido. Dejá que aparezcan palabras, recuerdos y voces. A veces es difícil distinguir nuestra propia mirada de las miradas que fuimos incorporando. Lo importante hoy no es encontrar una respuesta perfecta, sino empezar a notar de dónde vienen algunas de tus definiciones.",
        "pause_after": 8
    },
    {
        "label": "TU MAPA DE IDENTIDAD",
        "title": "Completá sin buscar respuestas lindas",
        "body": "Como persona… · En mis vínculos… · En trabajo/estudio… · Con mi cuerpo… · Cuando fracaso… · Cuando estoy sola…",
        "speech": "Ahora vamos a trabajar con tu mapa de identidad. Completá, sin buscar respuestas perfectas: como persona, yo soy. En mis vínculos, yo soy. En mi trabajo o estudio, yo soy. Con mi cuerpo, yo soy. Cuando fracaso, yo soy. Cuando estoy sola, yo soy. Escribí lo primero que aparezca. No busques que suene lindo. Buscamos honestidad. Después observá si aparecen palabras muy duras, absolutas o que parecen venir de otras personas.",
        "pause_after": 10
    },
    {
        "label": "EJERCICIO CENTRAL",
        "title": "Las etiquetas que aprendí a cargar",
        "body": "Etiqueta · ¿Quién me la transmitió? · ¿La sigo creyendo? · ¿Describe toda mi identidad?",
        "speech": "Después, pensá en algunas etiquetas que otras personas usaron para describirte. Por ejemplo: sensible, complicada, indecisa, intensa, débil. Y preguntate: ¿quién me transmitió esta idea? ¿Cuántas veces la escuché? ¿La sigo creyendo? ¿Esto describe toda mi identidad o solo una conducta, una etapa o la mirada de otra persona? Tal vez descubras que algunas palabras que usás para definirte nunca fueron realmente tuyas."
    },
    {
        "label": "RELECTURA MÁS JUSTA",
        "title": "No negar. Precisar.",
        "body": "“Sensible” → Percibo mucho\n“Indecisa” → Necesito tiempo para elegir\n“Intensa” → Vivo algunas emociones con fuerza",
        "speech": "Ahora probemos una relectura más justa. Soy sensible puede convertirse en: percibo mucho y algunas cosas me afectan profundamente. Soy indecisa puede convertirse en: a veces necesito tiempo para elegir. Soy intensa puede convertirse en: vivo algunas emociones con mucha fuerza. Soy débil puede convertirse en: hay algo que me está costando, y eso no define mi capacidad completa. Fijate que no estamos inventando una versión idealizada de vos. Estamos buscando una descripción más precisa y menos condenatoria."
    },
    {
        "label": "IDEA CLAVE",
        "title": "Una descripción no tiene que convertirse en una condena",
        "body": "No sos solamente una palabra, un error, una etapa ni la opinión de alguien.",
        "speech": "No estamos negando partes tuyas. Tampoco estamos reemplazando una frase negativa por una frase positiva vacía. Estamos haciendo algo más profundo: dejar de reducir toda tu identidad a una sola palabra. Podés ser sensible en algunas situaciones, insegura en otras, decidida en muchas más y valiente en momentos que quizás ni siquiera registrás. La identidad es mucho más amplia que la etiqueta que aparece cuando estás frustrada con vos misma."
    },
    {
        "label": "COMPROMISO · 24 HORAS",
        "title": "Cambiá la etiqueta por una descripción",
        "body": "“Soy un desastre” → “Hoy algo me salió mal”\n“Soy insegura” → “En esta situación me sentí insegura”",
        "speech": "Para las próximas veinticuatro horas, observá cada vez que aparezca una etiqueta absoluta. En lugar de soy un desastre, probá: hoy algo me salió mal. En lugar de soy insegura, probá: en esta situación me sentí insegura. En lugar de soy débil, preguntate: ¿qué parte de esto me está costando? Cambiar el lenguaje no borra lo que pasó. Te ayuda a mirar lo que pasó sin convertirlo automáticamente en una definición total de vos."
    },
    {
        "label": "DÍA 2 COMPLETADO",
        "title": "Hoy empezaste a separar quién sos de lo que otros dijeron de vos",
        "body": "2 / 30 · Racha: 2 días 🔥\nMañana: Lo que quiero para mi vida",
        "speech": "Cambiar el lenguaje cambia la manera en que interpretamos nuestra identidad. Hoy empezaste a separar quién sos de lo que otros dijeron de vos. Y eso ya es una forma de volver a mirarte con más precisión. Completaste el Día 2. Mañana vamos a trabajar con otra pregunta importante: ¿qué quiero para mi vida? Nos vemos en el Día 3."
    },
]


def font(size, bold=False):
    path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(path, size)


def wrap_px(draw, text, fnt, max_width):
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for w in words[1:]:
            test = cur + " " + w
            if draw.textbbox((0,0), test, font=fnt)[2] <= max_width:
                cur = test
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def draw_multiline(draw, x, y, lines, fnt, fill, spacing=12, anchor=None):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill, anchor=anchor)
        bbox = draw.textbbox((x, y), line if line else "Ag", font=fnt, anchor=anchor)
        y += (bbox[3]-bbox[1]) + spacing
    return y


def make_slide(scene, idx):
    img = Image.new("RGB", (W,H), BG)
    d = ImageDraw.Draw(img)
    # top brand
    d.text((50,55), "LUMINA", font=font(28, True), fill=PURPLE)
    d.rounded_rectangle((560,45,670,90), radius=22, fill=LAVENDER)
    d.text((615,67), f"{idx+1}/13", font=font(18, True), fill=PURPLE, anchor="mm")
    # progress
    d.rounded_rectangle((50,112,670,122), radius=5, fill="#E9DDF8")
    prog = max(30, int(620*(idx+1)/13))
    d.rounded_rectangle((50,112,50+prog,122), radius=5, fill=PURPLE)
    # label
    d.text((50,170), scene["label"], font=font(22, True), fill=PURPLE)
    # title
    title_font = font(48 if len(scene["title"]) < 48 else 42, True)
    title_lines = wrap_px(d, scene["title"], title_font, 620)
    y = draw_multiline(d, 50, 225, title_lines, title_font, DARK, spacing=12)
    y += 35
    # card
    body_font = font(29, False)
    body_lines = wrap_px(d, scene["body"], body_font, 540)
    line_h = 42
    card_h = max(210, 80 + len(body_lines)*line_h)
    if y + card_h > 1030:
        card_h = 1030-y
    d.rounded_rectangle((50,y,670,y+card_h), radius=32, fill=LAVENDER)
    by = y + 42
    for line in body_lines:
        d.text((90,by), line, font=body_font, fill=DARK)
        by += line_h
    # small therapeutic cue
    d.text((50,1120), "OBSERVÁ · ESCRIBÍ · CUESTIONÁ", font=font(19, True), fill=PURPLE)
    d.text((50,1165), "LUMINA · 30 días para volver a vos", font=font(17), fill=MUTED)
    return img


async def synth(text, out_mp3):
    comm = edge_tts.Communicate(text=text, voice=VOICE, rate=RATE)
    await comm.save(str(out_mp3))


def duration(path):
    r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",str(path)], capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def make_segment(img_path, audio_path, out_path, extra=0):
    dur = duration(audio_path) + extra
    subprocess.run([
        "ffmpeg","-y","-loop","1","-framerate","30","-i",str(img_path),"-i",str(audio_path),
        "-vf","scale=720:1280,format=yuv420p","-c:v","libx264","-preset","veryfast","-tune","stillimage",
        "-c:a","aac","-b:a","160k","-ar","48000","-ac","2","-t",f"{dur:.3f}","-shortest",str(out_path)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def add_pause(img_path, seconds, out_path):
    subprocess.run([
        "ffmpeg","-y","-loop","1","-framerate","30","-i",str(img_path),
        "-f","lavfi","-i","anullsrc=r=48000:cl=stereo",
        "-vf","scale=720:1280,format=yuv420p","-c:v","libx264","-preset","veryfast","-tune","stillimage",
        "-c:a","aac","-b:a","160k","-t",str(seconds),"-shortest",str(out_path)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


async def main():
    concat_entries = []
    for i, scene in enumerate(SCENES):
        img_path = OUT / f"slide_{i:02d}.png"
        make_slide(scene, i).save(img_path)
        audio_path = OUT / f"voice_{i:02d}.mp3"
        await synth(scene["speech"], audio_path)
        seg_path = OUT / f"seg_{i:02d}.mp4"
        make_segment(img_path, audio_path, seg_path)
        concat_entries.append(seg_path)
        if scene.get("pause_after"):
            pause_path = OUT / f"pause_{i:02d}.mp4"
            add_pause(img_path, scene["pause_after"], pause_path)
            concat_entries.append(pause_path)

    list_path = OUT / "concat.txt"
    list_path.write_text("\n".join([f"file '{p.resolve()}'" for p in concat_entries]))
    output = Path("LUMINA_Dia2_voz_natural.mp4")
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(list_path),"-c","copy",str(output)], check=True)
    print(output.resolve())
    print("duration", duration(output))

if __name__ == "__main__":
    asyncio.run(main())
