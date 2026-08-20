# LUMINA Premium — standalone

Esta carpeta contiene la versión comercial independiente de LUMINA.

## Regla de aislamiento

- NO modificar ni redeployar el proyecto `lumina-bienestar` usado por pacientes.
- NO cargar, embeber ni depender de `lumina-bienestar-1itnpymg9-lummina369-9311s-projects.vercel.app`.
- LUMINA Premium debe tener su propio frontend, autenticación, base de suscriptores y control de acceso.
- Los datos de suscriptores de bienestar no deben mezclarse con información clínica de pacientes.

## Pago

Plan mensual: 590 UYU.
Checkout actual: https://mpago.la/2gm55ou

## Próximo backend

Crear un proyecto Supabase independiente para autenticación y estado de suscripción. El frontend nunca debe exponer claves privadas o `service_role`. Toda tabla expuesta debe usar RLS.

## Flujo objetivo

1. Landing de LUMINA Premium.
2. Suscripción en Mercado Pago.
3. Confirmación del pago mediante backend/webhook.
4. Creación o activación de cuenta.
5. Login del miembro.
6. Acceso a `app.html` solo con suscripción activa.
7. Si la suscripción deja de estar activa, bloquear el contenido Premium sin afectar la app de pacientes.
