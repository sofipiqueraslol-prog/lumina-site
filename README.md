# LUMINA — acceso privado para pacientes

Administradora autorizada: **lummina369@gmail.com**

## Archivos

- `index.html`: ingreso de pacientes con código individual.
- `admin.html`: cuenta superior para crear, activar y suspender accesos.
- `app.html`: valida la sesión antes de abrir LUMINA Bienestar.
- `config.js`: conexión con Supabase.
- `supabase-setup.sql`: tablas, permisos, códigos y registro de ingresos.

## Activación

1. Abrir el proyecto de Supabase.
2. En **SQL Editor**, ejecutar completo `supabase-setup.sql`.
3. En **Authentication > Users**, crear `lummina369@gmail.com` con una contraseña privada.
4. Copiar el UUID de esa usuaria y ejecutar la instrucción final indicada en el SQL.
5. En **Project Settings > API**, copiar el Project URL y la anon public key.
6. Reemplazar los marcadores dentro de `config.js`.
7. Conectar este repositorio a Vercel y publicar.

## Datos visibles en el panel

- paciente o alias;
- estado activo o suspendido;
- vencimiento opcional;
- último acceso;
- cantidad de ingresos;
- registro reciente y tipo de dispositivo.

Los ejercicios terapéuticos continúan guardándose localmente en el navegador del paciente.
