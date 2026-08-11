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
OUT = Path("day4_build")
OUT.mkdir(exist_ok=True)

VOICE = "es-AR-ElenaNeural"
RATE = "-5%"

SCENES = [
    {
        "label": "DÍA 4 · 4/30",
        "title": "Mirarme con mis propios ojos",
        "body": "Hoy vamos a observar con qué mirada te estás describiendo.",
        "speech": "Bienvenida al Día 4 de LUMINA. Ayer empezaste a preguntarte qué querés realmente para tu vida. Hoy vamos a mirar algo todavía más íntimo: con qué ojos te estás mirando. Desde muy temprano aprendemos a vernos a través de las reacciones de otras personas. Un comentario, una comparación, una crítica o incluso la falta de reconocimiento pueden empezar a formar una imagen interna."
    },
    {
        "label": "UNA MIRADA APRENDIDA",
        "title": "No empezaste a mirarte en el vacío",
        "body": "Familia · vínculos · escuela · redes · cultura",
        "speech": "La manera en que te ves se fue construyendo con el tiempo. Familia, escuela, amistades, parejas, redes y cultura nos devuelven mensajes sobre cómo somos, cómo deberíamos ser y qué partes de nosotros parecen recibir aprobación. Algunas de esas miradas pueden ayudarnos a conocernos. Otras pueden quedarse adentro incluso cuando ya no nos representan."
    },
    {
        "label": "PREGUNTA CLAVE",
        "title": "¿Yo también me veo así?",
        "body": "Una opinión repetida puede sentirse propia aunque haya empezado afuera.",
        "speech": "Con el tiempo podemos olvidar una pregunta esencial: ¿yo también me veo así? Quizás alguien te hizo sentir que eras demasiado sensible, poco atractiva, difícil, insegura o que nunca eras suficiente. Y cuando una idea aparece durante años, puede empezar a sentirse como si hubiera nacido dentro tuyo."
    },
    {
        "label": "PERCEPCIÓN ≠ IDENTIDAD",
        "title": "La mirada de alguien no es una definición objetiva",
        "body": "Toda percepción está atravesada por historia, expectativas, necesidades y límites.",
        "speech": "Pero que alguien haya tenido una percepción sobre vos no significa que esa percepción sea una definición objetiva. Todos miramos a los demás desde nuestra propia historia, nuestras expectativas, nuestras necesidades y nuestros límites. Una crítica puede hablar de algo que hiciste, pero también puede estar atravesada por la sensibilidad o las expectativas de quien la formuló."
    },
    {
        "label": "RECUPERAR TU MIRADA",
        "title": "No idealizar. Integrar.",
        "body": "Una mirada más completa puede incluir fortalezas, dificultades, matices y contexto.",
        "speech": "Por eso, parte de conocerte implica empezar a recuperar tu propia mirada. No una mirada idealizada. No se trata de convencerte de que todo en vos es perfecto. Se trata de construir una mirada más completa, más precisa y más justa. Una mirada que pueda reconocer lo que te cuesta sin borrar todo lo demás que también sos."
    },
    {
        "label": "PREGUNTA DEL DÍA",
        "title": "Si dejaras afuera las opiniones ajenas…",
        "body": "¿Cómo te describirías vos?",
        "speech": "Hoy quiero preguntarte algo. Si durante unos minutos pudieras dejar afuera todas las opiniones que recibiste, ¿cómo te describirías vos? No busques una versión linda ni una versión perfecta. Intentá responder desde tu experiencia actual. ¿Qué reconocés en vos cuando nadie más está definiéndote?",
        "pause_after": 8
    },
    {
        "label": "EJERCICIO CENTRAL",
        "title": "Tres cosas que yo reconozco en mí",
        "body": "Elegí características que conocés por experiencia propia, no porque alguien te las dijo.",
        "speech": "Ahora vamos al ejercicio central. Primero escribí tres características tuyas que reconocés porque las experimentás vos, no simplemente porque alguien te las dijo. Puede ser algo que valorás, algo que te cuesta o un modo habitual de reaccionar. Lo importante es que puedas decir: esto lo reconozco en mí por mi propia experiencia.",
        "pause_after": 6
    },
    {
        "label": "SEGUNDA PARTE",
        "title": "Tres etiquetas que aprendí de otros",
        "body": "¿Quién me la transmitió? · ¿Cuándo empezó? · ¿La sigo creyendo?",
        "speech": "Después escribí tres etiquetas que sentís que aprendiste de otras personas. Tal vez aparezcan palabras como insegura, complicada, sensible, débil, fría, intensa o egoísta. Al lado de cada una anotá, si podés, de dónde creés que vino. Quién te la transmitió, cuándo empezó y cuánto seguís creyéndola hoy."
    },
    {
        "label": "PONELA A PRUEBA",
        "title": "¿Siempre soy así?",
        "body": "¿Sigue describiéndome? · ¿En qué situaciones no se cumple? · ¿Qué matiz falta?",
        "speech": "Ahora mirá cada etiqueta y preguntate: ¿esto sigue describiéndome? ¿Siempre soy así? ¿En qué situaciones esta etiqueta no se cumple? ¿Qué información está dejando afuera? Cuando una palabra es demasiado absoluta, suele perder precisión. Y cuando perdemos precisión, podemos terminar juzgándonos más de lo que la situación realmente justifica."
    },
    {
        "label": "MÁS PRECISO · MÁS JUSTO · MÁS MÍO",
        "title": "No reemplaces una etiqueta por una frase vacía",
        "body": "Buscá una descripción que incluya contexto y matices.",
        "speech": "El objetivo no es reemplazar una etiqueta negativa por una frase positiva vacía. No necesitamos pasar de soy insegura a soy completamente segura. Buscamos algo más realista. Una descripción que incluya contexto, matices y evidencia. Algo que te permita verte con mayor precisión, no simplemente sentirte mejor durante unos segundos."
    },
    {
        "label": "EJEMPLO",
        "title": "“Soy insegura” → una descripción más justa",
        "body": "Hay situaciones en las que dudo de mí y otras en las que puedo confiar en mis decisiones.",
        "speech": "Por ejemplo, en lugar de decir soy insegura, quizás una descripción más justa sería: hay situaciones en las que dudo de mí y otras en las que puedo confiar en mis decisiones. Fijate la diferencia. La dificultad sigue estando ahí, pero dejó de convertirse en toda tu identidad. Una mirada más justa incluye lo que te cuesta sin borrar tus recursos, tus cambios y tus excepciones."
    },
    {
        "label": "COMPROMISO · 24 HORAS",
        "title": "¿Esto es realmente lo que yo pienso de mí?",
        "body": "Cuando aparezca una crítica interna, observá si reconocés una voz, una expectativa o una mirada aprendida.",
        "speech": "Durante las próximas veinticuatro horas quiero que observes una situación en la que aparezca dentro de tu cabeza una mirada que parece venir de otra persona. Puede ser una crítica, una comparación o una frase automática. Cuando aparezca, preguntate: ¿esto es realmente lo que yo pienso de mí? ¿O estoy repitiendo una mirada que aprendí? No hace falta responder perfectamente. Solo empezá a distinguir las voces."
    },
    {
        "label": "DÍA 4 COMPLETADO",
        "title": "Hoy empezaste a recuperar tus propios ojos",
        "body": "4 / 30 · Racha: 4 días 🔥\nMañana: Mi iceberg personal",
        "speech": "Hoy empezaste a recuperar tus propios ojos. A reconocer que podés observar tus dificultades sin convertirlas en todo lo que sos, y que no toda mirada que llevás adentro nació realmente de vos. Completaste el Día 4 de LUMINA. Mañana vamos a explorar algo que todos tenemos: lo que mostramos y lo que casi nadie ve. Nos vemos en el Día 5."
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
        for word in words[1:]:
            test = cur + " " + word
            if draw.textbbox((0, 0), test, font=fnt)[2] <= max_width:
                cur = test
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def draw_multiline(draw, x, y, lines, fnt, fill, spacing=12):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        bbox = draw.textbbox((x, y), line if line else "Ag", font=fnt)
        y += (bbox[3] - bbox[1]) + spacing
    return y


def make_slide(scene, idx):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((50, 55), "LUMINA", font=font(28, True), fill=PURPLE)
    d.rounded_rectangle((560, 45, 670, 90), radius=22, fill=LAVENDER)
    d.text((615, 67), f"{idx+1}/13", font=font(18, True), fill=PURPLE, anchor="mm")
    d.rounded_rectangle((50, 112, 670, 122), radius=5, fill="#E9DDF8")
    prog = max(30, int(620 * (idx + 1) / 13))
    d.rounded_rectangle((50, 112, 50 + prog, 122), radius=5, fill=PURPLE)
    d.text((50, 170), scene["label"], font=font(22, True), fill=PURPLE)

    title_font = font(48 if len(scene["title"]) < 48 else 42, True)
    title_lines = wrap_px(d, scene["title"], title_font, 620)
    y = draw_multiline(d, 50, 225, title_lines, title_font, DARK, spacing=12)
    y += 35

    body_font = font(29)
    body_lines = wrap_px(d, scene["body"], body_font, 540)
    line_h = 42
    card_h = max(210, 80 + len(body_lines) * line_h)
    if y + card_h > 1030:
        card_h = 1030 - y
    d.rounded_rectangle((50, y, 670, y + card_h), radius=32, fill=LAVENDER)
    by = y + 42
    for line in body_lines:
        d.text((90, by), line, font=body_font, fill=DARK)
        by += line_h

    d.text((50, 1120), "OBSERVÁ · ESCRIBÍ · CUESTIONÁ", font=font(19, True), fill=PURPLE)
    d.text((50, 1165), "LUMINA · 30 días para volver a vos", font=font(17), fill=MUTED)
    return img


async def synth(text, out_mp3):
    await edge_tts.Communicate(text=text, voice=VOICE, rate=RATE).save(str(out_mp3))


def duration(path):
    result = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path)
    ], capture_output=True, text=True, check=True)
    return float(result.stdout.strip())


def make_segment(img_path, audio_path, out_path):
    dur = duration(audio_path)
    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-framerate", "30", "-i", str(img_path), "-i", str(audio_path),
        "-vf", "scale=720:1280,format=yuv420p", "-c:v", "libx264", "-preset", "veryfast", "-tune", "stillimage",
        "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2", "-t", f"{dur:.3f}", "-shortest", str(out_path)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def add_pause(img_path, seconds, out_path):
    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-framerate", "30", "-i", str(img_path),
        "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-vf", "scale=720:1280,format=yuv420p", "-c:v", "libx264", "-preset", "veryfast", "-tune", "stillimage",
        "-c:a", "aac", "-b:a", "160k", "-t", str(seconds), "-shortest", str(out_path)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


async def main():
    concat_entries = []
    for i, scene in enumerate(SCENES):
        img_path = OUT / f"slide_{i:02d}.png"
        audio_path = OUT / f"voice_{i:02d}.mp3"
        seg_path = OUT / f"seg_{i:02d}.mp4"
        make_slide(scene, i).save(img_path)
        await synth(scene["speech"], audio_path)
        make_segment(img_path, audio_path, seg_path)
        concat_entries.append(seg_path)
        if scene.get("pause_after"):
            pause_path = OUT / f"pause_{i:02d}.mp4"
            add_pause(img_path, scene["pause_after"], pause_path)
            concat_entries.append(pause_path)

    concat_file = OUT / "concat.txt"
    concat_file.write_text("\n".join(f"file '{p.resolve()}'" for p in concat_entries), encoding="utf-8")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-c", "copy", "LUMINA_Dia4_voz_natural.mp4"
    ], check=True)


if __name__ == "__main__":
    asyncio.run(main())
