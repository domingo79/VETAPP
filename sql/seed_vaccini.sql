-- ============================================================
-- seed_vaccini.sql
-- Catalogo vaccini standard per cane, gatto e cavallo.
-- Esegui nell'SQL Editor di Supabase DOPO aver applicato schema.sql
-- ============================================================

INSERT INTO public.vaccini_catalogo (nome, specie, tipo, descrizione) VALUES

-- ── CANE – obbligatori ────────────────────────────────────────────────────────
('Rabbia',                          'Cane', 'obbligatorio', 'Obbligatoria per legge in molte regioni italiane. Richiamo annuale o triennale secondo il vaccino usato.'),
('Cimurro (Morbo di Carré)',        'Cane', 'obbligatorio', 'Malattia virale grave del sistema nervoso e respiratorio. Inclusa nel vaccino polivalente.'),
('Parvovirus canino',               'Cane', 'obbligatorio', 'Gastroenterite emorragica ad alta mortalità nei cuccioli. Inclusa nel polivalente.'),
('Epatite infettiva canina (CAV-1)','Cane', 'obbligatorio', 'Adenovirus tipo 1 responsabile di epatite acuta. Inclusa nel polivalente.'),
('Leptospirosi',                    'Cane', 'obbligatorio', 'Batterio trasmissibile all'uomo (zoonosi). Richiamo annuale obbligatorio in zone a rischio.'),
('Parainfluenza canina',            'Cane', 'obbligatorio', 'Componente della "tosse dei canili". Spesso inclusa nel polivalente.'),

-- ── CANE – opzionali ─────────────────────────────────────────────────────────
('Tosse dei canili (Bordetella bronchiseptica)', 'Cane', 'opzionale', 'Consigliata prima di soggiorni in pensioni, dog sitter o mostre cinofili.'),
('Leishmaniosi',                    'Cane', 'opzionale', 'Consigliata in zone endemiche (Centro-Sud Italia). Richiamo annuale.'),
('Babesiosi (Piroplasmosi)',        'Cane', 'opzionale', 'Protegge dalla Babesia canis trasmessa da zecche. Consigliata in zone a rischio.'),
('Coronavirus canino',             'Cane', 'opzionale', 'Protegge da gastroenterite da coronavirus. Consigliata in cuccioli o soggetti a rischio.'),

-- ── GATTO – obbligatori ───────────────────────────────────────────────────────
('Trivalente felina (Rinotracheite + Calicivirus + Panleucopenia)', 'Gatto', 'obbligatorio', 'Vaccino di base per tutti i gatti. Richiamo ogni 1-3 anni secondo protocollo.'),
('Rabbia',                          'Gatto', 'obbligatorio', 'Obbligatoria per legge in alcune regioni e per i viaggi internazionali. Richiamo annuale o triennale.'),

-- ── GATTO – opzionali ─────────────────────────────────────────────────────────
('FeLV (Leucemia felina)',          'Gatto', 'opzionale', 'Consigliata per gatti con accesso all'esterno o a contatto con altri gatti. Richiamo annuale.'),
('Clamidiosi felina',               'Gatto', 'opzionale', 'Protegge da Chlamydophila felis responsabile di congiuntivite cronica.'),
('Peritonite infettiva felina (FIP)','Gatto', 'opzionale', 'Disponibile in alcuni paesi. Valutare con il veterinario in base al rischio.'),
('Bordetella bronchiseptica felina','Gatto', 'opzionale', 'Consigliata per gatti in colonie o catterie.'),

-- ── CAVALLO – obbligatori ─────────────────────────────────────────────────────
('Influenza equina',                'Cavallo', 'obbligatorio', 'Obbligatoria per partecipare a gare e manifestazioni FEI/FISE. Richiamo ogni 6 mesi.'),
('Tetano',                          'Cavallo', 'obbligatorio', 'Fondamentale per tutti i cavalli. Richiamo annuale o biennale.'),
('Encefalomielite equina virale (EEE/WEE)', 'Cavallo', 'obbligatorio', 'Obbligatoria in alcune aree geografiche. Consigliata in zone endemiche.'),

-- ── CAVALLO – opzionali ───────────────────────────────────────────────────────
('Herpesvirus equino (EHV-1 / EHV-4)', 'Cavallo', 'opzionale', 'Protegge da aborto virale e malattia respiratoria. Consigliata per fattrici e cavalli in competizione.'),
('West Nile virus',                 'Cavallo', 'opzionale', 'Consigliata in zone a rischio (pianura padana, centro Italia). Richiamo annuale.'),
('Rabbia equina',                   'Cavallo', 'opzionale', 'Consigliata in zone endemiche o per viaggi internazionali.'),
('Adenite equina (Strangles)',      'Cavallo', 'opzionale', 'Protegge da Streptococcus equi. Consigliata in scuderie con frequenti nuovi arrivi.'),
('Rotavirus equino',                'Cavallo', 'opzionale', 'Consigliata per fattrici gravide per proteggere i puledri da diarrea neonatale.')

ON CONFLICT DO NOTHING;
