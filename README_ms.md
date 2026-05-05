<div align="center">

# 🛡️ Pengesan Phishing

**Sistem Pengesan Phishing & Penipuan Berasaskan AI**

[![CI](https://github.com/nus111/phishing-detector/actions/workflows/ci.yml/badge.svg)](https://github.com/nus111/phishing-detector/actions/workflows/ci.yml)

**🌐 [English](README.md) | [中文](README_zh.md) | [Bahasa Melayu](README_ms.md) | [தமிழ்](README_ta.md)**

</div>

---

## Gambaran Keseluruhan

Sistem pengesan mesej phishing dan penipuan berasaskan AI berbilang bahasa yang berfungsi secara masa nyata, dengan tumpuan khas untuk melindungi golongan rentan yang bukan penutur bahasa Inggeris (pelarian, pekerja asing, pelajar antarabangsa) di Malaysia.

## Teknologi Digunakan

| Lapisan | Teknologi |
|---------|-----------|
| Frontend | React + Next.js + Tailwind CSS |
| Backend | Python FastAPI |
| Pangkalan Data | PostgreSQL |
| AI/ML | XLM-RoBERTa (Hugging Face Transformers) |
| Deployment | Docker + Docker Compose |

## Ciri-ciri

- 🔍 **Analisis Mesej Masa Nyata** — Tampal sebarang mesej untuk menyemak petunjuk phishing
- 🌍 **Sokongan Berbilang Bahasa** — English、中文、Bahasa Melayu、தமிழ்
- ⚠️ **Penilaian Risiko** — Tahap risiko berwarna (Rendah / Sederhana / Tinggi) dengan penjelasan terperinci
- 📚 **Pendidikan Keselamatan** — Petua, artikel dan kuiz untuk meningkatkan kesedaran phishing
- 📊 **Papan Pemuka Admin** — Trend ancaman, taburan bahasa, analitik pengguna
- 🤖 **Berasaskan AI** — Model pembelajaran mendalam XLM-RoBERTa untuk pengesanan tepat

## Mula Cepat

```bash
# Klon repositori
git clone https://github.com/nus111/phishing-detector.git
cd phishing-detector

# Salin konfigurasi persekitaran
cp .env.example .env
# Edit .env dengan tetapan anda

# Mula semua perkhidmatan
docker-compose up -d

# Akses:
# Frontend:   http://localhost:3000
# Backend:    http://localhost:8000
# ML Service: http://localhost:8001
# Dokumentasi API: http://localhost:8000/docs
```

## Struktur Projek

```
phishing-detector/
├── frontend/          # Frontend Next.js (React + Tailwind + i18n)
├── backend/           # Backend FastAPI (API REST + pengesahan JWT)
├── ml/                # Latihan & inferens model ML
├── docs/              # Dokumentasi API, Model, Deployment
├── docker-compose.yml # Orkestrasi perkhidmatan
└── .env.example       # Templat pemboleh ubah persekitaran
```

## Titik Akhir API

| Kaedah | Titik Akhir | Penerangan | Auth |
|--------|-------------|------------|------|
| POST | `/api/v1/auth/register` | Daftar | ❌ |
| POST | `/api/v1/auth/login` | Log Masuk | ❌ |
| GET | `/api/v1/auth/me` | Pengguna semasa | 🔒 |
| POST | `/api/v1/analyze` | Analisis mesej | 🔒 |
| GET | `/api/v1/analyze/history` | Sejarah analisis | 🔒 |
| GET | `/api/v1/education` | Kandungan pendidikan | ❌ |
| POST | `/api/v1/education/quiz/submit` | Hantar kuiz | 🔒 |
| GET | `/api/v1/admin/dashboard` | Statistik admin | 👑 |

> Dokumentasi API penuh tersedia di `http://localhost:8000/docs` (Swagger UI)

## Pasukan

| Nama | Peranan | Tanggungjawab |
|------|---------|---------------|
| Yang Jintao | Ketua Kumpulan, Frontend | UI/UX, pembangunan laman web, pengurusan projek |
| Lin Yubo | Keselamatan & Backend | API REST, pangkalan data, keselamatan, deployment |
| Liu Zeyu | Ketua Jurutera Data | Pra-pemprosesan data, pengekstrakan ciri, penilaian model |
| Li Hao | Jurutera Data | Pengumpulan data, pembersihan, penalaan model AI |
| Yang Junxi | Jurutera ML/AI | Pemilihan model, fine-tuning, analisis ralat |

## Penyelia

**Dr. Arafat Mohammed Rashad Al-dhaqm**
Sains Komputer, Universiti Taylor's

## Lesen

Projek ini untuk tujuan akademik — Projek Capstone Universiti Taylor's (PRJ63504).
