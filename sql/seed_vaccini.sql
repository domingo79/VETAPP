-- ============================================================
-- seed_vaccini.sql
-- Catalogo vaccini e trattamenti standard per cane, gatto e cavallo.
-- Esegui nell'SQL Editor di Supabase DOPO aver applicato schema.sql
-- ============================================================

INSERT INTO public.vaccini_catalogo (nome, specie, tipo, descrizione) VALUES

-- ── CANE – obbligatori ────────────────────────────────────────────────────────
('Rabbia',                              'Cane', 'obbligatorio', 'Obbligatoria per legge in molte regioni italiane. Richiamo annuale o triennale secondo il vaccino usato.'),
('Cimurro (Morbo di Carré)',            'Cane', 'obbligatorio', 'Malattia virale grave del sistema nervoso e respiratorio. Inclusa nel vaccino polivalente.'),
('Parvovirus canino',                   'Cane', 'obbligatorio', 'Gastroenterite emorragica ad alta mortalità nei cuccioli. Inclusa nel polivalente.'),
('Epatite infettiva canina (CAV-1)',    'Cane', 'obbligatorio', 'Adenovirus tipo 1 responsabile di epatite acuta. Inclusa nel polivalente.'),
('Leptospirosi (Vaccino giallo)',        'Cane', 'obbligatorio', 'Batterio trasmissibile all''uomo (zoonosi). Vaccino giallo. Richiamo annuale. Costo indicativo: 60€.'),
('Parainfluenza canina',                'Cane', 'obbligatorio', 'Componente della "tosse dei canili". Spesso inclusa nel polivalente.'),

-- ── CANE – opzionali ─────────────────────────────────────────────────────────
('Tosse dei canili (Bordetella bronchiseptica)', 'Cane', 'opzionale', 'Consigliata prima di soggiorni in pensioni, dog sitter o mostre cinofili.'),
('Leishmaniosi (Vaccino azzurro)',       'Cane', 'opzionale', 'Vaccino azzurro. Consigliata in zone endemiche (Centro-Sud Italia). Richiamo annuale. Costo indicativo: 90€.'),
('Babesiosi (Piroplasmosi)',            'Cane', 'opzionale', 'Protegge dalla Babesia canis trasmessa da zecche. Consigliata in zone a rischio.'),
('Coronavirus canino',                  'Cane', 'opzionale', 'Protegge da gastroenterite da coronavirus. Consigliata in cuccioli o soggetti a rischio.'),
('Profilassi filariosi (Vaccino marrone)', 'Cane', 'opzionale', 'Vaccino marrone. Prevenzione della filariosi cardiopolmonare trasmessa dalle zanzare. Richiamo annuale. Costo indicativo: 35€.'),
('Antiparassitario – Pipette',          'Cane', 'opzionale', 'Trattamento antiparassitario esterno (pulci, zecche, flebotomi). Applicazione mensile da aprile a settembre. Costo indicativo: 20€/pipetta, ~108€ per 2 scatole.'),

-- ── GATTO – obbligatori ───────────────────────────────────────────────────────
('Trivalente felina (Rinotracheite + Calicivirus + Panleucopenia)', 'Gatto', 'obbligatorio', 'Vaccino di base per tutti i gatti. Richiamo ogni 1-3 anni secondo protocollo.'),
('Rabbia',                              'Gatto', 'obbligatorio', 'Obbligatoria in alcune regioni e per i viaggi internazionali. Richiamo annuale o triennale.'),

-- ── GATTO – opzionali ─────────────────────────────────────────────────────────
('FeLV (Leucemia felina)',              'Gatto', 'opzionale', 'Consigliata per gatti con accesso all''esterno o a contatto con altri gatti. Richiamo annuale.'),
('Clamidiosi felina',                   'Gatto', 'opzionale', 'Protegge da Chlamydophila felis responsabile di congiuntivite cronica.'),
('Peritonite infettiva felina (FIP)',   'Gatto', 'opzionale', 'Disponibile in alcuni paesi. Valutare con il veterinario in base al rischio.'),
('Bordetella bronchiseptica felina',    'Gatto', 'opzionale', 'Consigliata per gatti in colonie o catterie.'),

-- ── CAVALLO – obbligatori ─────────────────────────────────────────────────────
('Tetano + Influenza equina (combinato)', 'Cavallo', 'obbligatorio', 'Vaccino combinato. Prima vaccinazione: 1ª dose subito, 2ª dopo 1 mese, 3ª dopo 6 mesi. Richiamo annuale. Obbligatorio per gare FEI/FISE. Costo indicativo: 40€/richiamo.'),
('Influenza equina',                    'Cavallo', 'obbligatorio', 'Obbligatoria per partecipare a gare e manifestazioni FEI/FISE. Richiamo ogni 6 mesi. Inclusa nel combinato Tetano+Influenza.'),
('Tetano',                              'Cavallo', 'obbligatorio', 'Fondamentale per tutti i cavalli. Incluso nel combinato Tetano+Influenza. Richiamo annuale. Costo indicativo: 40€ nel combinato.'),
('Encefalomielite equina virale (EEE/WEE)', 'Cavallo', 'obbligatorio', 'Obbligatoria in alcune aree geografiche. Consigliata in zone endemiche.'),

-- ── CAVALLO – opzionali ───────────────────────────────────────────────────────
('Herpesvirus equino (EHV-1 / EHV-4)', 'Cavallo', 'opzionale', 'Protegge da aborto virale e malattia respiratoria. Consigliata per fattrici e cavalli in competizione. Richiamo annuale. Costo indicativo: 50€.'),
('West Nile virus',                     'Cavallo', 'opzionale', 'Prima vaccinazione: 1ª dose subito, 2ª dopo 1 mese. Richiamo annuale. Consigliata in zone a rischio (pianura padana, centro Italia). Costo indicativo: 60€/richiamo.'),
('Vermifugo',                           'Cavallo', 'opzionale', 'Trattamento antiparassitario interno. 2 trattamenti l''anno consigliati. Esame feci preliminare raccomandato: ~80€. Costo vermifugo: 20-50€ a trattamento.'),
('Rabbia equina',                       'Cavallo', 'opzionale', 'Consigliata in zone endemiche o per viaggi internazionali.'),
('Adenite equina (Strangles)',          'Cavallo', 'opzionale', 'Protegge da Streptococcus equi. Consigliata in scuderie con frequenti nuovi arrivi.'),
('Rotavirus equino',                    'Cavallo', 'opzionale', 'Consigliata per fattrici gravide per proteggere i puledri da diarrea neonatale.')

ON CONFLICT DO NOTHING;
