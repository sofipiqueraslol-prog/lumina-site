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
OUT = Path("day5_build")
OUT.mkdir(exist_ok=True)

VOICE = "es-AR-ElenaNeural"
RATE = "-5%"

SCENES = [
    {
        "label": "DÍA 5 · 5/30",
        "title": "Mi iceberg personal",
        "body": "Lo que los demás ven de vos no muestra todo lo que vivís por dentro.",
        "speech": "Bienvenida al Día 5 de LUMINA. En estos primeros días empezaste a observar cómo te tratás, cómo te definís, qué cosas querés para tu vida y con qué ojos te mirás. Hoy vamos a trabajar con una imagen muy simple, pero muy poderosa: tu iceberg personal. La idea es mirar más allá de lo visible para reconocer también todo lo que forma parte de tu experiencia interna."
    },
    {
        "label": "LA PARTE VISIBLE",
        "title": "Lo que los demás suelen ver",
        "body": "Cómo hablás · cómo actuás · cómo reaccionás · qué mostrás",
        "speech": "Cuando vemos un iceberg, solo una parte aparece por encima del agua. Con las personas pasa algo parecido. Hay una parte de vos que los demás pueden observar con facilidad: cómo hablás, cómo actuás, cómo reaccionás, qué mostrás, qué decisiones tomás y qué roles ocupás. Esa parte es real, pero no es toda la historia."
    },
    {
        "label": "DEBAJO DEL AGUA",
        "title": "También existe todo lo que no siempre se ve",
        "body": "Miedos · necesidades · inseguridades · cansancio · deseos · esfuerzo",
        "speech": "Debajo de esa parte visible puede haber mucho más: miedos, necesidades, inseguridades, cansancio, tristeza, deseos, dudas, heridas, expectativas, esfuerzo y formas de protegerte. A veces incluso las personas más cercanas no conocen completamente esa parte. Y no porque estés haciendo algo mal, sino porque ninguna persona puede ver de forma automática todo lo que ocurre dentro de otra."
    },
    {
        "label": "UNA REACCIÓN NO ES TODA LA HISTORIA",
        "title": "Lo visible necesita contexto",
        "body": "Ven una reacción, pero no siempre la historia que hay detrás.",
        "speech": "Por eso puede pasar que alguien vea una reacción, pero no conozca la historia que hay detrás. Puede ver distancia sin conocer el miedo. Puede ver exigencia sin conocer la inseguridad. Puede ver silencio sin saber cuánto estás pensando. Puede ver enojo sin reconocer que debajo también había tristeza o necesidad. Comprender esto no significa justificar cualquier conducta. Significa agregar contexto."
    },
    {
        "label": "EL RIESGO",
        "title": "Quedarte solo con tu parte visible",
        "body": "También vos podés reducirte a una reacción, un rol o una etiqueta.",
        "speech": "El problema aparece cuando incluso vos empezás a mirarte solamente desde la parte visible. Cuando una reacción se convierte en una definición. Cuando un error se transforma en identidad. O cuando la imagen que los demás tienen de vos pesa más que todo lo que sabés de tu mundo interno. Ahí el iceberg se achica, y empezás a juzgarte desde una sola capa de tu experiencia."
    },
    {
        "label": "PREGUNTA DEL DÍA",
        "title": "¿Qué parte de vos casi nadie ve?",
        "body": "¿Qué existe profundamente en vos y no siempre es reconocido?",
        "speech": "Quiero proponerte una pregunta. ¿Qué parte de vos sentís que existe profundamente, pero no siempre es reconocida por los demás, o incluso por vos misma? Puede ser un miedo que escondés, una necesidad que minimizás, un esfuerzo que nadie ve, una sensibilidad que protegés o un deseo que todavía no te animaste a nombrar. No busques una respuesta perfecta. Solo observá qué aparece.",
        "pause_after": 8
    },
    {
        "label": "EJERCICIO CENTRAL",
        "title": "Dibujá tu iceberg",
        "body": "Arriba del agua: lo visible. Debajo del agua: tu experiencia interna.",
        "speech": "Ahora vamos al ejercicio central. Imaginá o dibujá un iceberg dividido por una línea de agua. En la parte de arriba escribí cosas que los demás suelen ver de vos. Podrían aparecer palabras como fuerte, responsable, tranquila, sensible, distante, exigente, divertida o intensa. No importa si son positivas o negativas. Registrá lo que suele quedar visible.",
        "pause_after": 5
    },
    {
        "label": "ARRIBA DEL AGUA",
        "title": "¿Qué imagen suele quedar a la vista?",
        "body": "Roles · conductas · logros · reacciones · formas de mostrarte",
        "speech": "También podés incluir roles, conductas y logros. Por ejemplo: soy la que resuelve, la que escucha, la que trabaja mucho, la que no pide ayuda, la que se muestra fuerte. Fijate qué parte de tu identidad suele recibir más atención porque es la que otros pueden observar con facilidad."
    },
    {
        "label": "DEBAJO DEL AGUA",
        "title": "¿Qué también vivís por dentro?",
        "body": "Emociones · necesidades · miedos · esfuerzos · deseos · contradicciones",
        "speech": "Después pasá a la parte de abajo. Escribí lo que también vivís pero no siempre se nota: emociones profundas, miedos, necesidades, dudas, esfuerzos silenciosos, deseos, contradicciones o cosas que te cuesta pedir. Tal vez debajo de la autosuficiencia exista necesidad de apoyo. Debajo de la exigencia, miedo a fallar. Debajo del silencio, necesidad de sentirte segura antes de hablar."
    },
    {
        "label": "INTEGRAR, NO ESCONDER",
        "title": "No hay una parte falsa y otra verdadera",
        "body": "Ambas forman parte de vos. La clave es no reducirte a una sola capa.",
        "speech": "No se trata de decidir que la parte visible es falsa y la profunda es la verdadera. Las dos forman parte de vos. Tampoco significa que tengas que contarle a todo el mundo lo que sentís o exponer cosas que preferís mantener privadas. El objetivo es que vos puedas reconocerlas. Integrar no es mostrar todo. Integrar es dejar de negar partes de tu propia experiencia."
    },
    {
        "label": "UNA MIRADA MÁS COMPLETA",
        "title": "Soy más que lo que muestro",
        "body": "Y también soy más que lo que otros alcanzan a ver.",
        "speech": "Una autoestima más sana necesita una mirada más completa. Podés reconocer una reacción sin convertirla en toda tu identidad. Podés valorar un logro y al mismo tiempo reconocer cuánto esfuerzo hubo detrás. Podés aceptar que necesitás apoyo sin borrar tu autonomía. Cuanto más completa es la mirada, menos dependés de una sola etiqueta para definirte."
    },
    {
        "label": "COMPROMISO · 24 HORAS",
        "title": "Reconocé una parte invisible",
        "body": "¿Qué esfuerzo, emoción o necesidad merece hoy ser tenida en cuenta?",
        "speech": "Durante las próximas veinticuatro horas quiero que reconozcas una parte de tu iceberg que normalmente pasa desapercibida. Puede ser un esfuerzo que nadie vio, una emoción que minimizaste o una necesidad que te cuesta validar. No necesitás hacer nada extraordinario. Solo nombrarla y decir: esto también forma parte de lo que estoy viviendo."
    },
    {
        "label": "DÍA 5 COMPLETADO",
        "title": "Hoy te miraste con más profundidad",
        "body": "5 / 30 · Racha: 5 días 🔥\nPrimera fase completada · Mañana: El triángulo de mi autoestima",
        "speech": "Hoy te miraste con más profundidad. Reconociste que lo que los demás ven no muestra todo lo que ocurre dentro tuyo, y que tu mundo interno también merece ser tenido en cuenta. Con esto completaste los primeros cinco días de LUMINA y cerraste la primera fase del recorrido. Mañana vamos a empezar a entender cómo se organiza tu autoestima a través de tres elementos muy importantes. Nos vemos en el Día 6."
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

    d.text((50, 1120), "OBSERVÁ · RECONOCÉ · INTEGRÁ", font=font(19, True), fill=PURPLE)
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
        "-c", "copy", "LUMINA_Dia5_voz_natural.mp4"
    ], check=True)


if __name__ == "__main__":
    asyncio.run(main())
