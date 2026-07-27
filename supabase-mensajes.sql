-- LUMINA: mensajería segura entre pacientes y profesional
create table if not exists public.patient_messages (
  id uuid primary key default gen_random_uuid(),
  patient_id uuid not null references public.patients(id) on delete cascade,
  sender text not null check (sender in ('patient','professional')),
  body text not null check (char_length(body) between 1 and 4000),
  read_at timestamptz,
  created_at timestamptz not null default now()
);

create index if not exists patient_messages_patient_created_idx
  on public.patient_messages(patient_id, created_at desc);

alter table public.patient_messages enable row level security;

-- La profesional autenticada puede leer y escribir todos los mensajes.
drop policy if exists "admin read messages" on public.patient_messages;
create policy "admin read messages" on public.patient_messages
for select to authenticated
using ((select auth.jwt()->>'email') = 'lummina369@gmail.com');

drop policy if exists "admin insert messages" on public.patient_messages;
create policy "admin insert messages" on public.patient_messages
for insert to authenticated
with check (
  (select auth.jwt()->>'email') = 'lummina369@gmail.com'
  and sender = 'professional'
);

drop policy if exists "admin update messages" on public.patient_messages;
create policy "admin update messages" on public.patient_messages
for update to authenticated
using ((select auth.jwt()->>'email') = 'lummina369@gmail.com');

-- Paciente: lista sus mensajes usando el token de sesión privado.
create or replace function public.patient_list_messages(p_token text)
returns table(id uuid, sender text, body text, read_at timestamptz, created_at timestamptz)
language plpgsql security definer set search_path = public
as $$
declare v_patient uuid;
begin
  select ps.patient_id into v_patient
  from public.patient_sessions ps
  join public.patients p on p.id = ps.patient_id
  where ps.session_token = p_token
    and ps.expires_at > now()
    and p.active = true
  limit 1;
  if v_patient is null then raise exception 'Sesión inválida o vencida'; end if;
  update public.patient_messages set read_at = coalesce(read_at, now())
    where patient_id = v_patient and sender = 'professional';
  return query
    select m.id,m.sender,m.body,m.read_at,m.created_at
    from public.patient_messages m
    where m.patient_id = v_patient
    order by m.created_at asc;
end;$$;

create or replace function public.patient_send_message(p_token text, p_body text)
returns jsonb language plpgsql security definer set search_path = public
as $$
declare v_patient uuid; v_body text := trim(p_body);
begin
  if v_body is null or char_length(v_body) < 1 or char_length(v_body) > 4000 then
    return jsonb_build_object('ok',false,'message','El mensaje debe tener entre 1 y 4000 caracteres.');
  end if;
  select ps.patient_id into v_patient
  from public.patient_sessions ps
  join public.patients p on p.id = ps.patient_id
  where ps.session_token = p_token
    and ps.expires_at > now()
    and p.active = true
  limit 1;
  if v_patient is null then return jsonb_build_object('ok',false,'message','Sesión inválida o vencida.'); end if;
  insert into public.patient_messages(patient_id,sender,body) values(v_patient,'patient',v_body);
  return jsonb_build_object('ok',true);
end;$$;

grant execute on function public.patient_list_messages(text) to anon, authenticated;
grant execute on function public.patient_send_message(text,text) to anon, authenticated;
