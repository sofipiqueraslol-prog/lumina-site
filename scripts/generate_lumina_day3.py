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
OUT = Path("day3_build")
OUT.mkdir(exist_ok=True)

VOICE = "es-AR-ElenaNeural"
RATE = "-5%"

SCENES = [
    {
        "label": "DÍA 3 · 3/30",
        "title": "Lo que quiero para mi vida",
        "body": "Hoy vamos a diferenciar lo que deseás de lo que sentís que deberías querer.",
        "speech": "Bienvenida al Día 3 de LUMINA. En estos primeros días empezaste a observar cómo te tratás y cómo te definís. Hoy vamos a mirar otra pregunta muy importante: qué querés para tu vida. Parece una pregunta sencilla, pero muchas veces nuestras respuestas están mezcladas con expectativas, costumbre, miedo o necesidad de aprobación."
    },
    {
        "label": "LO QUE QUIERO VS. LO QUE DEBERÍA QUERER",
        "title": "No todo deseo nació en vos",
        "body": "Expectativas · costumbre · miedo · aprobación",
        "speech": "Hay cosas que deseamos de verdad. Y hay otras que perseguimos porque sentimos que deberíamos quererlas. Tal vez elegiste una meta porque era lo esperable. Tal vez sostenés una forma de vivir porque cambiarla decepcionaría a alguien. Y entonces podemos terminar avanzando mucho, pero en una dirección que no se siente completamente nuestra."
    },
    {
        "label": "DOS PREGUNTAS DISTINTAS",
        "title": "¿Qué debería hacer? → ¿Qué quiero construir?",
        "body": "La primera suele traer exigencia. La segunda necesita honestidad.",
        "speech": "Por eso hay una diferencia importante entre preguntarte qué debería hacer y preguntarte qué quiero construir. La primera pregunta suele venir acompañada de exigencia. La segunda necesita honestidad. No siempre podemos elegir todo lo que nos pasa, pero sí podemos empezar a reconocer qué dirección se siente más coherente con nosotros."
    },
    {
        "label": "UN EJEMPLO COTIDIANO",
        "title": "Avanzar mucho no siempre significa avanzar hacia algo propio",
        "body": "Carrera · vínculo · cuerpo · éxito · estilo de vida",
        "speech": "Imaginá que llevás años persiguiendo una meta porque siempre pensaste que era lo correcto. Puede ser una carrera, una forma de vincularte, una imagen corporal, una idea de éxito o un estilo de vida. Desde afuera todo puede parecer lógico. Pero por dentro puede aparecer cansancio, desconexión o una sensación difícil de explicar."
    },
    {
        "label": "NO TODO CANSANCIO SIGNIFICA ABANDONAR",
        "title": "Primero preguntate de dónde salió la meta",
        "body": "¿La elegí? · ¿La heredé? · ¿La sostengo por miedo? · ¿La sostengo por aprobación?",
        "speech": "Eso no necesariamente significa que tengas que abandonar esa meta. Significa que vale la pena preguntarte de dónde salió. ¿La elegiste? ¿La heredaste? ¿La sostenés porque todavía te representa o porque cambiar de dirección se siente demasiado incómodo? La idea de hoy no es tomar decisiones impulsivas. Es mirar con más claridad."
    },
    {
        "label": "PREGUNTA DEL DÍA",
        "title": "¿Qué parte de tu vida elegís realmente?",
        "body": "¿Y qué parte sostenés porque sentís que deberías?",
        "speech": "Entonces quiero dejarte una pregunta para hoy. ¿Qué parte de tu vida elegís realmente y qué parte estás sosteniendo solamente porque sentís que deberías? No respondas rápido. A veces esta pregunta necesita un poco de silencio. Y a veces la primera respuesta que aparece es justamente la que solemos evitar.",
        "pause_after": 8
    },
    {
        "label": "EJERCICIO CENTRAL",
        "title": "Mi vida, según yo",
        "body": "No busques respuestas lindas. Buscá respuestas tuyas.",
        "speech": "Ahora vamos al ejercicio central del Día 3. Quiero que respondas estas preguntas con sinceridad. No busques respuestas perfectas ni respuestas que suenen bien. Buscá respuestas tuyas. A veces empezar a formular una pregunta con honestidad ya es una forma de volver a vos."
    },
    {
        "label": "PREGUNTAS 1 Y 2",
        "title": "¿Qué me hace bien? ¿Qué quiero vivir más?",
        "body": "1. ¿Qué cosas de mi vida me hacen genuinamente bien?\n2. ¿Qué me gustaría experimentar más durante los próximos años?",
        "speech": "Primero: ¿qué cosas de tu vida te hacen genuinamente bien? Pensá en momentos, vínculos, actividades, lugares o formas de vivir en las que sentís más conexión con vos. Segundo: ¿qué te gustaría experimentar más durante los próximos años? No pienses solamente en logros. También podés pensar en calma, libertad, vínculo, creatividad, aprendizaje o disfrute.",
        "pause_after": 5
    },
    {
        "label": "PREGUNTAS 3, 4 Y 5",
        "title": "Miedo, postergación y verdad",
        "body": "¿Qué intentaría sin tanto miedo? · ¿Qué deseo postergué? · ¿Qué parte de mi vida necesita más verdad?",
        "speech": "Tercero: ¿qué intentarías si el miedo a equivocarte tuviera menos poder sobre vos? Cuarto: ¿qué deseo venís postergando por priorizar expectativas ajenas? Y quinto: ¿qué parte de tu vida sentís que necesita hoy un poco más de verdad? Podés detener el video si necesitás más tiempo para escribir.",
        "pause_after": 8
    },
    {
        "label": "PROFUNDIZÁ UNA RESPUESTA",
        "title": "¿Lo quiero yo… o quiero sentir que hago lo correcto?",
        "body": "Elegí una respuesta y observá qué necesidad hay detrás.",
        "speech": "Ahora elegí una de tus respuestas y hacete una pregunta más: ¿esto lo quiero yo o quiero sentir que estoy haciendo lo correcto? No siempre es fácil distinguirlo. Muchas veces ambas cosas aparecen mezcladas. Pero cuanto más te hacés esta pregunta, más empieza a aclararse tu dirección interna."
    },
    {
        "label": "UNA VERDAD PEQUEÑA PUEDE CAMBIAR DIRECCIÓN",
        "title": "Observar no significa cambiar toda tu vida hoy",
        "body": "Reconocer primero. Decidir después.",
        "speech": "Reconectar con lo que querés no significa romper con todo, dejar tu vida actual o tomar decisiones impulsivas. Significa empezar a identificar en qué lugares estás siendo fiel a vos y en cuáles te estás alejando. A veces un cambio importante no empieza con una gran decisión. Empieza con una verdad pequeña que dejás de ignorar."
    },
    {
        "label": "COMPROMISO · 24 HORAS",
        "title": "¿Lo deseo o siento que debería?",
        "body": "Usá esta pregunta en una decisión cotidiana durante las próximas 24 horas.",
        "speech": "Para cerrar el Día 3, quiero proponerte un compromiso simple. Durante las próximas veinticuatro horas, prestá atención a una situación en la que tengas que elegir algo y preguntate: ¿lo deseo o siento que debería? No hace falta cambiar nada hoy. Solo observarlo con honestidad. Ese pequeño espacio entre la exigencia y tu deseo puede darte mucha información."
    },
    {
        "label": "DÍA 3 COMPLETADO",
        "title": "Hoy empezaste a mirar tu vida con tus propios criterios",
        "body": "3 / 30 · Racha: 3 días 🔥\nMañana: Mirarme con mis propios ojos",
        "speech": "Hoy empezaste a mirar tu vida con una pregunta distinta. No todo lo que perseguís nació necesariamente de un deseo propio, y reconocerlo no te obliga a cambiarlo todo. Primero necesitás saber qué parte de tu vida realmente elegiste. Completaste el Día 3 de LUMINA. Mañana vamos a trabajar con otra pregunta: cómo me veo cuando dejo de mirarme con los ojos de los demás. Nos vemos en el Día 4."
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
    d.text((50, 1120), "OBSERVÁ · ESCRIBÍ · ELEGÍ", font=font(19, True), fill=PURPLE)
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
        "-c", "copy", "LUMINA_Dia3_voz_natural.mp4"
    ], check=True)


if __name__ == "__main__":
    asyncio.run(main())
