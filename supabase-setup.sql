-- LUMINA: ejecutar completo en Supabase > SQL Editor
create extension if not exists pgcrypto;

create table if not exists public.admins (
  user_id uuid primary key references auth.users(id) on delete cascade,
  email text unique not null
);

create table if not exists public.patients (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  code_hash text not null,
  code_hint text,
  active boolean not null default true,
  expires_at timestamptz,
  created_at timestamptz not null default now(),
  last_access_at timestamptz,
  access_count integer not null default 0
);

create table if not exists public.patient_sessions (
  token uuid primary key default gen_random_uuid(),
  patient_id uuid not null references public.patients(id) on delete cascade,
  expires_at timestamptz not null default now() + interval '30 days',
  created_at timestamptz not null default now()
);

create table if not exists public.access_logs (
  id bigint generated always as identity primary key,
  patient_id uuid references public.patients(id) on delete set null,
  accessed_at timestamptz not null default now(),
  user_agent text
);

alter table public.admins enable row level security;
alter table public.patients enable row level security;
alter table public.patient_sessions enable row level security;
alter table public.access_logs enable row level security;

create or replace function public.is_lumina_admin()
returns boolean language sql stable security definer set search_path=public
as $$ select exists(select 1 from public.admins a where a.user_id=auth.uid() and lower(a.email)='lummina369@gmail.com') $$;

drop policy if exists "admin patients" on public.patients;
create policy "admin patients" on public.patients for all using(public.is_lumina_admin()) with check(public.is_lumina_admin());
drop policy if exists "admin logs" on public.access_logs;
create policy "admin logs" on public.access_logs for select using(public.is_lumina_admin());

create or replace function public.create_patient_access(p_name text,p_plain_code text,p_expires_at timestamptz default null)
returns jsonb language plpgsql security definer set search_path=public as $$
declare v_id uuid;
begin
 if not public.is_lumina_admin() then raise exception 'No autorizado'; end if;
 insert into patients(name,code_hash,code_hint,expires_at)
 values(trim(p_name),crypt(upper(trim(p_plain_code)),gen_salt('bf')),left(upper(trim(p_plain_code)),4)||'••••',p_expires_at)
 returning id into v_id;
 return jsonb_build_object('ok',true,'patient_id',v_id);
end $$;

create or replace function public.patient_login(p_code text,p_user_agent text default null)
returns jsonb language plpgsql security definer set search_path=public as $$
declare p patients%rowtype; s uuid;
begin
 select * into p from patients
 where active=true and (expires_at is null or expires_at>now())
 and code_hash=crypt(upper(trim(p_code)),code_hash)
 limit 1;
 if p.id is null then return jsonb_build_object('ok',false,'message','Código incorrecto, vencido o suspendido.'); end if;
 insert into patient_sessions(patient_id) values(p.id) returning token into s;
 insert into access_logs(patient_id,user_agent) values(p.id,left(coalesce(p_user_agent,''),500));
 update patients set last_access_at=now(),access_count=access_count+1 where id=p.id;
 return jsonb_build_object('ok',true,'session_token',s,'patient_name',p.name);
end $$;

grant execute on function public.patient_login(text,text) to anon,authenticated;
grant execute on function public.create_patient_access(text,text,timestamptz) to authenticated;

-- DESPUÉS de crear la usuaria lummina369@gmail.com en Authentication > Users,
-- ejecutar reemplazando EL_UUID_DE_LA_USUARIA:
-- insert into public.admins(user_id,email)
-- values ('EL_UUID_DE_LA_USUARIA','lummina369@gmail.com');
