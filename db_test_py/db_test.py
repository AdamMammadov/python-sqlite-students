import sqlite3

# Yeni database bağlantısı
conn = sqlite3.connect("ders.db")
cursor = conn.cursor()

# Köhnə cədvəlləri silirik (təmiz başlayaq)
cursor.execute("DROP TABLE IF EXISTS qiymet")
cursor.execute("DROP TABLE IF EXISTS telebe")

# Telebe cədvəli
cursor.execute("""
CREATE TABLE telebe (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ad TEXT NOT NULL,
    yas INTEGER,
    fakulte TEXT
)
""")

# Qiymət cədvəli
cursor.execute("""
CREATE TABLE qiymet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telebe_id INTEGER,
    ders TEXT,
    bal INTEGER,
    FOREIGN KEY (telebe_id) REFERENCES telebe(id)
)
""")

# Telebe məlumatları
cursor.executemany("""
INSERT INTO telebe (ad, yas, fakulte) VALUES (?, ?, ?)
""", [
    ("Ali", 20, "İnformasiya Texnologiyaları"),
    ("Nigar", 22, "Biznes"),
    ("Murad", 19, "Hüquq"),
    ("Leyla", 21, "İqtisadiyyat"),
    ("Orxan", 23, "İnformasiya Texnologiyaları")
])

# Qiymət məlumatları
cursor.executemany("""
INSERT INTO qiymet (telebe_id, ders, bal) VALUES (?, ?, ?)
""", [
    (1, "Proqramlaşdırma", 95),
    (1, "Riyaziyyat", 88),
    (2, "Marketinq", 77),
    (2, "Mühasibatlıq", 82),
    (3, "Hüquq nəzəriyyəsi", 91),
    (4, "Makroiqtisadiyyat", 68),
    (5, "Proqramlaşdırma", 99),
    (5, "Şəbəkələr", 85)
])

conn.commit()

# ---------------- SQL SORĞULAR ----------------

# 1. JOIN ilə tələbə + qiymət
cursor.execute("""
SELECT telebe.ad, telebe.fakulte, qiymet.ders, qiymet.bal
FROM telebe
JOIN qiymet ON telebe.id = qiymet.telebe_id
""")
print("1) Tələbələrin qiymətləri:", cursor.fetchall())

# 2. Ən yüksək orta bal
cursor.execute("""
SELECT telebe.ad, AVG(qiymet.bal) as orta_bal
FROM telebe
JOIN qiymet ON telebe.id = qiymet.telebe_id
GROUP BY telebe.ad
ORDER BY orta_bal DESC
LIMIT 1
""")
print("2) Ən yüksək orta bala sahib tələbə:", cursor.fetchall())

# 3. Fakültə üzrə orta bal
cursor.execute("""
SELECT telebe.fakulte, AVG(qiymet.bal)
FROM telebe
JOIN qiymet ON telebe.id = qiymet.telebe_id
GROUP BY telebe.fakulte
""")
print("3) Fakültə üzrə orta bal:", cursor.fetchall())

# 4. Ən aşağı bal
cursor.execute("""
SELECT telebe.ad, qiymet.ders, MIN(qiymet.bal)
FROM telebe
JOIN qiymet ON telebe.id = qiymet.telebe_id
""")
print("4) Ən aşağı bal:", cursor.fetchall())

# 5. 90+ bal alanlar
cursor.execute("""
SELECT telebe.ad, qiymet.ders, qiymet.bal
FROM telebe
JOIN qiymet ON telebe.id = qiymet.telebe_id
WHERE qiymet.bal >= 90
""")
print("5) 90+ bal alan tələbələr:", cursor.fetchall())

# ---------------- UPDATE və DELETE ----------------

# UPDATE: Leyla-nın Makroiqtisadiyyat balını 68 → 85 edək
cursor.execute("""
UPDATE qiymet
SET bal = 85
WHERE telebe_id = 4 AND ders = 'Makroiqtisadiyyat'
""")
conn.commit()

cursor.execute("""
SELECT telebe.ad, qiymet.ders, qiymet.bal
FROM telebe
JOIN qiymet ON telebe.id = qiymet.telebe_id
WHERE telebe.ad = 'Leyla'
""")
print("6) UPDATE sonrası Leyla:", cursor.fetchall())

# DELETE: Nigar-ı bazadan silək
cursor.execute("DELETE FROM telebe WHERE ad = 'Nigar'")
conn.commit()

cursor.execute("SELECT * FROM telebe")
print("7) DELETE sonrası tələbələr:", cursor.fetchall())

# Bağlantını bağlayırıq
conn.close()
