window.LUMINA_CONFIG = {
  SUPABASE_URL: "https://gwyzqpfeetlisxhgeiyq.supabase.co",
  SUPABASE_ANON_KEY: "sb_publishable_I7PmmPW_W1iewtF-tGbLAw_mcJ-qif7",
  ADMIN_EMAIL: "lummina369@gmail.com"
};

// En el panel profesional, una fecha de vencimiento debe durar hasta el final del día.
setTimeout(() => {
  const createButton = document.getElementById('create');
  const nameInput = document.getElementById('patientName');
  const expiresInput = document.getElementById('expires');
  const output = document.getElementById('newCode');
  if (!createButton || !nameInput || !expiresInput || !output || typeof sb === 'undefined') return;

  createButton.onclick = async () => {
    const name = nameInput.value.trim();
    if (!name) return alert('Escribí un nombre o alias');

    const code = 'LUM-' + crypto.getRandomValues(new Uint32Array(1))[0]
      .toString(36).toUpperCase().slice(0, 6);

    let expiresAt = null;
    if (expiresInput.value) {
      expiresAt = new Date(expiresInput.value + 'T23:59:59.999').toISOString();
    }

    const { error } = await sb.rpc('create_patient_access', {
      p_name: name,
      p_plain_code: code,
      p_expires_at: expiresAt
    });

    if (error) return alert(error.message);
    output.innerHTML = `Código creado para <b>${esc(name)}</b>: <span class="code">${code}</span><br><small>Copialo ahora. Se muestra una sola vez.</small>`;
    nameInput.value = '';
    load();
  };
}, 0);
