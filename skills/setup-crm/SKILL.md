---
name: setup-crm
description: "Da de alta un cliente nuevo en Twenty CRM (VPS Software Factory) — subdominio, instancia, modelo de datos y doble escritura (P17)"
argument-hint: "<cliente> [--mock]"
disable-model-invocation: true
---

Da de alta al cliente **$ARGUMENTS** en la infraestructura Twenty CRM del Cluster (`[cliente].crm.umohcrew.com`), siguiendo P17 paso a paso. Reglas: nunca inventar el esquema de datos (pedilo si no está en el vault), fiel al esquema dado salvo pedido explícito de mejorarlo, doble escritura obligatoria al cierre. Sin emojis.

Procedimiento:

1. Leé el perfil `$VAULT/.claude/cluster-os.json` (si no existe, sugerí `/cluster-os:setup` y pará). $VAULT sale de ahí. **Gate de identidad:** este comando toca infraestructura externa (VPS, DNS, Docker) — solo lo corre fran. Si el perfil dice sergio o dima, explicá que el alta CRM la ejecuta Franco y pará.

2. Leé `$VAULT/08 SISTEMA/protocolos/protocolo-alta-cliente-crm.md` completo — es la fuente de verdad de este comando, no improvises pasos. Leé también los registros de la primera corrida que el protocolo lista en "Ver también" (VPS/Traefik y modelo de datos Diim) si vas a tocar esos frentes.

3. Confirmá con Franco antes de tocar infraestructura (si no está ya claro en el pedido): nombre del cliente (define el subdominio), si existe un esquema de datos ya diseñado y validado con el cliente (pedí el archivo si no lo tenés — se replica fiel, las mejoras se ofrecen aparte), y si hace falta mock data (flag `--mock`).

4. Ejecutá los pasos 1-7 del protocolo en orden: infraestructura (VPS compartido + DNS + Traefik **file provider**, nunca el provider Docker) → instancia Twenty (nombre de proyecto `twenty-[cliente]`, sin overlap con otros clientes) → backup (pg_dump + cron 3am, retención 14 días) → alta de cuenta (acción humana, no la automatices) → conexión MCP → modelo de datos fiel al esquema → limpieza de módulos (desactivar, no borrar).

5. Si `--mock` está presente, ejecutá el paso 8: datos ficticios cubriendo la variedad de estados del pipeline, mails `@example.com`, y aclará SIEMPRE en el registro que son mock.

6. Cerrá con el paso 9 (doble escritura): registro fechado en `01 REGISTRO/` con el detalle técnico + actualización en `02 PROYECTOS/[Cliente].md`. Chequeá primero si el cliente ya tiene una herramienta de CRM decidida con él (Monday u otra): si es así, aclarar que este Twenty es un piloto técnico de Software Factory y no reemplaza esa decisión.

7. Verificá el criterio de éxito del protocolo antes de reportar terminado: `curl https://[cliente].crm.umohcrew.com/healthz` devuelve `{"status":"ok"}` con certificado válido, los objetos custom se ven vía MCP (`list_object_metadata_names`), no hay overlap de nombres Docker/volúmenes/subdominios, y la doble escritura existe y no contradice decisiones previas del cliente.
