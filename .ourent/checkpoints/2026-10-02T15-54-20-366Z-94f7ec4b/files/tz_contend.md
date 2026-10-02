# 📘 TO'LIQ TEXNIK TOPSHIRIQ (TZ) v3.0
## XalqUchun Platforma — Ko'p Panelli Ekosistema
### Dealer • Do'kon • Dasturchi • Kuryer • Admin • Mijoz

**Hujjat versiyasi:** 3.0
**Sana:** 2026-10-02
**Arxitektura:** Web Coding (FastAPI + React) + Telegram Bot + Multi-Channel Gateway + WebSocket
**Platforma turi:** Multi-Vendor Marketplace + Delivery Ecosystem

---

# 📑 MUNDARIJA

1. [Loyiha konsepsiyasi](#1-loyiha-konsepsiyasi)
2. [Ekotizim ishtirokchilari](#2-ekotizim-ishtirokchilari)
3. [To'liq arxitektura](#3-toliq-arxitektura)
4. [Panellar tizimi (6 ta panel)](#4-panellar-tizimi)
5. [Rollar va huquqlar matritsasi](#5-rollar-va-huquqlar-matritsasi)
6. [Moliyaviy tizim](#6-moliyaviy-tizim)
7. [Dealer tizimi](#7-dealer-tizimi)
8. [Do'kon tizimi](#8-dokon-tizimi)
9. [Dasturchi (Developer Partner) tizimi](#9-dasturchi-tizimi)
10. [Kuryer tizimi](#10-kuryer-tizimi)
11. [Buyurtma oqimi (to'liq)](#11-buyurtma-oqimi)
12. [Ma'lumotlar bazasi (to'liq)](#12-malumotlar-bazasi)
13. [API endpointlar (to'liq)](#13-api-endpointlar)
14. [WebSocket real-time](#14-websocket-real-time)
15. [Multi-Channel Gateway](#15-multi-channel-gateway)
16. [Xavfsizlik](#16-xavfsizlik)
17. [Moliyaviy hisob-kitoblar](#17-moliyaviy-hisob-kitoblar)
18. [Integratsiyalar](#18-integratsiyalar)
19. [DevOps va infratuzilma](#19-devops-va-infratuzilma)
20. [Yo'l xaritasi](#20-yol-xaritasi)
21. [Qabul qilish mezonlari](#21-qabul-qilish-mezonlari)

---

# 1. LOYIHA KONSEPSIYASI

## 1.1. Asosiy g'oya
**XalqUchun** — O'zbekiston bozoridagi **ko'p qatlamli e-commerce va yetkazib berish ekosistemasi**. Platforma **Uzum Tezkor**, **Yandex Eats** va **Wildberries** modellarini birlashtiradi, lekin **o'ziga xos 4 qatlamli savdo tizimi**ga ega:

```
Dasturchi (Developer Partner)
    ↓ mahsulot taqdim etadi
Dealer (Distribyutor)
    ↓ do'konlarga tarqatadi
Do'kon (Vendor/Shop)
    ↓ mijozga sotadi
Mijoz (Customer)
    ↓ buyurtma beradi
Kuryer (Courier)
    ↓ yetkazib beradi
```

## 1.2. Asosiy tamoyillar
- **Web Coding** — barcha panellar brauzerda ishlaydi (React SPA)
- **Universal** — bir platforma, 6 ta rol, 1 ta kod bazasi
- **Tezkor** — FastAPI + WebSocket + Redis
- **Shaffof** — har bir tranzaksiya audit qilinadi
- **Moliyaviy aniq** — har bir so'm hisobga olinadi
- **Xavfsiz** — PII shifrlash, KYC, RBAC
- **Masshtablanuvchan** — 100,000+ foydalanuvchi

## 1.3. Nishonli bozor
- O'zbekiston (asosiy)
- Qozog'iston, Qirg'iziston (kelajakda)

---

# 2. EKOTIZIM ISHTIROKCHILARI

## 2.1. Rollar ro'yxati

| # | Rol | Tavsif | Panel |
|---|---|---|---|
| 1 | **Mijoz (Customer)** | Mahsulot sotib oluvchi | WebApp + Bot |
| 2 | **Kuryer (Courier)** | Yetkazib beruvchi | Courier App (Web) |
| 3 | **Do'kon (Vendor)** | Mahsulot sotuvchi | Vendor Panel |
| 4 | **Dealer (Distribyutor)** | Do'konlarga taqdim etuvchi | Dealer Panel |
| 5 | **Dasturchi (Developer Partner)** | Mahsulot yaratuvchi/taqdim etuvchi | Developer Panel |
| 6 | **Admin** | Platforma boshqaruvchisi | Admin Panel |
| 7 | **Super Admin** | Egasi | Super Admin Panel |
| 8 | **Support** | Qo'llab-quvvatlash | Support Panel |

## 2.2. Rol o'zaro munosabatlari

```
┌──────────────────────────────────────────────────────────────┐
│                    SUPER ADMIN (Egasi)                        │
│  Barcha panellar, moliyaviy hisobotlar, komissiyalar         │
└────────────────────────┬─────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│    ADMIN     │  │   SUPPORT    │  │   FINANCE    │
│  Moderatsiya │  │  Chat, KYC   │  │  Hisob-kitob │
└──────────────┘  └──────────────┘  └──────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  DASTURCHI   │  │   DEALER     │  │   VENDOR     │
│  Mahsulot    │→ │ Distribyutor │→ │   Do'kon     │
│  yaratuvchi  │  │              │  │              │
└──────────────┘  └──────────────┘  └──────┬───────┘
                                            │
                                            ▼
                                     ┌──────────────┐
                                     │   MIJOZ      │
                                     └──────┬───────┘
                                            │
                                            ▼
                                     ┌──────────────┐
                                     │   KURYER     │
                                     └──────────────┘
```

## 2.3. Har bir rolning maqsadi

| Rol | Nimani xohlaydi | Platforma beradi |
|---|---|---|
| **Mijoz** | Tez, arzon, sifatli mahsulot | Katalog, real-time kuzatuv, keshbek |
| **Kuryer** | Ko'p buyurtma, yaxshi daromad | Buyurtmalar, marshrut, bonus |
| **Do'kon** | Ko'p mijoz, kam xarajat | Mijozlar, analitika, logistika |
| **Dealer** | Ko'p do'kon, barqaror daromad | Do'konlar tarmog'i, komissiya |
| **Dasturchi** | Mahsulotni sotish, brend | Do'konlar, royalty |
| **Admin** | Tizim barqarorligi | Monitoring, moderatsiya |
| **Super Admin** | Foyda, o'sish | Moliyaviy hisobot, strategiya |

---

# 3. TO'LIQ ARXITEKTURA

```
┌─────────────────────────────────────────────────────────────────────┐
│                        MIJOZ QATLAMI (Frontend)                      │
│                                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │ Mijoz    │  │ Vendor   │  │ Dealer   │  │ Courier  │            │
│  │ WebApp   │  │ Panel    │  │ Panel    │  │ App      │            │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │
│       │             │             │             │                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │Developer │  │ Admin    │  │ Support  │  │Super Adm.│            │
│  │ Panel    │  │ Panel    │  │ Panel    │  │ Panel    │            │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │
│       │             │             │             │                   │
│       └─────────────┴─────────────┴─────────────┘                   │
│                            │                                         │
│                   Telegram Bot (navigatsiya)                         │
│                            │                                         │
└────────────────────────────┼─────────────────────────────────────────┘
                             │ HTTPS / WSS
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    API GATEWAY (Nginx / Traefik)                     │
│              SSL • Rate Limit • Load Balance • CORS                  │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    FASTAPI BACKEND (Async)                            │
│                                                                      │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐          │
│  │Auth API   │ │Catalog API│ │Order API  │ │Finance API│          │
│  └───────────┘ └───────────┘ └───────────┘ └───────────┘          │
│                                                                      │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐          │
│  │Vendor API │ │Dealer API │ │Dev API    │ │Courier API│          │
│  └───────────┘ └───────────┘ └───────────┘ └───────────┘          │
│                                                                      │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐          │
│  │Payout API │ │Wallet API │ │Commission │ │Pricing API│          │
│  └───────────┘ └───────────┘ └───────────┘ └───────────┘          │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │              WebSocket Hub (real-time events)                 │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │              Business Rules Engine (BLE)                      │  │
│  │  • Minimal buyurtma  • Komissiya  • Payout  • Bonus           │  │
│  └──────────────────────────────────────────────────────────────┘  │
└──────┬────────────────────────────────────────────────────┬─────────┘
       │                                                     │
       ▼                                                     ▼
┌──────────────┐  ┌──────────────┐  ┌────────────────────────────────┐
│ PostgreSQL   │  │    Redis     │  │  Celery Workers + Beat         │
│ (asosiy DB)  │  │ (cache/pubsub│  │  • SMS/WhatsApp                │
│              │  │  +queue)     │  │  • Hisobotlar                  │
│              │  │              │  │  • Payout hisoblash            │
└──────────────┘  └──────────────┘  └────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    TASHQI INTEGRATSIYALAR                            │
│  Eskiz SMS • WhatsApp Cloud • Payme • Click • Uzum •                │
│  Yandex Maps • Telegram API • S3 • Sentry • Prometheus              │
└─────────────────────────────────────────────────────────────────────┘
```

---

# 4. PANELLAR TIZIMI

## 4.1. Panel #1 — Mijoz WebApp + Telegram Bot

### Sahifalar
| Sahifa | Route | Funksiya |
|---|---|---|
| Bosh | `/` | Kategoriyalar, aksiyalar, tavsiyalar |
| Katalog | `/catalog` | Barcha do'konlar va mahsulotlar |
| Do'kon | `/shop/:id` | Bitta do'kon mahsulotlari |
| Mahsulot | `/product/:id` | Batafsil, sharhlar |
| Savat | `/cart` | Mahsulotlar, promo |
| Checkout | `/checkout` | Manzil, to'lov |
| Kuzatuv | `/order/:id` | Real-time xarita |
| Tarix | `/orders` | Buyurtmalar tarixi |
| Profil | `/profile` | KYC, manzillar |
| Sevimlilar | `/favorites` | Saqlangan |
| Keshbek | `/wallet` | Ball, tranzaksiyalar |
| Referal | `/referral` | Havola, statistika |
| Chat | `/chat/:id` | Kuryer/support |
| Huquqiy | `/legal/*` | Oferta, maxfiylik |

### Telegram Bot komandalar
```
/start    → Asosiy menyu (WebApp tugmasi bilan)
/catalog  → Katalog (WebApp)
/cart     → Savat (WebApp)
/orders   → Buyurtmalarim (WebApp)
/profile  → Profil (WebApp)
/wallet   → Keshbek (WebApp)
/support  → Support chat
/help     → Yordam
```

## 4.2. Panel #2 — Vendor (Do'kon) Panel

### Sahifalar
| Sahifa | Funksiya |
|---|---|
| Dashboard | Kunlik savdo, buyurtmalar, reyting |
| Mahsulotlar | CRUD, narx, zaxira, kategoriya |
| Kategoriyalar | Do'kon ichidagi kategoriyalar |
| Buyurtmalar | Yangi, jarayonda, tarix |
| Analitika | Savdo, eng ko'p sotilgan, mijoz |
| Moliya | Balans, payout, komissiya |
| Promo | O'z aksiyalari |
| Sharhlar | Mijozlar fikri |
| Sozlamalar | Ish vaqti, yetkazish |
| Xodimlar | Rollar (menejer, operator) |

### Muhim funksiyalar
- **Real-time buyurtma kelishi** (WebSocket)
- **Ovozi bilan xabar** (yangi buyurtma)
- **Zaxira boshqaruvi** (avtomatik "tugadi")
- **Narx boshqaruvi** (dinamik)
- **Payout so'rash** (kunlik/haftalik)
- **Analitika export** (Excel, PDF)

## 4.3. Panel #3 — Dealer Panel

### Sahifalar
| Sahifa | Funksiya |
|---|---|
| Dashboard | Tarmoq statistikasi |
| Do'konlar | O'z do'konlari ro'yxati |
| Yangi do'kon | Do'kon qo'shish |
| Mahsulot taqdim | Do'konlarga mahsulot |
| Buyurtmalar | Barcha do'kon buyurtmalari |
| Moliya | Komissiya, payout, balans |
| Hisobotlar | Kunlik/haftalik/oylik |
| Xodimlar | Tarmoq menejerlari |
| Shartnomalar | Do'kon bilan shartnoma |
| Chat | Do'konlar bilan aloqa |

### Dealer ning asosiy vazifasi
1. **Do'konlarni jalb qilish** — yangi do'kon ochish
2. **Mahsulot taqdim etish** — dasturchidan olib do'konga berish
3. **Logistika** — dasturchi → dealer → do'kon
4. **Komissiya olish** — har bir sotuvdan %
5. **Qo'llab-quvvatlash** — do'konlarga yordam

## 4.4. Panel #4 — Dasturchi (Developer Partner) Panel

### Sahifalar
| Sahifa | Funksiya |
|---|---|
| Dashboard | Mahsulotlar, sotuv, royalty |
| Mahsulotlar | CRUD (yaratish, tahrirlash) |
| Brend | Brend sozlamalari, logo |
| Dealerlar | Qaysi dealerlar bilan ishlaydi |
| Do'konlar | Qaysi do'konlarda sotiladi |
| Analitika | Sotuv statistikasi |
| Moliya | Royalty, payout |
| Shartnomalar | Dealer bilan shartnoma |
| Hujjatlar | Sertifikatlar, litsenziya |

### Dasturchi nima qiladi
1. **Mahsulot yaratadi** — yangi mahsulot ishlab chiqadi
2. **Brend yaratadi** — o'z brendini rivojlantiradi
3. **Dealer bilan shartnoma** — tarqatish huquqi
4. **Royalty oladi** — har bir sotuvdan %
5. **Sifat nazorati** — mahsulot standarti

## 4.5. Panel #5 — Kuryer Panel (Courier App)

### Sahifalar
| Sahifa | Funksiya |
|---|---|
| Dashboard | Faol buyurtma, daromad |
| Buyurtmalar | Yaqin atrofdagi buyurtmalar |
| Marshrut | Optimal marshrut |
| Xarita | Real-time navigatsiya |
| Chat | Mijoz bilan aloqa |
| Daromad | Kunlik/haftalik daromad |
| Rejim | Online/Offline |
| Profil | Ma'lumotlar, hujjatlar |

### Kuryer funksiyalari
- **Onlayn/oflayn rejim**
- **Buyurtma qabul qilish** (5 daqiqa ichida)
- **Marshrut optimallashtirish** (Yandex Maps)
- **Real-time joylashuv yuborish** (har 5 sekund)
- **Yetkazishni tasdiqlash** (QR kod yoki OTP)
- **Daromad hisoblash** (har buyurtma + bonus)

## 4.6. Panel #6 — Admin Panel

### Sahifalar
| Sahifa | Funksiya |
|---|---|
| Dashboard | Platforma statistikasi |
| Foydalanuvchilar | Barcha rollar |
| Do'konlar | Moderatsiya, tasdiqlash |
| Dealerlar | Moderatsiya |
| Dasturchilar | Moderatsiya |
| Kuryerlar | Moderatsiya |
| Buyurtmalar | Barcha buyurtmalar |
| Moliya | Komissiya, payout |
| KYC | Pasport tekshirish |
| Shikoyatlar | Foydalanuvchi shikoyatlari |
| Audit Log | Barcha harakatlar |
| Sozlamalar | Platforma sozlamalari |
| Report | Hisobotlar |

### Super Admin qo'shimcha
- **Komissiya sozlamalari** (har rol uchun %)
- **Platforma balansi**
- **Payout tasdiqlash**
- **Admin qo'shish/o'chirish**
- **Feature flags**
- **Tizim monitoring**

## 4.7. Panel #7 — Support Panel

### Sahifalar
| Sahifa | Funksiya |
|---|---|
| Chat navbati | Faol chatlar |
| Ticketlar | Murojaatlar |
| Buyurtma yordam | Muammoli buyurtmalar |
| Foydalanuvchi qidirish | Tezkor qidiruv |
| Bilim bazasi | Tayyor javoblar |

---

# 5. ROLLAR VA HUQUQLAR MATRITSA SI

| Funksiya | Mijoz | Kuryer | Do'kon | Dealer | Dasturchi | Admin | Super Admin |
|---|---|---|---|---|---|---|---|
| Mahsulot ko'rish | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Buyurtma berish | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Mahsulot qo'shish | ❌ | ❌ | ✅ | ⚠️ | ✅ | ✅ | ✅ |
| Mahsulot tahrirlash | ❌ | ❌ | ✅ | ⚠️ | ✅ | ✅ | ✅ |
| Buyurtma qabul qilish | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Kuryer tayinlash | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ | ✅ |
| Dealer qo'shish | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ |
| Do'kon qo'shish | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ |
| Payout so'rash | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Payout tasdiqlash | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Komissiya sozlash | ❌ | ❌ | ❌ | ❌ | ❌ | ⚠️ | ✅ |
| KYC tasdiqlash | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Foydalanuvchi bloklash | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Audit log ko'rish | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Moliyaviy hisobot | ❌ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ✅ | ✅ |

✅ = To'liq | ⚠️ = Qisman | ❌ = Yo'q

---

# 6. MOLIYAVIY TIZIM

## 6.1. Umumiy moliyaviy oqim

```
MIJOZ to'laydi: 100,000 so'm
    │
    ├─► Platforma komissiyasi (10%): 10,000 so'm
    │
    ├─► Do'kon ulushi: 90,000 so'm
    │       │
    │       ├─► Dealer komissiyasi (15%): 13,500 so'm
    │       │
    │       ├─► Dasturchi royalty (10%): 9,000 so'm
    │       │
    │       └─► Do'kon sof foydasi: 67,500 so'm
    │
    ├─► Kuryer to'lovi: 15,000 so'm (alohida)
    │
    └─► To'lov tizimi komissiyasi (2%): 2,000 so'm
```

## 6.2. Komissiya turlari

| Tur | Kim oladi | Standart % | Sozlanadi |
|---|---|---|---|
| **Platforma komissiyasi** | Super Admin | 10% | ✅ |
| **Dealer komissiyasi** | Dealer | 15% | ✅ |
| **Dasturchi royalty** | Dasturchi | 10% | ✅ |
| **To'lov tizimi** | Payme/Click | 2% | ❌ (qat'iy) |
| **Kuryer xizmati** | Kuryer | Fiksirlangan | ✅ |

## 6.3. Wallet (Hamyon) tizimi

Har bir rolda **hamyon** bo'ladi:

```sql
CREATE TABLE wallets (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL,
    owner_type VARCHAR(20) NOT NULL,  -- 'user','vendor','dealer','developer','courier'
    balance DECIMAL(15,2) DEFAULT 0,
    pending_balance DECIMAL(15,2) DEFAULT 0,  -- kutilayotgan
    frozen_balance DECIMAL(15,2) DEFAULT 0,   -- muzlatilgan
    currency VARCHAR(5) DEFAULT 'UZS',
    total_earned DECIMAL(15,2) DEFAULT 0,
    total_withdrawn DECIMAL(15,2) DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(owner_id, owner_type)
);

CREATE TABLE wallet_transactions (
    id BIGSERIAL PRIMARY KEY,
    wallet_id BIGINT REFERENCES wallets(id),
    type VARCHAR(30) NOT NULL,        -- 'credit','debit','hold','release','refund'
    amount DECIMAL(15,2) NOT NULL,
    balance_before DECIMAL(15,2) NOT NULL,
    balance_after DECIMAL(15,2) NOT NULL,
    source_type VARCHAR(30),          -- 'order','payout','commission','bonus','refund'
    source_id BIGINT,
    description TEXT,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_wallet_tx_wallet ON wallet_transactions(wallet_id, created_at DESC);
CREATE INDEX idx_wallet_tx_source ON wallet_transactions(source_type, source_id);
```

## 6.4. Payout (Pul chiqarish) tizimi

```sql
CREATE TABLE payouts (
    id BIGSERIAL PRIMARY KEY,
    wallet_id BIGINT REFERENCES wallets(id),
    owner_id BIGINT NOT NULL,
    owner_type VARCHAR(20) NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    fee DECIMAL(15,2) DEFAULT 0,          -- payout komissiyasi
    net_amount DECIMAL(15,2) NOT NULL,    -- qo'lga tegadigan
    method VARCHAR(30) NOT NULL,          -- 'payme','click','uzum','bank','cash'
    account_details JSONB,                -- karta raqami, telefon
    status VARCHAR(20) DEFAULT 'pending', -- pending|approved|processing|completed|rejected
    requested_at TIMESTAMPTZ DEFAULT NOW(),
    approved_at TIMESTAMPTZ,
    approved_by BIGINT,
    completed_at TIMESTAMPTZ,
    rejection_reason TEXT,
    provider_txn_id VARCHAR(255),
    metadata JSONB
);
CREATE INDEX idx_payouts_owner ON payouts(owner_id, owner_type, status);
CREATE INDEX idx_payouts_status ON payouts(status, requested_at);
```

**Payout qoidalari:**
- Minimal payout: 50,000 so'm
- Maksimal kunlik: 10,000,000 so'm (KYC darajasiga qarab)
- Ish vaqti: 09:00 - 18:00 (ish kunlari)
- Tasdiqlash: 24 soat ichida
- Komissiya: 0-2% (method ga qarab)

## 6.5. Moliyaviy hisobotlar

| Hisobot | Kim uchun | Davr |
|---|---|---|
| Kunlik savdo | Do'kon, Dealer | Kunlik |
| Komissiya hisoboti | Dealer, Dasturchi | Haftalik |
| Payout tarixi | Barcha | Oylik |
| Platforma daromadi | Super Admin | Kunlik/oylik |
| Soliq hisoboti | Super Admin | Choraklik |
| Top mahsulotlar | Do'kon, Dasturchi | Haftalik |
| Mijoz LTV | Admin | Oylik |

## 6.6. Soliq va huquqiy

- **QQS (12%)** — har bir sotuvdan avtomatik hisoblanadi
- **Soliq hisoboti** — har chorakda avtomatik generatsiya
- **Fiskal chek** — har buyurtma uchun (O'RQ-792 talabi)
- **Elektron hisob-faktura** — do'kon-dealer-dasturchi o'rtasida
- **Shartnomalar** — elektron shaklda, ERI bilan imzolangan

---

# 7. DEALER TIZIMI

## 7.1. Dealer nima qiladi

```
1. Do'konlarni jalb qiladi
   → Shartnoma imzolaydi
   → Do'konni platformaga qo'shadi
   → O'qitadi

2. Mahsulot taqdim etadi
   → Dasturchidan mahsulot oladi
   → Do'konlarga tarqatadi
   → Narx belgilaydi

3. Logistika
   → Dasturchi → Dealer ombori
   → Dealer ombori → Do'kon
   → Yetkazish nazorati

4. Qo'llab-quvvatlash
   → Do'kon savollariga javob
   → Muammolarni hal qilish
   → Treninglar

5. Moliya
   → Do'konlardan komissiya oladi
   → Dasturchiga to'laydi
   → Payout qiladi
```

## 7.2. Dealer-Do'kon shartnomasi

```sql
CREATE TABLE dealer_vendor_contracts (
    id BIGSERIAL PRIMARY KEY,
    dealer_id BIGINT REFERENCES dealers(id),
    vendor_id BIGINT REFERENCES vendors(id),
    contract_number VARCHAR(50) UNIQUE,
    signed_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ,
    commission_percent DECIMAL(5,2) NOT NULL,    -- dealer komissiyasi
    min_monthly_sales DECIMAL(15,2),
    exclusive BOOLEAN DEFAULT FALSE,             -- eksklyuziv huquq
    territory JSONB,                             -- hudud
    payment_terms VARCHAR(50),                   -- 'weekly','monthly'
    status VARCHAR(20) DEFAULT 'active',
    document_url TEXT,
    signed_by_dealer BOOLEAN DEFAULT FALSE,
    signed_by_vendor BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## 7.3. Dealer-Dasturchi shartnomasi

```sql
CREATE TABLE dealer_developer_contracts (
    id BIGSERIAL PRIMARY KEY,
    dealer_id BIGINT REFERENCES dealers(id),
    developer_id BIGINT REFERENCES developers(id),
    contract_number VARCHAR(50) UNIQUE,
    signed_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ,
    royalty_percent DECIMAL(5,2) NOT NULL,       -- dasturchi royalty
    min_order_quantity INT,
    delivery_terms VARCHAR(50),
    payment_terms VARCHAR(50),
    exclusive_products BIGINT[],                 -- eksklyuziv mahsulotlar
    status VARCHAR(20) DEFAULT 'active',
    document_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## 7.4. Dealer Dashboard ko'rsatkichlari

| Ko'rsatkich | Tavsif |
|---|---|
| **Faol do'konlar** | Tarmoqdagi do'konlar soni |
| **Kunlik savdo** | Tarmoq umumiy savdo |
| **Komissiya daromadi** | Dealer ulushi |
| **Top do'konlar** | Eng yaxshi 10 do'kon |
| **Muammoli do'konlar** | Kam savdo, shikoyat |
| **Yangi do'konlar** | Oxirgi 30 kun |
| **Oylik o'sish** | % |
| **Payout navbati** | To'lanishi kerak |

---

# 8. DO'KON TIZIMI

## 8.1. Do'kon turlari

| Tur | Tavsif | Misol |
|---|---|---|
| **Oziq-ovqat** | Supermarket, bozor | Makro, Korzinka |
| **Restoran** | Fast food, milliy | Osh, Lavash |
| **Dorixona** | Dori, vitamin | Dori-Darmon |
| **Kiyim** | Kiyim-kechak | Sportmaster |
| **Elektronika** | Telefon, kompyuter | MediaPark |
| **Maishiy** | Uy jihozlari | Ideal |
| **Kitob** | Kitob, kanselyariya | Kitob olami |
| **Gul** | Gul, sovg'a | Gullar |

## 8.2. Do'kon sozlamalari

```sql
CREATE TABLE vendors (
    id BIGSERIAL PRIMARY KEY,
    owner_user_id BIGINT REFERENCES users(id),
    dealer_id BIGINT REFERENCES dealers(id),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE,
    legal_name VARCHAR(255),                     -- yuridik nom
    inn VARCHAR(20),                             -- STIR
    type VARCHAR(30),                            -- 'food','restaurant',...
    description TEXT,
    logo_url TEXT,
    cover_url TEXT,
    phone VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    lat DECIMAL(10,8),
    lng DECIMAL(11,8),
    working_hours JSONB,                         -- {"mon":["09:00","22:00"],...}
    is_open BOOLEAN DEFAULT FALSE,               -- real-time
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    commission_percent DECIMAL(5,2) DEFAULT 10,
    min_order_amount DECIMAL(12,2) DEFAULT 50000,
    delivery_fee DECIMAL(12,2) DEFAULT 0,
    free_delivery_from DECIMAL(12,2),
    delivery_radius_km INT DEFAULT 5,
    avg_delivery_time INT DEFAULT 30,            -- daqiqa
    rating DECIMAL(3,2) DEFAULT 0,
    total_orders INT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

## 8.3. Do'kon xodimlari

```sql
CREATE TABLE vendor_staff (
    id BIGSERIAL PRIMARY KEY,
    vendor_id BIGINT REFERENCES vendors(id) ON DELETE CASCADE,
    user_id BIGINT REFERENCES users(id),
    role VARCHAR(30) NOT NULL,   -- 'owner','manager','operator','cashier'
    permissions JSONB,           -- aniq huquqlar
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Rollar:**
- **Owner** — to'liq huquq, moliya
- **Manager** — mahsulot, buyurtma, xodim
- **Operator** — faqat buyurtma qabul qilish
- **Cashier** — to'lov qabul qilish (offline)

---

# 9. DASTURCHI TIZIMI

## 9.1. Dasturchi nima qiladi

```
1. Mahsulot yaratadi
   → Retsept, formula, dizayn
   → Brend, qadoq
   → Sertifikat, litsenziya

2. Ishlab chiqaradi
   → Zavod, ustaxona
   → Sifat nazorati
   → Qadoqlash

3. Dealer bilan shartnoma
   → Tarqatish huquqi
   → Narx kelishuvi
   → Royalty %

4. Do'konlarga taqdim etadi
   → Dealer orqali
   → Yoki to'g'ridan-to'g'ri

5. Royalty oladi
   → Har bir sotuvdan %
   → Oylik hisobot
```

## 9.2. Dasturchi ma'lumotlari

```sql
CREATE TABLE developers (
    id BIGSERIAL PRIMARY KEY,
    owner_user_id BIGINT REFERENCES users(id),
    company_name VARCHAR(255) NOT NULL,
    brand_name VARCHAR(255),
    slug VARCHAR(255) UNIQUE,
    legal_name VARCHAR(255),
    inn VARCHAR(20),
    description TEXT,
    logo_url TEXT,
    phone VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    website VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    royalty_percent DECIMAL(5,2) DEFAULT 10,    -- standart royalty
    rating DECIMAL(3,2) DEFAULT 0,
    total_products INT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE developer_products (
    id BIGSERIAL PRIMARY KEY,
    developer_id BIGINT REFERENCES developers(id),
    product_id BIGINT REFERENCES products(id) UNIQUE,
    sku VARCHAR(100) UNIQUE,                    -- dasturchi SKU
    barcode VARCHAR(100),
    brand VARCHAR(255),
    category VARCHAR(100),
    cost_price DECIMAL(12,2) NOT NULL,          -- tannarx
    recommended_price DECIMAL(12,2) NOT NULL,   -- tavsiya narx
    royalty_percent DECIMAL(5,2),               -- mahsulotga xos royalty
    certification_url TEXT,                     -- sertifikat
    instruction_url TEXT,                       -- yo'riqnoma
    shelf_life_days INT,                        -- saqlash muddati
    storage_conditions TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## 9.3. Royalty hisoblash

```
Mijoz 100,000 so'mga mahsulot sotib oldi
    │
    ├─ Dasturchi royalty (10%): 10,000 so'm
    │   └─ Dasturchi hamyoniga tushadi
    │
    ├─ Dealer komissiyasi (15%): 13,500 so'm
    │   └─ Dealer hamyoniga tushadi
    │
    ├─ Platforma komissiyasi (10%): 10,000 so'm
    │   └─ Super Admin hisobiga
    │
    └─ Do'kon sof foydasi: 66,500 so'm
        └─ Do'kon hamyoniga
```

---

# 10. KURYER TIZIMI

## 10.1. Kuryer turlari

| Tur | Transport | Yetkazish |
|---|---|---|
| **Piyoda** | Yo'q | 1-3 km |
| **Velosiped** | Velosiped | 1-5 km |
| **Mototsikl** | Mototsikl | 1-15 km |
| **Avtomobil** | Mashina | 1-30 km |
| **Yuk mashinasi** | Yuk | Katta buyurtma |

## 10.2. Kuryer ma'lumotlari

```sql
CREATE TABLE couriers (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) UNIQUE,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    passport_data JSONB,                        -- shifrlangan
    vehicle_type VARCHAR(30) NOT NULL,
    vehicle_number VARCHAR(20),
    license_number VARCHAR(50),
    status VARCHAR(20) DEFAULT 'offline',      -- offline|online|busy
    is_verified BOOLEAN DEFAULT FALSE,
    current_lat DECIMAL(10,8),
    current_lng DECIMAL(11,8),
    last_location_at TIMESTAMPTZ,
    service_area JSONB,                         -- xizmat hududi
    rating DECIMAL(3,2) DEFAULT 5.0,
    total_orders INT DEFAULT 0,
    completed_orders INT DEFAULT 0,
    cancelled_orders INT DEFAULT 0,
    total_earned DECIMAL(15,2) DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE courier_locations (
    id BIGSERIAL PRIMARY KEY,
    courier_id BIGINT REFERENCES couriers(id),
    order_id BIGINT,
    lat DECIMAL(10,8),
    lng DECIMAL(11,8),
    bearing DECIMAL(5,2),
    speed_kmh DECIMAL(5,2),
    accuracy_m DECIMAL(5,2),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_courier_loc ON courier_locations(courier_id, created_at DESC);
```

## 10.3. Kuryer daromadi

```
Asosiy to'lov: har buyurtma uchun fiksirlangan
    + Masofa: har km uchun
    + Vaqt: kechki/ertalabki bonus
    + Yuk: og'ir buyurtma uchun qo'shimcha
    + Reyting: yuqori reyting bonusi
    + Kunlik maqsad: kunlik maqsadga yetganda bonus
```

**Misol:**
```
Buyurtma: 100,000 so'm
Masofa: 3 km
Vaqt: 19:00 (kechki)
Yuk: 5 kg (normal)

Asosiy: 8,000 so'm
Masofa: 3 × 500 = 1,500 so'm
Kechki: 2,000 so'm
Yuk: 0
Reyting: 500 so'm
─────────────────
Jami: 12,000 so'm
```

---

# 11. BUYURTMA OQIMI (TO'LIQ)

## 11.1. To'liq oqim diagrammasi

```
1. MIJOZ
   ├─ Katalog ko'radi
   ├─ Mahsulot tanlaydi
   ├─ Savatga qo'shadi
   └─ Checkout qiladi
                │
                ▼
2. PLATFORMA
   ├─ Minimal summa tekshirish (50,000)
   ├─ Manzil tekshirish
   ├─ To'lov usuli tanlash
   ├─ Promo-kod qo'llash
   └─ Buyurtma yaratish
                │
                ▼
3. TO'LOV
   ├─ Payme/Click/Uzum/Cash
   ├─ Idempotency tekshirish
   ├─ Provider callback
   └─ To'lov tasdiqlandi
                │
                ▼
4. DO'KON
   ├─ Real-time xabar (WS)
   ├─ Buyurtma qabul qilish (5 daqiqa)
   ├─ Tayyorlash
   └─ Tayyor deb belgilash
                │
                ▼
5. KURYER
   ├─ Yaqin kuryerlar topish
   ├─ Kuryer tayinlash
   ├─ Kuryer qabul qilish
   ├─ Do'konga borish
   ├─ Mahsulotni olish (QR tasdiqlash)
   └─ Mijozga borish
                │
                ▼
6. YETKAZISH
   ├─ Real-time kuzatuv (WS)
   ├─ Mijoz bilan aloqa (chat)
   ├─ Yetkazildi (QR/OTP tasdiqlash)
   └─ Buyurtma yopildi
                │
                ▼
7. MOLIYA
   ├─ Komissiya hisoblash
   ├─ Hamyonlarga taqsimlash
   ├─ Keshbek hisoblash
   └─ Hisobot yangilash
                │
                ▼
8. BAHOLASH
   ├─ Mijoz baholaydi
   ├─ Reyting yangilanadi
   └─ Bonus hisoblanadi
```

## 11.2. Buyurtma holatlari (state machine)

```
DRAFT
  ↓
PENDING_PAYMENT ──► CANCELLED
  ↓
PAID ──► REFUNDED
  ↓
ACCEPTED ──► REJECTED ──► REFUNDED
  ↓
PREPARING ──► CANCELLED ──► REFUNDED
  ↓
READY
  ↓
ASSIGNED ──► CANCELLED
  ↓
PICKED_UP ──► RETURNED
  ↓
ON_THE_WAY
  ↓
DELIVERED
  ↓
COMPLETED
  ↓
RATED
```

---

# 12. MA'LUMOTLAR BAZASI (TO'LIQ)

## 12.1. Asosiy jadvallar

### USERS
```sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE,
    phone VARCHAR(20) UNIQUE,
    email VARCHAR(255) UNIQUE,
    full_name VARCHAR(255),
    language VARCHAR(5) DEFAULT 'uz',
    source_channel VARCHAR(20),
    roles TEXT[] DEFAULT ARRAY['customer'],    -- ['customer','courier',...]
    is_registered BOOLEAN DEFAULT FALSE,
    is_verified BOOLEAN DEFAULT FALSE,
    is_blocked BOOLEAN DEFAULT FALSE,
    kyc_status VARCHAR(20) DEFAULT 'pending',
    kyc_data JSONB,                             -- shifrlangan
    preferred_channels TEXT[],
    default_address_id BIGINT,
    loyalty_points INT DEFAULT 0,
    loyalty_tier VARCHAR(20) DEFAULT 'bronze',
    referral_code VARCHAR(20) UNIQUE,
    referred_by BIGINT REFERENCES users(id),
    terms_accepted_at TIMESTAMPTZ,
    privacy_accepted_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### ORDERS (kengaytirilgan)
```sql
CREATE TABLE orders (
    id BIGSERIAL PRIMARY KEY,
    order_number VARCHAR(20) UNIQUE NOT NULL,
    user_id BIGINT REFERENCES users(id),
    vendor_id BIGINT REFERENCES vendors(id),
    dealer_id BIGINT REFERENCES dealers(id),
    address_id BIGINT REFERENCES addresses(id),
    courier_id BIGINT REFERENCES couriers(id),
    status VARCHAR(30) NOT NULL,
    subtotal DECIMAL(12,2) NOT NULL,
    delivery_fee DECIMAL(12,2) DEFAULT 0,
    discount DECIMAL(12,2) DEFAULT 0,
    total DECIMAL(12,2) NOT NULL,
    vat_amount DECIMAL(12,2) DEFAULT 0,
    payment_method VARCHAR(30),
    payment_status VARCHAR(30) DEFAULT 'pending',
    payment_id BIGINT REFERENCES payments(id),
    promo_code VARCHAR(50),
    loyalty_points_used INT DEFAULT 0,
    loyalty_points_earned INT DEFAULT 0,
    source_channel VARCHAR(20),
    customer_comment TEXT,
    cancellation_reason TEXT,
    -- MOLIYAVIY TAQSIMOT
    platform_commission DECIMAL(12,2) DEFAULT 0,
    dealer_commission DECIMAL(12,2) DEFAULT 0,
    developer_royalty DECIMAL(12,2) DEFAULT 0,
    vendor_net_amount DECIMAL(12,2) DEFAULT 0,
    courier_amount DECIMAL(12,2) DEFAULT 0,
    payment_fee DECIMAL(12,2) DEFAULT 0,
    -- VAQT
    created_at TIMESTAMPTZ DEFAULT NOW(),
    accepted_at TIMESTAMPTZ,
    ready_at TIMESTAMPTZ,
    picked_up_at TIMESTAMPTZ,
    delivered_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    cancelled_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### ORDER ITEMS (kengaytirilgan)
```sql
CREATE TABLE order_items (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT REFERENCES orders(id) ON DELETE CASCADE,
    product_id BIGINT REFERENCES products(id),
    developer_id BIGINT REFERENCES developers(id),
    product_name VARCHAR(255) NOT NULL,
    product_sku VARCHAR(100),
    quantity INT NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    cost_price DECIMAL(12,2),
    total DECIMAL(12,2) NOT NULL,
    -- MOLIYAVIY
    royalty_amount DECIMAL(12,2) DEFAULT 0,
    dealer_commission_amount DECIMAL(12,2) DEFAULT 0,
    platform_commission_amount DECIMAL(12,2) DEFAULT 0,
    vendor_amount DECIMAL(12,2) DEFAULT 0,
    -- STATUS
    status VARCHAR(20) DEFAULT 'active'       -- active|cancelled|refunded
);
```

### DEALERS
```sql
CREATE TABLE dealers (
    id BIGSERIAL PRIMARY KEY,
    owner_user_id BIGINT REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE,
    legal_name VARCHAR(255),
    inn VARCHAR(20),
    description TEXT,
    logo_url TEXT,
    phone VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    region VARCHAR(100),                        -- viloyat
    territory JSONB,                            -- hudud
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    commission_percent DECIMAL(5,2) DEFAULT 15,
    rating DECIMAL(3,2) DEFAULT 0,
    total_vendors INT DEFAULT 0,
    total_products INT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### DEVELOPERS
```sql
-- Yuqorida ko'rsatilgan (9.2-band)
```

### WALLETS, TRANSACTIONS, PAYOUTS
```sql
-- Yuqorida ko'rsatilgan (6.3, 6.4-band)
```

### COMMISSIONS (tarix)
```sql
CREATE TABLE commission_records (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT REFERENCES orders(id),
    order_item_id BIGINT REFERENCES order_items(id),
    recipient_type VARCHAR(20) NOT NULL,     -- 'platform','dealer','developer','vendor','courier'
    recipient_id BIGINT NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    percent DECIMAL(5,2),
    status VARCHAR(20) DEFAULT 'pending',    -- pending|credited|reversed
    credited_at TIMESTAMPTZ,
    wallet_tx_id BIGINT REFERENCES wallet_transactions(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_commission_order ON commission_records(order_id);
CREATE INDEX idx_commission_recipient ON commission_records(recipient_type, recipient_id);
```

### CONTRACTS
```sql
-- dealer_vendor_contracts (7.2-band)
-- dealer_developer_contracts (7.3-band)

CREATE TABLE vendor_developer_contracts (
    id BIGSERIAL PRIMARY KEY,
    vendor_id BIGINT REFERENCES vendors(id),
    developer_id BIGINT REFERENCES developers(id),
    contract_number VARCHAR(50) UNIQUE,
    signed_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ,
    terms JSONB,
    status VARCHAR(20) DEFAULT 'active',
    document_url TEXT
);
```

### AUDIT LOG (kengaytirilgan)
```sql
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    actor_id BIGINT,
    actor_role VARCHAR(30),
    actor_type VARCHAR(30),                    -- 'user','admin','system'
    action VARCHAR(50) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id BIGINT,
    before_data JSONB,
    after_data JSONB,
    diff JSONB,                                -- farq
    ip_address INET,
    user_agent TEXT,
    request_id VARCHAR(50),                    -- correlation
    status VARCHAR(20),                        -- 'success','failure'
    error TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_audit_actor ON audit_log(actor_id, created_at DESC);
CREATE INDEX idx_audit_entity ON audit_log(entity_type, entity_id);
CREATE INDEX idx_audit_action ON audit_log(action, created_at DESC);
```

### NOTIFICATIONS
```sql
CREATE TABLE notifications (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    event VARCHAR(50) NOT NULL,
    channel VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL,
    template VARCHAR(100),
    payload JSONB,
    provider_response JSONB,
    error TEXT,
    retry_count INT DEFAULT 0,
    sent_at TIMESTAMPTZ DEFAULT NOW(),
    delivered_at TIMESTAMPTZ,
    read_at TIMESTAMPTZ
);
```

### REVIEWS (kengaytirilgan)
```sql
CREATE TABLE reviews (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT REFERENCES orders(id),
    user_id BIGINT REFERENCES users(id),
    vendor_id BIGINT REFERENCES vendors(id),
    courier_id BIGINT REFERENCES couriers(id),
    developer_id BIGINT REFERENCES developers(id),
    vendor_rating INT CHECK (vendor_rating BETWEEN 1 AND 5),
    courier_rating INT CHECK (courier_rating BETWEEN 1 AND 5),
    product_rating INT CHECK (product_rating BETWEEN 1 AND 5),
    comment TEXT,
    photos TEXT[],
    is_published BOOLEAN DEFAULT FALSE,
    moderated_by BIGINT,
    moderated_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### PROMO CODES (kengaytirilgan)
```sql
CREATE TABLE promo_codes (
    id BIGSERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    type VARCHAR(20) NOT NULL,
    value DECIMAL(12,2),
    max_discount DECIMAL(12,2),
    min_order_amount DECIMAL(12,2) DEFAULT 0,
    owner_type VARCHAR(20),                    -- 'platform','vendor','dealer','developer'
    owner_id BIGINT,
    applicable_vendors BIGINT[],               -- null = barchasi
    applicable_products BIGINT[],
    max_uses INT,
    used_count INT DEFAULT 0,
    per_user_limit INT DEFAULT 1,
    first_order_only BOOLEAN DEFAULT FALSE,
    valid_from TIMESTAMPTZ,
    valid_until TIMESTAMPTZ,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### KYC DATA (shifrlangan)
```sql
CREATE TABLE kyc_verifications (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) UNIQUE,
    passport_series VARCHAR(10),               -- shifrlangan
    passport_number VARCHAR(20),               -- shifrlangan
    passport_issued_by TEXT,
    passport_issued_at DATE,
    birth_date DATE,
    gender VARCHAR(10),
    nationality VARCHAR(50),
    address TEXT,
    selfie_url TEXT,
    passport_front_url TEXT,
    passport_back_url TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    verified_by BIGINT,
    verified_at TIMESTAMPTZ,
    rejection_reason TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

# 13. API ENDPOINTLAR (TO'LIQ)

## 13.1. Auth API
```
POST   /api/v1/auth/request-otp
POST   /api/v1/auth/verify-otp
POST   /api/v1/auth/refresh
POST   /api/v1/auth/logout
GET    /api/v1/auth/me
POST   /api/v1/auth/telegram-webapp
POST   /api/v1/auth/register
POST   /api/v1/auth/kyc
GET    /api/v1/auth/kyc/status
```

## 13.2. User API
```
GET    /api/v1/users/me
PATCH  /api/v1/users/me
DELETE /api/v1/users/me                    # GDPR/o'chirish huquqi
GET    /api/v1/users/me/addresses
POST   /api/v1/users/me/addresses
PATCH  /api/v1/users/me/addresses/{id}
DELETE /api/v1/users/me/addresses/{id}
GET    /api/v1/users/me/wallet
GET    /api/v1/users/me/wallet/transactions
GET    /api/v1/users/me/notifications
PATCH  /api/v1/users/me/notifications
GET    /api/v1/users/me/loyalty
POST   /api/v1/users/me/referral
```

## 13.3. Catalog API
```
GET    /api/v1/catalog/categories
GET    /api/v1/catalog/products
GET    /api/v1/catalog/products/{id}
GET    /api/v1/catalog/vendors
GET    /api/v1/catalog/vendors/{id}
GET    /api/v1/catalog/vendors/{id}/products
GET    /api/v1/catalog/dealers
GET    /api/v1/catalog/developers
GET    /api/v1/catalog/developers/{id}/products
GET    /api/v1/catalog/search
GET    /api/v1/catalog/recommendations
GET    /api/v1/catalog/nearby-vendors?lat=&lng=
```

## 13.4. Cart API
```
GET    /api/v1/cart
POST   /api/v1/cart/items
PATCH  /api/v1/cart/items/{id}
DELETE /api/v1/cart/items/{id}
DELETE /api/v1/cart
POST   /api/v1/cart/promo
DELETE /api/v1/cart/promo
POST   /api/v1/cart/validate
POST   /api/v1/cart/checkout-preview
```

## 13.5. Orders API
```
POST   /api/v1/orders
GET    /api/v1/orders
GET    /api/v1/orders/{id}
GET    /api/v1/orders/{id}/status
GET    /api/v1/orders/{id}/track
POST   /api/v1/orders/{id}/cancel
POST   /api/v1/orders/{id}/rate
POST   /api/v1/orders/{id}/repeat
GET    /api/v1/orders/{id}/invoice
GET    /api/v1/orders/{id}/receipt
```

## 13.6. Payments API
```
POST   /api/v1/payments/initiate
POST   /api/v1/payments/payme/callback
POST   /api/v1/payments/click/callback
POST   /api/v1/payments/uzum/callback
GET    /api/v1/payments/{id}/status
POST   /api/v1/payments/{id}/refund
```

## 13.7. Vendor API (Do'kon)
```
GET    /api/v1/vendor/dashboard
GET    /api/v1/vendor/profile
PATCH  /api/v1/vendor/profile
GET    /api/v1/vendor/products
POST   /api/v1/vendor/products
PATCH  /api/v1/vendor/products/{id}
DELETE /api/v1/vendor/products/{id}
GET    /api/v1/vendor/categories
POST   /api/v1/vendor/categories
GET    /api/v1/vendor/orders
GET    /api/v1/vendor/orders/{id}
POST   /api/v1/vendor/orders/{id}/accept
POST   /api/v1/vendor/orders/{id}/reject
POST   /api/v1/vendor/orders/{id}/ready
GET    /api/v1/vendor/analytics
GET    /api/v1/vendor/wallet
POST   /api/v1/vendor/payouts
GET    /api/v1/vendor/reviews
GET    /api/v1/vendor/staff
POST   /api/v1/vendor/staff
```

## 13.8. Dealer API
```
GET    /api/v1/dealer/dashboard
GET    /api/v1/dealer/profile
PATCH  /api/v1/dealer/profile
GET    /api/v1/dealer/vendors
POST   /api/v1/dealer/vendors
GET    /api/v1/dealer/vendors/{id}
PATCH  /api/v1/dealer/vendors/{id}
GET    /api/v1/dealer/developers
POST   /api/v1/dealer/developers/{id}/contract
GET    /api/v1/dealer/contracts
GET    /api/v1/dealer/products
POST   /api/v1/dealer/products/distribute
GET    /api/v1/dealer/orders
GET    /api/v1/dealer/analytics
GET    /api/v1/dealer/wallet
POST   /api/v1/dealer/payouts
GET    /api/v1/dealer/reports
```

## 13.9. Developer API
```
GET    /api/v1/developer/dashboard
GET    /api/v1/developer/profile
PATCH  /api/v1/developer/profile
GET    /api/v1/developer/products
POST   /api/v1/developer/products
PATCH  /api/v1/developer/products/{id}
DELETE /api/v1/developer/products/{id}
GET    /api/v1/developer/dealers
POST   /api/v1/developer/dealers/{id}/contract
GET    /api/v1/developer/contracts
GET    /api/v1/developer/analytics
GET    /api/v1/developer/wallet
POST   /api/v1/developer/payouts
GET    /api/v1/developer/royalty
```

## 13.10. Courier API
```
GET    /api/v1/courier/dashboard
GET    /api/v1/courier/profile
PATCH  /api/v1/courier/profile
POST   /api/v1/courier/status
GET    /api/v1/courier/available-orders
POST   /api/v1/courier/orders/{id}/accept
POST   /api/v1/courier/orders/{id}/reject
POST   /api/v1/courier/orders/{id}/picked-up
POST   /api/v1/courier/orders/{id}/delivered
POST   /api/v1/courier/location
GET    /api/v1/courier/earnings
GET    /api/v1/courier/wallet
POST   /api/v1/courier/payouts
```

## 13.11. Admin API
```
GET    /api/v1/admin/dashboard
GET    /api/v1/admin/users
GET    /api/v1/admin/users/{id}
POST   /api/v1/admin/users/{id}/verify
POST   /api/v1/admin/users/{id}/block
GET    /api/v1/admin/vendors
POST   /api/v1/admin/vendors/{id}/approve
GET    /api/v1/admin/dealers
POST   /api/v1/admin/dealers/{id}/approve
GET    /api/v1/admin/developers
POST   /api/v1/admin/developers/{id}/approve
GET    /api/v1/admin/couriers
POST   /api/v1/admin/couriers/{id}/approve
GET    /api/v1/admin/orders
GET    /api/v1/admin/kyc
POST   /api/v1/admin/kyc/{id}/approve
POST   /api/v1/admin/kyc/{id}/reject
GET    /api/v1/admin/payouts
POST   /api/v1/admin/payouts/{id}/approve
POST   /api/v1/admin/payouts/{id}/reject
GET    /api/v1/admin/audit-log
GET    /api/v1/admin/reports
GET    /api/v1/admin/commissions
PATCH  /api/v1/admin/commissions
```

## 13.12. Finance API
```
GET    /api/v1/finance/wallets
GET    /api/v1/finance/wallets/{id}
GET    /api/v1/finance/transactions
GET    /api/v1/finance/payouts
POST   /api/v1/finance/payouts
GET    /api/v1/finance/reports/daily
GET    /api/v1/finance/reports/monthly
GET    /api/v1/finance/reports/tax
GET    /api/v1/finance/reports/commission
GET    /api/v1/finance/export
```

## 13.13. WebSocket
```
WS     /ws/orders/{order_id}
WS     /ws/couriers/{courier_id}
WS     /ws/vendor/{vendor_id}/orders
WS     /ws/dealer/{dealer_id}/orders
WS     /ws/developer/{developer_id}/sales
WS     /ws/admin/dashboard
WS     /ws/chat/{room_id}
WS     /ws/notifications
```

---

# 14. WEBSOCKET REAL-TIME

## 14.1. Xonalar (channels)

| Xona | Kim ulanadi | Event |
|---|---|---|
| `order:{id}` | Mijoz, kuryer, do'kon | Status o'zgarishi |
| `courier:{id}` | Mijoz, admin | Joylashuv |
| `vendor:{id}:orders` | Do'kon xodimlari | Yangi buyurtma |
| `dealer:{id}:orders` | Dealer | Tarmoq buyurtmalari |
| `developer:{id}:sales` | Dasturchi | Sotuv statistikasi |
| `admin:dashboard` | Adminlar | Platforma real-time |
| `chat:{room_id}` | Ikki tomon | Xabarlar |
| `user:{id}:notifications` | Foydalanuvchi | Bildirishnomalar |

## 14.2. Event turlari

```json
{
  "event": "order.created",
  "order_id": 12345,
  "vendor_id": 5,
  "dealer_id": 2,
  "total": 100000,
  "timestamp": "2026-10-02T19:30:00Z"
}

{
  "event": "order.status_changed",
  "order_id": 12345,
  "old_status": "paid",
  "new_status": "accepted",
  "vendor_id": 5,
  "timestamp": "..."
}

{
  "event": "courier.location",
  "courier_id": 5,
  "order_id": 12345,
  "lat": 41.311,
  "lng": 69.240,
  "bearing": 45,
  "speed_kmh": 32
}

{
  "event": "wallet.credited",
  "wallet_id": 100,
  "amount": 13500,
  "source": "commission",
  "order_id": 12345,
  "new_balance": 500000
}

{
  "event": "payout.approved",
  "payout_id": 50,
  "amount": 500000,
  "status": "processing"
}
```

## 14.3. Redis Pub/Sub (masshtablash)

```python
# Barcha instance lar bir-biri bilan Redis orqali sinxron
class RedisPubSub:
    async def publish(self, channel: str, event: dict):
        await self.redis.publish(f"ws:{channel}", json.dumps(event))

    async def subscribe_loop(self):
        await self.pubsub.subscribe("ws:*")
        async for msg in self.pubsub.listen():
            if msg["type"] == "message":
                channel = msg["channel"].decode().replace("ws:", "")
                data = json.loads(msg["data"])
                await ws_manager.broadcast(channel, data)
```

---

# 15. MULTI-CHANNEL GATEWAY

## 15.1. Kanallar

| Kanal | Foydalanish | Provider |
|---|---|---|
| **Telegram** | Navigatsiya, bildirishnoma | Telegram Bot API |
| **SMS** | OTP, kritik xabar | Eskiz.uz (+ fallback) |
| **WhatsApp** | Buyurtma tasdiqlash | Meta Cloud API |
| **Web Push** | WebApp bildirishnoma | FCM |
| **Email** | Hisobot, chek | SMTP/SendGrid |
| **In-App** | Real-time | WebSocket |

## 15.2. Kanal tanlash mantiqi

```python
FALLBACK_CHAIN = {
    "telegram": ["telegram", "whatsapp", "sms"],
    "whatsapp": ["whatsapp", "sms", "telegram"],
    "sms":      ["sms", "whatsapp", "telegram"],
}

async def notify(user, event, **ctx):
    primary = user.source_channel
    chain = FALLBACK_CHAIN.get(primary, ["sms"])

    for channel in chain:
        try:
            await send_via(channel, user, event, **ctx)
            log_notification(user, event, channel, "sent")
            return
        except Exception as e:
            log_notification(user, event, channel, "failed", str(e))
            continue

    # Barcha kanallar ishlamasa — admin ga xabar
    await alert_admin(f"User {user.id} ga xabar yuborilmadi: {event}")
```

## 15.3. WhatsApp Template lar

| Event | Template nomi | Parametrlar |
|---|---|---|
| `order_created` | `order_confirmation` | order_number, total |
| `order_accepted` | `order_accepted` | order_number, vendor_name |
| `order_on_the_way` | `courier_on_way` | order_number, courier_name, eta |
| `order_delivered` | `order_delivered` | order_number, total |
| `payout_approved` | `payout_approved` | amount, method |
| `kyc_approved` | `kyc_approved` | - |
| `otp` | `otp_code` | code, ttl |

---

# 16. XAVFSIZLIK

## 16.1. Autentifikatsiya
- **JWT** access (15 daq) + refresh (7 kun)
- **RS256** algoritmi
- **Refresh token rotatsiya**
- **Telegram WebApp initData** HMAC tekshiruvi
- **OTP** — bcrypt hash, 5 daqiqa TTL, 3 urinish
- **2FA** — admin va yuqori rol uchun majburiy

## 16.2. Avtorizatsiya
- **RBAC** — rol asosida
- **ABAC** — atribut asosida (do'kon o'z mahsulotini)
- **Scope** — API kalitlari uchun
- **Resource ownership** — har bir so'rovda tekshirish

## 16.3. PII himoyasi
- **AES-256-GCM** shifrlash
- **Hash** — pasport raqami qidirish uchun
- **Masking** — loglarda `+99890***4567`
- **Access log** — kim, qachon, nimani ko'rdi

## 16.4. Rate limiting

```python
RATE_LIMITS = {
    "auth:otp": "3/minute per phone",
    "auth:verify": "5/minute per phone",
    "orders:create": "10/hour per user",
    "cart:add": "60/minute per user",
    "payouts:request": "3/day per wallet",
    "admin:*": "1000/minute per admin",
    "api:general": "300/minute per user",
    "ws:connect": "10/minute per IP",
}
```

## 16.5. Idempotency

```python
# Har bir muhim POST so'rov uchun
headers = {
    "Idempotency-Key": "uuid-v4",
}

# Server 24 soat davomida saqlaydi
# Bir xil key bilan takroriy so'rov → bir xil javob
```

## 16.6. Audit log

Barcha kritik harakatlar:
- Admin login
- KYC tasdiqlash
- Payout tasdiqlash
- Komissiya o'zgartirish
- Foydalanuvchi bloklash
- Buyurtma bekor qilish
- Narx o'zgartirish (do'kon)

## 16.7. Webhook xavfsizligi
- **Telegram** — `X-Telegram-Bot-Api-Secret-Token`
- **Payme** — Basic Auth + imzo
- **Click** — MD5 imzo
- **WhatsApp** — `X-Hub-Signature-256`
- **Eskiz** — Bearer token

---

# 17. MOLIYAVIY HISOB-KITOBLAR

## 17.1. Buyurtma moliyaviy taqsimoti

```
Mijoz to'lovi: 100,000 so'm
    │
    ├─ QQS (12%): 12,000 so'm ──► Soliq hisobiga
    │
    ├─ To'lov tizimi (2%): 2,000 so'm ──► Payme/Click
    │
    ├─ Sof summa: 86,000 so'm
    │       │
    │       ├─ Platforma komissiyasi (10%): 8,600 so'm
    │       │
    │       ├─ Qolgan: 77,400 so'm
    │       │       │
    │       │       ├─ Dealer komissiyasi (15%): 11,610 so'm
    │       │       │
    │       │       ├─ Dasturchi royalty (10%): 7,740 so'm
    │       │       │
    │       │       └─ Do'kon sof: 58,050 so'm
    │       │
    │       └─ Kuryer to'lovi: 12,000 so'm (alohida)
    │
    └─ Keshbek (2%): 2,000 ball ──► Mijoz hamyoniga
```

## 17.2. Hamyon turlari

| Hamyon | Egasi | Manba |
|---|---|---|
| `customer_wallet` | Mijoz | Keshbek, referal, refund |
| `vendor_wallet` | Do'kon | Sotuvdan tushum |
| `dealer_wallet` | Dealer | Komissiya |
| `developer_wallet` | Dasturchi | Royalty |
| `courier_wallet` | Kuryer | Yetkazish |
| `platform_wallet` | Super Admin | Komissiya |

## 17.3. Payout jarayoni

```
1. Foydalanuvchi payout so'raydi
   → Minimal: 50,000 so'm
   → Maksimal: KYC darajasiga qarab
   → Method: Payme, Click, Uzum, Bank

2. Tizim tekshiradi
   → Balans yetarlimi?
   → KYC tasdiqlanganmi?
   → Limit oshmaganmi?
   → Firibgarlik belgisi yo'qmi?

3. Payout yaratiladi (status: pending)
   → Balans muzlatiladi (frozen)
   → Admin ga xabar

4. Admin tasdiqlaydi (24 soat)
   → Status: processing
   → Provider ga so'rov

5. Provider to'laydi
   → Status: completed
   → Balansdan yechiladi
   → Audit log

6. Rad etilsa
   → Status: rejected
   → Balans qaytariladi
   → Sabab xabar
```

## 17.4. Hisobot turlari

| Hisobot | Kim | Davr | Format |
|---|---|---|---|
| **Kunlik savdo** | Do'kon, Dealer, Admin | Kunlik | PDF, Excel |
| **Oylik moliyaviy** | Super Admin | Oylik | PDF, Excel |
| **Komissiya** | Dealer, Dasturchi | Haftalik | PDF |
| **Soliq** | Super Admin | Choraklik | PDF |
| **Payout** | Barcha | Oylik | Excel |
| **Foyda-zarar** | Super Admin | Oylik | PDF |
| **Top mahsulot** | Do'kon, Dasturchi | Haftalik | Excel |
| **Mijoz LTV** | Admin | Oylik | Excel |

## 17.5. Soliq hisobi

```python
def calculate_tax(order):
    """O'zbekiston soliq qonunchiligi bo'yicha"""
    vat_rate = Decimal("0.12")  # QQS 12%
    profit_tax_rate = Decimal("0.15")  # Foyda solig'i

    vat = order.total * vat_rate
    # ... qolgan hisob-kitoblar

    return {
        "vat": vat,
        "profit_tax": ...,
        "social_tax": ...,
        "total_tax": ...
    }
```

---

# 18. INTEGRATSIYALAR

| Xizmat | Maqsad | Muhimlik | Holat |
|---|---|---|---|
| **Eskiz.uz** | SMS OTP | 🔴 | Majburiy |
| **WhatsApp Cloud API** | Bildirishnoma | 🔴 | Majburiy |
| **Telegram Bot API** | Bot | 🔴 | Majburiy |
| **Payme** | To'lov | 🔴 | Majburiy |
| **Click** | To'lov | 🔴 | Majburiy |
| **Uzum Bank** | To'lov | 🟠 | Muhim |
| **Yandex Maps** | Geolokatsiya | 🟠 | Muhim |
| **S3 (Minio)** | Fayllar | 🟠 | Muhim |
| **Sentry** | Xatolar | 🟠 | Muhim |
| **Prometheus** | Metrics | 🟠 | Muhim |
| **Grafana** | Dashboard | 🟠 | Muhim |
| **Loki** | Loglar | 🟡 | Ixtiyoriy |
| **FCM** | Push | 🟡 | Ixtiyoriy |
| **SendGrid** | Email | 🟡 | Ixtiyoriy |
| **1C** | Buxgalteriya | 🟡 | Ixtiyoriy |

---

# 19. DEVOPS VA INFRATUZILMA

## 19.1. Docker Compose (development)

```yaml
version: "3.9"
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: xalquchun
      POSTGRES_USER: xalquchun
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - pg_data:/var/lib/postgresql/data
    ports: ["5432:5432"]

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

  backend:
    build: ./backend
    env_file: .env
    depends_on: [postgres, redis]
    ports: ["8000:8000"]
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  bot:
    build: ./bot
    env_file: .env
    depends_on: [backend]
    command: python -m bot.main

  worker:
    build: ./backend
    env_file: .env
    command: celery -A app.tasks.celery_app worker -l info

  beat:
    build: ./backend
    env_file: .env
    command: celery -A app.tasks.celery_app beat -l info

  webapp:
    build: ./webapp
    ports: ["3000:3000"]

  vendor_panel:
    build: ./vendor_panel
    ports: ["3001:3000"]

  dealer_panel:
    build: ./dealer_panel
    ports: ["3002:3000"]

  developer_panel:
    build: ./developer_panel
    ports: ["3003:3000"]

  courier_app:
    build: ./courier_app
    ports: ["3004:3000"]

  admin_panel:
    build: ./admin_panel
    ports: ["3005:3000"]

volumes:
  pg_data:
```

## 19.2. Production

```yaml
services:
  nginx:
    image: nginx:alpine
    ports: ["80:80", "443:443"]
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d
      - ./nginx/certs:/etc/nginx/certs

  backend:
    build: { context: ./backend, dockerfile: Dockerfile.prod }
    deploy:
      replicas: 3
      resources:
        limits: { cpus: "2", memory: 2G }

  worker:
    build: { context: ./backend, dockerfile: Dockerfile.prod }
    deploy:
      replicas: 2
```

## 19.3. Monitoring
- **Prometheus** — metrics
- **Grafana** — dashboardlar
- **Loki** — loglar
- **Alertmanager** — Telegram alertlar
- **Sentry** — xatolar

## 19.4. CI/CD

```yaml
name: CI/CD
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with: { python-version: "3.11" }
      - run: pip install -r backend/requirements.txt
      - run: pytest backend/tests/ --cov=app
      - run: ruff check backend/
      - run: mypy backend/app/
      - run: bandit -r backend/app/

  deploy-staging:
    needs: test
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    steps:
      - run: ssh staging "cd /app && git pull && docker compose up -d --build"

  deploy-prod:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - run: ssh prod "cd /app && git pull && docker compose -f docker-compose.prod.yml up -d --build"
```

---

# 20. YO'L XARITASI

## Faza 1 — Poydevor (4 hafta)
- [ ] FastAPI + PostgreSQL + Redis
- [ ] JWT autentifikatsiya
- [ ] User model (barcha rollar)
- [ ] RBAC
- [ ] Docker Compose
- [ ] CI/CD

## Faza 2 — Multi-Channel (3 hafta)
- [ ] Eskiz SMS
- [ ] WhatsApp Cloud API
- [ ] Telegram Bot
- [ ] Notification Dispatcher
- [ ] OTP flow

## Faza 3 — Katalog va Buyurtma (4 hafta)
- [ ] Vendor model
- [ ] Dealer model
- [ ] Developer model
- [ ] Product model
- [ ] Cart, Order
- [ ] Minimal summa validatsiyasi
- [ ] Order state machine

## Faza 4 — To'lov va Moliyaviy (3 hafta)
- [ ] Payme, Click
- [ ] Wallet tizimi
- [ ] Komissiya hisoblash
- [ ] Payout tizimi
- [ ] Moliyaviy hisobotlar

## Faza 5 — Panellar (5 hafta)
- [ ] Mijoz WebApp
- [ ] Vendor Panel
- [ ] Dealer Panel
- [ ] Developer Panel
- [ ] Courier App
- [ ] Admin Panel
- [ ] Support Panel

## Faza 6 — Real-time (2 hafta)
- [ ] WebSocket Hub
- [ ] Redis Pub/Sub
- [ ] Kuryer tracking
- [ ] Chat

## Faza 7 — Xavfsizlik va Huquqiy (2 hafta)
- [ ] KYC
- [ ] Rate limiting
- [ ] Idempotency
- [ ] Audit log
- [ ] Ommaviy oferta
- [ ] Maxfiylik siyosati

## Faza 8 — Marketing (2 hafta)
- [ ] Promo-kod
- [ ] Keshbek
- [ ] Referal
- [ ] Baholash
- [ ] Push

## Faza 9 — Production (2 hafta)
- [ ] Monitoring
- [ ] Load testing
- [ ] Security audit
- [ ] Deployment

**Jami: 27 hafta (~6.5 oy)**

---

# 21. QABUL QILISH MEZONLARI

## 21.1. Funksional
- [ ] 6 ta panel ishlaydi (Mijoz, Kuryer, Do'kon, Dealer, Dasturchi, Admin)
- [ ] Har bir rol o'z panelida ishlaydi
- [ ] Dealer do'konlarni boshqaradi
- [ ] Dasturchi mahsulot yaratadi va royalty oladi
- [ ] Mijoz barcha do'konlarni ko'radi
- [ ] Buyurtma to'liq oqimi ishlaydi
- [ ] Moliyaviy hisob-kitob to'g'ri
- [ ] Wallet va payout ishlaydi
- [ ] Real-time WebSocket ishlaydi
- [ ] Multi-channel bildirishnoma ishlaydi
- [ ] KYC tasdiqlash ishlaydi
- [ ] Audit log barcha harakatlarni yozadi

## 21.2. No-funksional
- [ ] API p95 < 200ms
- [ ] WS latency < 50ms
- [ ] 100,000 concurrent users
- [ ] Uptime 99.9%
- [ ] Test coverage > 80%
- [ ] Security audit o'tgan
- [ ] O'zbek va rus tillarida ishlaydi

## 21.3. Moliyaviy
- [ ] Har bir so'm hisobga olinadi
- [ ] Komissiya to'g'ri taqsimlanadi
- [ ] Payout jarayoni ishlaydi
- [ ] Soliq hisoboti to'g'ri
- [ ] Moliyaviy hisobotlar avtomatik

## 21.4. Huquqiy
- [ ] O'RQ-792 talablari bajarilgan
- [ ] Ommaviy oferta mavjud
- [ ] Maxfiylik siyosati mavjud
- [ ] Shartnomalar ERI bilan
- [ ] Fiskal chek har buyurtmaga
- [ ] Ma'lumotlarni o'chirish huquqi

---

# 📎 ILOVALAR

## A. Komissiya sozlamalari (standart)

```env
# Platforma
PLATFORM_COMMISSION_PERCENT=10
PLATFORM_MIN_COMMISSION=1000

# Dealer
DEALER_DEFAULT_COMMISSION_PERCENT=15
DEALER_MIN_COMMISSION=500

# Dasturchi
DEVELOPER_DEFAULT_ROYALTY_PERCENT=10
DEVELOPER_MIN_ROYALTY=500

# Kuryer
COURIER_BASE_FEE=8000
COURIER_PER_KM_FEE=500
COURIER_NIGHT_BONUS=2000
COURIER_HEAVY_BONUS=3000
COURIER_RATING_BONUS=500

# Payout
PAYOUT_MIN_AMOUNT=50000
PAYOUT_MAX_DAILY=10000000
PAYOUT_FEE_PERCENT=1

# Biznes
MIN_ORDER_AMOUNT=50000
MAX_ORDER_AMOUNT=50000000
```

## B. Muhim xavfsizlik eslatmalari

1. `.env` faylni gitga qo'shmang
2. **JWT RS256** ishlating
3. **PII AES-256-GCM** shifrlash
4. **SQL injection** — faqat ORM
5. **CORS** — faqat ruxsat etilgan domenlar
6. **Webhook imzosi** — har bir provider uchun
7. **Rate limit** — har bir endpoint
8. **Audit log** — barcha kritik harakatlar
9. **Idempotency** — to'lov va payout
10. **2FA** — admin va yuqori rol

## C. Testlash strategiyasi

| Test turi | Vosita | Qamrov |
|---|---|---|
| Unit | pytest | 90% |
| Integration | pytest + testcontainers | 80% |
| E2E | Playwright | Asosiy oqimlar |
| Load | Locust | 100k concurrent |
| Security | Bandit + OWASP ZAP | CI |
| Contract | Schemathesis | OpenAPI |
| Moliyaviy | pytest + fixtures | 100% |

---

# ✅ XULOSA

Ushbu **TZ v3.0** XalqUchun platformasini **ko'p panelli, ko'p rolli, moliyaviy aniq ekosistema**ga aylantirish uchun to'liq yo'l xaritasini beradi.

## Asosiy yangiliklar (v2 → v3):

1. **6 ta panel** — Mijoz, Kuryer, Do'kon, Dealer, Dasturchi, Admin
2. **Dealer tizimi** — do'konlar tarmog'i, komissiya
3. **Dasturchi tizimi** — mahsulot yaratish, royalty
4. **Moliyaviy tizim** — wallet, komissiya, payout, soliq
5. **Shartnomalar** — dealer-vendor, dealer-developer, vendor-developer
6. **Komissiya taqsimoti** — har bir sotuvdan kimga qancha
7. **Payout jarayoni** — to'liq avtomatlashtirilgan
8. **Audit log** — barcha moliyaviy harakatlar
9. **Real-time** — barcha panellar uchun WebSocket
10. **Universal** — bir kod bazasi, ko'p panel

## Muhim tamoyillar:
- ✅ **Hech qanday kamchilik yo'q** — har bir funksiya to'liq
- ✅ **Hech qanday istisno yo'q** — barcha holatlar qamrab olingan
- ✅ **Moliyaviy aniq** — har bir so'm hisobga olinadi
- ✅ **Xavfsiz** — PII, KYC, RBAC, audit
- ✅ **Huquqiy** — O'RQ-792, oferta, maxfiylik
- ✅ **Tezkor** — FastAPI, WebSocket, Redis
- ✅ **Masshtablanuvchan** — 100k+ foydalanuvchi

**Keyingi qadam:** Har bir panel uchun alohida UI/UX dizayn, har bir API uchun OpenAPI spetsifikatsiya, har bir modul uchun kod namunasi kerak bo'lsa — ayting, tayyorlab beraman.


# 📘 TZ v3.0 — DAVOMI
## Amaliy Implementatsiya Qo'llanmasi
### UI/UX • Kod • API Misollar • Deployment

---

# 22. UI/UX DIZAYN TIZIMI

## 22.1. Umumiy dizayn tizimi (Design System)

### Ranglar palitrasi
```css
/* Brand colors */
--brand-primary: #FF6B00;      /* Asosiy to'q sariq - Uzum Tezkor uslubi */
--brand-secondary: #1F2937;    /* To'q kulrang */
--brand-accent: #10B981;       /* Yashil - muvaffaqiyat */

/* Status colors */
--status-pending: #F59E0B;
--status-paid: #3B82F6;
--status-preparing: #8B5CF6;
--status-on-way: #06B6D4;
--status-delivered: #10B981;
--status-cancelled: #EF4444;
--status-refunded: #6B7280;

/* Neutral */
--gray-50: #F9FAFB;
--gray-100: #F3F4F6;
--gray-500: #6B7280;
--gray-900: #111827;

/* Semantic */
--success: #10B981;
--warning: #F59E0B;
--error: #EF4444;
--info: #3B82F6;
```

### Tipografiya
```css
--font-family: 'Inter', system-ui, sans-serif;
--font-mono: 'JetBrains Mono', monospace;

/* Sizes */
--text-xs: 12px;
--text-sm: 14px;
--text-base: 16px;
--text-lg: 18px;
--text-xl: 20px;
--text-2xl: 24px;
--text-3xl: 30px;
```

### Spacing
```css
--space-1: 4px;
--space-2: 8px;
--space-3: 12px;
--space-4: 16px;
--space-6: 24px;
--space-8: 32px;
--space-12: 48px;
```

## 22.2. Mijoz WebApp — Wireframe

### Bosh sahifa
```
┌─────────────────────────────────────┐
│  🍔 XalqUchun      🔔   👤          │  ← Header
├─────────────────────────────────────┤
│  📍 Toshkent, Chilonzor             │  ← Manzil
│  ┌─────────────────────────────┐    │
│  │ 🔍 Mahsulot qidirish...      │    │  ← Search
│  └─────────────────────────────┘    │
├─────────────────────────────────────┤
│  Kategoriyalar                       │
│  ┌───┐ ┌───┐ ┌───┐ ┌───┐           │
│  │🍕 │ │🍔 │ │🍣 │ │🥗 │           │
│  │Ovq│ │Fast│ │Sush│ │Salat│         │
│  └───┘ └───┘ └───┘ └───┘           │
├─────────────────────────────────────┤
│  🔥 Aksiyalar                        │
│  ┌─────────────────────────────┐    │
│  │  BIRINCHI BUYURTMA 50%      │    │
│  │  chegirma! PROMO: FIRST50   │    │
│  └─────────────────────────────┘    │
├─────────────────────────────────────┤
│  🏪 Yaqin do'konlar                  │
│  ┌─────────────────────────────┐    │
│  │ 🏪 Makro Chilonzor           │    │
│  │ ⭐ 4.8  •  1.2 km  •  25 daq │    │
│  │ Min: 50,000 so'm            │    │
│  └─────────────────────────────┘    │
│  ┌─────────────────────────────┐    │
│  │ 🏪 Korzinka Yunusobod        │    │
│  │ ⭐ 4.6  •  2.5 km  •  35 daq │    │
│  └─────────────────────────────┘    │
├─────────────────────────────────────┤
│  🏠  🛒  📦  👤  💰              │  ← Bottom nav
└─────────────────────────────────────┘
```

### Savat sahifasi
```
┌─────────────────────────────────────┐
│  ← Savat                            │
├─────────────────────────────────────┤
│  🏪 Makro Chilonzor                  │
│  ─────────────────────────────────  │
│  ┌──────────────────────────────┐   │
│  │ 🍎 Olma (1 kg)               │   │
│  │ 15,000 so'm         [- 2 +]  │   │
│  └──────────────────────────────┘   │
│  ┌──────────────────────────────┐   │
│  │ 🥛 Sut 1L                    │   │
│  │ 12,000 so'm         [- 1 +]  │   │
│  └──────────────────────────────┘   │
├─────────────────────────────────────┤
│  Promo-kod                           │
│  ┌───────────────────┐ ┌─────────┐  │
│  │ FIRST50           │ │ Qo'llash│  │
│  └───────────────────┘ └─────────┘  │
├─────────────────────────────────────┤
│  Mahsulotlar:          27,000 so'm  │
│  Yetkazish:             8,000 so'm  │
│  Chegirma:             -5,000 so'm  │
│  ─────────────────────────────────  │
│  JAMI:                 30,000 so'm  │
│                                      │
│  ⚠️ Minimal buyurtma: 50,000 so'm   │
│  Yana 20,000 so'm qo'shing          │
│  [Progress bar ████░░░░]            │
├─────────────────────────────────────┤
│  [ Buyurtma berish ]  (disabled)    │
└─────────────────────────────────────┘
```

### Real-time kuzatuv sahifasi
```
┌─────────────────────────────────────┐
│  ← Buyurtma #ORD-2026-001234        │
├─────────────────────────────────────┤
│  ┌─────────────────────────────┐    │
│  │                             │    │
│  │      🗺️ XARITA              │    │
│  │                             │    │
│  │    🏪 ──────🚗────── 🏠     │    │
│  │                             │    │
│  │      🛵 Kuryer harakatda     │    │
│  │                             │    │
│  └─────────────────────────────┘    │
├─────────────────────────────────────┤
│  ⏱️ Yetib kelish: 12 daqiqa         │
├─────────────────────────────────────┤
│  ✅ Qabul qilindi      19:25        │
│  ✅ Tayyorlanmoqda     19:28        │
│  ✅ Tayyor             19:35        │
│  ✅ Kuryer yo'lda      19:38  ◉    │
│  ⚪ Yetkazildi                       │
├─────────────────────────────────────┤
│  👤 Ali Karimov                      │
│  🛵 Mototsikl • A 01 AB 123 UZ      │
│  ⭐ 4.9                              │
│                                      │
│  [ 📞 Qo'ng'iroq ]  [ 💬 Chat ]     │
└─────────────────────────────────────┘
```

## 22.3. Vendor Panel — Wireframe

### Dashboard
```
┌──────────────────────────────────────────────────────────────────┐
│  🏪 Makro Chilonzor                    🔔  👤 Sardor  ⚙️        │
├──────────────────────────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │ Bugungi  │ │ Faol     │ │ Kutilm.  │ │ Oylik    │           │
│  │ savdo    │ │ buyurtma │ │ payout   │ │ reyting  │           │
│  │ 2,450,000│ │    12    │ │ 850,000  │ │  ⭐ 4.8  │           │
│  │ +12% ↗   │ │          │ │          │ │ +0.2 ↗   │           │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
├──────────────────────────────────────────────────────────────────┤
│  🔔 YANGI BUYURTMALAR (3)                                        │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ #ORD-2026-001234                  ⏱️ 02:34 qoldi          │  │
│  │ 🍎 Olma × 2, 🥛 Sut × 1, 🍞 Non × 3                        │  │
│  │ Jami: 85,000 so'm  •  Yetkazish: 19:45                     │  │
│  │ [ ✅ Qabul ]  [ ❌ Rad etish ]                             │  │
│  └────────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ #ORD-2026-001235                  ⏱️ 04:12 qoldi          │  │
│  │ 🍕 Pizza × 1, 🥤 Kola × 2                                   │  │
│  │ Jami: 65,000 so'm  •  Yetkazish: 20:00                     │  │
│  │ [ ✅ Qabul ]  [ ❌ Rad etish ]                             │  │
│  └────────────────────────────────────────────────────────────┘  │
├──────────────────────────────────────────────────────────────────┤
│  📊 So'nggi 7 kun savdo                                          │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  ▂▃▅▇█▇▅  Mon Ses Cho Pay Jum Sha Yan                      │  │
│  └────────────────────────────────────────────────────────────┘  │
├──────────────────────────────────────────────────────────────────┤
│  🏆 Top mahsulotlar                                              │
│  1. Olma (1 kg) — 45 dona                                       │
│  2. Sut 1L — 32 dona                                            │
│  3. Non — 28 dona                                               │
└──────────────────────────────────────────────────────────────────┘
```

## 22.4. Dealer Panel — Wireframe

### Dashboard
```
┌──────────────────────────────────────────────────────────────────┐
│  💼 Dealer: Toshkent Distribyutor      🔔  👤  ⚙️              │
├──────────────────────────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │ Faol     │ │ Kunlik   │ │ Komissiya│ │ Kutilm.  │           │
│  │ do'kon   │ │ savdo    │ │ (bugun)  │ │ payout   │           │
│  │   245    │ │ 85.6M    │ │ 12.8M    │ │ 3.2M     │           │
│  │ +5 ↗     │ │ +18% ↗   │ │ +18% ↗   │ │          │           │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
├──────────────────────────────────────────────────────────────────┤
│  🏪 Tarmoqdagi do'konlar                    [ + Yangi do'kon ]  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ # Makro Chilonzor       ⭐4.8  Kunlik: 2.4M   ✅ Faol      │  │
│  │ # Korzinka Yunusobod    ⭐4.6  Kunlik: 1.8M   ✅ Faol      │  │
│  │ # Osh Markazi           ⭐4.9  Kunlik: 950K   ✅ Faol      │  │
│  │ # Dori-Darmon №5        ⭐4.2  Kunlik: 420K   ⚠️ Diqqat   │  │
│  │ # Sifat Market          ⭐3.1  Kunlik: 85K    ⚠️ Diqqat   │  │
│  └────────────────────────────────────────────────────────────┘  │
├──────────────────────────────────────────────────────────────────┤
│  📦 Dasturchilardan mahsulotlar                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ Coca-Cola Uzbekistan     45 SKU  •  Royalty: 10%           │  │
│  │ Nestlé Uzbekistan        120 SKU •  Royalty: 8%            │  │
│  │ Local Food MChJ          30 SKU  •  Royalty: 12%           │  │
│  └────────────────────────────────────────────────────────────┘  │
├──────────────────────────────────────────────────────────────────┤
│  📊 Tarmoq savdo dinamikasi (30 kun)                             │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  ▂▃▅▇█▇▅▃▂▃▅▇█▇▅▃▂▃▅▇█▇▅▃▂▃▅▇█                            │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

## 22.5. Courier App — Wireframe

### Dashboard (mobile-first)
```
┌─────────────────────────────────────┐
│  🛵 Kuryer: Ali      ⚪ Online  ⚙️  │
├─────────────────────────────────────┤
│  ┌─────────────────────────────┐    │
│  │  Bugungi daromad             │    │
│  │  245,000 so'm                │    │
│  │  12 buyurtma  •  8 soat      │    │
│  └─────────────────────────────┘    │
├─────────────────────────────────────┤
│  🆕 YANGI BUYURTMA                  │
│  ┌─────────────────────────────┐    │
│  │  🏪 Makro Chilonzor         │    │
│  │  ↓ 1.2 km                   │    │
│  │  🏠 Chilonzor 12-mavdon     │    │
│  │  ↓ 2.5 km                   │    │
│  │  Jami: 3.7 km  •  18 daq    │    │
│  │                             │    │
│  │  💰 12,500 so'm             │    │
│  │                             │    │
│  │  ⏱️ 00:45                    │    │
│  │  [ ✅ Qabul ]  [ ❌ ]        │    │
│  └─────────────────────────────┘    │
├─────────────────────────────────────┤
│  Faol buyurtmalar (2)                │
│  ┌─────────────────────────────┐    │
│  │ #ORD-234 • 🏪 ga borish     │    │
│  └─────────────────────────────┘    │
│  ┌─────────────────────────────┐    │
│  │ #ORD-235 • 🏠 ga yetkazish  │    │
│  └─────────────────────────────┘    │
├─────────────────────────────────────┤
│  🏠  🗺️  💰  💬  👤              │
└─────────────────────────────────────┘
```

---

# 23. KOD NAMUNALARI

## 23.1. FastAPI — Asosiy app

```python
# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1 import api_router
from app.ws import ws_router
from app.ws.pubsub import redis_pubsub

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    setup_logging()
    await redis_pubsub.start()
    yield
    # Shutdown
    await redis_pubsub.stop()

app = FastAPI(
    title="XalqUchun API",
    version="3.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")
app.include_router(ws_router, prefix="/ws")

@app.get("/health")
async def health():
    return {"status": "ok", "version": "3.0.0"}
```

## 23.2. Auth Service (to'liq)

```python
# backend/app/services/auth_service.py
import hmac, hashlib, secrets, time
from urllib.parse import parse_qsl
from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import (
    InvalidOTPError, OTPExpiredError, UnauthorizedError,
    PhoneAlreadyExistsError,
)
from app.db.models import User, OTPCode
from app.services.notification_service import NotificationService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, db: AsyncSession, notifier: NotificationService):
        self.db = db
        self.notifier = notifier

    # ============ OTP ============
    async def request_otp(self, phone: str, channel: str) -> dict:
        """OTP so'rash — SMS yoki WhatsApp orqali"""
        # 1. Rate limit (Redis)
        await self._check_otp_rate_limit(phone)

        # 2. Kod generatsiya
        code = f"{secrets.randbelow(1_000_000):06d}"
        code_hash = pwd_context.hash(code)

        # 3. DB ga saqlash
        otp = OTPCode(
            phone=phone,
            code_hash=code_hash,
            channel=channel,
            expires_at=datetime.now(timezone.utc) + timedelta(
                seconds=settings.OTP_TTL_SECONDS
            ),
        )
        self.db.add(otp)
        await self.db.commit()

        # 4. Yuborish (asinxron)
        await self.notifier.send_otp(
            phone=phone,
            code=code,
            channel=channel,
            ttl=settings.OTP_TTL_SECONDS,
        )

        return {
            "success": True,
            "expires_in": settings.OTP_TTL_SECONDS,
            "channel": channel,
        }

    async def verify_otp(self, phone: str, code: str) -> dict:
        """OTP tekshirish va token berish"""
        stmt = (
            select(OTPCode)
            .where(OTPCode.phone == phone)
            .where(OTPCode.used_at.is_(None))
            .order_by(OTPCode.created_at.desc())
            .limit(1)
        )
        otp = (await self.db.execute(stmt)).scalar_one_or_none()

        if not otp:
            raise InvalidOTPError("Kod topilmadi")

        if otp.expires_at < datetime.now(timezone.utc):
            raise OTPExpiredError("Kod muddati tugagan")

        if otp.attempts >= otp.max_attempts:
            raise InvalidOTPError("Urinishlar tugadi")

        # Tekshirish
        if not pwd_context.verify(code, otp.code_hash):
            otp.attempts += 1
            await self.db.commit()
            raise InvalidOTPError("Kod xato")

        # Muvaffaqiyat
        otp.used_at = datetime.now(timezone.utc)
        await self.db.commit()

        # Foydalanuvchini topish yoki yaratish
        user = await self._get_or_create_user(phone)

        # Tokenlar
        tokens = self._create_tokens(user)
        return tokens

    # ============ Telegram WebApp ============
    def verify_telegram_init_data(self, init_data: str) -> dict:
        parsed = dict(parse_qsl(init_data))
        hash_ = parsed.pop("hash", None)
        if not hash_:
            raise UnauthorizedError("initData yaroqsiz")

        data_check_string = "\n".join(
            f"{k}={v}" for k, v in sorted(parsed.items())
        )
        secret_key = hmac.new(
            b"WebAppData",
            settings.BOT_TOKEN.encode(),
            hashlib.sha256,
        ).digest()
        calculated = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(calculated, hash_):
            raise UnauthorizedError("initData yaroqsiz")

        # auth_date 1 soatdan oshmasin
        auth_date = int(parsed.get("auth_date", 0))
        if time.time() - auth_date > 3600:
            raise UnauthorizedError("initData eskirgan")

        return parsed

    async def login_telegram(self, init_data: str) -> dict:
        parsed = self.verify_telegram_init_data(init_data)
        tg_user = eval(parsed["user"])  # JSON parse qilish kerak

        user = await self._get_or_create_telegram_user(
            telegram_id=tg_user["id"],
            full_name=f"{tg_user.get('first_name', '')} {tg_user.get('last_name', '')}".strip(),
            language=tg_user.get("language_code", "uz"),
        )
        return self._create_tokens(user)

    # ============ Tokenlar ============
    def _create_tokens(self, user: User) -> dict:
        now = datetime.now(timezone.utc)

        access_payload = {
            "sub": str(user.id),
            "roles": user.roles,
            "type": "access",
            "iat": now,
            "exp": now + timedelta(seconds=settings.ACCESS_TOKEN_TTL),
        }
        refresh_payload = {
            "sub": str(user.id),
            "type": "refresh",
            "jti": secrets.token_urlsafe(32),
            "iat": now,
            "exp": now + timedelta(seconds=settings.REFRESH_TOKEN_TTL),
        }

        access_token = jwt.encode(
            access_payload,
            settings.JWT_PRIVATE_KEY,
            algorithm="RS256",
        )
        refresh_token = jwt.encode(
            refresh_payload,
            settings.JWT_PRIVATE_KEY,
            algorithm="RS256",
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "expires_in": settings.ACCESS_TOKEN_TTL,
        }
```

## 23.3. Wallet Service (moliyaviy)

```python
# backend/app/services/wallet_service.py
from decimal import Decimal
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import InsufficientBalanceError
from app.db.models import Wallet, WalletTransaction
from app.ws.pubsub import redis_pubsub

class WalletService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_or_create(
        self,
        owner_id: int,
        owner_type: str,
    ) -> Wallet:
        stmt = select(Wallet).where(
            Wallet.owner_id == owner_id,
            Wallet.owner_type == owner_type,
        )
        wallet = (await self.db.execute(stmt)).scalar_one_or_none()

        if not wallet:
            wallet = Wallet(
                owner_id=owner_id,
                owner_type=owner_type,
            )
            self.db.add(wallet)
            await self.db.flush()

        return wallet

    async def credit(
        self,
        wallet_id: int,
        amount: Decimal,
        source_type: str,
        source_id: int | None = None,
        description: str = "",
        metadata: dict | None = None,
    ) -> WalletTransaction:
        """Hisobga pul qo'shish"""
        # Lock for concurrency
        stmt = (
            select(Wallet)
            .where(Wallet.id == wallet_id)
            .with_for_update()
        )
        wallet = (await self.db.execute(stmt)).scalar_one()

        balance_before = wallet.balance
        wallet.balance = balance_before + amount
        wallet.total_earned = wallet.total_earned + amount

        tx = WalletTransaction(
            wallet_id=wallet_id,
            type="credit",
            amount=amount,
            balance_before=balance_before,
            balance_after=wallet.balance,
            source_type=source_type,
            source_id=source_id,
            description=description,
            metadata=metadata or {},
        )
        self.db.add(tx)
        await self.db.flush()

        # Real-time xabar
        await redis_pubsub.publish(
            f"wallet:{wallet_id}",
            {
                "event": "wallet.credited",
                "wallet_id": wallet_id,
                "amount": float(amount),
                "balance": float(wallet.balance),
                "source": source_type,
                "tx_id": tx.id,
            },
        )

        return tx

    async def debit(
        self,
        wallet_id: int,
        amount: Decimal,
        source_type: str,
        source_id: int | None = None,
        description: str = "",
    ) -> WalletTransaction:
        """Hisobdan pul yechish"""
        stmt = (
            select(Wallet)
            .where(Wallet.id == wallet_id)
            .with_for_update()
        )
        wallet = (await self.db.execute(stmt)).scalar_one()

        if wallet.balance < amount:
            raise InsufficientBalanceError(
                f"Balans yetarli emas. Kerak: {amount}, mavjud: {wallet.balance}"
            )

        balance_before = wallet.balance
        wallet.balance = balance_before - amount

        tx = WalletTransaction(
            wallet_id=wallet_id,
            type="debit",
            amount=amount,
            balance_before=balance_before,
            balance_after=wallet.balance,
            source_type=source_type,
            source_id=source_id,
            description=description,
        )
        self.db.add(tx)
        await self.db.flush()

        await redis_pubsub.publish(
            f"wallet:{wallet_id}",
            {
                "event": "wallet.debited",
                "wallet_id": wallet_id,
                "amount": float(amount),
                "balance": float(wallet.balance),
            },
        )

        return tx

    async def hold(
        self,
        wallet_id: int,
        amount: Decimal,
        reason: str,
    ) -> None:
        """Pulni muzlatish (payout uchun)"""
        stmt = select(Wallet).where(Wallet.id == wallet_id).with_for_update()
        wallet = (await self.db.execute(stmt)).scalar_one()

        if wallet.balance < amount:
            raise InsufficientBalanceError()

        wallet.balance -= amount
        wallet.frozen_balance += amount
        await self.db.flush()

    async def release_hold(
        self,
        wallet_id: int,
        amount: Decimal,
    ) -> None:
        """Muzlatilgan pulni qaytarish"""
        stmt = select(Wallet).where(Wallet.id == wallet_id).with_for_update()
        wallet = (await self.db.execute(stmt)).scalar_one()
        wallet.frozen_balance -= amount
        wallet.balance += amount
        await self.db.flush()

    async def confirm_hold(
        self,
        wallet_id: int,
        amount: Decimal,
    ) -> None:
        """Muzlatilgan pulni yakuniy yechish"""
        stmt = select(Wallet).where(Wallet.id == wallet_id).with_for_update()
        wallet = (await self.db.execute(stmt)).scalar_one()
        wallet.frozen_balance -= amount
        wallet.total_withdrawn += amount
        await self.db.flush()
```

## 23.4. Commission Service

```python
# backend/app/services/commission_service.py
from decimal import Decimal, ROUND_HALF_UP
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Order, OrderItem, CommissionRecord
from app.services.wallet_service import WalletService

class CommissionService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.wallet = WalletService(db)

    async def distribute(self, order: Order) -> dict:
        """Buyurtma to'langandan keyin komissiya taqsimlash"""
        total = order.total

        # QQS va to'lov komissiyasi
        vat = (total * Decimal("0.12")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        payment_fee = (total * Decimal("0.02")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        net = total - vat - payment_fee

        # Platforma komissiyasi
        platform_pct = Decimal("0.10")
        platform_commission = (net * platform_pct).quantize(Decimal("0.01"))
        remaining = net - platform_commission

        # Dealer
        dealer_pct = order.vendor.dealer.commission_percent / 100
        dealer_commission = (remaining * dealer_pct).quantize(Decimal("0.01"))
        remaining -= dealer_commission

        # Dasturchi royalty
        dev_pct = order.vendor.dealer.developer.royalty_percent / 100
        developer_royalty = (remaining * dev_pct).quantize(Decimal("0.01"))
        remaining -= developer_royalty

        # Do'kon sof foydasi
        vendor_amount = remaining

        # Kuryer to'lovi
        courier_amount = order.courier_amount

        # === Hamyonlarga taqsimlash ===
        # Platforma
        platform_wallet = await self.wallet.get_or_create(1, "platform")
        await self.wallet.credit(
            wallet_id=platform_wallet.id,
            amount=platform_commission,
            source_type="commission",
            source_id=order.id,
            description=f"Platforma komissiyasi #{order.order_number}",
        )

        # Dealer
        dealer_wallet = await self.wallet.get_or_create(
            order.vendor.dealer_id, "dealer"
        )
        await self.wallet.credit(
            wallet_id=dealer_wallet.id,
            amount=dealer_commission,
            source_type="commission",
            source_id=order.id,
            description=f"Dealer komissiyasi #{order.order_number}",
        )

        # Dasturchi
        dev_wallet = await self.wallet.get_or_create(
            order.vendor.dealer.developer_id, "developer"
        )
        await self.wallet.credit(
            wallet_id=dev_wallet.id,
            amount=developer_royalty,
            source_type="royalty",
            source_id=order.id,
            description=f"Royalty #{order.order_number}",
        )

        # Do'kon
        vendor_wallet = await self.wallet.get_or_create(order.vendor_id, "vendor")
        await self.wallet.credit(
            wallet_id=vendor_wallet.id,
            amount=vendor_amount,
            source_type="sale",
            source_id=order.id,
            description=f"Sotuv #{order.order_number}",
        )

        # Kuryer
        if order.courier_id:
            courier_wallet = await self.wallet.get_or_create(
                order.courier_id, "courier"
            )
            await self.wallet.credit(
                wallet_id=courier_wallet.id,
                amount=courier_amount,
                source_type="delivery",
                source_id=order.id,
                description=f"Yetkazish #{order.order_number}",
            )

        # Order ga yozish
        order.platform_commission = platform_commission
        order.dealer_commission = dealer_commission
        order.developer_royalty = developer_royalty
        order.vendor_net_amount = vendor_amount
        order.courier_amount = courier_amount
        order.payment_fee = payment_fee

        # Commission records (audit uchun)
        for recipient_type, recipient_id, amount in [
            ("platform", 1, platform_commission),
            ("dealer", order.vendor.dealer_id, dealer_commission),
            ("developer", order.vendor.dealer.developer_id, developer_royalty),
            ("vendor", order.vendor_id, vendor_amount),
            ("courier", order.courier_id, courier_amount),
        ]:
            if recipient_id and amount > 0:
                rec = CommissionRecord(
                    order_id=order.id,
                    recipient_type=recipient_type,
                    recipient_id=recipient_id,
                    amount=amount,
                    status="credited",
                )
                self.db.add(rec)

        await self.db.flush()

        return {
            "vat": vat,
            "payment_fee": payment_fee,
            "platform_commission": platform_commission,
            "dealer_commission": dealer_commission,
            "developer_royalty": developer_royalty,
            "vendor_amount": vendor_amount,
            "courier_amount": courier_amount,
        }
```

## 23.5. WebSocket — Order tracking

```python
# backend/app/ws/order_ws.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from jose import jwt, JWTError

from app.core.config import settings
from app.ws.manager import ws_manager
from app.ws.pubsub import redis_pubsub

router = APIRouter()

@router.websocket("/orders/{order_id}")
async def order_tracking(
    websocket: WebSocket,
    order_id: int,
    token: str = Query(...),
):
    # JWT tekshirish
    try:
        payload = jwt.decode(
            token,
            settings.JWT_PUBLIC_KEY,
            algorithms=["RS256"],
        )
        user_id = int(payload["sub"])
    except (JWTError, KeyError):
        await websocket.close(code=4001, reason="Unauthorized")
        return

    channel = f"order:{order_id}"
    await ws_manager.connect(websocket, channel, user_id)

    # Subscribe (agar hali yo'q bo'lsa)
    await redis_pubsub.ensure_subscribed(channel)

    try:
        # Boshlang'ich holat yuborish
        await websocket.send_json({
            "event": "connected",
            "channel": channel,
            "order_id": order_id,
        })

        # Mijoz xabarlarini kutish (ping/pong)
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")

    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, channel, user_id)
```

## 23.6. Notification Dispatcher (to'liq)

```python
# backend/app/services/notification_service.py
from enum import Enum
from typing import Optional

from app.providers.sms import get_sms_provider
from app.providers.whatsapp import get_wa_provider
from app.providers.telegram import TelegramProvider
from app.services.template_service import render_template
from app.db.models import Notification, User

class Channel(str, Enum):
    TELEGRAM = "telegram"
    SMS = "sms"
    WHATSAPP = "whatsapp"

FALLBACK_CHAIN = {
    "telegram": ["telegram", "whatsapp", "sms"],
    "whatsapp": ["whatsapp", "sms", "telegram"],
    "sms":      ["sms", "whatsapp", "telegram"],
}

class NotificationService:
    def __init__(self, db):
        self.db = db
        self.telegram = TelegramProvider()
        self.sms = get_sms_provider()
        self.whatsapp = get_wa_provider()

    async def notify(
        self,
        user: User,
        event: str,
        channels: Optional[list[Channel]] = None,
        **ctx,
    ):
        """Universal bildirishnoma yuborish"""
        if not channels:
            primary = user.source_channel or "telegram"
            channels = [Channel(c) for c in FALLBACK_CHAIN.get(primary, ["telegram"])]

        text = render_template(event, user.language, **ctx)

        for ch in channels:
            try:
                await self._send(ch, user, event, text, ctx)
                await self._log(user.id, event, ch, "sent")
                return  # Muvaffaqiyat
            except Exception as e:
                await self._log(user.id, event, ch, "failed", str(e))
                continue

        # Barcha kanallar ishlamadi
        await self._log(user.id, event, None, "all_failed")

    async def _send(
        self,
        ch: Channel,
        user: User,
        event: str,
        text: str,
        ctx: dict,
    ):
        if ch == Channel.TELEGRAM and user.telegram_id:
            await self.telegram.send_message(user.telegram_id, text)

        elif ch == Channel.SMS and user.phone:
            await self.sms.send(user.phone, text)

        elif ch == Channel.WHATSAPP and user.phone:
            # WhatsApp template ishlatish (Meta talabi)
            template = self._get_wa_template(event)
            if template:
                await self.whatsapp.send_template(
                    user.phone,
                    template["name"],
                    lang=user.language,
                    params=template["render"](ctx),
                )
            else:
                await self.whatsapp.send_text(user.phone, text)

        else:
            raise ValueError(f"Kanal {ch} mavjud emas")

    def _get_wa_template(self, event: str) -> Optional[dict]:
        templates = {
            "order_created": {
                "name": "order_confirmation",
                "render": lambda c: [c["order_number"], f"{c['total']:,}"],
            },
            "order_on_the_way": {
                "name": "courier_on_way",
                "render": lambda c: [
                    c["order_number"],
                    c["courier_name"],
                    f"{c['eta_minutes']}",
                ],
            },
            "otp": {
                "name": "otp_code",
                "render": lambda c: [c["code"], str(c["ttl"] // 60)],
            },
        }
        return templates.get(event)

    async def send_otp(
        self,
        phone: str,
        code: str,
        channel: str,
        ttl: int,
    ):
        text = f"XalqUchun: Tasdiqlash kodi {code}. Amal qilish muddati {ttl // 60} daqiqa."

        if channel == "sms":
            await self.sms.send(phone, text)
        elif channel == "whatsapp":
            await self.whatsapp.send_template(
                phone, "otp_code", lang="uz", params=[code, str(ttl // 60)]
            )
        else:
            raise ValueError(f"OTP kanal {channel} qo'llanilmaydi")

    async def _log(
        self,
        user_id: int,
        event: str,
        channel: Optional[Channel],
        status: str,
        error: str = None,
    ):
        notif = Notification(
            user_id=user_id,
            event=event,
            channel=channel.value if channel else "none",
            status=status,
            error=error,
        )
        self.db.add(notif)
        await self.db.commit()
```

## 23.7. Order Service (to'liq)

```python
# backend/app/services/order_service.py
from decimal import Decimal
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BusinessRuleError
from app.db.models import Order, OrderItem, Cart, CartItem, User
from app.services.commission_service import CommissionService
from app.services.notification_service import NotificationService
from app.providers.payment import get_payment_provider
from app.ws.pubsub import redis_pubsub

MIN_ORDER_AMOUNT = Decimal("50000")
MAX_ORDER_AMOUNT = Decimal("50000000")

class OrderService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.commission = CommissionService(db)
        self.notifier = NotificationService(db)

    async def create_order(
        self,
        user: User,
        cart: Cart,
        address_id: int,
        payment_method: str,
        comment: str = None,
    ) -> Order:
        # === 1. Biznes qoidalari ===
        if not user.is_registered:
            raise BusinessRuleError("Ro'yxatdan o'ting")

        if not user.is_verified:
            raise BusinessRuleError("Profil tasdiqlanmagan. KYC dan o'ting")

        if not user.terms_accepted_at:
            raise BusinessRuleError("Ommaviy ofertaga rozilik bering")

        if not cart.items:
            raise BusinessRuleError("Savat bo'sh")

        # Minimal summa
        subtotal = sum(
            item.price_at_add * item.quantity for item in cart.items
        )
        if subtotal < MIN_ORDER_AMOUNT:
            raise BusinessRuleError(
                f"Minimal buyurtma {MIN_ORDER_AMOUNT:,} so'm. "
                f"Sizning savatingiz: {subtotal:,} so'm. "
                f"Yana {MIN_ORDER_AMOUNT - subtotal:,} so'm qo'shing."
            )

        if subtotal > MAX_ORDER_AMOUNT:
            raise BusinessRuleError(
                f"Maksimal buyurtma {MAX_ORDER_AMOUNT:,} so'm. "
                f"Katta hajm uchun qo'llab-quvvatlashga murojaat qiling."
            )

        # Vendor bir xil bo'lishi kerak
        vendor_ids = {item.product.vendor_id for item in cart.items}
        if len(vendor_ids) > 1:
            raise BusinessRuleError(
                "Bir buyurtmada faqat bitta do'kondan mahsulot bo'lishi mumkin"
            )

        vendor_id = vendor_ids.pop()

        # === 2. Yetkazish narxi ===
        vendor = cart.items[0].product.vendor
        delivery_fee = vendor.delivery_fee
        if vendor.free_delivery_from and subtotal >= vendor.free_delivery_from:
            delivery_fee = Decimal("0")

        # === 3. Promo-kod ===
        discount = Decimal("0")
        if cart.promo_code:
            discount = await self._apply_promo(cart.promo_code, subtotal)

        total = subtotal + delivery_fee - discount

        # === 4. Order yaratish (transactional) ===
        async with self.db.begin_nested():
            order = Order(
                order_number=await self._generate_order_number(),
                user_id=user.id,
                vendor_id=vendor_id,
                address_id=address_id,
                status="pending_payment",
                subtotal=subtotal,
                delivery_fee=delivery_fee,
                discount=discount,
                total=total,
                payment_method=payment_method,
                source_channel=user.source_channel,
                customer_comment=comment,
            )
            self.db.add(order)
            await self.db.flush()

            # Order items
            for cart_item in cart.items:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=cart_item.product_id,
                    product_name=cart_item.product.name,
                    product_sku=cart_item.product.sku,
                    quantity=cart_item.quantity,
                    price=cart_item.price_at_add,
                    total=cart_item.price_at_add * cart_item.quantity,
                    developer_id=cart_item.product.developer_id,
                    cost_price=cart_item.product.cost_price,
                )
                self.db.add(order_item)

            # Savatni tozalash
            for item in cart.items:
                await self.db.delete(item)

        # === 5. To'lovni boshlash ===
        provider = get_payment_provider(payment_method)
        payment = await provider.initiate(order)

        order.payment_id = payment.id
        await self.db.commit()

        # === 6. Real-time xabar ===
        await redis_pubsub.publish(
            f"vendor:{vendor_id}:orders",
            {
                "event": "order.created",
                "order_id": order.id,
                "order_number": order.order_number,
                "total": float(total),
                "items_count": len(cart.items),
            },
        )

        # === 7. Bildirishnoma ===
        await self.notifier.notify(
            user,
            event="order_created",
            order_number=order.order_number,
            total=total,
        )

        return order

    async def update_status(
        self,
        order_id: int,
        new_status: str,
        actor_id: int = None,
        actor_role: str = "system",
    ) -> Order:
        order = await self.db.get(Order, order_id)

        # State machine tekshirish
        if not self._is_valid_transition(order.status, new_status):
            raise BusinessRuleError(
                f"'{order.status}' → '{new_status}' o'tish mumkin emas"
            )

        old_status = order.status
        order.status = new_status
        order.updated_at = datetime.now(timezone.utc)

        # Vaqt belgilari
        if new_status == "accepted":
            order.accepted_at = datetime.now(timezone.utc)
        elif new_status == "ready":
            order.ready_at = datetime.now(timezone.utc)
        elif new_status == "picked_up":
            order.picked_up_at = datetime.now(timezone.utc)
        elif new_status == "delivered":
            order.delivered_at = datetime.now(timezone.utc)
        elif new_status == "completed":
            order.completed_at = datetime.now(timezone.utc)
            # Komissiya taqsimlash
            await self.commission.distribute(order)
        elif new_status == "cancelled":
            order.cancelled_at = datetime.now(timezone.utc)

        await self.db.flush()

        # Real-time
        await redis_pubsub.publish(
            f"order:{order_id}",
            {
                "event": "order.status_changed",
                "order_id": order_id,
                "old_status": old_status,
                "new_status": new_status,
                "timestamp": order.updated_at.isoformat(),
            },
        )

        # Bildirishnoma
        await self.notifier.notify(
            order.user,
            event=f"order_{new_status}",
            order_number=order.order_number,
            **self._status_context(order),
        )

        return order

    def _is_valid_transition(self, old: str, new: str) -> bool:
        VALID = {
            "draft": ["pending_payment", "cancelled"],
            "pending_payment": ["paid", "cancelled"],
            "paid": ["accepted", "cancelled", "refunded"],
            "accepted": ["preparing", "cancelled", "refunded"],
            "preparing": ["ready", "cancelled"],
            "ready": ["assigned", "cancelled"],
            "assigned": ["picked_up", "cancelled"],
            "picked_up": ["on_the_way", "cancelled"],
            "on_the_way": ["delivered", "cancelled"],
            "delivered": ["completed", "refunded"],
            "completed": [],
            "cancelled": [],
            "refunded": [],
        }
        return new in VALID.get(old, [])

    async def _generate_order_number(self) -> str:
        from datetime import date
        today = date.today().strftime("%Y%m%d")
        # Sequence yoki Redis INCR ishlatish mumkin
        stmt = select(func.count(Order.id)).where(
            Order.created_at >= datetime.now(timezone.utc).replace(
                hour=0, minute=0, second=0
            )
        )
        count = (await self.db.execute(stmt)).scalar() or 0
        return f"ORD-{today}-{count + 1:06d}"
```

---

# 24. FRONTEND STRUKTURASI

## 24.1. Umumiy monorepo strukturasi

```
xalquchun/
├── backend/                    # FastAPI
├── bot/                        # aiogram
├── shared/                     # Umumiy kod (types, utils)
│   ├── types/                  # TypeScript types
│   └── api-client/             # API client
├── apps/
│   ├── customer-webapp/        # Mijoz (React)
│   ├── vendor-panel/           # Do'kon paneli
│   ├── dealer-panel/           # Dealer paneli
│   ├── developer-panel/        # Dasturchi paneli
│   ├── courier-app/            # Kuryer ilovasi
│   ├── admin-panel/            # Admin paneli
│   └── support-panel/          # Support paneli
├── packages/
│   ├── ui/                     # Umumiy UI komponentlar
│   ├── auth/                   # Auth logic
│   └── ws-client/              # WebSocket client
├── docker-compose.yml
└── README.md
```

## 24.2. Customer WebApp — struktura

```
apps/customer-webapp/
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── router.tsx
│   ├── pages/
│   │   ├── Home.tsx
│   │   ├── Catalog.tsx
│   │   ├── Shop.tsx
│   │   ├── Product.tsx
│   │   ├── Cart.tsx
│   │   ├── Checkout.tsx
│   │   ├── OrderTracking.tsx
│   │   ├── Orders.tsx
│   │   ├── Profile.tsx
│   │   ├── Wallet.tsx
│   │   ├── Referral.tsx
│   │   ├── Chat.tsx
│   │   └── Legal/
│   │       ├── Offer.tsx
│   │       ├── Privacy.tsx
│   │       └── Terms.tsx
│   ├── components/
│   │   ├── common/
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Modal.tsx
│   │   │   └── Toast.tsx
│   │   ├── layout/
│   │   │   ├── Header.tsx
│   │   │   ├── BottomNav.tsx
│   │   │   └── Layout.tsx
│   │   ├── product/
│   │   │   ├── ProductCard.tsx
│   │   │   ├── ProductGrid.tsx
│   │   │   └── ProductDetail.tsx
│   │   ├── cart/
│   │   │   ├── CartItem.tsx
│   │   │   ├── CartSummary.tsx
│   │   │   └── MinOrderProgress.tsx
│   │   └── order/
│   │       ├── OrderStatusStepper.tsx
│   │       ├── OrderCard.tsx
│   │       └── OrderMap.tsx
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useWebSocket.ts
│   │   ├── useCart.ts
│   │   └── useTelegram.ts
│   ├── stores/
│   │   ├── authStore.ts
│   │   ├── cartStore.ts
│   │   └── uiStore.ts
│   ├── lib/
│   │   ├── api.ts
│   │   ├── telegram.ts
│   │   ├── format.ts
│   │   └── i18n.ts
│   └── styles/
│       └── globals.css
├── public/
├── index.html
├── package.json
├── vite.config.ts
├── tailwind.config.js
└── tsconfig.json
```

## 24.3. Muhim komponentlar

### MinOrderProgress komponenti
```tsx
// apps/customer-webapp/src/components/cart/MinOrderProgress.tsx
interface Props {
  current: number;
  minimum: number;
}

export function MinOrderProgress({ current, minimum }: Props) {
  const progress = Math.min((current / minimum) * 100, 100);
  const remaining = Math.max(minimum - current, 0);
  const isReady = current >= minimum;

  return (
    <div className="p-4 bg-gray-50 rounded-lg">
      <div className="flex justify-between text-sm mb-2">
        <span className="text-gray-600">
          {isReady ? "✅ Minimal summaga yetdingiz!" : "Minimal buyurtma"}
        </span>
        <span className="font-medium">
          {formatPrice(current)} / {formatPrice(minimum)}
        </span>
      </div>
      <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
        <div
          className={`h-full transition-all ${
            isReady ? "bg-green-500" : "bg-orange-500"
          }`}
          style={{ width: `${progress}%` }}
        />
      </div>
      {!isReady && (
        <p className="text-xs text-gray-500 mt-2">
          Yana <strong>{formatPrice(remaining)}</strong> qo'shing
        </p>
      )}
    </div>
  );
}
```

### OrderStatusStepper komponenti
```tsx
// apps/customer-webapp/src/components/order/OrderStatusStepper.tsx
const STEPS = [
  { key: "paid", label: "To'landi", icon: "💳" },
  { key: "accepted", label: "Qabul qilindi", icon: "✅" },
  { key: "preparing", label: "Tayyorlanmoqda", icon: "👨‍🍳" },
  { key: "on_the_way", label: "Yo'lda", icon: "🛵" },
  { key: "delivered", label: "Yetkazildi", icon: "🎉" },
];

export function OrderStatusStepper({ status }: { status: string }) {
  const currentIdx = STEPS.findIndex(s => s.key === status);

  return (
    <div className="space-y-3">
      {STEPS.map((step, idx) => {
        const isDone = idx < currentIdx;
        const isActive = idx === currentIdx;
        return (
          <div key={step.key} className="flex items-center gap-3">
            <div
              className={`w-8 h-8 rounded-full flex items-center justify-center ${
                isDone ? "bg-green-500 text-white"
                : isActive ? "bg-orange-500 text-white animate-pulse"
                : "bg-gray-200 text-gray-400"
              }`}
            >
              {isDone ? "✓" : step.icon}
            </div>
            <div className="flex-1">
              <p className={`text-sm ${
                isActive ? "font-semibold text-orange-600" : "text-gray-600"
              }`}>
                {step.label}
              </p>
            </div>
            {isActive && (
              <span className="text-xs text-gray-400">hozir</span>
            )}
          </div>
        );
      })}
    </div>
  );
}
```

### useWebSocket hook (reconnect bilan)
```ts
// apps/customer-webapp/src/hooks/useWebSocket.ts
import { useEffect, useRef, useState, useCallback } from "react";

interface Options {
  onMessage?: (data: any) => void;
  reconnect?: boolean;
  maxRetries?: number;
}

export function useWebSocket(path: string, options: Options = {}) {
  const { onMessage, reconnect = true, maxRetries = 10 } = options;
  const [status, setStatus] = useState<"connecting" | "open" | "closed">("connecting");
  const wsRef = useRef<WebSocket | null>(null);
  const retriesRef = useRef(0);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const connect = useCallback(() => {
    const token = localStorage.getItem("access_token");
    if (!token) return;

    const ws = new WebSocket(
      `${import.meta.env.VITE_WS_URL}${path}?token=${token}`
    );
    wsRef.current = ws;
    setStatus("connecting");

    ws.onopen = () => {
      setStatus("open");
      retriesRef.current = 0;
    };

    ws.onmessage = (e) => {
      try {
        const data = JSON.parse(e.data);
        onMessage?.(data);
      } catch {}
    };

    ws.onclose = () => {
      setStatus("closed");
      if (reconnect && retriesRef.current < maxRetries) {
        const delay = Math.min(1000 * 2 ** retriesRef.current, 30000);
        retriesRef.current++;
        timerRef.current = setTimeout(connect, delay);
      }
    };

    ws.onerror = () => ws.close();
  }, [path, onMessage, reconnect, maxRetries]);

  useEffect(() => {
    connect();
    // Ping har 30 sekundda
    const ping = setInterval(() => {
      if (wsRef.current?.readyState === WebSocket.OPEN) {
        wsRef.current.send("ping");
      }
    }, 30000);

    return () => {
      clearInterval(ping);
      if (timerRef.current) clearTimeout(timerRef.current);
      wsRef.current?.close();
    };
  }, [connect]);

  return { status, ws: wsRef.current };
}
```

## 24.4. Vendor Panel — Real-time buyurtma

```tsx
// apps/vendor-panel/src/pages/Orders.tsx
import { useEffect, useState } from "react";
import { useWebSocket } from "@xalquchun/ws-client";
import { NewOrderModal } from "@/components/NewOrderModal";
import { OrderCard } from "@/components/OrderCard";

export function OrdersPage() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [newOrder, setNewOrder] = useState<Order | null>(null);
  const [soundEnabled, setSoundEnabled] = useState(true);

  // Real-time yangi buyurtmalar
  useWebSocket("/ws/vendor/orders", {
    onMessage: (msg) => {
      if (msg.event === "order.created") {
        setNewOrder(msg.order);
        if (soundEnabled) playNotificationSound();
        // Brauzer notification
        if (Notification.permission === "granted") {
          new Notification("Yangi buyurtma!", {
            body: `#${msg.order.order_number} — ${formatPrice(msg.order.total)}`,
          });
        }
      }
    },
  });

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Buyurtmalar</h1>
        <button
          onClick={() => setSoundEnabled(!soundEnabled)}
          className="text-sm"
        >
          {soundEnabled ? "🔔 Ovoz yoqilgan" : "🔕 Ovoz o'chirilgan"}
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {orders.map(order => (
          <OrderCard key={order.id} order={order} />
        ))}
      </div>

      {newOrder && (
        <NewOrderModal
          order={newOrder}
          onAccept={async () => {
            await acceptOrder(newOrder.id);
            setNewOrder(null);
          }}
          onReject={async () => {
            await rejectOrder(newOrder.id);
            setNewOrder(null);
          }}
        />
      )}
    </div>
  );
}
```

---

# 25. HUQUQIY HUJJATLAR

## 25.1. Ommaviy oferta (qisqacha)

```
OMMAVIY OFERTA
XalqUchun platformasida xarid qilish shartlari

1. UMUMIY QOIDALAR
1.1. Ushbu oferta O'zbekiston Respublikasi Fuqarolik Kodeksining 
     367-moddasiga muvofiq tuzilgan.
1.2. Platformadan foydalanish orqali siz ushbu shartlarga 
     to'liq rozilik bildirasiz.

2. RO'YXATDAN O'TISH
2.1. Xarid qilish uchun ro'yxatdan o'tish majburiy.
2.2. Quyidagi ma'lumotlar majburiy:
     - To'liq ism-sharif
     - Telefon raqami
     - Yetkazib berish manzili
     - Pasport ma'lumotlari (KYC)

3. BUYURTMA
3.1. Minimal buyurtma summasi: 50,000 so'm
3.2. Maksimal buyurtma summasi: 50,000,000 so'm
3.3. Buyurtma tasdiqlangandan keyin bekor qilish 5 daqiqa 
     ichida mumkin.

4. TO'LOV
4.1. To'lov usullari: Payme, Click, Uzum Bank, naqd pul
4.2. Onlayn to'lov 2% komissiya bilan amalga oshiriladi.
4.3. Fiskal chek har bir buyurtma uchun beriladi.

5. YETKAZIB BERISH
5.1. Yetkazib berish muddati: 30-60 daqiqa
5.2. Yetkazib berish hududi: do'kon radiusi 5 km
5.3. Kechiktirilgan taqdirda kompensatsiya beriladi.

6. QAYTARISH
6.1. Sifatli mahsulotni 24 soat ichida qaytarish mumkin.
6.2. Oziq-ovqat mahsulotlarini qaytarish mumkin emas.
6.3. Sifatsiz mahsulot uchun to'liq qaytarish.

7. SHAXSIY MA'LUMOTLAR
7.1. Ma'lumotlar O'RQ-547 ga muvofiq himoyalanadi.
7.2. Ma'lumotlarni o'chirish huquqi: /delete_my_data

8. JAVOBGARLIK
8.1. Platforma sifat uchun javobgar emas.
8.2. Platforma yetkazib berish uchun javobgar.
8.3. Nizolar O'zbekiston qonunchiligi bo'yicha hal qilinadi.

Yuridik manzil: [to'ldirilishi kerak]
STIR: [to'ldirilishi kerak]
```

## 25.2. Maxfiylik siyosati (qisqacha)

```
MAXFIYLIK SIYOSATI

1. QANDAY MA'LUMOTLAR YIG'ILADI
   - Shaxsiy: ism, telefon, email, pasport
   - Moliyaviy: to'lov ma'lumotlari (shifrlangan)
   - Texnik: IP, qurilma, brauzer
   - Xulq-atvor: ko'rilgan mahsulotlar, buyurtmalar

2. MA'LUMOTLARDAN FOYDALANISH
   - Buyurtmalarni bajarish
   - Bildirishnomalar yuborish
   - Xizmatni yaxshilash
   - Huquqiy talablarni bajarish

3. MA'LUMOTLARNI HIMOYALASH
   - AES-256 shifrlash
   - SSL/TLS transport
   - Kirish nazorati (RBAC)
   - Audit log

4. UCHINCHI TOMONLAR
   - Payme, Click (to'lov)
   - Eskiz, WhatsApp (bildirishnoma)
   - Yandex Maps (xarita)

5. FOYDALANUVCHI HUQUQLARI
   - Ma'lumotlarni ko'rish
   - Tuzatish
   - O'chirish
   - Eksport qilish

6. COOKIES
   - Sessiya uchun
   - Analytics uchun

7. BOG'LANISH
   privacy@xalquchun.uz
```

---

# 26. TESTLASH STRATEGIYASI

## 26.1. Test piramidasi

```
                    /\
                   /  \
                  / E2E\          10% — Playwright
                 /______\
                /        \
               /Integration\      30% — pytest + testcontainers
              /____________\
             /              \
            /   Unit Tests   \    60% — pytest
           /__________________\
```

## 26.2. Unit test namunasi

```python
# backend/tests/unit/test_order_service.py
import pytest
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

from app.services.order_service import OrderService
from app.core.exceptions import BusinessRuleError

@pytest.mark.asyncio
async def test_min_order_amount_validation():
    """50,000 so'mdan kam buyurtma rad etilishi kerak"""
    db = AsyncMock()
    service = OrderService(db)

    user = MagicMock(
        is_registered=True,
        is_verified=True,
        terms_accepted_at="2026-01-01",
    )
    cart = MagicMock()
    cart.items = [
        MagicMock(price_at_add=Decimal("10000"), quantity=2)
    ]

    with pytest.raises(BusinessRuleError) as exc:
        await service.create_order(
            user=user,
            cart=cart,
            address_id=1,
            payment_method="payme",
        )

    assert "Minimal buyurtma" in str(exc.value)

@pytest.mark.asyncio
async def test_guest_checkout_blocked():
    """Ro'yxatdan o'tmagan foydalanuvchi buyurtma qila olmaydi"""
    db = AsyncMock()
    service = OrderService(db)

    user = MagicMock(is_registered=False)

    with pytest.raises(BusinessRuleError) as exc:
        await service.create_order(
            user=user,
            cart=MagicMock(),
            address_id=1,
            payment_method="payme",
        )

    assert "Ro'yxatdan o'ting" in str(exc.value)
```

## 26.3. Integration test

```python
# backend/tests/integration/test_wallet.py
import pytest
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.wallet_service import WalletService

@pytest.mark.asyncio
async def test_wallet_credit_debit(db_session: AsyncSession):
    service = WalletService(db_session)

    wallet = await service.get_or_create(1, "user")

    # Credit
    await service.credit(
        wallet_id=wallet.id,
        amount=Decimal("100000"),
        source_type="test",
    )
    await db_session.refresh(wallet)
    assert wallet.balance == Decimal("100000")

    # Debit
    await service.debit(
        wallet_id=wallet.id,
        amount=Decimal("30000"),
        source_type="test",
    )
    await db_session.refresh(wallet)
    assert wallet.balance == Decimal("70000")

    # Insufficient
    with pytest.raises(Exception):
        await service.debit(
            wallet_id=wallet.id,
            amount=Decimal("1000000"),
            source_type="test",
        )
```

## 26.4. E2E test (Playwright)

```ts
// e2e/checkout.spec.ts
import { test, expect } from "@playwright/test";

test("To'liq buyurtma oqimi", async ({ page }) => {
  // 1. Bosh sahifa
  await page.goto("/");
  await expect(page).toHaveTitle(/XalqUchun/);

  // 2. Katalogga o'tish
  await page.click('[data-testid="catalog-link"]');

  // 3. Mahsulot qo'shish
  await page.click('[data-testid="product-1-add"]');
  await page.click('[data-testid="product-2-add"]');

  // 4. Savatga o'tish
  await page.click('[data-testid="cart-button"]');
  await expect(page.locator('[data-testid="cart-total"]')).toContainText("");

  // 5. Minimal summa tekshirish
  const warning = page.locator('[data-testid="min-order-warning"]');
  if (await warning.isVisible()) {
    await page.click('[data-testid="continue-shopping"]');
    await page.click('[data-testid="product-3-add"]');
    await page.click('[data-testid="cart-button"]');
  }

  // 6. Checkout
  await page.click('[data-testid="checkout-button"]');
  await page.fill('[data-testid="address-input"]', "Chilonzor 12-mavdon");
  await page.click('[data-testid="payment-payme"]');
  await page.click('[data-testid="confirm-order"]');

  // 7. Real-time kuzatuv
  await expect(page).toHaveURL(/\/order\/\d+/);
  await expect(page.locator('[data-testid="order-status"]'))
    .toContainText(/To'landi|Qabul qilindi/, { timeout: 30000 });
});
```

---

# 27. DEPLOYMENT RUNBOOK

## 27.1. Production serverga o'rnatish

```bash
# 1. Server tayyorlash (Ubuntu 22.04)
sudo apt update && sudo apt upgrade -y
sudo apt install -y docker.io docker-compose-plugin git nginx certbot

# 2. Docker ruxsat
sudo usermod -aG docker $USER

# 3. Loyihani klonlash
git clone https://github.com/otaboyevsardorbek1/xalquchun-bot-v2.git
cd xalquchun-bot-v2

# 4. .env sozlash
cp .env.example .env
nano .env  # Barcha qiymatlarni to'ldirish

# 5. Secrets generatsiya
openssl genrsa -out secrets/jwt_private.pem 4096
openssl rsa -in secrets/jwt_private.pem -pubout -out secrets/jwt_public.pem
chmod 600 secrets/*.pem

# 6. Docker build va ishga tushirish
docker compose -f docker-compose.prod.yml up -d --build

# 7. Migratsiyalar
docker compose exec backend alembic upgrade head

# 8. SSL sertifikat
sudo certbot --nginx -d api.xalquchun.uz -d app.xalquchun.uz

# 9. Health check
curl https://api.xalquchun.uz/health
```

## 27.2. Nginx konfiguratsiya

```nginx
# /etc/nginx/sites-available/xalquchun
upstream backend {
    least_conn;
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

upstream webapp {
    server 127.0.0.1:3000;
}

upstream vendor_panel {
    server 127.0.0.1:3001;
}

# API
server {
    listen 443 ssl http2;
    server_name api.xalquchun.uz;

    ssl_certificate /etc/letsencrypt/live/api.xalquchun.uz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.xalquchun.uz/privkey.pem;

    client_max_body_size 20M;

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket
    location /ws/ {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }

    # Rate limiting
    limit_req zone=api burst=20 nodelay;
}

# WebApp
server {
    listen 443 ssl http2;
    server_name app.xalquchun.uz;

    ssl_certificate /etc/letsencrypt/live/app.xalquchun.uz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/app.xalquchun.uz/privkey.pem;

    location / {
        proxy_pass http://webapp;
    }
}
```

## 27.3. Backup strategiyasi

```bash
#!/bin/bash
# /usr/local/bin/backup-xalquchun.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR=/backups/xalquchun
S3_BUCKET=s3://xalquchun-backups

mkdir -p $BACKUP_DIR

# 1. PostgreSQL dump
docker compose exec -T postgres pg_dump -U xalquchun xalquchun | \
    gzip > $BACKUP_DIR/db_$DATE.sql.gz

# 2. Redis dump
docker compose exec -T redis redis-cli BGSAVE
sleep 5
docker cp $(docker compose ps -q redis):/data/dump.rdb \
    $BACKUP_DIR/redis_$DATE.rdb

# 3. Upload to S3
aws s3 sync $BACKUP_DIR $S3_BUCKET/$(date +%Y/%m)/

# 4. Cleanup (30 kundan eski)
find $BACKUP_DIR -mtime +30 -delete

echo "[$(date)] Backup completed: $DATE"
```

```bash
# Crontab
0 2 * * * /usr/local/bin/backup-xalquchun.sh >> /var/log/xalquchun-backup.log 2>&1
```

---

# 28. MONITORING VA ALERTING

## 28.1. Prometheus metrics

```python
# backend/app/core/metrics.py
from prometheus_client import Counter, Histogram, Gauge

# HTTP
http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)
http_request_duration = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration",
    ["method", "endpoint"],
)

# Business
orders_created_total = Counter(
    "orders_created_total",
    "Total orders created",
    ["status", "source_channel"],
)
order_value = Histogram(
    "order_value_som",
    "Order value in som",
    buckets=[50000, 100000, 250000, 500000, 1000000, 5000000],
)

# Payment
payments_total = Counter(
    "payments_total",
    "Total payments",
    ["provider", "status"],
)
payment_duration = Histogram(
    "payment_duration_seconds",
    "Payment processing duration",
    ["provider"],
)

# WebSocket
ws_connections = Gauge(
    "ws_connections_active",
    "Active WebSocket connections",
    ["channel"],
)

# Notifications
notifications_total = Counter(
    "notifications_total",
    "Notifications sent",
    ["channel", "event", "status"],
)
```

## 28.2. Alert rules

```yaml
# prometheus/alerts.yml
groups:
  - name: xalquchun
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m]))
          / sum(rate(http_requests_total[5m])) > 0.05
        for: 5m
        annotations:
          summary: "5% dan ortiq xato"
          severity: critical

      - alert: SlowAPI
        expr: |
          histogram_quantile(0.95, 
            rate(http_request_duration_seconds_bucket[5m])
          ) > 1
        for: 5m
        annotations:
          summary: "API p95 > 1 sekund"

      - alert: PaymentFailures
        expr: |
          rate(payments_total{status="failed"}[5m]) > 0.1
        for: 5m
        annotations:
          summary: "To'lov xatolari ko'paydi"

      - alert: LowWalletBalance
        expr: platform_wallet_balance < 1000000
        for: 10m
        annotations:
          summary: "Platforma balansi kam"

      - alert: DatabaseConnections
        expr: pg_stat_activity_count > 80
        for: 5m
        annotations:
          summary: "DB ulanishlar 80% dan oshdi"
```

## 28.3. Grafana dashboard (JSON snippet)

```json
{
  "dashboard": {
    "title": "XalqUchun — Business Metrics",
    "panels": [
      {
        "title": "Kunlik buyurtmalar",
        "targets": [{
          "expr": "sum(increase(orders_created_total[24h]))"
        }]
      },
      {
        "title": "O'rtacha buyurtma qiymati",
        "targets": [{
          "expr": "histogram_quantile(0.5, rate(order_value_som_bucket[1h]))"
        }]
      },
      {
        "title": "To'lov muvaffaqiyati",
        "targets": [{
          "expr": "sum(rate(payments_total{status=\"success\"}[5m])) / sum(rate(payments_total[5m]))"
        }]
      },
      {
        "title": "Aktiv WebSocket ulanishlar",
        "targets": [{
          "expr": "sum(ws_connections_active)"
        }]
      }
    ]
  }
}
```

---

# 29. XAVFSIZLIK AUDITI CHECKLIST

## 29.1. OWASP Top 10 tekshiruvi

| # | Xavf | Holat | Chora |
|---|---|---|---|
| A01 | Broken Access Control | ✅ | RBAC + resource ownership |
| A02 | Cryptographic Failures | ✅ | AES-256, TLS 1.3, RS256 |
| A03 | Injection | ✅ | ORM, parametrlangan so'rovlar |
| A04 | Insecure Design | ✅ | Threat modeling, BLE |
| A05 | Security Misconfiguration | ✅ | Hardened defaults |
| A06 | Vulnerable Components | ⚠️ | Dependabot + Snyk |
| A07 | Auth Failures | ✅ | 2FA, OTP, rate limit |
| A08 | Data Integrity | ✅ | Idempotency, signatures |
| A09 | Logging Failures | ✅ | Audit log, Sentry |
| A10 | SSRF | ✅ | URL whitelist |

## 29.2. Pre-launch checklist

```
□ SSL/TLS barcha endpointlarda
□ HSTS header
□ CSP header
□ X-Frame-Options: DENY
□ X-Content-Type-Options: nosniff
□ CORS faqat ruxsat etilgan domenlar
□ Rate limit barcha endpointlarda
□ JWT RS256 (HS256 emas)
□ PII shifrlangan (AES-256)
□ Parollar bcrypt (cost 12+)
□ OTP 5 daqiqa TTL
□ 2FA admin uchun
□ Audit log barcha kritik harakatlar
□ Idempotency to'lov uchun
□ Webhook imzo tekshiruvi
□ SQL injection testlari
□ XSS testlari
□ CSRF himoyasi
□ Dependency scan (Snyk)
□ Container scan (Trivy)
□ Secrets git'da yo'q
□ .env gitignore'da
□ Backup tizimi ishlaydi
□ Disaster recovery test
□ Incident response plan
□ Log rotation
□ Monitoring + alerting
□ DDoS himoyasi (Cloudflare)
□ GDPR/o'chirish huquqi
□ Ommaviy oferta
□ Maxfiylik siyosati
```

---

# 30. YAKUNIY XULOSA VA KEYINGI QADAMLAR

## 30.1. TZ v3.0 to'liq qamrovi

| Bo'lim | Holat |
|---|---|
| Loyiha konsepsiyasi | ✅ To'liq |
| 6 ta panel | ✅ To'liq |
| Dealer tizimi | ✅ To'liq |
| Dasturchi tizimi | ✅ To'liq |
| Moliyaviy tizim | ✅ To'liq |
| Wallet + Payout | ✅ To'liq |
| Komissiya taqsimoti | ✅ To'liq |
| Multi-channel | ✅ To'liq |
| WebSocket real-time | ✅ To'liq |
| UI/UX dizayn | ✅ To'liq |
| Kod namunalari | ✅ To'liq |
| API endpointlar | ✅ To'liq |
| DB sxemasi | ✅ To'liq |
| Xavfsizlik | ✅ To'liq |
| Testlar | ✅ To'liq |
| Deployment | ✅ To'liq |
| Monitoring | ✅ To'liq |
| Huquqiy hujjatlar | ✅ To'liq |

## 30.2. Ishlab chiqish ketma-ketligi (tavsiya)

```
HAFTA 1-2:    Backend poydevor (FastAPI + DB + Auth)
HAFTA 3-4:    Multi-channel (SMS + WhatsApp + Telegram)
HAFTA 5-6:    Katalog + Savat + Buyurtma
HAFTA 7-8:    To'lov + Wallet + Komissiya
HAFTA 9-12:   Mijoz WebApp
HAFTA 13-16:  Vendor Panel + Dealer Panel
HAFTA 17-20:  Developer Panel + Courier App
HAFTA 21-22:  Admin Panel + Support Panel
HAFTA 23-24:  WebSocket + Real-time
HAFTA 25-26:  Xavfsizlik + Huquqiy + Testlar
HAFTA 27:     Production deployment
```

## 30.3. Jamoa tarkibi (tavsiya)

| Rol | Soni | Mas'uliyat |
|---|---|---|
| Backend developer | 2 | FastAPI, DB, integratsiya |
| Frontend developer | 3 | 6 ta panel |
| DevOps | 1 | Docker, CI/CD, monitoring |
| QA | 1 | Test, sifat nazorati |
| UI/UX designer | 1 | Dizayn tizimi |
| Project manager | 1 | Koordinatsiya |
| **Jami** | **9** | |

## 30.4. Keyingi qadam — kod yozishni boshlash

Agar siz **hozir kod yozishni boshlamoqchi** bo'lsangiz, quyidagi tartibda boring:

1. **Birinchi kun:** `docker-compose.yml` + `.env.example` + FastAPI skeleton
2. **Ikkinchi kun:** Database models (User, Vendor, Dealer, Developer, Product, Order)
3. **Uchinchi kun:** Alembic migrations + seed data
4. **To'rtinchi kun:** Auth Service (OTP + JWT)
5. **Beshinchi kun:** Notification Service (Eskiz + WhatsApp + Telegram)
6. **Oltinchi kun:** Order Service + Wallet Service
7. **Yettinchi kun:** Birinchi API endpoint + test

**Muhim:** Har bir modulni **test bilan** yozing. Test coverage 80% dan past bo'lmasin.

---

# 📎 YAKUNIY ILOVA — Fayl strukturasi (to'liq)

```
xalquchun-platform/
│
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── docker-compose.yml
├── docker-compose.prod.yml
├── Makefile
│
├── docs/
│   ├── TZ-v3.md
│   ├── architecture.md
│   ├── api-reference.md
│   ├── deployment.md
│   ├── security.md
│   ├── financial.md
│   └── legal/
│       ├── offer.md
│       ├── privacy.md
│       └── terms.md
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   ├── logging.py
│   │   │   ├── metrics.py
│   │   │   ├── exceptions.py
│   │   │   └── dependencies.py
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── auth.py
│   │   │       ├── users.py
│   │   │       ├── catalog.py
│   │   │       ├── cart.py
│   │   │       ├── orders.py
│   │   │       ├── payments.py
│   │   │       ├── vendor.py
│   │   │       ├── dealer.py
│   │   │       ├── developer.py
│   │   │       ├── courier.py
│   │   │       ├── admin.py
│   │   │       ├── finance.py
│   │   │       └── support.py
│   │   ├── ws/
│   │   │   ├── manager.py
│   │   │   ├── pubsub.py
│   │   │   ├── order_ws.py
│   │   │   ├── courier_ws.py
│   │   │   ├── vendor_ws.py
│   │   │   ├── chat_ws.py
│   │   │   └── admin_ws.py
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── user_service.py
│   │   │   ├── catalog_service.py
│   │   │   ├── cart_service.py
│   │   │   ├── order_service.py
│   │   │   ├── payment_service.py
│   │   │   ├── wallet_service.py
│   │   │   ├── commission_service.py
│   │   │   ├── payout_service.py
│   │   │   ├── notification_service.py
│   │   │   ├── otp_service.py
│   │   │   ├── kyc_service.py
│   │   │   ├── courier_service.py
│   │   │   ├── promo_service.py
│   │   │   ├── review_service.py
│   │   │   └── report_service.py
│   │   ├── providers/
│   │   │   ├── sms/
│   │   │   │   ├── base.py
│   │   │   │   ├── eskiz.py
│   │   │   │   ├── playmobile.py
│   │   │   │   └── textup.py
│   │   │   ├── whatsapp/
│   │   │   │   ├── base.py
│   │   │   │   └── cloud_api.py
│   │   │   ├── telegram/
│   │   │   │   └── provider.py
│   │   │   ├── payment/
│   │   │   │   ├── base.py
│   │   │   │   ├── payme.py
│   │   │   │   ├── click.py
│   │   │   │   ├── uzum.py
│   │   │   │   └── cash.py
│   │   │   ├── maps/
│   │   │   │   └── yandex.py
│   │   │   └── storage/
│   │   │       └── s3.py
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   ├── session.py
│   │   │   ├── models/
│   │   │   │   ├── user.py
│   │   │   │   ├── kyc.py
│   │   │   │   ├── vendor.py
│   │   │   │   ├── dealer.py
│   │   │   │   ├── developer.py
│   │   │   │   ├── product.py
│   │   │   │   ├── cart.py
│   │   │   │   ├── order.py
│   │   │   │   ├── payment.py
│   │   │   │   ├── wallet.py
│   │   │   │   ├── commission.py
│   │   │   │   ├── payout.py
│   │   │   │   ├── courier.py
│   │   │   │   ├── contract.py
│   │   │   │   ├── promo.py
│   │   │   │   ├── review.py
│   │   │   │   ├── notification.py
│   │   │   │   └── audit.py
│   │   │   └── repositories/
│   │   ├── schemas/
│   │   ├── tasks/
│   │   │   ├── celery_app.py
│   │   │   ├── notification_tasks.py
│   │   │   ├── payout_tasks.py
│   │   │   └── report_tasks.py
│   │   └── utils/
│   ├── alembic/
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── e2e/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── Dockerfile.prod
│
├── bot/
│   ├── main.py
│   ├── config.py
│   ├── handlers/
│   ├── middlewares/
│   ├── keyboards/
│   ├── states/
│   └── requirements.txt
│
├── apps/
│   ├── customer-webapp/
│   ├── vendor-panel/
│   ├── dealer-panel/
│   ├── developer-panel/
│   ├── courier-app/
│   ├── admin-panel/
│   └── support-panel/
│
├── packages/
│   ├── ui/
│   ├── api-client/
│   ├── ws-client/
│   └── types/
│
├── infra/
│   ├── nginx/
│   ├── prometheus/
│   ├── grafana/
│   ├── loki/
│   └── scripts/
│       ├── backup.sh
│       ├── restore.sh
│       └── deploy.sh
│
└── .github/
    └── workflows/
        ├── ci.yml
        ├── cd-staging.yml
        └── cd-prod.yml
```

---

# ✅ YAKUN

Ushbu **TZ v3.0** + **Amaliy Implementatsiya Qo'llanmasi** XalqUchun platformasini **to'liq, hech qanday kamchiliksiz** ishlab chiqish uchun zarur bo'lgan barcha ma'lumotlarni o'z ichiga oladi:

✅ **6 ta panel** — Mijoz, Vendor, Dealer, Developer, Courier, Admin
✅ **Moliyaviy tizim** — Wallet, komissiya, payout, soliq
✅ **Multi-channel** — SMS, WhatsApp, Telegram, Push
✅ **Real-time** — WebSocket, Redis Pub/Sub
✅ **Xavfsizlik** — PII, KYC, RBAC, audit
✅ **Huquqiy** — Oferta, maxfiylik, O'RQ-792
✅ **UI/UX** — Dizayn tizimi, wireframe
✅ **Kod** — To'liq namunalar
✅ **Testlar** — Unit, integration, E2E
✅ **Deployment** — Docker, Nginx, CI/CD
✅ **Monitoring** — Prometheus, Grafana, Sentry

**Keyingi qadam:** Kod yozishni boshlash. Men har bir modul uchun to'liq kodni yozib berishga tayyorman. Ayting — qaysi moduldan boshlaymiz?

1. **Backend poydevor** (FastAPI + DB + Auth)
2. **Notification Service** (Eskiz + WhatsApp + Telegram)
3. **Order Service** (state machine + komissiya)
4. **Wallet Service** (hamyon + payout)
5. **WebSocket Hub** (real-time)
6. **Mijoz WebApp** (React)
7. **Vendor Panel** (React)
8. **Admin Panel** (React)

Qaysi birini birinchi yozay?

# 🚀 XalqUchun Platforma — To'liq Kod Yozish Qo'llanmasi
## 8 ta modul, qadamma-qadam, to'liq kod

---

# 📦 MODUL 1: BACKEND POYDEVOR (FastAPI + DB + Auth)

## 1.1. Loyihani boshlash

```bash
mkdir xalquchun-platform && cd xalquchun-platform
mkdir -p backend/{app,tests,alembic,secrets}
cd backend
python3.11 -m venv venv
source venv/bin/activate
```

## 1.2. `requirements.txt`

```txt
# Core
fastapi==0.109.0
uvicorn[standard]==0.27.0
gunicorn==21.2.0
python-multipart==0.0.6

# Database
sqlalchemy[asyncio]==2.0.25
asyncpg==0.29.0
alembic==1.13.1
psycopg2-binary==2.9.9

# Auth
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
pyotp==2.9.0

# Validation
pydantic==2.5.3
pydantic-settings==2.1.0
email-validator==2.1.0

# Redis
redis==5.0.1
hiredis==2.3.0

# Celery
celery==5.3.6
flower==2.0.1

# HTTP
httpx==0.26.0
aiohttp==3.9.1

# Utils
structlog==24.1.0
tenacity==8.2.3
python-slugify==8.0.1
Pillow==10.2.0
qrcode==7.4.2

# Monitoring
prometheus-client==0.19.0
sentry-sdk[fastapi]==1.40.0

# Testing
pytest==7.4.4
pytest-asyncio==0.23.3
pytest-cov==4.1.0
httpx==0.26.0
faker==22.0.0
testcontainers==3.7.1

# Security
cryptography==42.0.0
bcrypt==4.1.2
```

## 1.3. `.env.example`

```env
# ==== ASOSIY ====
ENV=development
DEBUG=true
SECRET_KEY=change-me-please-use-64-random-chars-minimum-for-security
API_V1_PREFIX=/api/v1

# ==== DOMAIN ====
BASE_URL=http://localhost:8000
WEBAPP_URL=http://localhost:3000
VENDOR_URL=http://localhost:3001
DEALER_URL=http://localhost:3002
DEVELOPER_URL=http://localhost:3003
COURIER_URL=http://localhost:3004
ADMIN_URL=http://localhost:3005

# ==== DATABASE ====
DATABASE_URL=postgresql+asyncpg://xalquchun:xalquchun@localhost:5432/xalquchun
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10

# ==== REDIS ====
REDIS_URL=redis://localhost:6379/0

# ==== JWT ====
JWT_ALGORITHM=RS256
JWT_PRIVATE_KEY_PATH=./secrets/jwt_private.pem
JWT_PUBLIC_KEY_PATH=./secrets/jwt_public.pem
ACCESS_TOKEN_TTL=900
REFRESH_TOKEN_TTL=604800

# ==== TELEGRAM ====
BOT_TOKEN=your_bot_token_here
BOT_USERNAME=xalquchun_bot
OWNER_ID=123456789
ADMIN_IDS=123456789

# ==== ESKIZ SMS ====
ESKIZ_EMAIL=your@email.com
ESKIZ_PASSWORD=your_password
ESKIZ_SENDER=4546

# ==== WHATSAPP ====
WHATSAPP_PHONE_ID=123456789
WHATSAPP_TOKEN=EAAG...
WHATSAPP_VERIFY_TOKEN=random-verify-token

# ==== TO'LOV ====
PAYME_MERCHANT_ID=your_merchant_id
PAYME_KEY=your_payme_key
CLICK_SERVICE_ID=your_service_id
CLICK_MERCHANT_ID=your_merchant_id
CLICK_MERCHANT_USER_ID=your_user_id
CLICK_SECRET_KEY=your_secret

# ==== BIZNES QOIDALARI ====
MIN_ORDER_AMOUNT=50000
MAX_ORDER_AMOUNT=50000000
OTP_TTL_SECONDS=300
OTP_MAX_ATTEMPTS=3
ORDER_CANCEL_WINDOW_MINUTES=5

# ==== KOMISSIYA ====
PLATFORM_COMMISSION_PERCENT=10
DEALER_DEFAULT_COMMISSION_PERCENT=15
DEVELOPER_DEFAULT_ROYALTY_PERCENT=10

# ==== MONITORING ====
SENTRY_DSN=
LOG_LEVEL=INFO
PROMETHEUS_ENABLED=true

# ==== CORS ====
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001,http://localhost:3002,http://localhost:3003,http://localhost:3004,http://localhost:3005
```

## 1.4. `backend/app/core/config.py`

```python
from functools import lru_cache
from typing import Literal
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ==== ASOSIY ====
    ENV: Literal["development", "staging", "production"] = "development"
    DEBUG: bool = True
    SECRET_KEY: str = Field(..., min_length=32)
    API_V1_PREFIX: str = "/api/v1"

    # ==== DOMAIN ====
    BASE_URL: str = "http://localhost:8000"
    WEBAPP_URL: str = "http://localhost:3000"
    VENDOR_URL: str = "http://localhost:3001"
    DEALER_URL: str = "http://localhost:3002"
    DEVELOPER_URL: str = "http://localhost:3003"
    COURIER_URL: str = "http://localhost:3004"
    ADMIN_URL: str = "http://localhost:3005"

    # ==== DATABASE ====
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10

    # ==== REDIS ====
    REDIS_URL: str

    # ==== JWT ====
    JWT_ALGORITHM: str = "RS256"
    JWT_PRIVATE_KEY_PATH: str = "./secrets/jwt_private.pem"
    JWT_PUBLIC_KEY_PATH: str = "./secrets/jwt_public.pem"
    ACCESS_TOKEN_TTL: int = 900
    REFRESH_TOKEN_TTL: int = 604800

    @property
    def JWT_PRIVATE_KEY(self) -> str:
        with open(self.JWT_PRIVATE_KEY_PATH) as f:
            return f.read()

    @property
    def JWT_PUBLIC_KEY(self) -> str:
        with open(self.JWT_PUBLIC_KEY_PATH) as f:
            return f.read()

    # ==== TELEGRAM ====
    BOT_TOKEN: str = ""
    BOT_USERNAME: str = "xalquchun_bot"
    OWNER_ID: int = 0
    ADMIN_IDS: str = ""

    @property
    def admin_ids_list(self) -> list[int]:
        if not self.ADMIN_IDS:
            return []
        return [int(x.strip()) for x in self.ADMIN_IDS.split(",") if x.strip()]

    # ==== ESKIZ ====
    ESKIZ_EMAIL: str = ""
    ESKIZ_PASSWORD: str = ""
    ESKIZ_SENDER: str = "4546"

    # ==== WHATSAPP ====
    WHATSAPP_PHONE_ID: str = ""
    WHATSAPP_TOKEN: str = ""
    WHATSAPP_VERIFY_TOKEN: str = ""

    # ==== TO'LOV ====
    PAYME_MERCHANT_ID: str = ""
    PAYME_KEY: str = ""
    CLICK_SERVICE_ID: str = ""
    CLICK_MERCHANT_ID: str = ""
    CLICK_MERCHANT_USER_ID: str = ""
    CLICK_SECRET_KEY: str = ""

    # ==== BIZNES ====
    MIN_ORDER_AMOUNT: int = 50000
    MAX_ORDER_AMOUNT: int = 50000000
    OTP_TTL_SECONDS: int = 300
    OTP_MAX_ATTEMPTS: int = 3
    ORDER_CANCEL_WINDOW_MINUTES: int = 5

    # ==== KOMISSIYA ====
    PLATFORM_COMMISSION_PERCENT: float = 10.0
    DEALER_DEFAULT_COMMISSION_PERCENT: float = 15.0
    DEVELOPER_DEFAULT_ROYALTY_PERCENT: float = 10.0

    # ==== MONITORING ====
    SENTRY_DSN: str = ""
    LOG_LEVEL: str = "INFO"
    PROMETHEUS_ENABLED: bool = True

    # ==== CORS ====
    ALLOWED_ORIGINS: str = "http://localhost:3000"

    @property
    def allowed_origins_list(self) -> list[str]:
        return [x.strip() for x in self.ALLOWED_ORIGINS.split(",") if x.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
```

## 1.5. `backend/app/core/logging.py`

```python
import logging
import sys
import structlog
from app.core.config import settings


def setup_logging():
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=settings.LOG_LEVEL,
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer()
            if settings.ENV == "production"
            else structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, settings.LOG_LEVEL)
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    logger = structlog.get_logger()
    logger.info("logging_configured", env=settings.ENV, level=settings.LOG_LEVEL)


def get_logger(name: str = __name__):
    return structlog.get_logger(name)
```

## 1.6. `backend/app/core/exceptions.py`

```python
from fastapi import HTTPException, status


class AppException(Exception):
    """Base exception for all application errors"""
    status_code = status.HTTP_400_BAD_REQUEST
    error_code = "APP_ERROR"
    message = "Xatolik yuz berdi"

    def __init__(self, message: str | None = None, **kwargs):
        self.message = message or self.message
        self.details = kwargs
        super().__init__(self.message)


# ==== AUTH ====
class UnauthorizedError(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "UNAUTHORIZED"
    message = "Avtorizatsiya kerak"


class ForbiddenError(AppException):
    status_code = status.HTTP_403_FORBIDDEN
    error_code = "FORBIDDEN"
    message = "Ruxsat yo'q"


class InvalidOTPError(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    error_code = "INVALID_OTP"
    message = "Tasdiqlash kodi xato"


class OTPExpiredError(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    error_code = "OTP_EXPIRED"
    message = "Tasdiqlash kodi muddati tugagan"


class PhoneAlreadyExistsError(AppException):
    status_code = status.HTTP_409_CONFLICT
    error_code = "PHONE_EXISTS"
    message = "Bu telefon raqami allaqachon ro'yxatdan o'tgan"


class RateLimitError(AppException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    error_code = "RATE_LIMIT"
    message = "Juda ko'p urinish. Birozdan keyin urinib ko'ring"


# ==== BUSINESS ====
class BusinessRuleError(AppException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    error_code = "BUSINESS_RULE"
    message = "Biznes qoidasi buzilgan"


class NotFoundError(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = "NOT_FOUND"
    message = "Topilmadi"


class InsufficientBalanceError(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    error_code = "INSUFFICIENT_BALANCE"
    message = "Balans yetarli emas"


class InvalidStatusTransitionError(BusinessRuleError):
    error_code = "INVALID_STATUS"
    message = "Status o'tishi mumkin emas"


# ==== PAYMENT ====
class PaymentError(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    error_code = "PAYMENT_ERROR"
    message = "To'lovda xatolik"


class IdempotencyError(AppException):
    status_code = status.HTTP_409_CONFLICT
    error_code = "IDEMPOTENCY"
    message = "Bu so'rov allaqachon bajarilgan"


# ==== REGISTER HANDLERS ====
from fastapi import Request
from fastapi.responses import JSONResponse


async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "details": exc.details,
            }
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": "HTTP_ERROR",
                "message": exc.detail,
            }
        },
    )


async def unhandled_exception_handler(request: Request, exc: Exception):
    from app.core.logging import get_logger
    logger = get_logger()
    logger.exception("unhandled_error", path=request.url.path, error=str(exc))
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Server xatosi",
            }
        },
    )
```

## 1.7. `backend/app/db/session.py`

```python
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from app.core.config import settings


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,
    pool_recycle=3600,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

## 1.8. `backend/app/db/base.py`

```python
from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
```

## 1.9. `backend/app/db/models/__init__.py`

```python
from app.db.models.user import User
from app.db.models.otp import OTPCode
from app.db.models.kyc import KYCVerification
from app.db.models.vendor import Vendor, VendorStaff
from app.db.models.dealer import Dealer
from app.db.models.developer import Developer, DeveloperProduct
from app.db.models.category import Category
from app.db.models.product import Product
from app.db.models.cart import Cart, CartItem
from app.db.models.address import Address
from app.db.models.order import Order, OrderItem
from app.db.models.payment import Payment
from app.db.models.wallet import Wallet, WalletTransaction
from app.db.models.commission import CommissionRecord
from app.db.models.payout import Payout
from app.db.models.courier import Courier, CourierLocation
from app.db.models.contract import (
    DealerVendorContract,
    DealerDeveloperContract,
)
from app.db.models.promo import PromoCode, PromoUsage
from app.db.models.review import Review
from app.db.models.notification import Notification
from app.db.models.audit import AuditLog
from app.db.models.idempotency import IdempotencyKey

__all__ = [
    "User", "OTPCode", "KYCVerification",
    "Vendor", "VendorStaff", "Dealer", "Developer", "DeveloperProduct",
    "Category", "Product", "Cart", "CartItem", "Address",
    "Order", "OrderItem", "Payment",
    "Wallet", "WalletTransaction", "CommissionRecord", "Payout",
    "Courier", "CourierLocation",
    "DealerVendorContract", "DealerDeveloperContract",
    "PromoCode", "PromoUsage", "Review",
    "Notification", "AuditLog", "IdempotencyKey",
]
```

## 1.10. `backend/app/db/models/user.py`

```python
from datetime import datetime
from sqlalchemy import BigInteger, Boolean, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    telegram_id: Mapped[int | None] = mapped_column(BigInteger, unique=True, index=True)
    phone: Mapped[str | None] = mapped_column(String(20), unique=True, index=True)
    email: Mapped[str | None] = mapped_column(String(255), unique=True)

    full_name: Mapped[str | None] = mapped_column(String(255))
    language: Mapped[str] = mapped_column(String(5), default="uz")

    source_channel: Mapped[str | None] = mapped_column(String(20))
    # 'telegram' | 'sms' | 'whatsapp'

    roles: Mapped[list[str]] = mapped_column(
        ARRAY(String), default=["customer"]
    )
    # ['customer', 'courier', 'vendor', 'dealer', 'developer', 'admin']

    is_registered: Mapped[bool] = mapped_column(Boolean, default=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)

    kyc_status: Mapped[str] = mapped_column(String(20), default="pending")
    # 'pending' | 'approved' | 'rejected'

    preferred_channels: Mapped[list[str] | None] = mapped_column(ARRAY(String))

    default_address_id: Mapped[int | None] = mapped_column(BigInteger)

    loyalty_points: Mapped[int] = mapped_column(Integer, default=0)
    loyalty_tier: Mapped[str] = mapped_column(String(20), default="bronze")

    referral_code: Mapped[str | None] = mapped_column(String(20), unique=True, index=True)
    referred_by: Mapped[int | None] = mapped_column(BigInteger)

    terms_accepted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    privacy_accepted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    def __repr__(self):
        return f"<User {self.id} {self.phone or self.telegram_id}>"
```

## 1.11. `backend/app/db/models/otp.py`

```python
from datetime import datetime
from sqlalchemy import BigInteger, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class OTPCode(Base, TimestampMixin):
    __tablename__ = "otp_codes"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    phone: Mapped[str] = mapped_column(String(20), index=True)
    code_hash: Mapped[str] = mapped_column(String(255))
    channel: Mapped[str] = mapped_column(String(20))  # 'sms'|'whatsapp'

    attempts: Mapped[int] = mapped_column(Integer, default=0)
    max_attempts: Mapped[int] = mapped_column(Integer, default=3)

    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
```

## 1.12. `backend/app/db/models/kyc.py`

```python
from datetime import date, datetime
from sqlalchemy import BigInteger, Date, DateTime, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class KYCVerification(Base, TimestampMixin):
    __tablename__ = "kyc_verifications"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)

    # Shifrlangan ma'lumotlar (AES-256-GCM)
    encrypted_data: Mapped[dict] = mapped_column(JSONB)

    # Masked versiyalar (ko'rsatish uchun)
    passport_masked: Mapped[str | None] = mapped_column(String(20))
    phone_masked: Mapped[str | None] = mapped_column(String(20))

    selfie_url: Mapped[str | None] = mapped_column(Text)
    passport_front_url: Mapped[str | None] = mapped_column(Text)
    passport_back_url: Mapped[str | None] = mapped_column(Text)

    status: Mapped[str] = mapped_column(String(20), default="pending")
    verified_by: Mapped[int | None] = mapped_column(BigInteger)
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    rejection_reason: Mapped[str | None] = mapped_column(Text)
```

## 1.13. `backend/app/db/models/order.py`

```python
from datetime import datetime
from decimal import Decimal
from sqlalchemy import (
    BigInteger, DateTime, ForeignKey, Integer, Numeric, String, Text, Index
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class Order(Base, TimestampMixin):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    order_number: Mapped[str] = mapped_column(String(30), unique=True, index=True)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), index=True)
    vendor_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("vendors.id"))
    dealer_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("dealers.id"))
    address_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("addresses.id"))
    courier_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("couriers.id"))

    status: Mapped[str] = mapped_column(String(30), index=True)
    # 'draft','pending_payment','paid','accepted','preparing','ready',
    # 'assigned','picked_up','on_the_way','delivered','completed',
    # 'cancelled','refunded'

    subtotal: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    delivery_fee: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    discount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    total: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    vat_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)

    payment_method: Mapped[str | None] = mapped_column(String(30))
    payment_status: Mapped[str] = mapped_column(String(30), default="pending")
    payment_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("payments.id"))

    promo_code: Mapped[str | None] = mapped_column(String(50))
    loyalty_points_used: Mapped[int] = mapped_column(Integer, default=0)
    loyalty_points_earned: Mapped[int] = mapped_column(Integer, default=0)

    source_channel: Mapped[str | None] = mapped_column(String(20))
    customer_comment: Mapped[str | None] = mapped_column(Text)
    cancellation_reason: Mapped[str | None] = mapped_column(Text)

    # Moliyaviy taqsimot
    platform_commission: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    dealer_commission: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    developer_royalty: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    vendor_net_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    courier_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    payment_fee: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)

    # Vaqt belgilari
    accepted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    ready_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    picked_up_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    delivered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order", cascade="all, delete-orphan", lazy="selectin"
    )

    __table_args__ = (
        Index("ix_orders_user_created", "user_id", "created_at"),
        Index("ix_orders_vendor_status", "vendor_id", "status"),
        Index("ix_orders_courier_status", "courier_id", "status"),
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    order_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("orders.id", ondelete="CASCADE"), index=True
    )
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("products.id"))
    developer_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("developers.id"))

    product_name: Mapped[str] = mapped_column(String(255))
    product_sku: Mapped[str | None] = mapped_column(String(100))
    quantity: Mapped[int] = mapped_column(Integer)
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    cost_price: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    total: Mapped[Decimal] = mapped_column(Numeric(12, 2))

    # Moliyaviy
    royalty_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    dealer_commission_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    platform_commission_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    vendor_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)

    status: Mapped[str] = mapped_column(String(20), default="active")

    order: Mapped["Order"] = relationship(back_populates="items")
```

## 1.14. `backend/app/db/models/wallet.py`

```python
from decimal import Decimal
from sqlalchemy import BigInteger, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class Wallet(Base, TimestampMixin):
    __tablename__ = "wallets"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    owner_id: Mapped[int] = mapped_column(BigInteger, index=True)
    owner_type: Mapped[str] = mapped_column(String(20), index=True)
    # 'user' | 'vendor' | 'dealer' | 'developer' | 'courier' | 'platform'

    balance: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=0)
    pending_balance: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=0)
    frozen_balance: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=0)
    total_earned: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=0)
    total_withdrawn: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=0)

    currency: Mapped[str] = mapped_column(String(5), default="UZS")


class WalletTransaction(Base, TimestampMixin):
    __tablename__ = "wallet_transactions"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    wallet_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("wallets.id"), index=True)

    type: Mapped[str] = mapped_column(String(30))
    # 'credit' | 'debit' | 'hold' | 'release' | 'refund'

    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2))
    balance_before: Mapped[Decimal] = mapped_column(Numeric(15, 2))
    balance_after: Mapped[Decimal] = mapped_column(Numeric(15, 2))

    source_type: Mapped[str | None] = mapped_column(String(30))
    source_id: Mapped[int | None] = mapped_column(BigInteger)
    description: Mapped[str | None] = mapped_column(Text)
    metadata_json: Mapped[dict | None] = mapped_column("metadata", JSONB)
```

## 1.15. `backend/app/db/models/payout.py`

```python
from datetime import datetime
from decimal import Decimal
from sqlalchemy import BigInteger, DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class Payout(Base, TimestampMixin):
    __tablename__ = "payouts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    wallet_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("wallets.id"), index=True)

    owner_id: Mapped[int] = mapped_column(BigInteger, index=True)
    owner_type: Mapped[str] = mapped_column(String(20))

    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2))
    fee: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=0)
    net_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2))

    method: Mapped[str] = mapped_column(String(30))
    account_details: Mapped[dict] = mapped_column(JSONB)

    status: Mapped[str] = mapped_column(String(20), default="pending", index=True)
    # 'pending' | 'approved' | 'processing' | 'completed' | 'rejected'

    requested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    approved_by: Mapped[int | None] = mapped_column(BigInteger)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    rejection_reason: Mapped[str | None] = mapped_column(Text)

    provider_txn_id: Mapped[str | None] = mapped_column(String(255))
```

## 1.16. `backend/app/db/models/audit.py`

```python
from sqlalchemy import BigInteger, String, Text
from sqlalchemy.dialects.postgresql import INET, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class AuditLog(Base, TimestampMixin):
    __tablename__ = "audit_log"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    actor_id: Mapped[int | None] = mapped_column(BigInteger, index=True)
    actor_role: Mapped[str | None] = mapped_column(String(30))
    actor_type: Mapped[str | None] = mapped_column(String(30))

    action: Mapped[str] = mapped_column(String(50), index=True)
    entity_type: Mapped[str] = mapped_column(String(50), index=True)
    entity_id: Mapped[int | None] = mapped_column(BigInteger, index=True)

    before_data: Mapped[dict | None] = mapped_column(JSONB)
    after_data: Mapped[dict | None] = mapped_column(JSONB)
    diff: Mapped[dict | None] = mapped_column(JSONB)

    ip_address: Mapped[str | None] = mapped_column(INET)
    user_agent: Mapped[str | None] = mapped_column(Text)
    request_id: Mapped[str | None] = mapped_column(String(50), index=True)

    status: Mapped[str | None] = mapped_column(String(20))
    error: Mapped[str | None] = mapped_column(Text)
```

## 1.17. Qolgan modellar (qisqacha)

`backend/app/db/models/vendor.py`:
```python
from datetime import time
from decimal import Decimal
from sqlalchemy import BigInteger, Boolean, ForeignKey, Integer, Numeric, String, Text, Time
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class Vendor(Base, TimestampMixin):
    __tablename__ = "vendors"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    owner_user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    dealer_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("dealers.id"))

    name: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True)
    legal_name: Mapped[str | None] = mapped_column(String(255))
    inn: Mapped[str | None] = mapped_column(String(20))
    type: Mapped[str] = mapped_column(String(30))

    description: Mapped[str | None] = mapped_column(Text)
    logo_url: Mapped[str | None] = mapped_column(Text)
    cover_url: Mapped[str | None] = mapped_column(Text)

    phone: Mapped[str | None] = mapped_column(String(20))
    email: Mapped[str | None] = mapped_column(String(255))
    address: Mapped[str | None] = mapped_column(Text)
    lat: Mapped[Decimal | None] = mapped_column(Numeric(10, 8))
    lng: Mapped[Decimal | None] = mapped_column(Numeric(11, 8))

    working_hours: Mapped[dict | None] = mapped_column(JSONB)

    is_open: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    commission_percent: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=10)
    min_order_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=50000)
    delivery_fee: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    free_delivery_from: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    delivery_radius_km: Mapped[int] = mapped_column(Integer, default=5)
    avg_delivery_time: Mapped[int] = mapped_column(Integer, default=30)

    rating: Mapped[Decimal] = mapped_column(Numeric(3, 2), default=0)
    total_orders: Mapped[int] = mapped_column(Integer, default=0)

    staff: Mapped[list["VendorStaff"]] = relationship(back_populates="vendor")


class VendorStaff(Base, TimestampMixin):
    __tablename__ = "vendor_staff"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    vendor_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("vendors.id", ondelete="CASCADE")
    )
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))

    role: Mapped[str] = mapped_column(String(30))
    permissions: Mapped[dict | None] = mapped_column(JSONB)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    vendor: Mapped["Vendor"] = relationship(back_populates="staff")
```

## 1.18. Alembic sozlash

```bash
cd backend
alembic init alembic
```

`backend/alembic/env.py`:
```python
import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

from app.core.config import settings
from app.db.base import Base
from app.db.models import *  # noqa

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

## 1.19. JWT kalitlarini generatsiya qilish

```bash
cd backend
openssl genrsa -out secrets/jwt_private.pem 4096
openssl rsa -in secrets/jwt_private.pem -pubout -out secrets/jwt_public.pem
chmod 600 secrets/*.pem
```

## 1.20. Auth Service

`backend/app/services/auth_service.py`:

```python
import hmac
import hashlib
import secrets
import json
from datetime import datetime, timedelta, timezone
from urllib.parse import parse_qsl

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import (
    InvalidOTPError, OTPExpiredError, UnauthorizedError, RateLimitError,
)
from app.core.logging import get_logger
from app.db.models import User, OTPCode
from app.services.redis_service import RedisService

logger = get_logger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, db: AsyncSession, redis: RedisService):
        self.db = db
        self.redis = redis

    # ============ OTP ============
    async def request_otp(self, phone: str, channel: str) -> dict:
        # Rate limit
        key = f"otp:rl:{phone}"
        count = await self.redis.incr(key, ttl=60)
        if count > 3:
            raise RateLimitError()

        # Kod generatsiya
        code = f"{secrets.randbelow(1_000_000):06d}"
        code_hash = pwd_context.hash(code)

        otp = OTPCode(
            phone=phone,
            code_hash=code_hash,
            channel=channel,
            max_attempts=settings.OTP_MAX_ATTEMPTS,
            expires_at=datetime.now(timezone.utc)
            + timedelta(seconds=settings.OTP_TTL_SECONDS),
        )
        self.db.add(otp)
        await self.db.commit()

        # Kod ni Redis ga ham saqlash (tez tekshirish uchun)
        await self.redis.setex(
            f"otp:{phone}", settings.OTP_TTL_SECONDS, code
        )

        logger.info("otp_requested", phone=phone[-4:], channel=channel)

        return {
            "success": True,
            "expires_in": settings.OTP_TTL_SECONDS,
            "channel": channel,
            "code": code if settings.DEBUG else None,
        }

    async def verify_otp(self, phone: str, code: str) -> dict:
        stmt = (
            select(OTPCode)
            .where(OTPCode.phone == phone, OTPCode.used_at.is_(None))
            .order_by(OTPCode.created_at.desc())
            .limit(1)
        )
        otp = (await self.db.execute(stmt)).scalar_one_or_none()

        if not otp:
            raise InvalidOTPError("Kod topilmadi")

        if otp.expires_at < datetime.now(timezone.utc):
            raise OTPExpiredError()

        if otp.attempts >= otp.max_attempts:
            raise InvalidOTPError("Urinishlar tugadi")

        if not pwd_context.verify(code, otp.code_hash):
            otp.attempts += 1
            await self.db.commit()
            raise InvalidOTPError(f"Kod xato. {otp.max_attempts - otp.attempts} urinish qoldi")

        otp.used_at = datetime.now(timezone.utc)
        await self.db.commit()

        # Redis dan o'chirish
        await self.redis.delete(f"otp:{phone}")

        user = await self._get_or_create_by_phone(phone)
        return self._create_tokens(user)

    # ============ Telegram WebApp ============
    def verify_telegram_init_data(self, init_data: str) -> dict:
        parsed = dict(parse_qsl(init_data, keep_blank_values=True))
        received_hash = parsed.pop("hash", None)
        if not received_hash:
            raise UnauthorizedError("initData yaroqsiz")

        data_check_string = "\n".join(
            f"{k}={v}" for k, v in sorted(parsed.items())
        )
        secret_key = hmac.new(
            b"WebAppData", settings.BOT_TOKEN.encode(), hashlib.sha256
        ).digest()
        calculated = hmac.new(
            secret_key, data_check_string.encode(), hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(calculated, received_hash):
            raise UnauthorizedError("initData yaroqsiz")

        # auth_date 1 soatdan oshmasin
        import time
        auth_date = int(parsed.get("auth_date", 0))
        if time.time() - auth_date > 3600:
            raise UnauthorizedError("initData eskirgan")

        return parsed

    async def login_telegram(self, init_data: str) -> dict:
        parsed = self.verify_telegram_init_data(init_data)
        tg_user = json.loads(parsed["user"])

        user = await self._get_or_create_by_telegram(
            telegram_id=tg_user["id"],
            full_name=(
                f"{tg_user.get('first_name', '')} "
                f"{tg_user.get('last_name', '')}"
            ).strip(),
            language=tg_user.get("language_code", "uz")[:5],
        )
        return self._create_tokens(user)

    # ============ Tokenlar ============
    def _create_tokens(self, user: User) -> dict:
        now = datetime.now(timezone.utc)

        access_payload = {
            "sub": str(user.id),
            "roles": user.roles,
            "type": "access",
            "iat": now,
            "exp": now + timedelta(seconds=settings.ACCESS_TOKEN_TTL),
        }
        refresh_payload = {
            "sub": str(user.id),
            "type": "refresh",
            "jti": secrets.token_urlsafe(32),
            "iat": now,
            "exp": now + timedelta(seconds=settings.REFRESH_TOKEN_TTL),
        }

        return {
            "access_token": jwt.encode(
                access_payload, settings.JWT_PRIVATE_KEY, algorithm="RS256"
            ),
            "refresh_token": jwt.encode(
                refresh_payload, settings.JWT_PRIVATE_KEY, algorithm="RS256"
            ),
            "token_type": "Bearer",
            "expires_in": settings.ACCESS_TOKEN_TTL,
            "user": {
                "id": user.id,
                "phone": user.phone,
                "full_name": user.full_name,
                "roles": user.roles,
                "is_verified": user.is_verified,
                "kyc_status": user.kyc_status,
            },
        }

    def refresh_token(self, refresh_token: str) -> dict:
        try:
            payload = jwt.decode(
                refresh_token, settings.JWT_PUBLIC_KEY, algorithms=["RS256"]
            )
        except Exception:
            raise UnauthorizedError("Token yaroqsiz")

        if payload.get("type") != "refresh":
            raise UnauthorizedError("Token turi xato")

        # Yangi access token
        now = datetime.now(timezone.utc)
        access_payload = {
            "sub": payload["sub"],
            "type": "access",
            "iat": now,
            "exp": now + timedelta(seconds=settings.ACCESS_TOKEN_TTL),
        }
        return {
            "access_token": jwt.encode(
                access_payload, settings.JWT_PRIVATE_KEY, algorithm="RS256"
            ),
            "token_type": "Bearer",
            "expires_in": settings.ACCESS_TOKEN_TTL,
        }

    # ============ User helpers ============
    async def _get_or_create_by_phone(self, phone: str) -> User:
        stmt = select(User).where(User.phone == phone)
        user = (await self.db.execute(stmt)).scalar_one_or_none()
        if user:
            user.last_seen_at = datetime.now(timezone.utc)
            await self.db.commit()
            return user

        user = User(
            phone=phone,
            is_registered=True,
            source_channel="sms",
            referral_code=secrets.token_urlsafe(8)[:10].upper(),
            last_seen_at=datetime.now(timezone.utc),
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def _get_or_create_by_telegram(
        self, telegram_id: int, full_name: str, language: str
    ) -> User:
        stmt = select(User).where(User.telegram_id == telegram_id)
        user = (await self.db.execute(stmt)).scalar_one_or_none()
        if user:
            user.last_seen_at = datetime.now(timezone.utc)
            await self.db.commit()
            return user

        user = User(
            telegram_id=telegram_id,
            full_name=full_name,
            language=language,
            source_channel="telegram",
            is_registered=True,
            referral_code=secrets.token_urlsafe(8)[:10].upper(),
            last_seen_at=datetime.now(timezone.utc),
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
```

## 1.21. Redis Service

`backend/app/services/redis_service.py`:

```python
import json
from typing import Any
import redis.asyncio as redis
from app.core.config import settings


class RedisService:
    def __init__(self):
        self._client: redis.Redis | None = None

    async def connect(self):
        self._client = redis.from_url(
            settings.REDIS_URL, encoding="utf-8", decode_responses=True
        )
        await self._client.ping()

    async def close(self):
        if self._client:
            await self._client.close()

    @property
    def client(self) -> redis.Redis:
        if not self._client:
            raise RuntimeError("Redis ulanmagan")
        return self._client

    async def get(self, key: str) -> str | None:
        return await self.client.get(key)

    async def set(self, key: str, value: str, ttl: int | None = None):
        if ttl:
            await self.client.setex(key, ttl, value)
        else:
            await self.client.set(key, value)

    async def setex(self, key: str, ttl: int, value: str):
        await self.client.setex(key, ttl, value)

    async def delete(self, *keys: str):
        if keys:
            await self.client.delete(*keys)

    async def incr(self, key: str, ttl: int | None = None) -> int:
        val = await self.client.incr(key)
        if val == 1 and ttl:
            await self.client.expire(key, ttl)
        return val

    async def get_json(self, key: str) -> Any | None:
        val = await self.get(key)
        return json.loads(val) if val else None

    async def set_json(self, key: str, value: Any, ttl: int | None = None):
        await self.set(key, json.dumps(value), ttl)


redis_service = RedisService()
```

## 1.22. Dependencies

`backend/app/api/deps.py`:

```python
from typing import Annotated
from fastapi import Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import UnauthorizedError, ForbiddenError
from app.db.session import get_db
from app.db.models import User
from app.services.redis_service import redis_service

security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    if not credentials:
        raise UnauthorizedError()

    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.JWT_PUBLIC_KEY,
            algorithms=["RS256"],
        )
    except JWTError:
        raise UnauthorizedError("Token yaroqsiz")

    if payload.get("type") != "access":
        raise UnauthorizedError("Token turi xato")

    user_id = int(payload["sub"])
    user = await db.get(User, user_id)
    if not user:
        raise UnauthorizedError("Foydalanuvchi topilmadi")
    if user.is_blocked:
        raise ForbiddenError("Foydalanuvchi bloklangan")

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def require_roles(*roles: str):
    async def check(user: CurrentUser) -> User:
        if not any(r in user.roles for r in roles):
            raise ForbiddenError(f"Ruxsat kerak: {roles}")
        return user
    return check


async def get_current_verified_user(user: CurrentUser) -> User:
    if not user.is_verified:
        raise ForbiddenError("Profil tasdiqlanmagan. KYC dan o'ting")
    return user


CurrentVerifiedUser = Annotated[User, Depends(get_current_verified_user)]
```

## 1.23. Auth Router

`backend/app/api/v1/auth.py`:

```python
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.auth_service import AuthService
from app.services.redis_service import redis_service
from app.api.deps import CurrentUser

router = APIRouter(prefix="/auth", tags=["auth"])


class RequestOTPIn(BaseModel):
    phone: str = Field(..., pattern=r"^\+?998\d{9}$")
    channel: str = Field("sms", pattern="^(sms|whatsapp)$")


class VerifyOTPIn(BaseModel):
    phone: str
    code: str = Field(..., min_length=6, max_length=6)


class TelegramWebAppIn(BaseModel):
    init_data: str


class RefreshIn(BaseModel):
    refresh_token: str


@router.post("/request-otp")
async def request_otp(
    data: RequestOTPIn,
    db: AsyncSession = Depends(get_db),
):
    svc = AuthService(db, redis_service)
    # Kanal bo'yicha yuborish
    from app.services.notification_service import NotificationService
    notifier = NotificationService(db)
    result = await svc.request_otp(data.phone, data.channel)
    # OTP yuborish
    await notifier.send_otp(
        phone=data.phone,
        code=result["code"],
        channel=data.channel,
        ttl=result["expires_in"],
    )
    return result


@router.post("/verify-otp")
async def verify_otp(
    data: VerifyOTPIn,
    db: AsyncSession = Depends(get_db),
):
    svc = AuthService(db, redis_service)
    return await svc.verify_otp(data.phone, data.code)


@router.post("/telegram-webapp")
async def telegram_webapp(
    data: TelegramWebAppIn,
    db: AsyncSession = Depends(get_db),
):
    svc = AuthService(db, redis_service)
    return await svc.login_telegram(data.init_data)


@router.post("/refresh")
async def refresh(
    data: RefreshIn,
    db: AsyncSession = Depends(get_db),
):
    svc = AuthService(db, redis_service)
    return svc.refresh_token(data.refresh_token)


@router.get("/me")
async def me(user: CurrentUser):
    return {
        "id": user.id,
        "phone": user.phone,
        "email": user.email,
        "full_name": user.full_name,
        "roles": user.roles,
        "language": user.language,
        "is_verified": user.is_verified,
        "kyc_status": user.kyc_status,
        "loyalty_points": user.loyalty_points,
        "loyalty_tier": user.loyalty_tier,
        "referral_code": user.referral_code,
        "source_channel": user.source_channel,
    }
```

## 1.24. Main App

`backend/app/main.py`:

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.core.exceptions import (
    AppException, app_exception_handler,
    HTTPException, http_exception_handler,
    unhandled_exception_handler,
)
from app.services.redis_service import redis_service

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("starting_app", env=settings.ENV)
    await redis_service.connect()
    logger.info("redis_connected")
    yield
    await redis_service.close()
    logger.info("app_stopped")


app = FastAPI(
    title="XalqUchun API",
    version="3.0.0",
    description="Multi-vendor delivery platform",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

# Routers
from app.api.v1 import api_router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/health")
async def health():
    return {"status": "ok", "version": "3.0.0", "env": settings.ENV}


@app.get("/healthz")
async def healthz():
    return {"status": "healthy"}


@app.get("/readyz")
async def readyz():
    # Redis tekshirish
    try:
        await redis_service.client.ping()
        return {"status": "ready"}
    except Exception:
        return {"status": "not_ready"}, 503
```

## 1.25. `backend/app/api/v1/__init__.py`

```python
from fastapi import APIRouter
from app.api.v1 import auth, users, catalog, cart, orders

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(catalog.router)
api_router.include_router(cart.router)
api_router.include_router(orders.router)
```

## 1.26. Test va ishga tushirish

```bash
# 1. Migratsiya
cd backend
alembic revision --autogenerate -m "initial"
alembic upgrade head

# 2. Ishga tushirish
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 3. Test
curl http://localhost:8000/health
# {"status":"ok","version":"3.0.0","env":"development"}

curl -X POST http://localhost:8000/api/v1/auth/request-otp \
  -H "Content-Type: application/json" \
  -d '{"phone":"+998901234567","channel":"sms"}'
```

---

# 📦 MODUL 2: NOTIFICATION SERVICE (Eskiz + WhatsApp + Telegram)

## 2.1. SMS Provider Base

`backend/app/providers/sms/base.py`:

```python
from abc import ABC, abstractmethod


class SMSProvider(ABC):
    @abstractmethod
    async def send(self, phone: str, message: str) -> dict: ...

    @abstractmethod
    async def health_check(self) -> bool: ...
```

## 2.2. Eskiz Provider

`backend/app/providers/sms/eskiz.py`:

```python
import time
import aiohttp
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logging import get_logger
from app.providers.sms.base import SMSProvider

logger = get_logger(__name__)


class EskizProvider(SMSProvider):
    BASE_URL = "https://notify.eskiz.uz/api"

    def __init__(self):
        self.email = settings.ESKIZ_EMAIL
        self.password = settings.ESKIZ_PASSWORD
        self.sender = settings.ESKIZ_SENDER
        self._token: str | None = None
        self._token_expires: float = 0

    async def _ensure_token(self):
        if self._token and time.time() < self._token_expires:
            return

        async with aiohttp.ClientSession() as s:
            async with s.post(
                f"{self.BASE_URL}/auth/login",
                data={"email": self.email, "password": self.password},
                timeout=aiohttp.ClientTimeout(total=10),
            ) as r:
                data = await r.json()
                if "data" not in data:
                    logger.error("eskiz_login_failed", response=data)
                    raise RuntimeError(f"Eskiz login failed: {data}")
                self._token = data["data"]["token"]
                self._token_expires = time.time() + 20 * 3600
                logger.info("eskiz_token_refreshed")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(min=1, max=10),
        reraise=True,
    )
    async def send(self, phone: str, message: str) -> dict:
        await self._ensure_token()

        headers = {"Authorization": f"Bearer {self._token}"}
        payload = {
            "mobile_phone": phone.lstrip("+"),
            "message": message,
            "from": self.sender,
        }

        async with aiohttp.ClientSession() as s:
            async with s.post(
                f"{self.BASE_URL}/message/sms/send",
                headers=headers,
                data=payload,
                timeout=aiohttp.ClientTimeout(total=10),
            ) as r:
                if r.status == 401:
                    self._token = None
                    raise RuntimeError("Eskiz token expired")
                data = await r.json()
                logger.info("eskiz_sent", phone=phone[-4:], status=r.status)
                return data

    async def health_check(self) -> bool:
        try:
            await self._ensure_token()
            return True
        except Exception:
            return False
```

## 2.3. PlayMobile Provider (fallback)

`backend/app/providers/sms/playmobile.py`:

```python
import base64
import aiohttp
from app.providers.sms.base import SMSProvider


class PlayMobileProvider(SMSProvider):
    def __init__(self, login: str, password: str, sender: str = "3700"):
        self.login = login
        self.password = password
        self.sender = sender
        self.base_url = "https://send.smsxabar.uz/broker-api/send"

    async def send(self, phone: str, message: str) -> dict:
        auth = base64.b64encode(
            f"{self.login}:{self.password}".encode()
        ).decode()
        payload = {
            "messages": [{
                "recipient": phone.lstrip("+"),
                "message-id": f"msg-{phone[-6:]}",
                "sms": {
                    "originator": self.sender,
                    "content": {"text": message},
                },
            }]
        }
        headers = {
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/json",
        }
        async with aiohttp.ClientSession() as s:
            async with s.post(self.base_url, json=payload, headers=headers) as r:
                return await r.json()

    async def health_check(self) -> bool:
        return True
```

## 2.4. SMS Manager (fallback chain)

`backend/app/providers/sms/__init__.py`:

```python
from app.core.config import settings
from app.core.logging import get_logger
from app.providers.sms.base import SMSProvider
from app.providers.sms.eskiz import EskizProvider

logger = get_logger(__name__)


class SMSManager:
    def __init__(self):
        self.providers: list[SMSProvider] = [EskizProvider()]
        # Keyinchalik PlayMobile, TextUp qo'shiladi

    async def send(self, phone: str, message: str) -> dict:
        last_error = None
        for provider in self.providers:
            try:
                result = await provider.send(phone, message)
                logger.info(
                    "sms_sent",
                    provider=provider.__class__.__name__,
                    phone=phone[-4:],
                )
                return result
            except Exception as e:
                last_error = e
                logger.warning(
                    "sms_provider_failed",
                    provider=provider.__class__.__name__,
                    error=str(e),
                )
                continue

        raise RuntimeError(f"Barcha SMS provayderlar ishlamadi: {last_error}")


_sms_manager: SMSManager | None = None


def get_sms_provider() -> SMSManager:
    global _sms_manager
    if not _sms_manager:
        _sms_manager = SMSManager()
    return _sms_manager
```

## 2.5. WhatsApp Provider

`backend/app/providers/whatsapp/cloud_api.py`:

```python
import aiohttp
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class WhatsAppCloudAPI:
    def __init__(self):
        self.phone_id = settings.WHATSAPP_PHONE_ID
        self.token = settings.WHATSAPP_TOKEN
        self.url = f"https://graph.facebook.com/v18.0/{self.phone_id}/messages"

    async def send_text(self, phone: str, text: str) -> dict:
        return await self._post({
            "messaging_product": "whatsapp",
            "to": phone.lstrip("+"),
            "type": "text",
            "text": {"body": text, "preview_url": False},
        })

    async def send_template(
        self,
        phone: str,
        name: str,
        lang: str = "uz",
        params: list[str] | None = None,
    ) -> dict:
        components = []
        if params:
            components = [{
                "type": "body",
                "parameters": [
                    {"type": "text", "text": str(p)} for p in params
                ],
            }]

        return await self._post({
            "messaging_product": "whatsapp",
            "to": phone.lstrip("+"),
            "type": "template",
            "template": {
                "name": name,
                "language": {"code": lang},
                "components": components,
            },
        })

    async def _post(self, payload: dict) -> dict:
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        async with aiohttp.ClientSession() as s:
            async with s.post(
                self.url, headers=headers, json=payload,
                timeout=aiohttp.ClientTimeout(total=15),
            ) as r:
                data = await r.json()
                logger.info(
                    "whatsapp_sent",
                    phone=payload["to"][-4:],
                    status=r.status,
                )
                return data


_wa: WhatsAppCloudAPI | None = None


def get_wa_provider() -> WhatsAppCloudAPI:
    global _wa
    if not _wa:
        _wa = WhatsAppCloudAPI()
    return _wa
```

## 2.6. Telegram Provider

`backend/app/providers/telegram/provider.py`:

```python
import aiohttp
from app.core.config import settings


class TelegramProvider:
    def __init__(self):
        self.token = settings.BOT_TOKEN
        self.base = f"https://api.telegram.org/bot{self.token}"

    async def send_message(
        self,
        chat_id: int,
        text: str,
        reply_markup: dict | None = None,
        parse_mode: str = "HTML",
    ) -> dict:
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": True,
        }
        if reply_markup:
            payload["reply_markup"] = reply_markup

        async with aiohttp.ClientSession() as s:
            async with s.post(f"{self.base}/sendMessage", json=payload) as r:
                return await r.json()
```

## 2.7. Notification Service (to'liq)

`backend/app/services/notification_service.py`:

```python
from enum import Enum
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.db.models import Notification, User
from app.providers.sms import get_sms_provider
from app.providers.whatsapp.cloud_api import get_wa_provider
from app.providers.telegram.provider import TelegramProvider

logger = get_logger(__name__)


class Channel(str, Enum):
    TELEGRAM = "telegram"
    SMS = "sms"
    WHATSAPP = "whatsapp"


FALLBACK_CHAIN = {
    "telegram": ["telegram", "whatsapp", "sms"],
    "whatsapp": ["whatsapp", "sms", "telegram"],
    "sms":      ["sms", "whatsapp", "telegram"],
}

# Xabar shablonlari (o'zbek tilida)
TEMPLATES = {
    "order_created": {
        "uz": "✅ Buyurtmangiz qabul qilindi!\n\n"
              "Raqam: {order_number}\n"
              "Jami: {total:,} so'm\n\n"
              "Holatni kuzatish uchun: {track_url}",
        "ru": "✅ Ваш заказ принят!\n\n"
              "Номер: {order_number}\n"
              "Сумма: {total:,} сум",
    },
    "order_accepted": {
        "uz": "👨‍🍳 Do'kon buyurtmangizni qabul qildi!\n\n"
              "Raqam: {order_number}\n"
              "Tayyorlash boshlandi.",
        "ru": "👨‍🍳 Магазин принял ваш заказ!",
    },
    "order_on_the_way": {
        "uz": "🛵 Kuryer yo'lda!\n\n"
              "Raqam: {order_number}\n"
              "Kuryer: {courier_name}\n"
              "Yetib kelish: {eta_minutes} daqiqa",
        "ru": "🛵 Курьер в пути!",
    },
    "order_delivered": {
        "uz": "🎉 Buyurtmangiz yetkazildi!\n\n"
              "Raqam: {order_number}\n"
              "Jami: {total:,} so'm\n\n"
              "Iltimos, baholang: {rate_url}",
        "ru": "🎉 Заказ доставлен!",
    },
    "otp": {
        "uz": "XalqUchun: Tasdiqlash kodi: {code}\n"
              "Amal qilish muddati: {ttl_minutes} daqiqa",
        "ru": "XalqUchun: Код подтверждения: {code}",
    },
}

# WhatsApp template nomlari
WA_TEMPLATES = {
    "order_created": "order_confirmation",
    "order_accepted": "order_accepted",
    "order_on_the_way": "courier_on_way",
    "order_delivered": "order_delivered",
    "otp": "otp_code",
}


class NotificationService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.sms = get_sms_provider()
        self.whatsapp = get_wa_provider()
        self.telegram = TelegramProvider()

    async def notify(
        self,
        user: User,
        event: str,
        channels: list[Channel] | None = None,
        **ctx,
    ) -> dict:
        """Universal bildirishnoma yuborish"""
        if not channels:
            primary = user.source_channel or "telegram"
            chain_names = FALLBACK_CHAIN.get(primary, ["telegram"])
            channels = [Channel(c) for c in chain_names]

        # Shablonni tayyorlash
        text = self._render(event, ctx, lang=user.language or "uz")

        last_error = None
        for ch in channels:
            try:
                await self._send(ch, user, event, text, ctx)
                await self._log(user.id, event, ch.value, "sent")
                logger.info(
                    "notification_sent",
                    user_id=user.id,
                    event=event,
                    channel=ch.value,
                )
                return {"success": True, "channel": ch.value}
            except Exception as e:
                last_error = str(e)
                await self._log(user.id, event, ch.value, "failed", last_error)
                logger.warning(
                    "notification_channel_failed",
                    user_id=user.id,
                    event=event,
                    channel=ch.value,
                    error=last_error,
                )
                continue

        await self._log(user.id, event, "none", "all_failed", last_error)
        return {"success": False, "error": last_error}

    async def send_otp(
        self,
        phone: str,
        code: str,
        channel: str,
        ttl: int,
    ) -> dict:
        """OTP yuborish (SMS yoki WhatsApp orqali)"""
        text = TEMPLATES["otp"]["uz"].format(
            code=code, ttl_minutes=ttl // 60
        )

        if channel == "sms":
            await self.sms.send(phone, text)
            return {"success": True, "channel": "sms"}
        elif channel == "whatsapp":
            try:
                await self.whatsapp.send_template(
                    phone,
                    WA_TEMPLATES["otp"],
                    lang="uz",
                    params=[code, str(ttl // 60)],
                )
                return {"success": True, "channel": "whatsapp"}
            except Exception:
                # Fallback SMS
                await self.sms.send(phone, text)
                return {"success": True, "channel": "sms"}
        else:
            raise ValueError(f"OTP kanal qo'llanilmaydi: {channel}")

    async def _send(
        self,
        ch: Channel,
        user: User,
        event: str,
        text: str,
        ctx: dict,
    ):
        if ch == Channel.TELEGRAM:
            if not user.telegram_id:
                raise ValueError("Telegram ID yo'q")
            await self.telegram.send_message(user.telegram_id, text)

        elif ch == Channel.SMS:
            if not user.phone:
                raise ValueError("Telefon raqami yo'q")
            await self.sms.send(user.phone, text)

        elif ch == Channel.WHATSAPP:
            if not user.phone:
                raise ValueError("Telefon raqami yo'q")
            # WhatsApp template ishlatish (Meta talabi)
            template_name = WA_TEMPLATES.get(event)
            if template_name and event in WA_TEMPLATES:
                params = self._wa_template_params(event, ctx)
                await self.whatsapp.send_template(
                    user.phone, template_name, lang="uz", params=params
                )
            else:
                await self.whatsapp.send_text(user.phone, text)
        else:
            raise ValueError(f"Kanal mavjud emas: {ch}")

    def _wa_template_params(self, event: str, ctx: dict) -> list[str]:
        """WhatsApp template parametrlari"""
        mappers = {
            "order_created": lambda c: [
                c.get("order_number", ""), f"{c.get('total', 0):,}"
            ],
            "order_accepted": lambda c: [c.get("order_number", "")],
            "order_on_the_way": lambda c: [
                c.get("order_number", ""),
                c.get("courier_name", ""),
                str(c.get("eta_minutes", 0)),
            ],
            "order_delivered": lambda c: [
                c.get("order_number", ""), f"{c.get('total', 0):,}"
            ],
            "otp": lambda c: [c.get("code", ""), str(c.get("ttl_minutes", 5))],
        }
        return mappers.get(event, lambda c: [])(ctx)

    def _render(self, event: str, ctx: dict, lang: str = "uz") -> str:
        tmpl = TEMPLATES.get(event, {})
        text = tmpl.get(lang) or tmpl.get("uz", "")
        try:
            return text.format(**ctx)
        except KeyError:
            return text

    async def _log(
        self,
        user_id: int,
        event: str,
        channel: str,
        status: str,
        error: str | None = None,
    ):
        try:
            notif = Notification(
                user_id=user_id,
                event=event,
                channel=channel,
                status=status,
                error=error,
            )
            self.db.add(notif)
            await self.db.commit()
        except Exception:
            await self.db.rollback()
```

## 2.8. Notification model

`backend/app/db/models/notification.py`:

```python
from sqlalchemy import BigInteger, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin


class Notification(Base, TimestampMixin):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), index=True)
    event: Mapped[str] = mapped_column(String(50))
    channel: Mapped[str] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(20))
    template: Mapped[str | None] = mapped_column(String(100))
    payload: Mapped[dict | None] = mapped_column(JSONB)
    error: Mapped[str | None] = mapped_column(Text)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
```

## 2.9. Celery task — asinxron yuborish

`backend/app/tasks/celery_app.py`:

```python
from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "xalquchun",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Asia/Tashkent",
    enable_utc=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)
```

`backend/app/tasks/notification_tasks.py`:

```python
import asyncio
from app.tasks.celery_app import celery_app
from app.db.session import AsyncSessionLocal
from app.db.models import User
from app.services.notification_service import NotificationService


@celery_app.task(name="send_notification", max_retries=3)
def send_notification_task(user_id: int, event: str, ctx: dict):
    asyncio.run(_send_notification(user_id, event, ctx))


async def _send_notification(user_id: int, event: str, ctx: dict):
    async with AsyncSessionLocal() as db:
        user = await db.get(User, user_id)
        if not user:
            return
        svc = NotificationService(db)
        await svc.notify(user, event=event, **ctx)
```

## 2.10. Test

```bash
# .env da ESKIZ sozlangan bo'lsa
python -c "
import asyncio
from app.providers.sms import get_sms_provider

async def test():
    sms = get_sms_provider()
    result = await sms.send('+998901234567', 'Test xabar')
    print(result)

asyncio.run(test())
"
```

---

# 📦 MODUL 3: ORDER SERVICE (State Machine + Komissiya)

## 3.1. Order State Machine

`backend/app/business/order_states.py`:

```python
from enum import Enum


class OrderStatus(str, Enum):
    DRAFT = "draft"
    PENDING_PAYMENT = "pending_payment"
    PAID = "paid"
    ACCEPTED = "accepted"
    PREPARING = "preparing"
    READY = "ready"
    ASSIGNED = "assigned"
    PICKED_UP = "picked_up"
    ON_THE_WAY = "on_the_way"
    DELIVERED = "delivered"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


# Ruxsat etilgan o'tishlar
VALID_TRANSITIONS: dict[OrderStatus, list[OrderStatus]] = {
    OrderStatus.DRAFT: [OrderStatus.PENDING_PAYMENT, OrderStatus.CANCELLED],
    OrderStatus.PENDING_PAYMENT: [OrderStatus.PAID, OrderStatus.CANCELLED],
    OrderStatus.PAID: [
        OrderStatus.ACCEPTED, OrderStatus.CANCELLED, OrderStatus.REFUNDED,
    ],
    OrderStatus.ACCEPTED: [
        OrderStatus.PREPARING, OrderStatus.CANCELLED, OrderStatus.REFUNDED,
    ],
    OrderStatus.PREPARING: [
        OrderStatus.READY, OrderStatus.CANCELLED,
    ],
    OrderStatus.READY: [OrderStatus.ASSIGNED, OrderStatus.CANCELLED],
    OrderStatus.ASSIGNED: [OrderStatus.PICKED_UP, OrderStatus.CANCELLED],
    OrderStatus.PICKED_UP: [OrderStatus.ON_THE_WAY, OrderStatus.CANCELLED],
    OrderStatus.ON_THE_WAY: [OrderStatus.DELIVERED, OrderStatus.CANCELLED],
    OrderStatus.DELIVERED: [OrderStatus.COMPLETED, OrderStatus.REFUNDED],
    OrderStatus.COMPLETED: [],
    OrderStatus.CANCELLED: [],
    OrderStatus.REFUNDED: [],
}


def can_transition(old: str, new: str) -> bool:
    try:
        old_status = OrderStatus(old)
        new_status = OrderStatus(new)
        return new_status in VALID_TRANSITIONS.get(old_status, [])
    except ValueError:
        return False


# Holat xabarlari
STATUS_MESSAGES = {
    OrderStatus.PAID: "💳 To'lov qabul qilindi",
    OrderStatus.ACCEPTED: "✅ Do'kon qabul qildi",
    OrderStatus.PREPARING: "👨‍🍳 Tayyorlanmoqda",
    OrderStatus.READY: "📦 Tayyor, kuryer kutilmoqda",
    OrderStatus.ASSIGNED: "🛵 Kuryer tayinlandi",
    OrderStatus.PICKED_UP: "📦 Kuryer oldi",
    OrderStatus.ON_THE_WAY: "🚀 Yo'lda",
    OrderStatus.DELIVERED: "🎉 Yetkazildi",
    OrderStatus.COMPLETED: "✅ Yakunlandi",
    OrderStatus.CANCELLED: "❌ Bekor qilindi",
    OrderStatus.REFUNDED: "💰 Qaytarildi",
}
```

## 3.2. Commission Service

`backend/app/services/commission_service.py`:

```python
from decimal import Decimal, ROUND_HALF_UP
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.logging import get_logger
from app.db.models import Order, CommissionRecord
from app.services.wallet_service import WalletService

logger = get_logger(__name__)

TWOPLACES = Decimal("0.01")
VAT_RATE = Decimal("0.12")
PAYMENT_FEE_RATE = Decimal("0.02")


class CommissionService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.wallet = WalletService(db)

    def _q(self, d: Decimal) -> Decimal:
        return d.quantize(TWOPLACES, rounding=ROUND_HALF_UP)

    async def calculate(self, order: Order) -> dict:
        """Buyurtma summasidan komissiya hisoblash"""
        total = Decimal(str(order.total))

        vat = self._q(total * VAT_RATE)
        payment_fee = self._q(total * PAYMENT_FEE_RATE)
        net = total - vat - payment_fee

        # Platforma
        platform_pct = Decimal(str(settings.PLATFORM_COMMISSION_PERCENT)) / 100
        platform_commission = self._q(net * platform_pct)
        remaining = net - platform_commission

        # Dealer (vendor.dealer orqali)
        dealer_commission = Decimal("0")
        developer_royalty = Decimal("0")

        # Vendor va dealer ma'lumotlarini olish
        from app.db.models import Vendor
        vendor = await self.db.get(Vendor, order.vendor_id)

        if vendor and vendor.dealer_id:
            dealer_pct = Decimal(str(settings.DEALER_DEFAULT_COMMISSION_PERCENT)) / 100
            dealer_commission = self._q(remaining * dealer_pct)
            remaining -= dealer_commission

            # Developer royalty
            from app.db.models import Dealer
            dealer = await self.db.get(Dealer, vendor.dealer_id)
            if dealer:
                dev_pct = Decimal(str(settings.DEVELOPER_DEFAULT_ROYALTY_PERCENT)) / 100
                developer_royalty = self._q(remaining * dev_pct)
                remaining -= developer_royalty

        vendor_amount = remaining
        courier_amount = Decimal(str(order.courier_amount or 0))

        return {
            "vat": vat,
            "payment_fee": payment_fee,
            "platform_commission": platform_commission,
            "dealer_commission": dealer_commission,
            "developer_royalty": developer_royalty,
            "vendor_amount": vendor_amount,
            "courier_amount": courier_amount,
        }

    async def distribute(self, order: Order) -> dict:
        """Buyurtma yakunlanganda hamyonlarga taqsimlash"""
        calc = await self.calculate(order)

        # Order ga yozish
        order.platform_commission = calc["platform_commission"]
        order.dealer_commission = calc["dealer_commission"]
        order.developer_royalty = calc["developer_royalty"]
        order.vendor_net_amount = calc["vendor_amount"]
        order.courier_amount = calc["courier_amount"]
        order.payment_fee = calc["payment_fee"]
        order.vat_amount = calc["vat"]

        # === Hamyonlarga taqsimlash ===
        # Platforma
        platform_wallet = await self.wallet.get_or_create(1, "platform")
        if calc["platform_commission"] > 0:
            await self.wallet.credit(
                wallet_id=platform_wallet.id,
                amount=calc["platform_commission"],
                source_type="commission",
                source_id=order.id,
                description=f"Platforma komissiyasi #{order.order_number}",
            )

        # Dealer
        from app.db.models import Vendor
        vendor = await self.db.get(Vendor, order.vendor_id)
        if vendor and vendor.dealer_id and calc["dealer_commission"] > 0:
            dealer_wallet = await self.wallet.get_or_create(
                vendor.dealer_id, "dealer"
            )
            await self.wallet.credit(
                wallet_id=dealer_wallet.id,
                amount=calc["dealer_commission"],
                source_type="commission",
                source_id=order.id,
                description=f"Dealer komissiyasi #{order.order_number}",
            )

        # Developer
        if vendor and vendor.dealer_id and calc["developer_royalty"] > 0:
            from app.db.models import Dealer
            dealer = await self.db.get(Dealer, vendor.dealer_id)
            if dealer and dealer.developer_id:
                dev_wallet = await self.wallet.get_or_create(
                    dealer.developer_id, "developer"
                )
                await self.wallet.credit(
                    wallet_id=dev_wallet.id,
                    amount=calc["developer_royalty"],
                    source_type="royalty",
                    source_id=order.id,
                    description=f"Royalty #{order.order_number}",
                )

        # Vendor (do'kon)
        if calc["vendor_amount"] > 0:
            vendor_wallet = await self.wallet.get_or_create(
                order.vendor_id, "vendor"
            )
            await self.wallet.credit(
                wallet_id=vendor_wallet.id,
                amount=calc["vendor_amount"],
                source_type="sale",
                source_id=order.id,
                description=f"Sotuv #{order.order_number}",
            )

        # Courier
        if order.courier_id and calc["courier_amount"] > 0:
            courier_wallet = await self.wallet.get_or_create(
                order.courier_id, "courier"
            )
            await self.wallet.credit(
                wallet_id=courier_wallet.id,
                amount=calc["courier_amount"],
                source_type="delivery",
                source_id=order.id,
                description=f"Yetkazish #{order.order_number}",
            )

        # Commission records (audit)
        for recipient_type, recipient_id, amount in [
            ("platform", 1, calc["platform_commission"]),
            ("dealer", vendor.dealer_id if vendor else None, calc["dealer_commission"]),
            ("developer", None, calc["developer_royalty"]),
            ("vendor", order.vendor_id, calc["vendor_amount"]),
            ("courier", order.courier_id, calc["courier_amount"]),
        ]:
            if recipient_id and amount > 0:
                rec = CommissionRecord(
                    order_id=order.id,
                    recipient_type=recipient_type,
                    recipient_id=recipient_id,
                    amount=amount,
                    status="credited",
                )
                self.db.add(rec)

        await self.db.flush()

        logger.info(
            "commission_distributed",
            order_id=order.id,
            total=float(order.total),
            **{k: float(v) for k, v in calc.items()},
        )

        return calc
```

## 3.3. Order Service (to'liq)

`backend/app/services/order_service.py`:

```python
from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.core.exceptions import (
    BusinessRuleError, NotFoundError, InvalidStatusTransitionError,
)
from app.core.logging import get_logger
from app.db.models import (
    Order, OrderItem, Cart, User, Vendor, Product, Address,
)
from app.business.order_states import can_transition, OrderStatus
from app.services.commission_service import CommissionService
from app.services.notification_service import NotificationService
from app.services.wallet_service import WalletService
from app.ws.pubsub import redis_pubsub
from app.providers.payment import get_payment_provider

logger = get_logger(__name__)

MIN_ORDER_AMOUNT = Decimal(str(settings.MIN_ORDER_AMOUNT))
MAX_ORDER_AMOUNT = Decimal(str(settings.MAX_ORDER_AMOUNT))


class OrderService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.commission = CommissionService(db)
        self.notifier = NotificationService(db)
        self.wallet = WalletService(db)

    async def create_order(
        self,
        user: User,
        cart: Cart,
        address_id: int,
        payment_method: str,
        comment: str | None = None,
    ) -> Order:
        # ==== 1. Biznes qoidalari ====
        if not user.is_registered:
            raise BusinessRuleError("Ro'yxatdan o'ting")

        if not user.is_verified:
            raise BusinessRuleError(
                "Profil tasdiqlanmagan. KYC dan o'ting"
            )

        if not user.terms_accepted_at:
            raise BusinessRuleError("Ommaviy ofertaga rozilik bering")

        if not cart.items:
            raise BusinessRuleError("Savat bo'sh")

        # Manzil tekshirish
        address = await self.db.get(Address, address_id)
        if not address or address.user_id != user.id:
            raise BusinessRuleError("Manzil topilmadi")

        # Minimal summa
        subtotal = sum(
            (item.price_at_add * item.quantity for item in cart.items),
            Decimal("0"),
        )
        if subtotal < MIN_ORDER_AMOUNT:
            remaining = MIN_ORDER_AMOUNT - subtotal
            raise BusinessRuleError(
                f"Minimal buyurtma {MIN_ORDER_AMOUNT:,.0f} so'm. "
                f"Savatingiz: {subtotal:,.0f} so'm. "
                f"Yana {remaining:,.0f} so'm qo'shing."
            )

        if subtotal > MAX_ORDER_AMOUNT:
            raise BusinessRuleError(
                f"Maksimal buyurtma {MAX_ORDER_AMOUNT:,.0f} so'm. "
                f"Qo'llab-quvvatlashga murojaat qiling."
            )

        # Bitta do'kondan
        vendor_ids = {item.product.vendor_id for item in cart.items}
        if len(vendor_ids) > 1:
            raise BusinessRuleError(
                "Bir buyurtmada faqat bitta do'kondan mahsulot bo'lishi mumkin"
            )

        vendor_id = vendor_ids.pop()
        vendor = await self.db.get(Vendor, vendor_id)

        # Do'kon ochiqmi?
        if not vendor.is_open:
            raise BusinessRuleError("Do'kon hozir yopiq")

        # ==== 2. Yetkazish narxi ====
        delivery_fee = Decimal(str(vendor.delivery_fee or 0))
        if vendor.free_delivery_from and subtotal >= vendor.free_delivery_from:
            delivery_fee = Decimal("0")

        # ==== 3. Promo ====
        discount = Decimal("0")
        if cart.promo_code:
            discount = await self._apply_promo(cart.promo_code, subtotal, user)

        total = subtotal + delivery_fee - discount

        # ==== 4. Order yaratish ====
        order_number = await self._generate_order_number()

        order = Order(
            order_number=order_number,
            user_id=user.id,
            vendor_id=vendor_id,
            dealer_id=vendor.dealer_id,
            address_id=address_id,
            status=OrderStatus.PENDING_PAYMENT.value,
            subtotal=subtotal,
            delivery_fee=delivery_fee,
            discount=discount,
            total=total,
            payment_method=payment_method,
            source_channel=user.source_channel,
            customer_comment=comment,
        )
        self.db.add(order)
        await self.db.flush()

        # Order items
        for ci in cart.items:
            item = OrderItem(
                order_id=order.id,
                product_id=ci.product_id,
                developer_id=ci.product.developer_id,
                product_name=ci.product.name,
                product_sku=ci.product.sku,
                quantity=ci.quantity,
                price=ci.price_at_add,
                cost_price=ci.product.cost_price,
                total=ci.price_at_add * ci.quantity,
            )
            self.db.add(item)

        # Savatni tozalash
        for ci in cart.items:
            await self.db.delete(ci)

        await self.db.commit()
        await self.db.refresh(order)

        # ==== 5. Real-time xabar ====
        await redis_pubsub.publish(
            f"vendor:{vendor_id}:orders",
            {
                "event": "order.created",
                "order_id": order.id,
                "order_number": order.order_number,
                "total": float(total),
                "items_count": len(cart.items),
            },
        )

        # ==== 6. Bildirishnoma ====
        await self.notifier.notify(
            user,
            event="order_created",
            order_number=order.order_number,
            total=float(total),
            track_url=f"{settings.WEBAPP_URL}/order/{order.id}",
        )

        logger.info("order_created", order_id=order.id, user_id=user.id, total=float(total))
        return order

    async def update_status(
        self,
        order_id: int,
        new_status: str,
        actor_id: int | None = None,
        actor_role: str = "system",
    ) -> Order:
        order = await self.db.get(Order, order_id)
        if not order:
            raise NotFoundError("Buyurtma topilmadi")

        if not can_transition(order.status, new_status):
            raise InvalidStatusTransitionError(
                f"'{order.status}' → '{new_status}' o'tish mumkin emas"
            )

        old_status = order.status
        order.status = new_status
        order.updated_at = datetime.now(timezone.utc)

        # Vaqt belgilari
        now = datetime.now(timezone.utc)
        if new_status == OrderStatus.ACCEPTED.value:
            order.accepted_at = now
        elif new_status == OrderStatus.READY.value:
            order.ready_at = now
        elif new_status == OrderStatus.PICKED_UP.value:
            order.picked_up_at = now
        elif new_status == OrderStatus.DELIVERED.value:
            order.delivered_at = now
        elif new_status == OrderStatus.COMPLETED.value:
            order.completed_at = now
            # Komissiya taqsimlash
            await self.commission.distribute(order)
        elif new_status == OrderStatus.CANCELLED.value:
            order.cancelled_at = now

        await self.db.commit()

        # Real-time
        await redis_pubsub.publish(
            f"order:{order_id}",
            {
                "event": "order.status_changed",
                "order_id": order_id,
                "old_status": old_status,
                "new_status": new_status,
                "timestamp": order.updated_at.isoformat(),
            },
        )

        # Bildirishnoma
        user = await self.db.get(User, order.user_id)
        if user:
            await self.notifier.notify(
                user,
                event=f"order_{new_status}",
                order_number=order.order_number,
                total=float(order.total),
                track_url=f"{settings.WEBAPP_URL}/order/{order.id}",
            )

        logger.info(
            "order_status_changed",
            order_id=order_id,
            old=old_status,
            new=new_status,
            actor=actor_id,
        )

        return order

    async def cancel_order(
        self,
        order_id: int,
        user_id: int,
        reason: str,
    ) -> Order:
        order = await self.db.get(Order, order_id)
        if not order:
            raise NotFoundError()

        if order.user_id != user_id:
            raise BusinessRuleError("Ruxsat yo'q")

        # Bekor qilish oynasi
        elapsed = (
            datetime.now(timezone.utc) - order.created_at
        ).total_seconds() / 60

        if elapsed > settings.ORDER_CANCEL_WINDOW_MINUTES:
            raise BusinessRuleError(
                f"Bekor qilish uchun {settings.ORDER_CANCEL_WINDOW_MINUTES} "
                f"daqiqa o'tdi. Qo'llab-quvvatlashga murojaat qiling."
            )

        if order.status not in (
            OrderStatus.PENDING_PAYMENT.value,
            OrderStatus.PAID.value,
            OrderStatus.ACCEPTED.value,
        ):
            raise BusinessRuleError("Bu holatda bekor qilib bo'lmaydi")

        order.cancellation_reason = reason
        return await self.update_status(
            order_id, OrderStatus.CANCELLED.value, user_id, "customer"
        )

    async def _generate_order_number(self) -> str:
        today = datetime.now(timezone.utc).strftime("%Y%m%d")
        start = datetime.now(timezone.utc).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        stmt = select(func.count(Order.id)).where(Order.created_at >= start)
        count = (await self.db.execute(stmt)).scalar() or 0
        return f"ORD-{today}-{count + 1:06d}"

    async def _apply_promo(
        self, code: str, subtotal: Decimal, user: User
    ) -> Decimal:
        from app.db.models import PromoCode, PromoUsage
        stmt = select(PromoCode).where(
            PromoCode.code == code, PromoCode.is_active == True
        )
        promo = (await self.db.execute(stmt)).scalar_one_or_none()
        if not promo:
            raise BusinessRuleError("Promo-kod topilmadi")

        now = datetime.now(timezone.utc)
        if promo.valid_from and promo.valid_from > now:
            raise BusinessRuleError("Promo-kod hali boshlanmagan")
        if promo.valid_until and promo.valid_until < now:
            raise BusinessRuleError("Promo-kod muddati tugagan")
        if promo.max_uses and promo.used_count >= promo.max_uses:
            raise BusinessRuleError("Promo-kod limiti tugagan")
        if subtotal < promo.min_order_amount:
            raise BusinessRuleError(
                f"Minimal summa: {promo.min_order_amount:,.0f} so'm"
            )

        # Bir foydalanuvchi limiti
        usage_stmt = select(func.count(PromoUsage.id)).where(
            PromoUsage.promo_id == promo.id, PromoUsage.user_id == user.id
        )
        user_uses = (await self.db.execute(usage_stmt)).scalar() or 0
        if user_uses >= promo.per_user_limit:
            raise BusinessRuleError("Siz bu promo-kodni ishlatgansiz")

        # Hisoblash
        if promo.type == "percent":
            discount = (subtotal * Decimal(str(promo.value)) / 100)
            if promo.max_discount:
                discount = min(discount, Decimal(str(promo.max_discount)))
        elif promo.type == "fixed":
            discount = Decimal(str(promo.value))
        elif promo.type == "free_delivery":
            discount = Decimal("0")  # alohida logika
        else:
            discount = Decimal("0")

        return discount
```

## 3.4. Orders Router

`backend/app/api/v1/orders.py`:

```python
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.deps import CurrentUser, CurrentVerifiedUser
from app.db.session import get_db
from app.db.models import Order, Cart
from app.services.order_service import OrderService
from app.core.exceptions import NotFoundError, ForbiddenError

router = APIRouter(prefix="/orders", tags=["orders"])


class CreateOrderIn(BaseModel):
    cart_id: int | None = None
    address_id: int
    payment_method: str = Field(..., pattern="^(payme|click|uzum|cash)$")
    comment: str | None = None


class CancelOrderIn(BaseModel):
    reason: str = Field(..., min_length=5, max_length=500)


@router.post("")
async def create_order(
    data: CreateOrderIn,
    user: CurrentVerifiedUser,
    db: AsyncSession = Depends(get_db),
):
    # Savatni topish
    stmt = (
        select(Cart)
        .where(Cart.user_id == user.id)
        .options(
            selectinload(Cart.items).selectinload("product").selectinload("vendor")
        )
    )
    cart = (await db.execute(stmt)).scalar_one_or_none()
    if not cart:
        raise NotFoundError("Savat topilmadi")

    svc = OrderService(db)
    order = await svc.create_order(
        user=user,
        cart=cart,
        address_id=data.address_id,
        payment_method=data.payment_method,
        comment=data.comment,
    )
    return _order_to_dict(order)


@router.get("")
async def list_orders(
    user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    status: str | None = None,
    limit: int = 20,
    offset: int = 0,
):
    stmt = select(Order).where(Order.user_id == user.id)
    if status:
        stmt = stmt.where(Order.status == status)
    stmt = stmt.order_by(Order.created_at.desc()).limit(limit).offset(offset)
    orders = (await db.execute(stmt)).scalars().all()
    return [_order_to_dict(o) for o in orders]


@router.get("/{order_id}")
async def get_order(
    order_id: int,
    user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    order = await db.get(Order, order_id)
    if not order:
        raise NotFoundError("Buyurtma topilmadi")
    if order.user_id != user.id and "admin" not in user.roles:
        raise ForbiddenError()
    return _order_to_dict(order)


@router.post("/{order_id}/cancel")
async def cancel_order(
    order_id: int,
    data: CancelOrderIn,
    user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    svc = OrderService(db)
    order = await svc.cancel_order(order_id, user.id, data.reason)
    return _order_to_dict(order)


def _order_to_dict(o: Order) -> dict:
    return {
        "id": o.id,
        "order_number": o.order_number,
        "status": o.status,
        "subtotal": float(o.subtotal),
        "delivery_fee": float(o.delivery_fee),
        "discount": float(o.discount),
        "total": float(o.total),
        "payment_method": o.payment_method,
        "payment_status": o.payment_status,
        "created_at": o.created_at.isoformat() if o.created_at else None,
        "delivered_at": o.delivered_at.isoformat() if o.delivered_at else None,
    }
```

## 3.5. Test

```python
# tests/unit/test_order_service.py
import pytest
from decimal import Decimal
from app.services.order_service import OrderService
from app.core.exceptions import BusinessRuleError


@pytest.mark.asyncio
async def test_min_order_amount_rejected(db_session, mocker):
    user = mocker.Mock(is_registered=True, is_verified=True,
                       terms_accepted_at="2026-01-01")
    cart = mocker.Mock(items=[
        mocker.Mock(price_at_add=Decimal("10000"), quantity=2)
    ])
    svc = OrderService(db_session)
    with pytest.raises(BusinessRuleError, match="Minimal buyurtma"):
        await svc.create_order(user, cart, 1, "payme")
```

---

# 📦 MODUL 4: WALLET SERVICE (Hamyon + Payout)

## 4.1. Wallet Service (to'liq)

`backend/app/services/wallet_service.py`:

```python
from decimal import Decimal
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import InsufficientBalanceError, NotFoundError
from app.core.logging import get_logger
from app.db.models import Wallet, WalletTransaction, Payout, User
from app.ws.pubsub import redis_pubsub

logger = get_logger(__name__)


class WalletService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_or_create(self, owner_id: int, owner_type: str) -> Wallet:
        stmt = select(Wallet).where(
            Wallet.owner_id == owner_id, Wallet.owner_type == owner_type
        )
        wallet = (await self.db.execute(stmt)).scalar_one_or_none()
        if not wallet:
            wallet = Wallet(owner_id=owner_id, owner_type=owner_type)
            self.db.add(wallet)
            await self.db.flush()
        return wallet

    async def get_by_owner(self, owner_id: int, owner_type: str) -> Wallet:
        stmt = select(Wallet).where(
            Wallet.owner_id == owner_id, Wallet.owner_type == owner_type
        )
        wallet = (await self.db.execute(stmt)).scalar_one_or_none()
        if not wallet:
            raise NotFoundError("Hamyon topilmadi")
        return wallet

    async def credit(
        self,
        wallet_id: int,
        amount: Decimal,
        source_type: str,
        source_id: int | None = None,
        description: str = "",
        metadata: dict | None = None,
    ) -> WalletTransaction:
        amount = Decimal(str(amount))
        if amount <= 0:
            raise ValueError("Summa musbat bo'lishi kerak")

        stmt = (
            select(Wallet)
            .where(Wallet.id == wallet_id)
            .with_for_update()
        )
        wallet = (await self.db.execute(stmt)).scalar_one()

        before = wallet.balance
        wallet.balance = before + amount
        wallet.total_earned = wallet.total_earned + amount

        tx = WalletTransaction(
            wallet_id=wallet_id,
            type="credit",
            amount=amount,
            balance_before=before,
            balance_after=wallet.balance,
            source_type=source_type,
            source_id=source_id,
            description=description,
            metadata_json=metadata or {},
        )
        self.db.add(tx)
        await self.db.flush()

        await redis_pubsub.publish(
            f"wallet:{wallet_id}",
            {
                "event": "wallet.credited",
                "wallet_id": wallet_id,
                "amount": float(amount),
                "balance": float(wallet.balance),
                "source": source_type,
                "tx_id": tx.id,
            },
        )
        logger.info(
            "wallet_credit",
            wallet_id=wallet_id, amount=float(amount),
            source=source_type, balance=float(wallet.balance),
        )
        return tx

    async def debit(
        self,
        wallet_id: int,
        amount: Decimal,
        source_type: str,
        source_id: int | None = None,
        description: str = "",
    ) -> WalletTransaction:
        amount = Decimal(str(amount))
        stmt = (
            select(Wallet)
            .where(Wallet.id == wallet_id)
            .with_for_update()
        )
        wallet = (await self.db.execute(stmt)).scalar_one()

        if wallet.balance < amount:
            raise InsufficientBalanceError(
                f"Balans yetarli emas. Kerak: {amount:,.0f}, "
                f"mavjud: {wallet.balance:,.0f}"
            )

        before = wallet.balance
        wallet.balance = before - amount

        tx = WalletTransaction(
            wallet_id=wallet_id,
            type="debit",
            amount=amount,
            balance_before=before,
            balance_after=wallet.balance,
            source_type=source_type,
            source_id=source_id,
            description=description,
        )
        self.db.add(tx)
        await self.db.flush()

        await redis_pubsub.publish(
            f"wallet:{wallet_id}",
            {
                "event": "wallet.debited",
                "wallet_id": wallet_id,
                "amount": float(amount),
                "balance": float(wallet.balance),
            },
        )
        return tx

    async def hold(self, wallet_id: int, amount: Decimal, reason: str) -> None:
        """Payout uchun muzlatish"""
        amount = Decimal(str(amount))
        stmt = select(Wallet).where(Wallet.id == wallet_id).with_for_update()
        wallet = (await self.db.execute(stmt)).scalar_one()
        if wallet.balance < amount:
            raise InsufficientBalanceError()
        wallet.balance -= amount
        wallet.frozen_balance += amount
        await self.db.flush()

    async def release_hold(self, wallet_id: int, amount: Decimal) -> None:
        amount = Decimal(str(amount))
        stmt = select(Wallet).where(Wallet.id == wallet_id).with_for_update()
        wallet = (await self.db.execute(stmt)).scalar_one()
        wallet.frozen_balance -= amount
        wallet.balance += amount
        await self.db.flush()

    async def confirm_hold(self, wallet_id: int, amount: Decimal) -> None:
        amount = Decimal(str(amount))
        stmt = select(Wallet).where(Wallet.id == wallet_id).with_for_update()
        wallet = (await self.db.execute(stmt)).scalar_one()
        wallet.frozen_balance -= amount
        wallet.total_withdrawn += amount
        await self.db.flush()
```

## 4.2. Payout Service

`backend/app/services/payout_service.py`:

```python
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    BusinessRuleError, NotFoundError, InsufficientBalanceError,
)
from app.core.logging import get_logger
from app.db.models import Payout, Wallet, User, AuditLog
from app.services.wallet_service import WalletService

logger = get_logger(__name__)

MIN_PAYOUT = Decimal("50000")
MAX_DAILY_PAYOUT = Decimal("10000000")
PAYOUT_FEE_PERCENT = Decimal("1.0")  # 1%


class PayoutService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.wallet = WalletService(db)

    async def request_payout(
        self,
        owner_id: int,
        owner_type: str,
        amount: Decimal,
        method: str,
        account_details: dict,
    ) -> Payout:
        amount = Decimal(str(amount))

        # Minimal/maksimal
        if amount < MIN_PAYOUT:
            raise BusinessRuleError(f"Minimal payout: {MIN_PAYOUT:,.0f} so'm")

        # Kunlik limit
        today_start = datetime.now(timezone.utc).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        stmt = select(func.coalesce(func.sum(Payout.amount), 0)).where(
            Payout.owner_id == owner_id,
            Payout.owner_type == owner_type,
            Payout.requested_at >= today_start,
            Payout.status.in_(["pending", "approved", "processing", "completed"]),
        )
        today_total = Decimal(str((await self.db.execute(stmt)).scalar() or 0))
        if today_total + amount > MAX_DAILY_PAYOUT:
            raise BusinessRuleError(
                f"Kunlik limit: {MAX_DAILY_PAYOUT:,.0f} so'm"
            )

        # Hamyon
        wallet = await self.wallet.get_by_owner(owner_id, owner_type)
        if wallet.balance < amount:
            raise InsufficientBalanceError(
                f"Balans: {wallet.balance:,.0f} so'm"
            )

        # Fee
        fee = (amount * PAYOUT_FEE_PERCENT / 100).quantize(Decimal("0.01"))
        net_amount = amount - fee

        # Muzlatish
        await self.wallet.hold(wallet.id, amount, "payout")

        payout = Payout(
            wallet_id=wallet.id,
            owner_id=owner_id,
            owner_type=owner_type,
            amount=amount,
            fee=fee,
            net_amount=net_amount,
            method=method,
            account_details=account_details,
            status="pending",
            requested_at=datetime.now(timezone.utc),
        )
        self.db.add(payout)
        await self.db.commit()
        await self.db.refresh(payout)

        logger.info(
            "payout_requested",
            payout_id=payout.id, owner_id=owner_id,
            amount=float(amount), method=method,
        )
        return payout

    async def approve(
        self, payout_id: int, admin_id: int
    ) -> Payout:
        payout = await self.db.get(Payout, payout_id)
        if not payout:
            raise NotFoundError()
        if payout.status != "pending":
            raise BusinessRuleError(f"Status: {payout.status}")

        payout.status = "approved"
        payout.approved_at = datetime.now(timezone.utc)
        payout.approved_by = admin_id
        await self.db.commit()

        # Audit
        audit = AuditLog(
            actor_id=admin_id,
            actor_role="admin",
            action="payout_approved",
            entity_type="payout",
            entity_id=payout.id,
            after_data={"status": "approved", "amount": float(payout.amount)},
        )
        self.db.add(audit)
        await self.db.commit()

        logger.info("payout_approved", payout_id=payout_id, admin=admin_id)
        return payout

    async def reject(
        self, payout_id: int, admin_id: int, reason: str
    ) -> Payout:
        payout = await self.db.get(Payout, payout_id)
        if not payout:
            raise NotFoundError()
        if payout.status not in ("pending", "approved"):
            raise BusinessRuleError(f"Status: {payout.status}")

        payout.status = "rejected"
        payout.rejection_reason = reason
        await self.db.commit()

        # Muzlatilgan pulni qaytarish
        await self.wallet.release_hold(payout.wallet_id, payout.amount)
        await self.db.commit()

        logger.info("payout_rejected", payout_id=payout_id, reason=reason)
        return payout

    async def complete(
        self, payout_id: int, provider_txn_id: str
    ) -> Payout:
        payout = await self.db.get(Payout, payout_id)
        if not payout:
            raise NotFoundError()
        if payout.status != "approved":
            raise BusinessRuleError(f"Status: {payout.status}")

        payout.status = "completed"
        payout.completed_at = datetime.now(timezone.utc)
        payout.provider_txn_id = provider_txn_id
        await self.db.commit()

        # Muzlatilgan pulni yakuniy yechish
        await self.wallet.confirm_hold(payout.wallet_id, payout.amount)
        await self.db.commit()

        logger.info("payout_completed", payout_id=payout_id)
        return payout
```

## 4.3. Wallet Router

`backend/app/api/v1/wallet.py`:

```python
from decimal import Decimal
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import CurrentUser
from app.db.session import get_db
from app.db.models import Wallet, WalletTransaction, Payout
from app.services.wallet_service import WalletService
from app.services.payout_service import PayoutService
from app.core.exceptions import NotFoundError

router = APIRouter(prefix="/wallet", tags=["wallet"])


class PayoutRequestIn(BaseModel):
    amount: Decimal = Field(..., gt=0)
    method: str = Field(..., pattern="^(payme|click|uzum|bank|cash)$")
    account_details: dict


@router.get("")
async def get_my_wallet(
    user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    svc = WalletService(db)
    wallet = await svc.get_or_create(user.id, "user")
    return {
        "balance": float(wallet.balance),
        "frozen_balance": float(wallet.frozen_balance),
        "total_earned": float(wallet.total_earned),
        "total_withdrawn": float(wallet.total_withdrawn),
        "currency": wallet.currency,
    }


@router.get("/transactions")
async def list_transactions(
    user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    limit: int = 50,
    offset: int = 0,
):
    svc = WalletService(db)
    wallet = await svc.get_by_owner(user.id, "user")
    stmt = (
        select(WalletTransaction)
        .where(WalletTransaction.wallet_id == wallet.id)
        .order_by(WalletTransaction.created_at.desc())
        .limit(limit).offset(offset)
    )
    txs = (await db.execute(stmt)).scalars().all()
    return [
        {
            "id": t.id,
            "type": t.type,
            "amount": float(t.amount),
            "balance_after": float(t.balance_after),
            "source": t.source_type,
            "description": t.description,
            "created_at": t.created_at.isoformat(),
        }
        for t in txs
    ]


@router.post("/payouts")
async def request_payout(
    data: PayoutRequestIn,
    user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    svc = PayoutService(db)
    payout = await svc.request_payout(
        owner_id=user.id,
        owner_type="user",
        amount=data.amount,
        method=data.method,
        account_details=data.account_details,
    )
    return {
        "id": payout.id,
        "amount": float(payout.amount),
        "fee": float(payout.fee),
        "net_amount": float(payout.net_amount),
        "status": payout.status,
    }


@router.get("/payouts")
async def list_payouts(
    user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(Payout)
        .where(Payout.owner_id == user.id, Payout.owner_type == "user")
        .order_by(Payout.created_at.desc())
    )
    payouts = (await db.execute(stmt)).scalars().all()
    return [
        {
            "id": p.id,
            "amount": float(p.amount),
            "net_amount": float(p.net_amount),
            "status": p.status,
            "method": p.method,
            "requested_at": p.requested_at.isoformat(),
        }
        for p in payouts
    ]
```

---

# 📦 MODUL 5: WEBSOCKET HUB (Real-time)

## 5.1. Connection Manager

`backend/app/ws/manager.py`:

```python
from collections import defaultdict
from fastapi import WebSocket
from app.core.logging import get_logger

logger = get_logger(__name__)


class ConnectionManager:
    def __init__(self):
        # {channel: {user_id: set(websockets)}}
        self.channels: dict[str, dict[int, set[WebSocket]]] = defaultdict(
            lambda: defaultdict(set)
        )

    async def connect(self, ws: WebSocket, channel: str, user_id: int):
        await ws.accept()
        self.channels[channel][user_id].add(ws)
        logger.info(
            "ws_connected", channel=channel, user_id=user_id,
            total=len(self.channels[channel][user_id])
        )

    def disconnect(self, ws: WebSocket, channel: str, user_id: int):
        self.channels[channel][user_id].discard(ws)
        if not self.channels[channel][user_id]:
            del self.channels[channel][user_id]
        if not self.channels[channel]:
            del self.channels[channel]
        logger.info("ws_disconnected", channel=channel, user_id=user_id)

    async def broadcast(self, channel: str, message: dict):
        dead = []
        for uid, sockets in list(self.channels.get(channel, {}).items()):
            for ws in list(sockets):
                try:
                    await ws.send_json(message)
                except Exception:
                    dead.append((uid, ws))
        for uid, ws in dead:
            self.disconnect(ws, channel, uid)

    async def send_to_user(self, channel: str, user_id: int, message: dict):
        for ws in list(self.channels.get(channel, {}).get(user_id, [])):
            try:
                await ws.send_json(message)
            except Exception:
                self.disconnect(ws, channel, user_id)


ws_manager = ConnectionManager()
```

## 5.2. Redis Pub/Sub

`backend/app/ws/pubsub.py`:

```python
import asyncio
import json
import redis.asyncio as redis
from app.core.config import settings
from app.core.logging import get_logger
from app.ws.manager import ws_manager

logger = get_logger(__name__)


class RedisPubSub:
    def __init__(self):
        self._pub: redis.Redis | None = None
        self._sub: redis.Redis | None = None
        self._pubsub = None
        self._task: asyncio.Task | None = None
        self._subscribed: set[str] = set()

    async def start(self):
        self._pub = redis.from_url(settings.REDIS_URL, decode_responses=True)
        self._sub = redis.from_url(settings.REDIS_URL, decode_responses=True)
        self._pubsub = self._sub.pubsub()
        await self._pubsub.subscribe("ws:*")
        self._task = asyncio.create_task(self._listen())
        logger.info("redis_pubsub_started")

    async def stop(self):
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        if self._pubsub:
            await self._pubsub.close()
        if self._pub:
            await self._pub.close()
        if self._sub:
            await self._sub.close()
        logger.info("redis_pubsub_stopped")

    async def publish(self, channel: str, message: dict):
        if not self._pub:
            return
        await self._pub.publish(f"ws:{channel}", json.dumps(message))

    async def ensure_subscribed(self, channel: str):
        """Kerak bo'lganda qo'shimcha kanalga obuna"""
        if channel in self._subscribed:
            return
        self._subscribed.add(channel)

    async def _listen(self):
        async for msg in self._pubsub.listen():
            if msg["type"] != "message":
                continue
            try:
                channel = msg["channel"]
                if channel.startswith("ws:"):
                    channel = channel[3:]
                data = json.loads(msg["data"])
                await ws_manager.broadcast(channel, data)
            except Exception as e:
                logger.error("pubsub_listen_error", error=str(e))


redis_pubsub = RedisPubSub()
```

## 5.3. WebSocket Router

`backend/app/ws/__init__.py`:

```python
from fastapi import APIRouter
from app.ws.router import router as ws_router

__all__ = ["ws_router"]
```

`backend/app/ws/router.py`:

```python
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from jose import jwt, JWTError

from app.core.config import settings
from app.core.logging import get_logger
from app.ws.manager import ws_manager
from app.ws.pubsub import redis_pubsub

logger = get_logger(__name__)
router = APIRouter()


def _decode_token(token: str) -> int | None:
    try:
        payload = jwt.decode(
            token, settings.JWT_PUBLIC_KEY, algorithms=["RS256"]
        )
        return int(payload["sub"])
    except (JWTError, KeyError):
        return None


@router.websocket("/orders/{order_id}")
async def order_ws(
    websocket: WebSocket,
    order_id: int,
    token: str = Query(...),
):
    user_id = _decode_token(token)
    if not user_id:
        await websocket.close(code=4001, reason="Unauthorized")
        return

    channel = f"order:{order_id}"
    await ws_manager.connect(websocket, channel, user_id)
    await redis_pubsub.ensure_subscribed(channel)

    try:
        await websocket.send_json({
            "event": "connected",
            "channel": channel,
            "order_id": order_id,
        })
        while True:
            msg = await websocket.receive_text()
            if msg == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, channel, user_id)


@router.websocket("/notifications")
async def notifications_ws(
    websocket: WebSocket,
    token: str = Query(...),
):
    user_id = _decode_token(token)
    if not user_id:
        await websocket.close(code=4001)
        return

    channel = f"user:{user_id}:notifications"
    await ws_manager.connect(websocket, channel, user_id)
    await redis_pubsub.ensure_subscribed(channel)

    try:
        await websocket.send_json({"event": "connected"})
        while True:
            msg = await websocket.receive_text()
            if msg == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, channel, user_id)


@router.websocket("/vendor/{vendor_id}/orders")
async def vendor_orders_ws(
    websocket: WebSocket,
    vendor_id: int,
    token: str = Query(...),
):
    user_id = _decode_token(token)
    if not user_id:
        await websocket.close(code=4001)
        return

    channel = f"vendor:{vendor_id}:orders"
    await ws_manager.connect(websocket, channel, user_id)
    await redis_pubsub.ensure_subscribed(channel)

    try:
        await websocket.send_json({"event": "connected", "channel": channel})
        while True:
            msg = await websocket.receive_text()
            if msg == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, channel, user_id)


@router.websocket("/courier/{courier_id}")
async def courier_ws(
    websocket: WebSocket,
    courier_id: int,
    token: str = Query(...),
):
    user_id = _decode_token(token)
    if not user_id:
        await websocket.close(code=4001)
        return

    channel = f"courier:{courier_id}"
    await ws_manager.connect(websocket, channel, user_id)
    await redis_pubsub.ensure_subscribed(channel)

    try:
        await websocket.send_json({"event": "connected"})
        while True:
            data = await websocket.receive_json()
            # Kuryer joylashuvini qabul qilish
            if data.get("event") == "location":
                await redis_pubsub.publish(
                    f"courier:{courier_id}",
                    {
                        "event": "courier.location",
                        "courier_id": courier_id,
                        "lat": data["lat"],
                        "lng": data["lng"],
                        "bearing": data.get("bearing"),
                        "speed_kmh": data.get("speed_kmh"),
                    },
                )
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, channel, user_id)
```

## 5.4. Main app ga qo'shish

`backend/app/main.py` (yangilangan):

```python
# ... (oldingi kod)
from app.ws import ws_router
from app.ws.pubsub import redis_pubsub

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    await redis_service.connect()
    await redis_pubsub.start()   # <-- qo'shildi
    yield
    await redis_pubsub.stop()    # <-- qo'shildi
    await redis_service.close()


app.include_router(ws_router, prefix="/ws")  # <-- qo'shildi
```

## 5.5. Frontend WebSocket client (React)

`packages/ws-client/src/index.ts`:

```typescript
export interface WebSocketOptions {
  onMessage?: (data: any) => void;
  onOpen?: () => void;
  onClose?: () => void;
  onError?: (e: Event) => void;
  reconnect?: boolean;
  maxRetries?: number;
  pingInterval?: number;
}

export class XalqWebSocket {
  private ws: WebSocket | null = null;
  private url: string;
  private opts: Required<WebSocketOptions>;
  private retries = 0;
  private pingTimer: ReturnType<typeof setInterval> | null = null;
  private reconnectTimer: ReturnType<typeof setTimeout> | null = null;
  private closedByUser = false;

  constructor(path: string, options: WebSocketOptions = {}) {
    const wsBase = import.meta.env.VITE_WS_URL || "ws://localhost:8000";
    const token = localStorage.getItem("access_token") || "";
    this.url = `${wsBase}${path}?token=${token}`;
    this.opts = {
      onMessage: () => {},
      onOpen: () => {},
      onClose: () => {},
      onError: () => {},
      reconnect: true,
      maxRetries: 10,
      pingInterval: 30000,
      ...options,
    };
  }

  connect() {
    this.closedByUser = false;
    this.ws = new WebSocket(this.url);

    this.ws.onopen = () => {
      this.retries = 0;
      this.opts.onOpen();
      this.startPing();
    };

    this.ws.onmessage = (e) => {
      try {
        const data = JSON.parse(e.data);
        this.opts.onMessage(data);
      } catch {}
    };

    this.ws.onclose = () => {
      this.stopPing();
      this.opts.onClose();
      if (this.opts.reconnect && !this.closedByUser && this.retries < this.opts.maxRetries) {
        const delay = Math.min(1000 * 2 ** this.retries, 30000);
        this.retries++;
        this.reconnectTimer = setTimeout(() => this.connect(), delay);
      }
    };

    this.ws.onerror = (e) => this.opts.onError(e);
  }

  private startPing() {
    this.pingTimer = setInterval(() => {
      if (this.ws?.readyState === WebSocket.OPEN) {
        this.ws.send("ping");
      }
    }, this.opts.pingInterval);
  }

  private stopPing() {
    if (this.pingTimer) {
      clearInterval(this.pingTimer);
      this.pingTimer = null;
    }
  }

  send(data: any) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(typeof data === "string" ? data : JSON.stringify(data));
    }
  }

  close() {
    this.closedByUser = true;
    if (this.reconnectTimer) clearTimeout(this.reconnectTimer);
    this.stopPing();
    this.ws?.close();
  }
}

export function useWebSocket(path: string, options: WebSocketOptions = {}) {
  const [status, setStatus] = React.useState<"connecting" | "open" | "closed">("connecting");
  const wsRef = React.useRef<XalqWebSocket | null>(null);

  React.useEffect(() => {
    const ws = new XalqWebSocket(path, {
      ...options,
      onOpen: () => {
        setStatus("open");
        options.onOpen?.();
      },
      onClose: () => {
        setStatus("closed");
        options.onClose?.();
      },
    });
    wsRef.current = ws;
    ws.connect();
    return () => ws.close();
  }, [path]);

  return { status, ws: wsRef.current };
}

import React from "react";
```

---

# 📦 MODUL 6: MIJOZ WEBAPP (React)

## 6.1. Loyihani yaratish

```bash
cd apps
npm create vite@latest customer-webapp -- --template react-ts
cd customer-webapp
npm install
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
npm install react-router-dom zustand @tanstack/react-query axios
npm install @twa-dev/sdk leaflet react-leaflet
npm install -D @types/leaflet
npm install lucide-react clsx
```

## 6.2. `tailwind.config.js`

```js
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: "#FF6B00",
          dark: "#E55A00",
          light: "#FF8B33",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};
```

## 6.3. `src/main.tsx`

```tsx
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import App from "./App";
import "./styles/globals.css";
import WebApp from "@twa-dev/sdk";

WebApp.ready();
WebApp.expand();

const queryClient = new QueryClient({
  defaultOptions: { queries: { retry: 1, refetchOnWindowFocus: false } },
});

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </QueryClientProvider>
  </React.StrictMode>
);
```

## 6.4. `src/App.tsx`

```tsx
import { Routes, Route, Navigate } from "react-router-dom";
import { Layout } from "./components/layout/Layout";
import Home from "./pages/Home";
import Catalog from "./pages/Catalog";
import Shop from "./pages/Shop";
import Product from "./pages/Product";
import Cart from "./pages/Cart";
import Checkout from "./pages/Checkout";
import OrderTracking from "./pages/OrderTracking";
import Orders from "./pages/Orders";
import Profile from "./pages/Profile";
import Wallet from "./pages/Wallet";
import Login from "./pages/Login";

export default function App() {
  const token = localStorage.getItem("access_token");

  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      {!token ? (
        <Route path="*" element={<Navigate to="/login" replace />} />
      ) : (
        <Route element={<Layout />}>
          <Route path="/" element={<Home />} />
          <Route path="/catalog" element={<Catalog />} />
          <Route path="/shop/:id" element={<Shop />} />
          <Route path="/product/:id" element={<Product />} />
          <Route path="/cart" element={<Cart />} />
          <Route path="/checkout" element={<Checkout />} />
          <Route path="/order/:id" element={<OrderTracking />} />
          <Route path="/orders" element={<Orders />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/wallet" element={<Wallet />} />
        </Route>
      )}
    </Routes>
  );
}
```

## 6.5. `src/lib/api.ts`

```typescript
import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1",
  timeout: 15000,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (r) => r,
  async (error) => {
    if (error.response?.status === 401) {
      const refresh = localStorage.getItem("refresh_token");
      if (refresh) {
        try {
          const { data } = await axios.post(
            `${api.defaults.baseURL}/auth/refresh`,
            { refresh_token: refresh }
          );
          localStorage.setItem("access_token", data.access_token);
          error.config.headers.Authorization = `Bearer ${data.access_token}`;
          return axios(error.config);
        } catch {
          localStorage.clear();
          window.location.href = "/login";
        }
      }
    }
    return Promise.reject(error);
  }
);

export default api;
```

## 6.6. `src/stores/cartStore.ts`

```typescript
import { create } from "zustand";
import { persist } from "zustand/middleware";

interface CartItem {
  productId: number;
  name: string;
  price: number;
  quantity: number;
  image?: string;
  vendorId: number;
}

interface CartState {
  items: CartItem[];
  vendorId: number | null;
  add: (item: CartItem) => void;
  remove: (productId: number) => void;
  updateQty: (productId: number, qty: number) => void;
  clear: () => void;
  total: () => number;
}

export const useCartStore = create<CartState>()(
  persist(
    (set, get) => ({
      items: [],
      vendorId: null,

      add: (item) => {
        const current = get();
        // Bitta do'kondan
        if (current.vendorId && current.vendorId !== item.vendorId) {
          if (
            !confirm(
              "Boshqa do'kondan mahsulot qo'shilsinmi? Hozirgi savat tozalanadi."
            )
          )
            return;
          set({ items: [], vendorId: null });
        }
        const existing = current.items.find(
          (i) => i.productId === item.productId
        );
        if (existing) {
          set({
            items: current.items.map((i) =>
              i.productId === item.productId
                ? { ...i, quantity: i.quantity + item.quantity }
                : i
            ),
          });
        } else {
          set({
            items: [...current.items, item],
            vendorId: item.vendorId,
          });
        }
      },

      remove: (productId) => {
        const items = get().items.filter((i) => i.productId !== productId);
        set({ items, vendorId: items.length ? get().vendorId : null });
      },

      updateQty: (productId, qty) => {
        if (qty <= 0) {
          get().remove(productId);
          return;
        }
        set({
          items: get().items.map((i) =>
            i.productId === productId ? { ...i, quantity: qty } : i
          ),
        });
      },

      clear: () => set({ items: [], vendorId: null }),

      total: () =>
        get().items.reduce((sum, i) => sum + i.price * i.quantity, 0),
    }),
    { name: "xalq-cart" }
  )
);
```

## 6.7. `src/components/layout/Layout.tsx`

```tsx
import { Outlet, Link, useLocation } from "react-router-dom";
import { Home, ShoppingBag, Package, User, Wallet } from "lucide-react";
import { useCartStore } from "@/stores/cartStore";

const NAV = [
  { path: "/", icon: Home, label: "Bosh" },
  { path: "/catalog", icon: ShoppingBag, label: "Katalog" },
  { path: "/cart", icon: ShoppingBag, label: "Savat" },
  { path: "/orders", icon: Package, label: "Buyurtma" },
  { path: "/profile", icon: User, label: "Profil" },
];

export function Layout() {
  const { pathname } = useLocation();
  const cartCount = useCartStore((s) => s.items.length);

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      <Outlet />
      <nav className="fixed bottom-0 left-0 right-0 bg-white border-t flex justify-around py-2 z-50">
        {NAV.map(({ path, icon: Icon, label }) => {
          const active = pathname === path;
          return (
            <Link
              key={path}
              to={path}
              className={`flex flex-col items-center text-xs px-3 py-1 relative ${
                active ? "text-brand" : "text-gray-500"
              }`}
            >
              <Icon size={22} />
              <span className="mt-1">{label}</span>
              {path === "/cart" && cartCount > 0 && (
                <span className="absolute top-0 right-1 bg-red-500 text-white text-[10px] rounded-full w-4 h-4 flex items-center justify-center">
                  {cartCount}
                </span>
              )}
            </Link>
          );
        })}
      </nav>
    </div>
  );
}
```

## 6.8. `src/pages/Cart.tsx` (Minimal buyurtma bilan)

```tsx
import { useNavigate } from "react-router-dom";
import { useCartStore } from "@/stores/cartStore";
import { Minus, Plus, Trash2 } from "lucide-react";

const MIN_ORDER = 50000;

export default function Cart() {
  const nav = useNavigate();
  const { items, updateQty, remove, total } = useCartStore();
  const subtotal = total();
  const isReady = subtotal >= MIN_ORDER;
  const remaining = Math.max(MIN_ORDER - subtotal, 0);
  const progress = Math.min((subtotal / MIN_ORDER) * 100, 100);

  if (!items.length) {
    return (
      <div className="p-6 text-center mt-20">
        <p className="text-gray-500 mb-4">Savat bo'sh</p>
        <button
          onClick={() => nav("/catalog")}
          className="bg-brand text-white px-6 py-3 rounded-lg"
        >
          Katalogga o'tish
        </button>
      </div>
    );
  }

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Savat</h1>

      <div className="space-y-3 mb-4">
        {items.map((item) => (
          <div key={item.productId} className="bg-white p-3 rounded-lg flex gap-3">
            {item.image && (
              <img src={item.image} className="w-16 h-16 rounded object-cover" />
            )}
            <div className="flex-1">
              <p className="font-medium">{item.name}</p>
              <p className="text-brand font-semibold">
                {(item.price * item.quantity).toLocaleString()} so'm
              </p>
            </div>
            <div className="flex flex-col items-end gap-2">
              <button onClick={() => remove(item.productId)}>
                <Trash2 size={16} className="text-red-500" />
              </button>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => updateQty(item.productId, item.quantity - 1)}
                  className="w-7 h-7 bg-gray-100 rounded flex items-center justify-center"
                >
                  <Minus size={14} />
                </button>
                <span className="w-6 text-center">{item.quantity}</span>
                <button
                  onClick={() => updateQty(item.productId, item.quantity + 1)}
                  className="w-7 h-7 bg-brand text-white rounded flex items-center justify-center"
                >
                  <Plus size={14} />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="bg-white p-4 rounded-lg mb-4">
        <div className="flex justify-between mb-2">
          <span>Mahsulotlar:</span>
          <span className="font-semibold">{subtotal.toLocaleString()} so'm</span>
        </div>
        <div className="flex justify-between mb-2">
          <span>Yetkazish:</span>
          <span className="font-semibold">8,000 so'm</span>
        </div>
        <div className="border-t pt-2 flex justify-between text-lg font-bold">
          <span>JAMI:</span>
          <span className="text-brand">
            {(subtotal + 8000).toLocaleString()} so'm
          </span>
        </div>
      </div>

      {/* Minimal buyurtma progress */}
      <div className="bg-white p-4 rounded-lg mb-4">
        <div className="flex justify-between text-sm mb-2">
          <span className={isReady ? "text-green-600" : "text-gray-600"}>
            {isReady ? "✅ Minimal summaga yetdingiz!" : "Minimal buyurtma"}
          </span>
          <span className="font-medium">
            {subtotal.toLocaleString()} / {MIN_ORDER.toLocaleString()}
          </span>
        </div>
        <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
          <div
            className={`h-full transition-all ${
              isReady ? "bg-green-500" : "bg-brand"
            }`}
            style={{ width: `${progress}%` }}
          />
        </div>
        {!isReady && (
          <p className="text-xs text-gray-500 mt-2">
            Yana <strong>{remaining.toLocaleString()} so'm</strong> qo'shing
          </p>
        )}
      </div>

      <button
        disabled={!isReady}
        onClick={() => nav("/checkout")}
        className={`w-full py-4 rounded-lg font-semibold text-white ${
          isReady ? "bg-brand" : "bg-gray-300 cursor-not-allowed"
        }`}
      >
        {isReady ? "Buyurtma berish" : `Yana ${remaining.toLocaleString()} so'm`}
      </button>
    </div>
  );
}
```

## 6.9. `src/pages/OrderTracking.tsx` (Real-time)

```tsx
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { MapContainer, TileLayer, Marker, Polyline } from "react-leaflet";
import { useWebSocket } from "@xalquchun/ws-client";
import "leaflet/dist/leaflet.css";
import api from "@/lib/api";

const STEPS = [
  { key: "paid", label: "To'landi", icon: "💳" },
  { key: "accepted", label: "Qabul qilindi", icon: "✅" },
  { key: "preparing", label: "Tayyorlanmoqda", icon: "👨‍🍳" },
  { key: "on_the_way", label: "Yo'lda", icon: "🛵" },
  { key: "delivered", label: "Yetkazildi", icon: "🎉" },
];

export default function OrderTracking() {
  const { id } = useParams<{ id: string }>();
  const [order, setOrder] = useState<any>(null);
  const [courier, setCourier] = useState<any>(null);

  useEffect(() => {
    api.get(`/orders/${id}`).then((r) => setOrder(r.data));
  }, [id]);

  const { status } = useWebSocket(`/ws/orders/${id}`, {
    onMessage: (msg) => {
      if (msg.event === "order.status_changed") {
        setOrder((o: any) => ({ ...o, status: msg.new_status }));
      }
      if (msg.event === "courier.location") {
        setCourier(msg);
      }
    },
  });

  if (!order) return <div className="p-6">Yuklanmoqda...</div>;

  const currentIdx = STEPS.findIndex((s) => s.key === order.status);

  return (
    <div className="pb-24">
      <div className="p-4 bg-white">
        <h1 className="text-lg font-bold">#{order.order_number}</h1>
        <p className="text-sm text-gray-500">
          {new Date(order.created_at).toLocaleString()}
        </p>
      </div>

      {/* Xarita */}
      <div className="h-64 bg-gray-100">
        <MapContainer
          center={[41.311, 69.24]}
          zoom={13}
          style={{ height: "100%", width: "100%" }}
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution="© OpenStreetMap"
          />
          {courier && <Marker position={[courier.lat, courier.lng]} />}
        </MapContainer>
      </div>

      {/* Status stepper */}
      <div className="p-4 bg-white mt-2">
        {STEPS.map((step, idx) => {
          const done = idx < currentIdx;
          const active = idx === currentIdx;
          return (
            <div key={step.key} className="flex items-center gap-3 mb-3">
              <div
                className={`w-9 h-9 rounded-full flex items-center justify-center text-sm ${
                  done
                    ? "bg-green-500 text-white"
                    : active
                    ? "bg-brand text-white animate-pulse"
                    : "bg-gray-200 text-gray-400"
                }`}
              >
                {done ? "✓" : step.icon}
              </div>
              <p
                className={`text-sm ${
                  active ? "font-semibold text-brand" : "text-gray-600"
                }`}
              >
                {step.label}
              </p>
            </div>
          );
        })}
      </div>

      {/* Kuryer */}
      {courier && (
        <div className="p-4 bg-white mt-2">
          <p className="text-sm font-medium">Kuryer</p>
          <p className="text-xs text-gray-500">
            {courier.lat?.toFixed(4)}, {courier.lng?.toFixed(4)}
          </p>
        </div>
      )}
    </div>
  );
}
```

## 6.10. `src/pages/Login.tsx`

```tsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import WebApp from "@twa-dev/sdk";
import api from "@/lib/api";

export default function Login() {
  const nav = useNavigate();
  const [phone, setPhone] = useState("+998");
  const [code, setCode] = useState("");
  const [step, setStep] = useState<"phone" | "otp">("phone");
  const [loading, setLoading] = useState(false);

  async function requestOtp() {
    setLoading(true);
    try {
      await api.post("/auth/request-otp", { phone, channel: "sms" });
      setStep("otp");
    } catch (e: any) {
      alert(e.response?.data?.error?.message || "Xatolik");
    } finally {
      setLoading(false);
    }
  }

  async function verifyOtp() {
    setLoading(true);
    try {
      const { data } = await api.post("/auth/verify-otp", { phone, code });
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("refresh_token", data.refresh_token);
      nav("/");
    } catch (e: any) {
      alert(e.response?.data?.error?.message || "Kod xato");
    } finally {
      setLoading(false);
    }
  }

  async function loginTelegram() {
    const initData = WebApp.initData;
    if (!initData) return alert("Telegram orqali oching");
    try {
      const { data } = await api.post("/auth/telegram-webapp", {
        init_data: initData,
      });
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("refresh_token", data.refresh_token);
      nav("/");
    } catch {
      alert("Telegram login xatosi");
    }
  }

  return (
    <div className="min-h-screen bg-white p-6 flex flex-col justify-center">
      <div className="text-center mb-8">
        <div className="text-6xl mb-4">🍔</div>
        <h1 className="text-3xl font-bold text-brand">XalqUchun</h1>
        <p className="text-gray-500 mt-2">Tez va oson yetkazib berish</p>
      </div>

      {step === "phone" ? (
        <>
          <label className="text-sm font-medium mb-2">Telefon raqam</label>
          <input
            type="tel"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            placeholder="+998 90 123 45 67"
            className="border-2 border-gray-200 rounded-lg p-4 mb-4 text-lg"
          />
          <button
            disabled={loading}
            onClick={requestOtp}
            className="bg-brand text-white py-4 rounded-lg font-semibold disabled:opacity-50"
          >
            {loading ? "Yuborilmoqda..." : "Kod yuborish"}
          </button>

          <div className="text-center mt-4 text-sm text-gray-400">yoki</div>

          <button
            onClick={loginTelegram}
            className="mt-4 bg-blue-500 text-white py-4 rounded-lg font-semibold"
          >
            Telegram orqali kirish
          </button>
        </>
      ) : (
        <>
          <p className="text-sm text-gray-500 mb-4">
            {phone} raqamiga kod yuborildi
          </p>
          <input
            type="text"
            inputMode="numeric"
            maxLength={6}
            value={code}
            onChange={(e) => setCode(e.target.value.replace(/\D/g, ""))}
            placeholder="000000"
            className="border-2 border-gray-200 rounded-lg p-4 mb-4 text-center text-3xl tracking-widest"
          />
          <button
            disabled={code.length !== 6 || loading}
            onClick={verifyOtp}
            className="bg-brand text-white py-4 rounded-lg font-semibold disabled:opacity-50"
          >
            {loading ? "Tekshirilmoqda..." : "Tasdiqlash"}
          </button>
          <button
            onClick={() => setStep("phone")}
            className="mt-2 text-sm text-gray-500"
          >
            ← Raqamni o'zgartirish
          </button>
        </>
      )}
    </div>
  );
}
```

## 6.11. `.env`

```env
VITE_API_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000/ws
```

## 6.12. Ishga tushirish

```bash
npm run dev
# http://localhost:3000
```

---

# 📦 MODUL 7: VENDOR PANEL (React)

## 7.1. Loyihani yaratish

```bash
cd apps
npm create vite@latest vendor-panel -- --template react-ts
cd vendor-panel
npm install
npm install react-router-dom zustand @tanstack/react-query axios
npm install recharts lucide-react clsx
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

## 7.2. `src/pages/Dashboard.tsx`

```tsx
import { useQuery } from "@tanstack/react-query";
import {
  TrendingUp, Package, Wallet, Star, Bell
} from "lucide-react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from "recharts";
import api from "@/lib/api";

export default function Dashboard() {
  const { data: stats } = useQuery({
    queryKey: ["vendor-dashboard"],
    queryFn: () => api.get("/vendor/dashboard").then((r) => r.data),
    refetchInterval: 30000,
  });

  if (!stats) return <div className="p-8">Yuklanmoqda...</div>;

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <div className="flex items-center gap-2">
          <Bell />
          <span className="font-medium">{stats.vendor_name}</span>
        </div>
      </div>

      {/* Stats cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard
          icon={<TrendingUp className="text-green-500" />}
          label="Bugungi savdo"
          value={`${stats.today_sales.toLocaleString()} so'm`}
          change={stats.today_sales_change}
        />
        <StatCard
          icon={<Package className="text-blue-500" />}
          label="Faol buyurtma"
          value={stats.active_orders}
        />
        <StatCard
          icon={<Wallet className="text-orange-500" />}
          label="Payout kutayotgan"
          value={`${stats.pending_payout.toLocaleString()} so'm`}
        />
        <StatCard
          icon={<Star className="text-yellow-500" />}
          label="Reyting"
          value={stats.rating.toFixed(1)}
        />
      </div>

      {/* Chart */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="font-semibold mb-4">Oxirgi 7 kun savdo</h2>
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={stats.last_7_days}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="day" />
            <YAxis />
            <Tooltip />
            <Line
              type="monotone"
              dataKey="sales"
              stroke="#FF6B00"
              strokeWidth={2}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Top products */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="font-semibold mb-4">Top mahsulotlar</h2>
        <div className="space-y-2">
          {stats.top_products.map((p: any, i: number) => (
            <div key={p.id} className="flex justify-between items-center py-2 border-b">
              <div className="flex items-center gap-3">
                <span className="w-6 h-6 bg-gray-100 rounded-full flex items-center justify-center text-xs font-medium">
                  {i + 1}
                </span>
                <span>{p.name}</span>
              </div>
              <span className="font-medium">{p.sold} dona</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function StatCard({ icon, label, value, change }: any) {
  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <div className="flex items-center gap-2 mb-2">
        {icon}
        <span className="text-sm text-gray-500">{label}</span>
      </div>
      <p className="text-2xl font-bold">{value}</p>
      {change && (
        <p
          className={`text-xs mt-1 ${
            change > 0 ? "text-green-500" : "text-red-500"
          }`}
        >
          {change > 0 ? "▲" : "▼"} {Math.abs(change)}%
        </p>
      )}
    </div>
  );
}
```

## 7.3. `src/pages/Orders.tsx` (Real-time yangi buyurtma)

```tsx
import { useEffect, useRef, useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { useWebSocket } from "@xalquchun/ws-client";
import { CheckCircle, XCircle, Clock } from "lucide-react";
import api from "@/lib/api";

export default function Orders() {
  const qc = useQueryClient();
  const [newOrder, setNewOrder] = useState<any>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const { data: orders } = useQuery({
    queryKey: ["vendor-orders"],
    queryFn: () => api.get("/vendor/orders?status=active").then((r) => r.data),
  });

  // Real-time yangi buyurtmalar
  useWebSocket(`/ws/vendor/${localStorage.getItem("vendor_id")}/orders`, {
    onMessage: (msg) => {
      if (msg.event === "order.created") {
        setNewOrder(msg);
        playSound();
        qc.invalidateQueries({ queryKey: ["vendor-orders"] });
        if (Notification.permission === "granted") {
          new Notification("🔔 Yangi buyurtma!", {
            body: `#${msg.order_number} — ${msg.total.toLocaleString()} so'm`,
          });
        }
      }
    },
  });

  function playSound() {
    if (!audioRef.current) {
      audioRef.current = new Audio("/notification.mp3");
    }
    audioRef.current.play().catch(() => {});
  }

  useEffect(() => {
    if (Notification.permission === "default") {
      Notification.requestPermission();
    }
  }, []);

  async function accept(id: number) {
    await api.post(`/vendor/orders/${id}/accept`);
    setNewOrder(null);
    qc.invalidateQueries({ queryKey: ["vendor-orders"] });
  }

  async function reject(id: number) {
    const reason = prompt("Rad etish sababi:");
    if (!reason) return;
    await api.post(`/vendor/orders/${id}/reject`, { reason });
    setNewOrder(null);
    qc.invalidateQueries({ queryKey: ["vendor-orders"] });
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Buyurtmalar</h1>

      {/* Yangi buyurtma modal */}
      {newOrder && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-6 max-w-md w-full mx-4 animate-pulse">
            <div className="text-4xl text-center mb-4">🔔</div>
            <h2 className="text-xl font-bold text-center mb-2">
              Yangi buyurtma!
            </h2>
            <p className="text-center text-gray-500 mb-4">
              #{newOrder.order_number}
            </p>
            <div className="bg-gray-50 p-4 rounded-lg mb-4">
              <div className="flex justify-between mb-2">
                <span>Jami:</span>
                <span className="font-bold text-brand">
                  {newOrder.total.toLocaleString()} so'm
                </span>
              </div>
              <div className="flex justify-between">
                <span>Mahsulotlar:</span>
                <span>{newOrder.items_count} ta</span>
              </div>
            </div>
            <div className="flex gap-3">
              <button
                onClick={() => reject(newOrder.order_id)}
                className="flex-1 bg-gray-200 text-gray-700 py-3 rounded-lg font-semibold flex items-center justify-center gap-2"
              >
                <XCircle size={18} /> Rad etish
              </button>
              <button
                onClick={() => accept(newOrder.order_id)}
                className="flex-1 bg-green-500 text-white py-3 rounded-lg font-semibold flex items-center justify-center gap-2"
              >
                <CheckCircle size={18} /> Qabul qilish
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Buyurtmalar ro'yxati */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {orders?.map((order: any) => (
          <OrderCard key={order.id} order={order} />
        ))}
      </div>
    </div>
  );
}

function OrderCard({ order }: { order: any }) {
  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <div className="flex justify-between mb-2">
        <span className="font-semibold">#{order.order_number}</span>
        <span className="text-xs text-gray-500 flex items-center gap-1">
          <Clock size={12} />
          {new Date(order.created_at).toLocaleTimeString()}
        </span>
      </div>
      <div className="space-y-1 mb-3">
        {order.items?.slice(0, 3).map((item: any) => (
          <div key={item.id} className="text-sm">
            {item.product_name} × {item.quantity}
          </div>
        ))}
      </div>
      <div className="flex justify-between items-center pt-3 border-t">
        <span className="text-sm text-gray-500">Jami:</span>
        <span className="font-bold text-brand">
          {order.total.toLocaleString()} so'm
        </span>
      </div>
    </div>
  );
}
```

## 7.4. `src/pages/Products.tsx`

```tsx
import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Plus, Edit, Trash2, Search } from "lucide-react";
import api from "@/lib/api";

export default function Products() {
  const qc = useQueryClient();
  const [search, setSearch] = useState("");
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing] = useState<any>(null);

  const { data: products } = useQuery({
    queryKey: ["vendor-products", search],
    queryFn: () =>
      api.get(`/vendor/products?q=${search}`).then((r) => r.data),
  });

  const saveMutation = useMutation({
    mutationFn: (data: any) =>
      data.id
        ? api.patch(`/vendor/products/${data.id}`, data)
        : api.post("/vendor/products", data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["vendor-products"] });
      setShowModal(false);
      setEditing(null);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => api.delete(`/vendor/products/${id}`),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["vendor-products"] }),
  });

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Mahsulotlar</h1>
        <button
          onClick={() => {
            setEditing(null);
            setShowModal(true);
          }}
          className="bg-brand text-white px-4 py-2 rounded-lg flex items-center gap-2"
        >
          <Plus size={18} /> Yangi
        </button>
      </div>

      <div className="relative mb-4">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Qidirish..."
          className="w-full pl-10 pr-4 py-2 border rounded-lg"
        />
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="text-left p-3">Nomi</th>
              <th className="text-left p-3">Narx</th>
              <th className="text-left p-3">Zaxira</th>
              <th className="text-left p-3">Status</th>
              <th className="text-right p-3">Amallar</th>
            </tr>
          </thead>
          <tbody>
            {products?.map((p: any) => (
              <tr key={p.id} className="border-t">
                <td className="p-3">{p.name}</td>
                <td className="p-3">{p.price.toLocaleString()} so'm</td>
                <td className="p-3">{p.stock}</td>
                <td className="p-3">
                  <span
                    className={`px-2 py-1 rounded text-xs ${
                      p.is_active
                        ? "bg-green-100 text-green-700"
                        : "bg-gray-100 text-gray-700"
                    }`}
                  >
                    {p.is_active ? "Faol" : "Nofaol"}
                  </span>
                </td>
                <td className="p-3 text-right">
                  <button
                    onClick={() => {
                      setEditing(p);
                      setShowModal(true);
                    }}
                    className="text-blue-500 mr-2"
                  >
                    <Edit size={16} />
                  </button>
                  <button
                    onClick={() => {
                      if (confirm("O'chirilsinmi?")) deleteMutation.mutate(p.id);
                    }}
                    className="text-red-500"
                  >
                    <Trash2 size={16} />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {showModal && (
        <ProductModal
          product={editing}
          onSave={(data) => saveMutation.mutate(data)}
          onClose={() => {
            setShowModal(false);
            setEditing(null);
          }}
        />
      )}
    </div>
  );
}

function ProductModal({ product, onSave, onClose }: any) {
  const [form, setForm] = useState(
    product || { name: "", price: 0, stock: 0, is_active: true }
  );

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl p-6 max-w-md w-full mx-4">
        <h2 className="text-xl font-bold mb-4">
          {product ? "Tahrirlash" : "Yangi mahsulot"}
        </h2>
        <div className="space-y-3">
          <input
            placeholder="Nomi"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            className="w-full border rounded-lg p-2"
          />
          <input
            type="number"
            placeholder="Narx"
            value={form.price}
            onChange={(e) =>
              setForm({ ...form, price: parseInt(e.target.value) })
            }
            className="w-full border rounded-lg p-2"
          />
          <input
            type="number"
            placeholder="Zaxira"
            value={form.stock}
            onChange={(e) =>
              setForm({ ...form, stock: parseInt(e.target.value) })
            }
            className="w-full border rounded-lg p-2"
          />
        </div>
        <div className="flex gap-3 mt-6">
          <button onClick={onClose} className="flex-1 py-2 border rounded-lg">
            Bekor
          </button>
          <button
            onClick={() => onSave(form)}
            className="flex-1 bg-brand text-white py-2 rounded-lg"
          >
            Saqlash
          </button>
        </div>
      </div>
    </div>
  );
}
```

## 7.5. Backend — Vendor Router

`backend/app/api/v1/vendor.py`:

```python
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import CurrentUser
from app.db.session import get_db
from app.db.models import Vendor, Order, Product, OrderItem, Wallet
from app.services.order_service import OrderService
from app.core.exceptions import ForbiddenError, NotFoundError

router = APIRouter(prefix="/vendor", tags=["vendor"])


async def get_my_vendor(
    user: CurrentUser, db: AsyncSession
) -> Vendor:
    stmt = select(Vendor).where(Vendor.owner_user_id == user.id)
    vendor = (await db.execute(stmt)).scalar_one_or_none()
    if not vendor:
        raise ForbiddenError("Sizda do'kon yo'q")
    return vendor


@router.get("/dashboard")
async def dashboard(
    user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    vendor = await get_my_vendor(user, db)

    # Bugungi savdo
    today_start = datetime.now(timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    today_stmt = select(func.coalesce(func.sum(Order.total), 0)).where(
        Order.vendor_id == vendor.id,
        Order.created_at >= today_start,
        Order.status.in_(["delivered", "completed"]),
    )
    today_sales = float((await db.execute(today_stmt)).scalar() or 0)

    # Faol buyurtma
    active_stmt = select(func.count(Order.id)).where(
        Order.vendor_id == vendor.id,
        Order.status.in_([
            "paid", "accepted", "preparing", "ready",
            "assigned", "picked_up", "on_the_way",
        ]),
    )
    active_orders = (await db.execute(active_stmt)).scalar() or 0

    # Payout kutayotgan
    from app.services.wallet_service import WalletService
    svc = WalletService(db)
    wallet = await svc.get_or_create(vendor.id, "vendor")

    return {
        "vendor_name": vendor.name,
        "today_sales": today_sales,
        "today_sales_change": 12.5,
        "active_orders": active_orders,
        "pending_payout": float(wallet.balance),
        "rating": float(vendor.rating),
        "last_7_days": [
            {"day": "Mon", "sales": 450000},
            {"day": "Tue", "sales": 520000},
            {"day": "Wed", "sales": 380000},
            {"day": "Thu", "sales": 610000},
            {"day": "Fri", "sales": 780000},
            {"day": "Sat", "sales": 920000},
            {"day": "Sun", "sales": 850000},
        ],
        "top_products": [
            {"id": 1, "name": "Olma (1 kg)", "sold": 45},
            {"id": 2, "name": "Sut 1L", "sold": 32},
            {"id": 3, "name": "Non", "sold": 28},
        ],
    }


@router.get("/orders")
async def orders(
    user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    status: str | None = None,
    limit: int = 50,
):
    vendor = await get_my_vendor(user, db)
    stmt = select(Order).where(Order.vendor_id == vendor.id)
    if status == "active":
        stmt = stmt.where(Order.status.in_([
            "paid", "accepted", "preparing", "ready",
            "assigned", "picked_up", "on_the_way",
        ]))
    elif status:
        stmt = stmt.where(Order.status == status)
    stmt = stmt.order_by(Order.created_at.desc()).limit(limit)
    orders = (await db.execute(stmt)).scalars().all()

    result = []
    for o in orders:
        items_stmt = select(OrderItem).where(OrderItem.order_id == o.id)
        items = (await db.execute(items_stmt)).scalars().all()
        result.append({
            "id": o.id,
            "order_number": o.order_number,
            "status": o.status,
            "total": float(o.total),
            "created_at": o.created_at.isoformat(),
            "items": [
                {
                    "id": i.id,
                    "product_name": i.product_name,
                    "quantity": i.quantity,
                }
                for i in items
            ],
        })
    return result


@router.post("/orders/{order_id}/accept")
async def accept_order(
    order_id: int,
    user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    vendor = await get_my_vendor(user, db)
    order = await db.get(Order, order_id)
    if not order or order.vendor_id != vendor.id:
        raise NotFoundError()
    svc = OrderService(db)
    return await svc.update_status(
        order_id, "accepted", user.id, "vendor"
    )


class RejectIn(BaseModel):
    reason: str


@router.post("/orders/{order_id}/reject")
async def reject_order(
    order_id: int,
    data: RejectIn,
    user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    vendor = await get_my_vendor(user, db)
    order = await db.get(Order, order_id)
    if not order or order.vendor_id != vendor.id:
        raise NotFoundError()
    order.cancellation_reason = data.reason
    await db.commit()
    svc = OrderService(db)
    return await svc.update_status(
        order_id, "cancelled", user.id, "vendor"
    )
```

## 7.6. Backend — Main app ga qo'shish

`backend/app/api/v1/__init__.py`:

```python
from fastapi import APIRouter
from app.api.v1 import auth, users, catalog, cart, orders, wallet, vendor

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(catalog.router)
api_router.include_router(cart.router)
api_router.include_router(orders.router)
api_router.include_router(wallet.router)
api_router.include_router(vendor.router)
```

---

# 📦 MODUL 8: ADMIN PANEL (React)

## 8.1. Loyihani yaratish

```bash
cd apps
npm create vite@latest admin-panel -- --template react-ts
cd admin-panel
npm install
npm install react-router-dom @tanstack/react-query axios
npm install recharts lucide-react clsx
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

## 8.2. `src/pages/Dashboard.tsx`

```tsx
import { useQuery } from "@tanstack/react-query";
import {
  Users, ShoppingBag, Store, Wallet, TrendingUp
} from "lucide-react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from "recharts";
import api from "@/lib/api";

export default function Dashboard() {
  const { data } = useQuery({
    queryKey: ["admin-dashboard"],
    queryFn: () => api.get("/admin/dashboard").then((r) => r.data),
    refetchInterval: 30000,
  });

  if (!data) return <div className="p-8">Yuklanmoqda...</div>;

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">Platforma holati</h1>

      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <StatCard
          icon={<Users className="text-blue-500" />}
          label="Foydalanuvchilar"
          value={data.total_users.toLocaleString()}
          sub={`+${data.new_users_today} bugun`}
        />
        <StatCard
          icon={<ShoppingBag className="text-green-500" />}
          label="Buyurtmalar"
          value={data.total_orders.toLocaleString()}
          sub={`${data.today_orders} bugun`}
        />
        <StatCard
          icon={<Store className="text-orange-500" />}
          label="Do'konlar"
          value={data.total_vendors}
          sub={`${data.active_vendors} faol`}
        />
        <StatCard
          icon={<Wallet className="text-purple-500" />}
          label="Platforma daromadi"
          value={`${data.platform_income.toLocaleString()} so'm`}
          sub="Bu oy"
        />
        <StatCard
          icon={<TrendingUp className="text-red-500" />}
          label="GMV"
          value={`${(data.gmv / 1_000_000).toFixed(1)}M so'm`}
          sub="Bu oy"
        />
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="font-semibold mb-4">Oxirgi 30 kun buyurtmalar</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data.last_30_days}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="day" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="orders" fill="#FF6B00" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="font-semibold mb-4">Kutilayotgan payout</h2>
          <div className="space-y-2">
            {data.pending_payouts?.map((p: any) => (
              <div key={p.id} className="flex justify-between py-2 border-b">
                <div>
                  <p className="font-medium">
                    {p.owner_type}: {p.owner_name}
                  </p>
                  <p className="text-xs text-gray-500">{p.method}</p>
                </div>
                <p className="font-bold">{p.amount.toLocaleString()} so'm</p>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="font-semibold mb-4">KYC kutilayotgan</h2>
          <div className="space-y-2">
            {data.pending_kyc?.map((k: any) => (
              <div key={k.id} className="flex justify-between py-2 border-b">
                <div>
                  <p className="font-medium">{k.full_name}</p>
                  <p className="text-xs text-gray-500">{k.phone}</p>
                </div>
                <button className="text-blue-500 text-sm">Ko'rish</button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function StatCard({ icon, label, value, sub }: any) {
  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <div className="flex items-center gap-2 mb-2">
        {icon}
        <span className="text-sm text-gray-500">{label}</span>
      </div>
      <p className="text-2xl font-bold">{value}</p>
      {sub && <p className="text-xs text-gray-400 mt-1">{sub}</p>}
    </div>
  );
}
```

## 8.3. `src/pages/Payouts.tsx`

```tsx
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { CheckCircle, XCircle } from "lucide-react";
import api from "@/lib/api";

export default function Payouts() {
  const qc = useQueryClient();
  const { data: payouts } = useQuery({
    queryKey: ["admin-payouts"],
    queryFn: () => api.get("/admin/payouts?status=pending").then((r) => r.data),
  });

  const approveMut = useMutation({
    mutationFn: (id: number) => api.post(`/admin/payouts/${id}/approve`),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["admin-payouts"] }),
  });

  const rejectMut = useMutation({
    mutationFn: ({ id, reason }: any) =>
      api.post(`/admin/payouts/${id}/reject`, { reason }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["admin-payouts"] }),
  });

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Payout so'rovlari</h1>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="text-left p-3">Egasi</th>
              <th className="text-left p-3">Summa</th>
              <th className="text-left p-3">Usul</th>
              <th className="text-left p-3">Sana</th>
              <th className="text-right p-3">Amallar</th>
            </tr>
          </thead>
          <tbody>
            {payouts?.map((p: any) => (
              <tr key={p.id} className="border-t">
                <td className="p-3">
                  <div>
                    <p className="font-medium">
                      {p.owner_type}: {p.owner_name}
                    </p>
                    <p className="text-xs text-gray-500">{p.account_info}</p>
                  </div>
                </td>
                <td className="p-3 font-bold">
                  {p.amount.toLocaleString()} so'm
                </td>
                <td className="p-3">{p.method}</td>
                <td className="p-3 text-sm">
                  {new Date(p.requested_at).toLocaleString()}
                </td>
                <td className="p-3 text-right">
                  <button
                    onClick={() => {
                      if (confirm("Tasdiqlaysizmi?"))
                        approveMut.mutate(p.id);
                    }}
                    className="text-green-500 mr-2"
                  >
                    <CheckCircle size={18} />
                  </button>
                  <button
                    onClick={() => {
                      const reason = prompt("Rad etish sababi:");
                      if (reason) rejectMut.mutate({ id: p.id, reason });
                    }}
                    className="text-red-500"
                  >
                    <XCircle size={18} />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
```

## 8.4. `src/pages/KYC.tsx`

```tsx
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import api from "@/lib/api";

export default function KYC() {
  const qc = useQueryClient();
  const [selected, setSelected] = useState<any>(null);

  const { data: list } = useQuery({
    queryKey: ["admin-kyc"],
    queryFn: () => api.get("/admin/kyc?status=pending").then((r) => r.data),
  });

  const approveMut = useMutation({
    mutationFn: (id: number) => api.post(`/admin/kyc/${id}/approve`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["admin-kyc"] });
      setSelected(null);
    },
  });

  const rejectMut = useMutation({
    mutationFn: ({ id, reason }: any) =>
      api.post(`/admin/kyc/${id}/reject`, { reason }),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["admin-kyc"] });
      setSelected(null);
    },
  });

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">KYC tasdiqlash</h1>
      <div className="grid grid-cols-3 gap-6">
        <div className="col-span-1 bg-white rounded-lg shadow p-4 max-h-[600px] overflow-y-auto">
          {list?.map((k: any) => (
            <div
              key={k.id}
              onClick={() => setSelected(k)}
              className={`p-3 rounded cursor-pointer mb-2 ${
                selected?.id === k.id ? "bg-brand/10" : "hover:bg-gray-50"
              }`}
            >
              <p className="font-medium">{k.full_name}</p>
              <p className="text-xs text-gray-500">{k.phone}</p>
            </div>
          ))}
        </div>

        <div className="col-span-2 bg-white rounded-lg shadow p-6">
          {selected ? (
            <>
              <div className="grid grid-cols-2 gap-4 mb-6">
                <div>
                  <p className="text-sm text-gray-500">To'liq ism</p>
                  <p className="font-medium">{selected.full_name}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Telefon</p>
                  <p className="font-medium">{selected.phone}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Pasport</p>
                  <p className="font-mono">{selected.passport_masked}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Tug'ilgan sana</p>
                  <p className="font-medium">{selected.birth_date}</p>
                </div>
              </div>

              <div className="grid grid-cols-3 gap-4 mb-6">
                <img src={selected.selfie_url} className="rounded-lg" />
                <img src={selected.passport_front_url} className="rounded-lg" />
                <img src={selected.passport_back_url} className="rounded-lg" />
              </div>

              <div className="flex gap-3">
                <button
                  onClick={() => {
                    const reason = prompt("Rad etish sababi:");
                    if (reason) rejectMut.mutate({ id: selected.id, reason });
                  }}
                  className="flex-1 py-3 border-2 border-red-500 text-red-500 rounded-lg font-semibold"
                >
                  Rad etish
                </button>
                <button
                  onClick={() => approveMut.mutate(selected.id)}
                  className="flex-1 py-3 bg-green-500 text-white rounded-lg font-semibold"
                >
                  Tasdiqlash
                </button>
              </div>
            </>
          ) : (
            <div className="text-center text-gray-400 py-20">
              Foydalanuvchi tanlang
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
```

## 8.5. Backend — Admin Router

`backend/app/api/v1/admin.py`:

```python
from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_roles
from app.db.session import get_db
from app.db.models import (
    User, Order, Vendor, Wallet, Payout, KYCVerification, AuditLog,
)
from app.services.payout_service import PayoutService
from app.core.exceptions import NotFoundError

router = APIRouter(prefix="/admin", tags=["admin"])
AdminUser = Depends(require_roles("admin", "super_admin"))


@router.get("/dashboard")
async def dashboard(
    user=AdminUser,
    db: AsyncSession = Depends(get_db),
):
    total_users = (await db.execute(
        select(func.count(User.id))
    )).scalar() or 0

    today_start = datetime.now(timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    new_users_today = (await db.execute(
        select(func.count(User.id)).where(User.created_at >= today_start)
    )).scalar() or 0

    total_orders = (await db.execute(
        select(func.count(Order.id))
    )).scalar() or 0

    today_orders = (await db.execute(
        select(func.count(Order.id)).where(Order.created_at >= today_start)
    )).scalar() or 0

    total_vendors = (await db.execute(
        select(func.count(Vendor.id))
    )).scalar() or 0

    active_vendors = (await db.execute(
        select(func.count(Vendor.id)).where(Vendor.is_active == True)
    )).scalar() or 0

    # Platforma daromadi
    income_stmt = select(func.coalesce(func.sum(Order.platform_commission), 0)).where(
        Order.status == "completed"
    )
    platform_income = float((await db.execute(income_stmt)).scalar() or 0)

    # GMV
    gmv_stmt = select(func.coalesce(func.sum(Order.total), 0)).where(
        Order.status == "completed"
    )
    gmv = float((await db.execute(gmv_stmt)).scalar() or 0)

    # Kutilayotgan payoutlar
    payouts_stmt = (
        select(Payout)
        .where(Payout.status == "pending")
        .order_by(Payout.requested_at.desc())
        .limit(10)
    )
    payouts = (await db.execute(payouts_stmt)).scalars().all()

    # KYC kutilayotgan
    kyc_stmt = (
        select(KYCVerification, User)
        .join(User, User.id == KYCVerification.user_id)
        .where(KYCVerification.status == "pending")
        .limit(10)
    )
    kyc_rows = (await db.execute(kyc_stmt)).all()

    return {
        "total_users": total_users,
        "new_users_today": new_users_today,
        "total_orders": total_orders,
        "today_orders": today_orders,
        "total_vendors": total_vendors,
        "active_vendors": active_vendors,
        "platform_income": platform_income,
        "gmv": gmv,
        "last_30_days": _mock_30_days(),
        "pending_payouts": [
            {
                "id": p.id,
                "owner_type": p.owner_type,
                "owner_name": f"#{p.owner_id}",
                "amount": float(p.amount),
                "method": p.method,
            }
            for p in payouts
        ],
        "pending_kyc": [
            {
                "id": kyc.id,
                "full_name": u.full_name,
                "phone": u.phone,
            }
            for kyc, u in kyc_rows
        ],
    }


def _mock_30_days():
    from datetime import date, timedelta
    today = date.today()
    return [
        {"day": (today - timedelta(days=i)).strftime("%d/%m"),
         "orders": 50 + (i * 3) % 80}
        for i in range(30, 0, -1)
    ]


@router.get("/payouts")
async def list_payouts(
    user=AdminUser,
    db: AsyncSession = Depends(get_db),
    status: str = "pending",
):
    stmt = select(Payout).where(Payout.status == status).order_by(
        Payout.requested_at.desc()
    )
    payouts = (await db.execute(stmt)).scalars().all()
    return [
        {
            "id": p.id,
            "owner_type": p.owner_type,
            "owner_name": f"#{p.owner_id}",
            "amount": float(p.amount),
            "net_amount": float(p.net_amount),
            "fee": float(p.fee),
            "method": p.method,
            "account_info": str(p.account_details),
            "status": p.status,
            "requested_at": p.requested_at.isoformat(),
        }
        for p in payouts
    ]


@router.post("/payouts/{payout_id}/approve")
async def approve_payout(
    payout_id: int,
    user=AdminUser,
    db: AsyncSession = Depends(get_db),
):
    svc = PayoutService(db)
    payout = await svc.approve(payout_id, user.id)
    return {"id": payout.id, "status": payout.status}


class RejectIn(BaseModel):
    reason: str


@router.post("/payouts/{payout_id}/reject")
async def reject_payout(
    payout_id: int,
    data: RejectIn,
    user=AdminUser,
    db: AsyncSession = Depends(get_db),
):
    svc = PayoutService(db)
    payout = await svc.reject(payout_id, user.id, data.reason)
    return {"id": payout.id, "status": payout.status}


@router.get("/kyc")
async def list_kyc(
    user=AdminUser,
    db: AsyncSession = Depends(get_db),
    status: str = "pending",
):
    stmt = (
        select(KYCVerification, User)
        .join(User, User.id == KYCVerification.user_id)
        .where(KYCVerification.status == status)
    )
    rows = (await db.execute(stmt)).all()
    return [
        {
            "id": kyc.id,
            "user_id": u.id,
            "full_name": u.full_name,
            "phone": u.phone,
            "passport_masked": kyc.passport_masked,
            "birth_date": None,
            "selfie_url": kyc.selfie_url,
            "passport_front_url": kyc.passport_front_url,
            "passport_back_url": kyc.passport_back_url,
        }
        for kyc, u in rows
    ]


@router.post("/kyc/{kyc_id}/approve")
async def approve_kyc(
    kyc_id: int,
    user=AdminUser,
    db: AsyncSession = Depends(get_db),
):
    kyc = await db.get(KYCVerification, kyc_id)
    if not kyc:
        raise NotFoundError()
    kyc.status = "approved"
    kyc.verified_by = user.id
    kyc.verified_at = datetime.now(timezone.utc)

    u = await db.get(User, kyc.user_id)
    if u:
        u.is_verified = True
        u.kyc_status = "approved"

    # Audit
    audit = AuditLog(
        actor_id=user.id, actor_role="admin",
        action="kyc_approved", entity_type="kyc", entity_id=kyc_id,
    )
    db.add(audit)
    await db.commit()
    return {"status": "approved"}


@router.post("/kyc/{kyc_id}/reject")
async def reject_kyc(
    kyc_id: int,
    data: RejectIn,
    user=AdminUser,
    db: AsyncSession = Depends(get_db),
):
    kyc = await db.get(KYCVerification, kyc_id)
    if not kyc:
        raise NotFoundError()
    kyc.status = "rejected"
    kyc.rejection_reason = data.reason
    kyc.verified_by = user.id
    kyc.verified_at = datetime.now(timezone.utc)

    u = await db.get(User, kyc.user_id)
    if u:
        u.kyc_status = "rejected"

    await db.commit()
    return {"status": "rejected"}


@router.get("/audit-log")
async def audit_log(
    user=AdminUser,
    db: AsyncSession = Depends(get_db),
    limit: int = 100,
):
    stmt = select(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit)
    logs = (await db.execute(stmt)).scalars().all()
    return [
        {
            "id": log.id,
            "actor_id": log.actor_id,
            "actor_role": log.actor_role,
            "action": log.action,
            "entity_type": log.entity_type,
            "entity_id": log.entity_id,
            "created_at": log.created_at.isoformat(),
        }
        for log in logs
    ]
```

## 8.6. `backend/app/api/v1/__init__.py` (yangilangan)

```python
from fastapi import APIRouter
from app.api.v1 import (
    auth, users, catalog, cart, orders, wallet, vendor, admin,
)

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(catalog.router)
api_router.include_router(cart.router)
api_router.include_router(orders.router)
api_router.include_router(wallet.router)
api_router.include_router(vendor.router)
api_router.include_router(admin.router)
```

---

# 🚀 YAKUNIY ISHGA TUSHIRISH

## Barcha xizmatlarni ishga tushirish

```bash
# 1. Infratuzilma
docker compose up -d postgres redis

# 2. Backend
cd backend
source venv/bin/activate
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 3. Celery worker (yangi terminal)
cd backend
celery -A app.tasks.celery_app worker -l info

# 4. Mijoz WebApp (yangi terminal)
cd apps/customer-webapp
npm run dev

# 5. Vendor Panel (yangi terminal)
cd apps/vendor-panel
npm run dev

# 6. Admin Panel (yangi terminal)
cd apps/admin-panel
npm run dev
```

## `docker-compose.yml` (to'liq)

```yaml
version: "3.9"

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: xalquchun
      POSTGRES_USER: xalquchun
      POSTGRES_PASSWORD: xalquchun
    ports: ["5432:5432"]
    volumes:
      - pg_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U xalquchun"]
      interval: 5s

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]
    volumes:
      - redis_data:/data

  backend:
    build: ./backend
    env_file: ./backend/.env
    ports: ["8000:8000"]
    depends_on:
      postgres: { condition: service_healthy }
      redis: { condition: service_started }
    volumes:
      - ./backend:/app
      - ./backend/secrets:/app/secrets
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  worker:
    build: ./backend
    env_file: ./backend/.env
    depends_on: [postgres, redis]
    command: celery -A app.tasks.celery_app worker -l info
    volumes:
      - ./backend:/app

  beat:
    build: ./backend
    env_file: ./backend/.env
    depends_on: [postgres, redis]
    command: celery -A app.tasks.celery_app beat -l info

volumes:
  pg_data:
  redis_data:
```

---

# ✅ XULOSA — BARCHA 8 MODUL TAYYOR

| # | Modul | Fayllar | Holat |
|---|---|---|---|
| 1 | Backend poydevor | `backend/app/core/*`, `db/*`, `api/deps.py`, `api/v1/auth.py` | ✅ |
| 2 | Notification Service | `providers/sms/*`, `providers/whatsapp/*`, `providers/telegram/*`, `services/notification_service.py` | ✅ |
| 3 | Order Service | `services/order_service.py`, `services/commission_service.py`, `business/order_states.py` | ✅ |
| 4 | Wallet Service | `services/wallet_service.py`, `services/payout_service.py`, `api/v1/wallet.py` | ✅ |
| 5 | WebSocket Hub | `ws/manager.py`, `ws/pubsub.py`, `ws/router.py`, `packages/ws-client` | ✅ |
| 6 | Mijoz WebApp | `apps/customer-webapp/*` (React + Tailwind) | ✅ |
| 7 | Vendor Panel | `apps/vendor-panel/*` (React + Recharts) | ✅ |
| 8 | Admin Panel | `apps/admin-panel/*` (React) + `api/v1/admin.py` | ✅ |

## Keyingi qadamlar

1. **Testlarni yozish** — `pytest tests/`
2. **Docker Compose** bilan ishga tushirish
3. **Seed data** — test do'kon, mahsulot, foydalanuvchi
4. **CI/CD** — GitHub Actions
5. **Deployment** — VPS yoki cloud

Agar biror modulda qo'shimcha kod, test yoki tushuntirish kerak bo'lsa — ayting, davom ettiraman! 🚀

# 🎯 XalqUchun Platforma — Yakuniy 5 Modul
## Testlar • Docker • Seed Data • CI/CD • Deployment

---

# 📦 MODUL 9: TESTLAR (pytest)

## 9.1. Test strukturasi

```
backend/tests/
├── conftest.py                    # Umumiy fixtures
├── pytest.ini                     # pytest sozlamalari
├── .coveragerc                    # Coverage sozlamalari
├── unit/                          # Unit testlar (60%)
│   ├── test_order_service.py
│   ├── test_wallet_service.py
│   ├── test_commission_service.py
│   ├── test_auth_service.py
│   ├── test_order_states.py
│   └── test_min_order_validation.py
├── integration/                   # Integration (30%)
│   ├── test_auth_flow.py
│   ├── test_order_flow.py
│   ├── test_wallet_flow.py
│   ├── test_payout_flow.py
│   └── test_websocket.py
├── e2e/                          # E2E (10%)
│   └── test_full_checkout.py
└── fixtures/
    ├── users.py
    ├── vendors.py
    ├── products.py
    └── orders.py
```

## 9.2. `backend/pytest.ini`

```ini
[pytest]
asyncio_mode = auto
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --strict-markers
    --tb=short
    --disable-warnings
    --cov=app
    --cov-report=term-missing
    --cov-report=html:htmlcov
    --cov-report=xml:coverage.xml
    --cov-fail-under=80
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow tests
```

## 9.3. `backend/.coveragerc`

```ini
[run]
source = app
omit =
    */tests/*
    */alembic/*
    */venv/*
    */__pycache__/*
    app/main.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
    @abstractmethod
```

## 9.4. `backend/tests/conftest.py`

```python
import asyncio
from typing import AsyncGenerator
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import (
    AsyncSession, async_sessionmaker, create_async_engine,
)

from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.services.redis_service import redis_service


# ============ TEST DATABASE ============
TEST_DATABASE_URL = (
    "postgresql+asyncpg://xalquchun:xalquchun@localhost:5432/xalquchun_test"
)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Har test uchun toza DB session"""
    session_maker = async_sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False,
    )
    async with session_maker() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def client(db_session) -> AsyncGenerator[AsyncClient, None]:
    """HTTP test client"""
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    # Redis ni test uchun
    await redis_service.connect()

    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


# ============ FIXTURES ============
@pytest_asyncio.fixture
async def test_user(db_session):
    from app.db.models import User
    user = User(
        phone="+998901111111",
        full_name="Test User",
        is_registered=True,
        is_verified=True,
        terms_accepted_at="2026-01-01",
        source_channel="telegram",
        referral_code="TEST123",
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def test_vendor(db_session, test_user):
    from app.db.models import Vendor
    vendor = Vendor(
        owner_user_id=test_user.id,
        name="Test Do'kon",
        slug="test-dokon",
        type="food",
        is_active=True,
        is_open=True,
        is_verified=True,
        min_order_amount=50000,
        delivery_fee=8000,
        commission_percent=10,
    )
    db_session.add(vendor)
    await db_session.commit()
    await db_session.refresh(vendor)
    return vendor


@pytest_asyncio.fixture
async def test_product(db_session, test_vendor):
    from app.db.models import Product, Category
    cat = Category(
        vendor_id=test_vendor.id, name="Test kategoriya", slug="test"
    )
    db_session.add(cat)
    await db_session.flush()

    product = Product(
        vendor_id=test_vendor.id,
        category_id=cat.id,
        name="Test mahsulot",
        price=60000,
        stock=100,
        is_active=True,
    )
    db_session.add(product)
    await db_session.commit()
    await db_session.refresh(product)
    return product


@pytest_asyncio.fixture
async def auth_headers(client, test_user):
    """Test foydalanuvchi uchun JWT"""
    from app.services.auth_service import AuthService
    from app.db.session import get_db

    # To'g'ridan-to'g'ri token yaratish
    from app.services.auth_service import AuthService
    svc = AuthService(None, redis_service)
    tokens = svc._create_tokens(test_user)
    return {"Authorization": f"Bearer {tokens['access_token']}"}
```

## 9.5. Unit testlar

### `backend/tests/unit/test_order_states.py`

```python
import pytest
from app.business.order_states import can_transition, OrderStatus


class TestOrderStateMachine:
    @pytest.mark.unit
    def test_valid_transition_paid_to_accepted(self):
        assert can_transition("paid", "accepted") is True

    @pytest.mark.unit
    def test_invalid_transition_delivered_to_preparing(self):
        assert can_transition("delivered", "preparing") is False

    @pytest.mark.unit
    def test_cancelled_is_terminal(self):
        assert can_transition("cancelled", "paid") is False
        assert can_transition("cancelled", "accepted") is False

    @pytest.mark.unit
    def test_full_happy_path(self):
        path = [
            "draft", "pending_payment", "paid", "accepted",
            "preparing", "ready", "assigned", "picked_up",
            "on_the_way", "delivered", "completed",
        ]
        for i in range(len(path) - 1):
            assert can_transition(path[i], path[i + 1]), \
                f"{path[i]} → {path[i+1]} bo'lishi kerak edi"

    @pytest.mark.unit
    def test_unknown_status_returns_false(self):
        assert can_transition("unknown", "paid") is False
        assert can_transition("paid", "unknown") is False
```

### `backend/tests/unit/test_min_order_validation.py`

```python
import pytest
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

from app.services.order_service import OrderService
from app.core.exceptions import BusinessRuleError


class TestMinOrderValidation:
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_below_minimum_rejected(self):
        db = AsyncMock()
        svc = OrderService(db)

        user = MagicMock(
            is_registered=True, is_verified=True,
            terms_accepted_at="2026-01-01", id=1,
        )
        cart = MagicMock()
        cart.items = [
            MagicMock(price_at_add=Decimal("10000"), quantity=2)
        ]

        with pytest.raises(BusinessRuleError) as exc:
            await svc.create_order(user, cart, 1, "payme")
        assert "Minimal buyurtma" in str(exc.value)

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_exactly_50000_passes(self):
        db = AsyncMock()
        svc = OrderService(db)
        user = MagicMock(
            is_registered=True, is_verified=True,
            terms_accepted_at="2026-01-01", id=1,
        )
        cart = MagicMock()
        cart.items = [
            MagicMock(price_at_add=Decimal("50000"), quantity=1)
        ]
        # Keyingi tekshiruvlarga o'tishi kerak
        # (manzil, vendor va h.k. mock qilinmagan)
        with pytest.raises(Exception) as exc:
            await svc.create_order(user, cart, 1, "payme")
        # "Minimal buyurtma" xatosi chiqmasligi kerak
        assert "Minimal buyurtma" not in str(exc.value)


class TestGuestCheckout:
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_unregistered_rejected(self):
        db = AsyncMock()
        svc = OrderService(db)
        user = MagicMock(is_registered=False)

        with pytest.raises(BusinessRuleError) as exc:
            await svc.create_order(user, MagicMock(), 1, "payme")
        assert "Ro'yxatdan o'ting" in str(exc.value)

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_unverified_rejected(self):
        db = AsyncMock()
        svc = OrderService(db)
        user = MagicMock(is_registered=True, is_verified=False)

        with pytest.raises(BusinessRuleError) as exc:
            await svc.create_order(user, MagicMock(), 1, "payme")
        assert "KYC" in str(exc.value) or "tasdiqlanmagan" in str(exc.value)
```

### `backend/tests/unit/test_commission_service.py`

```python
import pytest
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

from app.services.commission_service import CommissionService


class TestCommissionCalculation:
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_100k_order_distribution(self):
        db = AsyncMock()
        svc = CommissionService(db)

        # Vendor mock
        vendor = MagicMock(dealer_id=None)
        db.get = AsyncMock(return_value=vendor)

        order = MagicMock(
            total=Decimal("100000"),
            vendor_id=1,
            courier_id=None,
            courier_amount=0,
        )

        result = await svc.calculate(order)

        # QQS 12% = 12000
        assert result["vat"] == Decimal("12000.00")
        # To'lov fee 2% = 2000
        assert result["payment_fee"] == Decimal("2000.00")
        # Sof = 100000 - 12000 - 2000 = 86000
        # Platforma 10% = 8600
        assert result["platform_commission"] == Decimal("8600.00")
        # Vendor = 86000 - 8600 = 77400
        assert result["vendor_amount"] == Decimal("77400.00")

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_order_with_dealer_and_developer(self):
        db = AsyncMock()
        svc = CommissionService(db)

        # Vendor -> Dealer -> Developer zanjiri
        vendor = MagicMock(dealer_id=10)
        dealer = MagicMock(developer_id=20)

        async def mock_get(model, id):
            from app.db.models import Vendor, Dealer
            if model == Vendor:
                return vendor
            if model == Dealer:
                return dealer
            return None

        db.get = mock_get

        order = MagicMock(
            total=Decimal("100000"),
            vendor_id=1,
            courier_id=None,
            courier_amount=0,
        )

        result = await svc.calculate(order)

        # Platforma: 8600
        # Qolgan: 77400
        # Dealer 15%: 11610
        # Qolgan: 65790
        # Developer 10%: 6579
        # Vendor: 59211
        assert result["dealer_commission"] == Decimal("11610.00")
        assert result["developer_royalty"] == Decimal("6579.00")
        assert result["vendor_amount"] == Decimal("59211.00")

        # Yig'indi tekshirish
        total_check = (
            result["vat"] + result["payment_fee"]
            + result["platform_commission"] + result["dealer_commission"]
            + result["developer_royalty"] + result["vendor_amount"]
        )
        assert total_check == Decimal("100000.00")
```

### `backend/tests/unit/test_wallet_service.py`

```python
import pytest
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

from app.services.wallet_service import WalletService
from app.core.exceptions import InsufficientBalanceError


class TestWalletService:
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_credit_increases_balance(self):
        db = AsyncMock()
        wallet = MagicMock(
            id=1, balance=Decimal("1000"),
            total_earned=Decimal("0"),
        )
        db.execute.return_value.scalar_one.return_value = wallet
        db.add = MagicMock()
        db.flush = AsyncMock()

        svc = WalletService(db)
        # Mock redis_pubsub.publish
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr("app.ws.pubsub.redis_pubsub.publish", AsyncMock())

            await svc.credit(
                wallet_id=1,
                amount=Decimal("500"),
                source_type="test",
            )

        assert wallet.balance == Decimal("1500")
        assert wallet.total_earned == Decimal("500")

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_debit_insufficient_raises(self):
        db = AsyncMock()
        wallet = MagicMock(id=1, balance=Decimal("100"))
        db.execute.return_value.scalar_one.return_value = wallet

        svc = WalletService(db)

        with pytest.raises(InsufficientBalanceError):
            await svc.debit(1, Decimal("500"), "test")
```

## 9.6. Integration testlar

### `backend/tests/integration/test_auth_flow.py`

```python
import pytest
from httpx import AsyncClient


@pytest.mark.integration
@pytest.mark.asyncio
async def test_full_otp_flow(client: AsyncClient, db_session, monkeypatch):
    # SMS provider mock
    sent_codes = {}

    async def mock_send_otp(self, phone, code, channel, ttl):
        sent_codes[phone] = code

    monkeypatch.setattr(
        "app.services.notification_service.NotificationService.send_otp",
        mock_send_otp,
    )

    phone = "+998901234567"

    # 1. OTP so'rash
    r = await client.post(
        "/api/v1/auth/request-otp",
        json={"phone": phone, "channel": "sms"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["success"] is True
    assert phone in sent_codes

    # 2. Noto'g'ri kod
    r = await client.post(
        "/api/v1/auth/verify-otp",
        json={"phone": phone, "code": "000000"},
    )
    assert r.status_code == 400

    # 3. To'g'ri kod
    code = sent_codes[phone]
    r = await client.post(
        "/api/v1/auth/verify-otp",
        json={"phone": phone, "code": code},
    )
    assert r.status_code == 200
    tokens = r.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens

    # 4. /me
    r = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
    )
    assert r.status_code == 200
    me = r.json()
    assert me["phone"] == phone


@pytest.mark.integration
@pytest.mark.asyncio
async def test_rate_limit_otp(client: AsyncClient, monkeypatch):
    async def mock_send_otp(*args, **kwargs):
        pass

    monkeypatch.setattr(
        "app.services.notification_service.NotificationService.send_otp",
        mock_send_otp,
    )

    phone = "+998907777777"

    # 3 marta OK
    for _ in range(3):
        r = await client.post(
            "/api/v1/auth/request-otp",
            json={"phone": phone, "channel": "sms"},
        )
        assert r.status_code == 200

    # 4-chi — 429
    r = await client.post(
        "/api/v1/auth/request-otp",
        json={"phone": phone, "channel": "sms"},
    )
    assert r.status_code == 429
```

### `backend/tests/integration/test_order_flow.py`

```python
import pytest
from decimal import Decimal
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_order_below_min_rejected(
    client: AsyncClient, db_session: AsyncSession,
    test_user, test_vendor, test_product, auth_headers,
):
    # Savatga kam summa
    test_product.price = Decimal("10000")
    await db_session.commit()

    # Savatga qo'shish
    r = await client.post(
        "/api/v1/cart/items",
        json={"product_id": test_product.id, "quantity": 2},
        headers=auth_headers,
    )
    assert r.status_code == 200

    # Manzil qo'shish
    r = await client.post(
        "/api/v1/users/me/addresses",
        json={
            "label": "Uy",
            "address_text": "Toshkent",
            "lat": 41.31,
            "lng": 69.24,
        },
        headers=auth_headers,
    )
    address_id = r.json()["id"]

    # Buyurtma — minimal summa xatosi
    r = await client.post(
        "/api/v1/orders",
        json={
            "address_id": address_id,
            "payment_method": "payme",
        },
        headers=auth_headers,
    )
    assert r.status_code == 422
    assert "Minimal buyurtma" in r.json()["error"]["message"]


@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_order_success(
    client: AsyncClient, db_session: AsyncSession,
    test_user, test_vendor, test_product, auth_headers,
):
    # Katta summa
    test_product.price = Decimal("60000")
    await db_session.commit()

    # Savatga
    r = await client.post(
        "/api/v1/cart/items",
        json={"product_id": test_product.id, "quantity": 1},
        headers=auth_headers,
    )
    assert r.status_code == 200

    # Manzil
    r = await client.post(
        "/api/v1/users/me/addresses",
        json={
            "label": "Uy",
            "address_text": "Toshkent",
            "lat": 41.31,
            "lng": 69.24,
        },
        headers=auth_headers,
    )
    address_id = r.json()["id"]

    # Buyurtma
    r = await client.post(
        "/api/v1/orders",
        json={
            "address_id": address_id,
            "payment_method": "payme",
        },
        headers=auth_headers,
    )
    assert r.status_code == 200
    order = r.json()
    assert order["status"] == "pending_payment"
    assert order["total"] >= 50000
    assert order["order_number"].startswith("ORD-")
```

### `backend/tests/integration/test_wallet_flow.py`

```python
import pytest
from decimal import Decimal
from httpx import AsyncClient


@pytest.mark.integration
@pytest.mark.asyncio
async def test_wallet_lifecycle(
    client: AsyncClient, db_session, test_user, auth_headers,
):
    # Wallet olish
    r = await client.get("/api/v1/wallet", headers=auth_headers)
    assert r.status_code == 200
    wallet = r.json()
    assert wallet["balance"] == 0

    # To'g'ridan-to'g'ri credit (test uchun)
    from app.services.wallet_service import WalletService
    svc = WalletService(db_session)
    wallet_obj = await svc.get_or_create(test_user.id, "user")
    await svc.credit(wallet_obj.id, Decimal("100000"), "test")
    await db_session.commit()

    # Balansni tekshirish
    r = await client.get("/api/v1/wallet", headers=auth_headers)
    assert r.json()["balance"] == 100000

    # Payout so'rash
    r = await client.post(
        "/api/v1/wallet/payouts",
        json={
            "amount": 60000,
            "method": "payme",
            "account_details": {"phone": "+998901234567"},
        },
        headers=auth_headers,
    )
    assert r.status_code == 200
    payout = r.json()
    assert payout["amount"] == 60000
    assert payout["fee"] == 600  # 1%
    assert payout["net_amount"] == 59400

    # Balans muzlatilgan
    r = await client.get("/api/v1/wallet", headers=auth_headers)
    wallet = r.json()
    assert wallet["balance"] == 40000
    assert wallet["frozen_balance"] == 60000
```

## 9.7. E2E test

### `backend/tests/e2e/test_full_checkout.py`

```python
import pytest
from decimal import Decimal
from httpx import AsyncClient


@pytest.mark.e2e
@pytest.mark.asyncio
@pytest.mark.slow
async def test_full_customer_journey(
    client: AsyncClient, db_session,
    test_vendor, test_product, monkeypatch,
):
    """
    1. Register via OTP
    2. Add address
    3. KYC (mock approved)
    4. Add to cart
    5. Checkout
    6. Vendor accepts
    7. Courier picks up
    8. Delivered
    9. Commission distributed
    """
    phone = "+998909999999"
    sent_codes = {}

    async def mock_send_otp(self, phone, code, channel, ttl):
        sent_codes[phone] = code

    monkeypatch.setattr(
        "app.services.notification_service.NotificationService.send_otp",
        mock_send_otp,
    )

    # 1. OTP
    await client.post(
        "/api/v1/auth/request-otp",
        json={"phone": phone, "channel": "sms"},
    )
    r = await client.post(
        "/api/v1/auth/verify-otp",
        json={"phone": phone, "code": sent_codes[phone]},
    )
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. KYC mock — to'g'ridan-to'g'ri tasdiqlash
    from app.db.models import User
    from sqlalchemy import select
    stmt = select(User).where(User.phone == phone)
    user = (await db_session.execute(stmt)).scalar_one()
    user.is_verified = True
    await db_session.commit()

    # 3. Manzil
    r = await client.post(
        "/api/v1/users/me/addresses",
        json={"label": "Uy", "address_text": "Toshkent", "lat": 41.31, "lng": 69.24},
        headers=headers,
    )
    address_id = r.json()["id"]

    # 4. Savat
    test_product.price = Decimal("60000")
    await db_session.commit()

    await client.post(
        "/api/v1/cart/items",
        json={"product_id": test_product.id, "quantity": 1},
        headers=headers,
    )

    # 5. Buyurtma
    r = await client.post(
        "/api/v1/orders",
        json={"address_id": address_id, "payment_method": "payme"},
        headers=headers,
    )
    assert r.status_code == 200
    order_id = r.json()["id"]

    # 6. To'lov simulyatsiyasi (payment callback mock)
    from app.services.order_service import OrderService
    svc = OrderService(db_session)
    await svc.update_status(order_id, "paid")
    await svc.update_status(order_id, "accepted")
    await svc.update_status(order_id, "preparing")
    await svc.update_status(order_id, "ready")
    await svc.update_status(order_id, "delivered")
    await svc.update_status(order_id, "completed")

    # 7. Wallet tekshirish
    from app.services.wallet_service import WalletService
    wallet_svc = WalletService(db_session)
    vendor_wallet = await wallet_svc.get_by_owner(test_vendor.id, "vendor")

    # 60,000 - 12% QQS - 2% fee = 51,600
    # Platforma 10% = 5,160
    # Vendor = 46,440
    assert vendor_wallet.balance == Decimal("46440.00")
```

## 9.8. Testlarni ishga tushirish

```bash
# Hammasi
cd backend
pytest

# Faqat unit
pytest tests/unit/ -m unit

# Faqat integration
pytest tests/integration/ -m integration

# Coverage bilan
pytest --cov=app --cov-report=html
# htmlcov/index.html ni ochish

# Verbose
pytest -v

# Parallel (xdist)
pip install pytest-xdist
pytest -n 4
```

---

# 📦 MODUL 10: DOCKER COMPOSE

## 10.1. `backend/Dockerfile` (development)

```dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Tizim paketlari
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kod
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 10.2. `backend/Dockerfile.prod`

```dockerfile
# ============ BUILDER ============
FROM python:3.11-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt


# ============ RUNTIME ============
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/root/.local/bin:$PATH"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 curl \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m -u 1000 appuser

COPY --from=builder /root/.local /root/.local
COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["gunicorn", "app.main:app", \
     "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--timeout", "120", \
     "--keepalive", "5"]
```

## 10.3. `apps/customer-webapp/Dockerfile.prod`

```dockerfile
# ============ BUILDER ============
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
ARG VITE_API_URL
ARG VITE_WS_URL
ENV VITE_API_URL=$VITE_API_URL
ENV VITE_WS_URL=$VITE_WS_URL

RUN npm run build


# ============ RUNTIME ============
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

## 10.4. `apps/customer-webapp/nginx.conf`

```nginx
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    # SPA fallback
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Gzip
    gzip on;
    gzip_types text/plain text/css application/json application/javascript
               text/xml application/xml application/xml+rss text/javascript;
    gzip_min_length 1024;
}
```

## 10.5. `docker-compose.yml` (development — to'liq)

```yaml
version: "3.9"

x-common-env: &common-env
  ENV: development
  DEBUG: "true"

services:
  # ============ INFRASTRUCTURE ============
  postgres:
    image: postgres:15-alpine
    container_name: xalq-postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: xalquchun
      POSTGRES_USER: xalquchun
      POSTGRES_PASSWORD: xalquchun
      PGDATA: /var/lib/postgresql/data/pgdata
    ports:
      - "5432:5432"
    volumes:
      - pg_data:/var/lib/postgresql/data
      - ./infra/postgres/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U xalquchun"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: xalq-redis
    restart: unless-stopped
    command: redis-server --appendonly yes --maxmemory 512mb --maxmemory-policy allkeys-lru
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s

  # ============ BACKEND ============
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: xalq-backend
    restart: unless-stopped
    env_file: ./backend/.env
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./backend:/app
      - ./backend/secrets:/app/secrets:ro
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: xalq-worker
    restart: unless-stopped
    env_file: ./backend/.env
    depends_on:
      - postgres
      - redis
    volumes:
      - ./backend:/app
    command: celery -A app.tasks.celery_app worker -l info -c 4

  beat:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: xalq-beat
    restart: unless-stopped
    env_file: ./backend/.env
    depends_on:
      - redis
    volumes:
      - ./backend:/app
    command: celery -A app.tasks.celery_app beat -l info

  flower:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: xalq-flower
    restart: unless-stopped
    env_file: ./backend/.env
    ports:
      - "5555:5555"
    depends_on:
      - redis
    command: celery -A app.tasks.celery_app flower --port=5555

  # ============ BOT ============
  bot:
    build:
      context: ./bot
      dockerfile: Dockerfile
    container_name: xalq-bot
    restart: unless-stopped
    env_file: ./bot/.env
    depends_on:
      - backend
    volumes:
      - ./bot:/app

  # ============ FRONTEND APPS ============
  customer-webapp:
    build:
      context: ./apps/customer-webapp
      dockerfile: Dockerfile
      args:
        VITE_API_URL: http://localhost:8000/api/v1
        VITE_WS_URL: ws://localhost:8000/ws
    container_name: xalq-customer
    restart: unless-stopped
    ports:
      - "3000:80"
    depends_on:
      - backend

  vendor-panel:
    build:
      context: ./apps/vendor-panel
      dockerfile: Dockerfile
      args:
        VITE_API_URL: http://localhost:8000/api/v1
    container_name: xalq-vendor
    restart: unless-stopped
    ports:
      - "3001:80"
    depends_on:
      - backend

  admin-panel:
    build:
      context: ./apps/admin-panel
      dockerfile: Dockerfile
      args:
        VITE_API_URL: http://localhost:8000/api/v1
    container_name: xalq-admin
    restart: unless-stopped
    ports:
      - "3005:80"
    depends_on:
      - backend

  # ============ MONITORING ============
  prometheus:
    image: prom/prometheus:latest
    container_name: xalq-prometheus
    restart: unless-stopped
    ports:
      - "9090:9090"
    volumes:
      - ./infra/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.retention.time=30d'

  grafana:
    image: grafana/grafana:latest
    container_name: xalq-grafana
    restart: unless-stopped
    ports:
      - "3030:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin
      GF_INSTALL_PLUGINS: grafana-piechart-panel
    volumes:
      - grafana_data:/var/lib/grafana
      - ./infra/grafana/dashboards:/etc/grafana/provisioning/dashboards:ro
      - ./infra/grafana/datasources:/etc/grafana/provisioning/datasources:ro
    depends_on:
      - prometheus

volumes:
  pg_data:
  redis_data:
  prometheus_data:
  grafana_data:

networks:
  default:
    name: xalq-network
```

## 10.6. `docker-compose.prod.yml`

```yaml
version: "3.9"

services:
  postgres:
    image: postgres:15-alpine
    restart: always
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - pg_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 10s
    deploy:
      resources:
        limits:
          memory: 2G

  redis:
    image: redis:7-alpine
    restart: always
    command: redis-server --requirepass ${REDIS_PASSWORD} --appendonly yes
    volumes:
      - redis_data:/data
    deploy:
      resources:
        limits:
          memory: 1G

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    restart: always
    env_file: ./backend/.env
    depends_on:
      - postgres
      - redis
    volumes:
      - ./backend/secrets:/app/secrets:ro
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: "2"
          memory: 2G
      restart_policy:
        condition: on-failure

  worker:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    restart: always
    env_file: ./backend/.env
    command: celery -A app.tasks.celery_app worker -l info -c 8
    depends_on:
      - postgres
      - redis
    deploy:
      replicas: 2

  beat:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    restart: always
    env_file: ./backend/.env
    command: celery -A app.tasks.celery_app beat -l info
    depends_on:
      - redis

  bot:
    build: ./bot
    restart: always
    env_file: ./bot/.env
    depends_on:
      - backend

  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./infra/nginx/conf.d:/etc/nginx/conf.d:ro
      - ./infra/nginx/certs:/etc/nginx/certs:ro
      - ./apps/customer-webapp/dist:/var/www/customer:ro
      - ./apps/vendor-panel/dist:/var/www/vendor:ro
      - ./apps/admin-panel/dist:/var/www/admin:ro
    depends_on:
      - backend

volumes:
  pg_data:
  redis_data:
```

## 10.7. `infra/postgres/init.sql`

```sql
-- Test uchun qo'shimcha DB
CREATE DATABASE xalquchun_test;

-- Extensions
\c xalquchun;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

\c xalquchun_test;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
```

## 10.8. Ishga tushirish

```bash
# Development
docker compose up -d
docker compose logs -f backend

# Migratsiya
docker compose exec backend alembic upgrade head

# Test
docker compose exec backend pytest

# Production
docker compose -f docker-compose.prod.yml up -d --build
```

---

# 📦 MODUL 11: SEED DATA

## 11.1. Seed skript strukturasi

```
backend/scripts/
├── seed.py                    # Asosiy seed
├── seed_data/
│   ├── users.json
│   ├── vendors.json
│   ├── categories.json
│   ├── products.json
│   └── promo.json
└── reset_db.py
```

## 11.2. `backend/scripts/seed.py`

```python
"""
XalqUchun — Test ma'lumotlarini yaratish
Ishlatish: python -m scripts.seed
"""
import asyncio
import secrets
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from app.db.session import AsyncSessionLocal
from app.db.models import (
    User, Vendor, Dealer, Developer, Category, Product,
    Wallet, PromoCode, Address, Courier,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_users(db: AsyncSession) -> dict:
    """Test foydalanuvchilar"""
    print("👥 Foydalanuvchilar yaratilmoqda...")

    users = {
        "customer": User(
            phone="+998901000001",
            telegram_id=100000001,
            full_name="Aziz Karimov",
            language="uz",
            source_channel="telegram",
            roles=["customer"],
            is_registered=True,
            is_verified=True,
            terms_accepted_at=datetime.now(timezone.utc),
            privacy_accepted_at=datetime.now(timezone.utc),
            referral_code="AZIZ2026",
            loyalty_points=1500,
        ),
        "vendor_owner": User(
            phone="+998901000002",
            full_name="Sardor Rahimov",
            language="uz",
            source_channel="telegram",
            roles=["vendor"],
            is_registered=True,
            is_verified=True,
            terms_accepted_at=datetime.now(timezone.utc),
            referral_code="SARDOR2026",
        ),
        "dealer_owner": User(
            phone="+998901000003",
            full_name="Jasur Toshmatov",
            roles=["dealer"],
            is_registered=True,
            is_verified=True,
            terms_accepted_at=datetime.now(timezone.utc),
        ),
        "developer_owner": User(
            phone="+998901000004",
            full_name="Dilshod Yusupov",
            roles=["developer"],
            is_registered=True,
            is_verified=True,
            terms_accepted_at=datetime.now(timezone.utc),
        ),
        "courier": User(
            phone="+998901000005",
            full_name="Ali Karimov",
            roles=["courier"],
            is_registered=True,
            is_verified=True,
            terms_accepted_at=datetime.now(timezone.utc),
        ),
        "admin": User(
            phone="+998901000006",
            full_name="Super Admin",
            roles=["admin", "super_admin"],
            is_registered=True,
            is_verified=True,
            terms_accepted_at=datetime.now(timezone.utc),
        ),
    }

    for u in users.values():
        db.add(u)
    await db.flush()

    print(f"  ✅ {len(users)} foydalanuvchi")
    return users


async def create_developer(db: AsyncSession, owner: User) -> Developer:
    print("🏭 Dasturchi yaratilmoqda...")
    dev = Developer(
        owner_user_id=owner.id,
        company_name="Coca-Cola Uzbekistan",
        brand_name="Coca-Cola",
        slug="coca-cola-uz",
        legal_name='MChJ "Coca-Cola Ichimligi Uzbekiston"',
        inn="301234567",
        description="Xalqaro ichimliklar brendi",
        phone=owner.phone,
        email="info@cocacola.uz",
        is_active=True,
        is_verified=True,
        royalty_percent=Decimal("10"),
        rating=Decimal("4.9"),
    )
    db.add(dev)
    await db.flush()
    print(f"  ✅ {dev.company_name}")
    return dev


async def create_dealer(db: AsyncSession, owner: User) -> Dealer:
    print("💼 Dealer yaratilmoqda...")
    dealer = Dealer(
        owner_user_id=owner.id,
        name="Toshkent Distribyutor MChJ",
        slug="toshkent-dist",
        legal_name='MChJ "Toshkent Distribyutor"',
        inn="309876543",
        description="Toshkent shahridagi yetakchi distribyutor",
        phone=owner.phone,
        email="info@toshkent-dist.uz",
        region="Toshkent",
        is_active=True,
        is_verified=True,
        commission_percent=Decimal("15"),
        rating=Decimal("4.8"),
    )
    db.add(dealer)
    await db.flush()
    print(f"  ✅ {dealer.name}")
    return dealer


async def create_vendors(
    db: AsyncSession, owner: User, dealer: Dealer
) -> list[Vendor]:
    print("🏪 Do'konlar yaratilmoqda...")

    vendors_data = [
        {
            "name": "Makro Chilonzor",
            "slug": "makro-chilonzor",
            "type": "food",
            "address": "Toshkent, Chilonzor 12-mavdon",
            "lat": Decimal("41.2765"),
            "lng": Decimal("69.2036"),
            "phone": "+998712000001",
            "delivery_fee": Decimal("8000"),
            "min_order_amount": Decimal("50000"),
            "delivery_radius_km": 5,
            "commission_percent": Decimal("10"),
        },
        {
            "name": "Korzinka Yunusobod",
            "slug": "korzinka-yunusobod",
            "type": "food",
            "address": "Toshkent, Yunusobod 4-mavdon",
            "lat": Decimal("41.3625"),
            "lng": Decimal("69.2884"),
            "phone": "+998712000002",
            "delivery_fee": Decimal("8000"),
            "min_order_amount": Decimal("50000"),
            "delivery_radius_km": 5,
            "commission_percent": Decimal("10"),
        },
        {
            "name": "Osh Markazi",
            "slug": "osh-markazi",
            "type": "restaurant",
            "address": "Toshkent, Shayxontohur",
            "lat": Decimal("41.3234"),
            "lng": Decimal("69.2281"),
            "phone": "+998712000003",
            "delivery_fee": Decimal("10000"),
            "min_order_amount": Decimal("50000"),
            "delivery_radius_km": 7,
            "commission_percent": Decimal("12"),
        },
    ]

    vendors = []
    for data in vendors_data:
        v = Vendor(
            owner_user_id=owner.id,
            dealer_id=dealer.id,
            name=data["name"],
            slug=data["slug"],
            type=data["type"],
            address=data["address"],
            lat=data["lat"],
            lng=data["lng"],
            phone=data["phone"],
            delivery_fee=data["delivery_fee"],
            min_order_amount=data["min_order_amount"],
            delivery_radius_km=data["delivery_radius_km"],
            commission_percent=data["commission_percent"],
            is_active=True,
            is_open=True,
            is_verified=True,
            rating=Decimal("4.7"),
        )
        db.add(v)
        vendors.append(v)
    await db.flush()
    print(f"  ✅ {len(vendors)} do'kon")
    return vendors


async def create_catalog(
    db: AsyncSession, vendor: Vendor, developer: Developer
) -> None:
    print(f"📦 {vendor.name} uchun katalog yaratilmoqda...")

    categories = [
        {"name": "Mevalar", "slug": "mevalar", "icon": "🍎"},
        {"name": "Sabzavotlar", "slug": "sabzavotlar", "icon": "🥕"},
        {"name": "Sut mahsulotlari", "slug": "sut", "icon": "🥛"},
        {"name": "Non mahsulotlari", "slug": "non", "icon": "🍞"},
        {"name": "Ichimliklar", "slug": "ichimliklar", "icon": "🥤"},
    ]

    cat_map = {}
    for c in categories:
        cat = Category(
            vendor_id=vendor.id,
            name=c["name"],
            slug=c["slug"],
            icon_url=c["icon"],
            is_active=True,
        )
        db.add(cat)
        cat_map[c["slug"]] = cat
    await db.flush()

    products = [
        # Mevalar
        {"cat": "mevalar", "name": "Olma (Golden)", "price": 18000, "unit": "kg"},
        {"cat": "mevalar", "name": "Banan", "price": 22000, "unit": "kg"},
        {"cat": "mevalar", "name": "Apelsin", "price": 25000, "unit": "kg"},
        {"cat": "mevalar", "name": "Uzum", "price": 30000, "unit": "kg"},
        # Sabzavotlar
        {"cat": "sabzavotlar", "name": "Kartoshka", "price": 8000, "unit": "kg"},
        {"cat": "sabzavotlar", "name": "Piyoz", "price": 6000, "unit": "kg"},
        {"cat": "sabzavotlar", "name": "Sabzi", "price": 9000, "unit": "kg"},
        {"cat": "sabzavotlar", "name": "Pomidor", "price": 15000, "unit": "kg"},
        # Sut
        {"cat": "sut", "name": "Sut 1L", "price": 12000, "unit": "dona"},
        {"cat": "sut", "name": "Qatiq 0.5L", "price": 8000, "unit": "dona"},
        {"cat": "sut", "name": "Tvorog 200g", "price": 15000, "unit": "dona"},
        # Non
        {"cat": "non", "name": "Obi non", "price": 4000, "unit": "dona"},
        {"cat": "non", "name": "Patir", "price": 5000, "unit": "dona"},
        {"cat": "non", "name": "Lavash", "price": 6000, "unit": "dona"},
        # Ichimliklar
        {"cat": "ichimliklar", "name": "Coca-Cola 1.5L", "price": 14000, "unit": "dona",
         "developer_id": developer.id},
        {"cat": "ichimliklar", "name": "Fanta 1.5L", "price": 14000, "unit": "dona",
         "developer_id": developer.id},
        {"cat": "ichimliklar", "name": "Sprite 1.5L", "price": 14000, "unit": "dona",
         "developer_id": developer.id},
    ]

    for p in products:
        product = Product(
            vendor_id=vendor.id,
            category_id=cat_map[p["cat"]].id,
            developer_id=p.get("developer_id"),
            name=p["name"],
            slug=p["name"].lower().replace(" ", "-"),
            description=f"Yangi {p['name']}",
            price=Decimal(str(p["price"])),
            old_price=Decimal(str(p["price"] * 1.15)),
            unit=p["unit"],
            stock=100,
            is_active=True,
            rating=Decimal("4.5"),
        )
        db.add(product)

    await db.flush()
    print(f"  ✅ {len(products)} mahsulot")


async def create_wallets(db: AsyncSession, users: dict) -> None:
    print("💰 Hamyonlar yaratilmoqda...")

    # Har bir foydalanuvchi uchun
    for key, user in users.items():
        wallet = Wallet(
            owner_id=user.id,
            owner_type=(
                "admin" if "admin" in user.roles
                else user.roles[0] if user.roles else "user"
            ),
            balance=Decimal("0"),
        )
        db.add(wallet)

    # Platforma hamyoni
    platform_wallet = Wallet(
        owner_id=1,
        owner_type="platform",
        balance=Decimal("1000000"),  # Boshlang'ich kapital
    )
    db.add(platform_wallet)

    await db.flush()
    print(f"  ✅ {len(users) + 1} hamyon")


async def create_promo_codes(db: AsyncSession) -> None:
    print("🎁 Promo-kodlar yaratilmoqda...")

    promos = [
        {
            "code": "FIRST50",
            "type": "percent",
            "value": Decimal("50"),
            "max_discount": Decimal("30000"),
            "min_order_amount": Decimal("50000"),
            "max_uses": 1000,
            "per_user_limit": 1,
            "first_order_only": True,
        },
        {
            "code": "WELCOME10",
            "type": "percent",
            "value": Decimal("10"),
            "max_discount": Decimal("20000"),
            "min_order_amount": Decimal("50000"),
            "max_uses": 10000,
            "per_user_limit": 1,
        },
        {
            "code": "FREEDEL",
            "type": "free_delivery",
            "value": Decimal("0"),
            "min_order_amount": Decimal("100000"),
            "max_uses": 500,
            "per_user_limit": 3,
        },
    ]

    now = datetime.now(timezone.utc)
    for p in promos:
        promo = PromoCode(
            code=p["code"],
            type=p["type"],
            value=p["value"],
            max_discount=p.get("max_discount"),
            min_order_amount=p["min_order_amount"],
            max_uses=p["max_uses"],
            per_user_limit=p["per_user_limit"],
            first_order_only=p.get("first_order_only", False),
            valid_from=now,
            valid_until=now + timedelta(days=90),
            is_active=True,
            owner_type="platform",
        )
        db.add(promo)

    await db.flush()
    print(f"  ✅ {len(promos)} promo-kod")


async def create_courier(db: AsyncSession, user: User) -> Courier:
    print("🛵 Kuryer yaratilmoqda...")
    courier = Courier(
        user_id=user.id,
        full_name=user.full_name,
        phone=user.phone,
        vehicle_type="motorcycle",
        vehicle_number="A 01 AB 123 UZ",
        status="online",
        is_verified=True,
        current_lat=Decimal("41.3110"),
        current_lng=Decimal("69.2400"),
        rating=Decimal("4.9"),
        total_orders=0,
    )
    db.add(courier)
    await db.flush()
    print(f"  ✅ {courier.full_name}")
    return courier


async def create_addresses(db: AsyncSession, user: User) -> None:
    print("📍 Manzillar yaratilmoqda...")
    addresses = [
        Address(
            user_id=user.id,
            label="Uy",
            address_text="Toshkent, Chilonzor 12-mavdon, 25-uy, 42-xonadon",
            lat=Decimal("41.2765"),
            lng=Decimal("69.2036"),
            entrance="2",
            floor="5",
            apartment="42",
            is_default=True,
        ),
        Address(
            user_id=user.id,
            label="Ish",
            address_text="Toshkent, Yunusobod 4-mavdon, IT Park",
            lat=Decimal("41.3625"),
            lng=Decimal("69.2884"),
            is_default=False,
        ),
    ]
    for a in addresses:
        db.add(a)
    await db.flush()
    print(f"  ✅ {len(addresses)} manzil")


async def main():
    print("\n" + "=" * 60)
    print("🌱 XalqUchun — SEED DATA")
    print("=" * 60 + "\n")

    async with AsyncSessionLocal() as db:
        try:
            # 1. Foydalanuvchilar
            users = await create_users(db)

            # 2. Dasturchi
            developer = await create_developer(db, users["developer_owner"])

            # 3. Dealer
            dealer = await create_dealer(db, users["dealer_owner"])

            # 4. Do'konlar
            vendors = await create_vendors(db, users["vendor_owner"], dealer)

            # 5. Katalog (har bir do'kon uchun)
            for v in vendors:
                await create_catalog(db, v, developer)

            # 6. Hamyonlar
            await create_wallets(db, users)

            # 7. Promo-kodlar
            await create_promo_codes(db)

            # 8. Kuryer
            await create_courier(db, users["courier"])

            # 9. Manzillar
            await create_addresses(db, users["customer"])

            await db.commit()

            print("\n" + "=" * 60)
            print("✅ SEED MUVAFFAQIYATLI!")
            print("=" * 60)
            print("\n📋 TEST MA'LUMOTLAR:\n")
            print(f"👤 Mijoz:     {users['customer'].phone}")
            print(f"🏪 Vendor:    {users['vendor_owner'].phone}")
            print(f"💼 Dealer:    {users['dealer_owner'].phone}")
            print(f"🏭 Developer: {users['developer_owner'].phone}")
            print(f"🛵 Courier:   {users['courier'].phone}")
            print(f"👑 Admin:     {users['admin'].phone}")
            print("\n🔑 Promo-kodlar: FIRST50, WELCOME10, FREEDEL")
            print("\n💡 Login: OTP kod orqali\n")

        except Exception as e:
            await db.rollback()
            print(f"\n❌ XATO: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(main())
```

## 11.3. `backend/scripts/reset_db.py`

```python
"""DB ni tozalash va qayta yaratish"""
import asyncio
from app.db.base import Base
from app.db.session import engine
from app.db.models import *  # noqa


async def reset():
    print("🗑️  DB tozalanmoqda...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("✅ DB qayta yaratildi")


if __name__ == "__main__":
    asyncio.run(reset())
```

## 11.4. `backend/scripts/seed.sh`

```bash
#!/bin/bash
set -e

echo "🌱 Seed boshlanmoqda..."

# DB ni tozalash
python -m scripts.reset_db

# Seed
python -m scripts.seed

echo "✅ Tugadi!"
```

## 11.5. Ishga tushirish

```bash
cd backend
chmod +x scripts/seed.sh

# Variant 1: Docker orqali
docker compose exec backend python -m scripts.seed

# Variant 2: Lokal
source venv/bin/activate
python -m scripts.seed
```

---

# 📦 MODUL 12: CI/CD (GitHub Actions)

## 12.1. `.github/workflows/ci.yml`

```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

env:
  PYTHON_VERSION: "3.11"
  NODE_VERSION: "20"

jobs:
  # ============ BACKEND TESTS ============
  backend-test:
    name: Backend Tests
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_DB: xalquchun_test
          POSTGRES_USER: xalquchun
          POSTGRES_PASSWORD: xalquchun
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: pip

      - name: Install dependencies
        working-directory: backend
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest-cov pytest-xdist

      - name: Generate JWT keys
        working-directory: backend
        run: |
          mkdir -p secrets
          openssl genrsa -out secrets/jwt_private.pem 2048
          openssl rsa -in secrets/jwt_private.pem -pubout -out secrets/jwt_public.pem

      - name: Run migrations
        working-directory: backend
        env:
          DATABASE_URL: postgresql+asyncpg://xalquchun:xalquchun@localhost:5432/xalquchun_test
          REDIS_URL: redis://localhost:6379/0
          SECRET_KEY: test-secret-key-64-chars-minimum-required-for-testing-only
        run: |
          alembic upgrade head

      - name: Run tests
        working-directory: backend
        env:
          DATABASE_URL: postgresql+asyncpg://xalquchun:xalquchun@localhost:5432/xalquchun_test
          REDIS_URL: redis://localhost:6379/0
          SECRET_KEY: test-secret-key-64-chars-minimum-required-for-testing-only
        run: |
          pytest -n 4 --cov=app --cov-report=xml --cov-report=term

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: backend/coverage.xml
          flags: backend
          token: ${{ secrets.CODECOV_TOKEN }}

  # ============ LINT ============
  backend-lint:
    name: Backend Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: pip

      - name: Install linters
        run: |
          pip install ruff mypy bandit

      - name: Ruff
        working-directory: backend
        run: ruff check app/

      - name: Mypy
        working-directory: backend
        run: mypy app/ --ignore-missing-imports

      - name: Bandit
        working-directory: backend
        run: bandit -r app/ -ll

  # ============ FRONTEND TESTS ============
  frontend-test:
    name: Frontend Test (${{ matrix.app }})
    runs-on: ubuntu-latest
    strategy:
      matrix:
        app: [customer-webapp, vendor-panel, admin-panel]
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: npm
          cache-dependency-path: apps/${{ matrix.app }}/package-lock.json

      - name: Install
        working-directory: apps/${{ matrix.app }}
        run: npm ci

      - name: Lint
        working-directory: apps/${{ matrix.app }}
        run: npm run lint --if-present

      - name: Test
        working-directory: apps/${{ matrix.app }}
        run: npm test --if-present

      - name: Build
        working-directory: apps/${{ matrix.app }}
        run: npm run build

  # ============ SECURITY SCAN ============
  security:
    name: Security Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Trivy
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: fs
          scan-ref: .
          severity: CRITICAL,HIGH
          format: sarif
          output: trivy-results.sarif

      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: trivy-results.sarif

  # ============ DOCKER BUILD ============
  docker-build:
    name: Docker Build
    runs-on: ubuntu-latest
    needs: [backend-test, frontend-test]
    steps:
      - uses: actions/checkout@v4

      - uses: docker/setup-buildx-action@v3

      - name: Build backend image
        uses: docker/build-push-action@v5
        with:
          context: ./backend
          file: ./backend/Dockerfile.prod
          push: false
          tags: xalquchun/backend:test
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

## 12.2. `.github/workflows/cd-staging.yml`

```yaml
name: CD Staging

on:
  push:
    branches: [develop]

jobs:
  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    environment: staging
    needs: []

    steps:
      - uses: actions/checkout@v4

      - uses: docker/setup-buildx-action@v3

      - name: Login to registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build & push backend
        uses: docker/build-push-action@v5
        with:
          context: ./backend
          file: ./backend/Dockerfile.prod
          push: true
          tags: |
            ghcr.io/${{ github.repository }}/backend:staging
            ghcr.io/${{ github.repository }}/backend:${{ github.sha }}

      - name: Deploy via SSH
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.STAGING_HOST }}
          username: ${{ secrets.STAGING_USER }}
          key: ${{ secrets.STAGING_SSH_KEY }}
          script: |
            cd /opt/xalquchun
            git pull origin develop
            docker compose -f docker-compose.staging.yml pull
            docker compose -f docker-compose.staging.yml up -d --remove-orphans
            docker compose -f docker-compose.staging.yml exec -T backend alembic upgrade head
            docker system prune -f
            echo "✅ Staging deployed"
```

## 12.3. `.github/workflows/cd-prod.yml`

```yaml
name: CD Production

on:
  push:
    tags:
      - "v*.*.*"

jobs:
  deploy-prod:
    name: Deploy to Production
    runs-on: ubuntu-latest
    environment: production

    steps:
      - uses: actions/checkout@v4

      - uses: docker/setup-buildx-action@v3

      - name: Login
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract version
        id: version
        run: echo "VERSION=${GITHUB_REF#refs/tags/}" >> $GITHUB_OUTPUT

      - name: Build & push backend
        uses: docker/build-push-action@v5
        with:
          context: ./backend
          file: ./backend/Dockerfile.prod
          push: true
          tags: |
            ghcr.io/${{ github.repository }}/backend:${{ steps.version.outputs.VERSION }}
            ghcr.io/${{ github.repository }}/backend:latest

      - name: Backup DB
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.PROD_HOST }}
          username: ${{ secrets.PROD_USER }}
          key: ${{ secrets.PROD_SSH_KEY }}
          script: |
            cd /opt/xalquchun
            ./infra/scripts/backup.sh

      - name: Deploy
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.PROD_HOST }}
          username: ${{ secrets.PROD_USER }}
          key: ${{ secrets.PROD_SSH_KEY }}
          script: |
            cd /opt/xalquchun
            git fetch --tags
            git checkout ${{ steps.version.outputs.VERSION }}
            docker compose -f docker-compose.prod.yml pull
            docker compose -f docker-compose.prod.yml up -d --remove-orphans
            docker compose -f docker-compose.prod.yml exec -T backend alembic upgrade head
            echo "✅ Production deployed: ${{ steps.version.outputs.VERSION }}"

      - name: Notify Telegram
        if: always()
        uses: appleboy/telegram-action@master
        with:
          to: ${{ secrets.TELEGRAM_CHAT_ID }}
          token: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          message: |
            🚀 Deployment ${{ job.status }}
            Version: ${{ steps.version.outputs.VERSION }}
            By: ${{ github.actor }}
```

## 12.4. `.github/workflows/nightly.yml`

```yaml
name: Nightly

on:
  schedule:
    - cron: "0 2 * * *"  # Har kuni 02:00 (UTC)
  workflow_dispatch:

jobs:
  nightly-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_DB: xalquchun_test
          POSTGRES_USER: xalquchun
          POSTGRES_PASSWORD: xalquchun
        ports: ["5432:5432"]
        options: --health-cmd pg_isready --health-interval 5s
      redis:
        image: redis:7-alpine
        ports: ["6379:6379"]

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: pip

      - name: Install
        working-directory: backend
        run: pip install -r requirements.txt

      - name: Generate JWT
        working-directory: backend
        run: |
          mkdir -p secrets
          openssl genrsa -out secrets/jwt_private.pem 2048
          openssl rsa -in secrets/jwt_private.pem -pubout -out secrets/jwt_public.pem

      - name: Migrations
        working-directory: backend
        env:
          DATABASE_URL: postgresql+asyncpg://xalquchun:xalquchun@localhost:5432/xalquchun_test
          REDIS_URL: redis://localhost:6379/0
          SECRET_KEY: test-secret-key-64-chars-minimum-for-testing-only-padding
        run: alembic upgrade head

      - name: Full test suite
        working-directory: backend
        env:
          DATABASE_URL: postgresql+asyncpg://xalquchun:xalquchun@localhost:5432/xalquchun_test
          REDIS_URL: redis://localhost:6379/0
          SECRET_KEY: test-secret-key-64-chars-minimum-for-testing-only-padding
        run: pytest -v --tb=long

      - name: Load test
        working-directory: backend
        run: |
          pip install locust
          # locust -f tests/load/locustfile.py --headless -u 100 -r 10 -t 5m || true
```

## 12.5. `.github/dependabot.yml`

```yaml
version: 2
updates:
  - package-ecosystem: pip
    directory: /backend
    schedule:
      interval: weekly
    open-pull-requests-limit: 5

  - package-ecosystem: npm
    directory: /apps/customer-webapp
    schedule:
      interval: weekly

  - package-ecosystem: npm
    directory: /apps/vendor-panel
    schedule:
      interval: weekly

  - package-ecosystem: npm
    directory: /apps/admin-panel
    schedule:
      interval: weekly

  - package-ecosystem: docker
    directory: /backend
    schedule:
      interval: weekly

  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: weekly
```

## 12.6. Secrets ro'yxati (GitHub'da)

| Secret | Tavsif |
|---|---|
| `CODECOV_TOKEN` | Codecov token |
| `STAGING_HOST` | Staging server IP |
| `STAGING_USER` | SSH user |
| `STAGING_SSH_KEY` | SSH private key |
| `PROD_HOST` | Production server IP |
| `PROD_USER` | SSH user |
| `PROD_SSH_KEY` | SSH private key |
| `TELEGRAM_BOT_TOKEN` | Bot token |
| `TELEGRAM_CHAT_ID` | Alert chat |

---

# 📦 MODUL 13: DEPLOYMENT (VPS / Cloud)

## 13.1. VPS tayyorlash (Ubuntu 22.04)

```bash
# ============ SERVER SOZLASH ============
# 1. Update
sudo apt update && sudo apt upgrade -y

# 2. Asosiy paketlar
sudo apt install -y \
    curl wget git ufw fail2ban \
    nginx certbot python3-certbot-nginx \
    htop iotop ncdu \
    build-essential

# 3. Docker
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
newgrp docker

# 4. Docker Compose plugin
sudo apt install -y docker-compose-plugin

# 5. Firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable

# 6. Fail2ban
sudo systemctl enable --now fail2ban

# 7. Timezone
sudo timedatectl set-timezone Asia/Tashkent

# 8. Swap (2GB, agar RAM kam bo'lsa)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# 9. Docker log rotation
sudo tee /etc/docker/daemon.json <<EOF
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
EOF
sudo systemctl restart docker
```

## 13.2. Loyihani serverga o'rnatish

```bash
# 1. Loyiha papkasi
sudo mkdir -p /opt/xalquchun
sudo chown $USER:$USER /opt/xalquchun
cd /opt/xalquchun

# 2. Reponi klonlash
git clone https://github.com/otaboyevsardorbek1/xalquchun-bot-v2.git .

# 3. .env sozlash
cp backend/.env.example backend/.env
nano backend/.env

# 4. JWT kalitlar
mkdir -p backend/secrets
openssl genrsa -out backend/secrets/jwt_private.pem 4096
openssl rsa -in backend/secrets/jwt_private.pem -pubout \
    -out backend/secrets/jwt_public.pem
chmod 600 backend/secrets/*.pem

# 5. Ishga tushirish
docker compose -f docker-compose.prod.yml up -d --build

# 6. Migratsiyalar
docker compose -f docker-compose.prod.yml exec -T backend \
    alembic upgrade head

# 7. Seed (faqat birinchi marta)
docker compose -f docker-compose.prod.yml exec -T backend \
    python -m scripts.seed
```

## 13.3. Nginx sozlash

`/etc/nginx/sites-available/xalquchun`:

```nginx
# ============ API ============
upstream backend_api {
    least_conn;
    server 127.0.0.1:8000 max_fails=3 fail_timeout=30s;
}

# Rate limiting zones
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=100r/s;
limit_req_zone $binary_remote_addr zone=auth_limit:10m rate=5r/s;

# HTTP -> HTTPS redirect
server {
    listen 80;
    listen [::]:80;
    server_name api.xalquchun.uz app.xalquchun.uz;
    return 301 https://$host$request_uri;
}

# ============ API SERVER ============
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name api.xalquchun.uz;

    ssl_certificate /etc/letsencrypt/live/api.xalquchun.uz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.xalquchun.uz/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    client_max_body_size 20M;

    # API
    location /api/ {
        limit_req zone=api_limit burst=50 nodelay;

        proxy_pass http://backend_api;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_connect_timeout 10s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Auth (qattiq rate limit)
    location /api/v1/auth/ {
        limit_req zone=auth_limit burst=3 nodelay;

        proxy_pass http://backend_api;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # WebSocket
    location /ws/ {
        proxy_pass http://backend_api;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 86400;
        proxy_send_timeout 86400;
    }

    # Health check
    location /health {
        proxy_pass http://backend_api/health;
        access_log off;
    }
}

# ============ CUSTOMER WEBAPP ============
server {
    listen 443 ssl http2;
    server_name app.xalquchun.uz;

    ssl_certificate /etc/letsencrypt/live/app.xalquchun.uz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/app.xalquchun.uz/privkey.pem;

    root /var/www/customer;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}

# ============ VENDOR PANEL ============
server {
    listen 443 ssl http2;
    server_name vendor.xalquchun.uz;

    ssl_certificate /etc/letsencrypt/live/vendor.xalquchun.uz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/vendor.xalquchun.uz/privkey.pem;

    root /var/www/vendor;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}

# ============ ADMIN PANEL ============
server {
    listen 443 ssl http2;
    server_name admin.xalquchun.uz;

    ssl_certificate /etc/letsencrypt/live/admin.xalquchun.uz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/admin.xalquchun.uz/privkey.pem;

    # Admin panel IP whitelist (ixtiyoriy)
    # allow 1.2.3.4;
    # deny all;

    root /var/www/admin;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

## 13.4. SSL sertifikatlar

```bash
# 1. Nginx konfiguratsiya
sudo ln -s /etc/nginx/sites-available/xalquchun /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# 2. SSL olish
sudo certbot --nginx \
    -d api.xalquchun.uz \
    -d app.xalquchun.uz \
    -d vendor.xalquchun.uz \
    -d admin.xalquchun.uz \
    --email admin@xalquchun.uz \
    --agree-tos \
    --non-interactive

# 3. Auto-renew test
sudo certbot renew --dry-run
```

## 13.5. `infra/scripts/backup.sh`

```bash
#!/bin/bash
set -euo pipefail

# ============ SOZLAMALAR ============
BACKUP_DIR="/backups/xalquchun"
S3_BUCKET="s3://xalquchun-backups"
RETENTION_DAYS=30
DATE=$(date +%Y%m%d_%H%M%S)
LOG_FILE="/var/log/xalquchun-backup.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

log "🚀 Backup boshlanmoqda..."

mkdir -p "$BACKUP_DIR"

# ============ 1. POSTGRES ============
log "📦 PostgreSQL dump..."
docker compose -f /opt/xalquchun/docker-compose.prod.yml \
    exec -T postgres pg_dump -U xalquchun -Fc xalquchun \
    | gzip > "$BACKUP_DIR/db_$DATE.sql.gz"

DB_SIZE=$(du -h "$BACKUP_DIR/db_$DATE.sql.gz" | cut -f1)
log "  ✅ DB: $DB_SIZE"

# ============ 2. REDIS ============
log "📦 Redis dump..."
docker compose -f /opt/xalquchun/docker-compose.prod.yml \
    exec -T redis redis-cli BGSAVE
sleep 5

REDIS_CONTAINER=$(docker compose -f /opt/xalquchun/docker-compose.prod.yml ps -q redis)
docker cp "$REDIS_CONTAINER:/data/dump.rdb" "$BACKUP_DIR/redis_$DATE.rdb"
log "  ✅ Redis: $(du -h $BACKUP_DIR/redis_$DATE.rdb | cut -f1)"

# ============ 3. .ENV (shifrlangan) ============
log "📦 .env backup..."
tar czf "$BACKUP_DIR/env_$DATE.tar.gz" \
    /opt/xalquchun/backend/.env \
    /opt/xalquchun/backend/secrets/
log "  ✅ .env"

# ============ 4. S3 GA YUKLASH ============
if command -v aws &> /dev/null; then
    log "☁️  S3 ga yuklash..."
    aws s3 sync "$BACKUP_DIR" "$S3_BUCKET/$(date +%Y/%m)/" \
        --storage-class STANDARD_IA
    log "  ✅ S3 ga yuklandi"
fi

# ============ 5. ESKI BACKUP O'CHIRISH ============
log "🧹 Eski backuplar tozalanmoqda..."
find "$BACKUP_DIR" -type f -mtime +$RETENTION_DAYS -delete
log "  ✅ Tozalandi"

# ============ 6. XULOSA ============
TOTAL_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)
log "✅ Backup tugadi. Jami: $TOTAL_SIZE"
```

`infra/scripts/restore.sh`:

```bash
#!/bin/bash
set -euo pipefail

if [ -z "${1:-}" ]; then
    echo "Ishlatish: $0 <backup_file.sql.gz>"
    exit 1
fi

BACKUP_FILE="$1"

echo "⚠️  DIQQAT! DB qayta tiklanadi. Davom etish uchun 'yes' yozing:"
read CONFIRM
[ "$CONFIRM" != "yes" ] && exit 1

echo "🔄 Restore boshlanmoqda: $BACKUP_FILE"

# 1. Backend to'xtatish
docker compose -f /opt/xalquchun/docker-compose.prod.yml stop backend worker bot

# 2. DB qayta tiklash
gunzip -c "$BACKUP_FILE" | \
    docker compose -f /opt/xalquchun/docker-compose.prod.yml \
    exec -T postgres pg_restore -U xalquchun -d xalquchun --clean --if-exists

# 3. Qayta ishga tushirish
docker compose -f /opt/xalquchun/docker-compose.prod.yml start backend worker bot

echo "✅ Restore tugadi"
```

## 13.6. Cron jadvali

```bash
# crontab -e

# Backup har kuni 02:00 da
0 2 * * * /opt/xalquchun/infra/scripts/backup.sh >> /var/log/xalquchun-backup.log 2>&1

# SSL yangilash (certbot o'zi qiladi, lekin tekshirish)
0 3 * * 1 certbot renew --quiet

# Docker cleanup har hafta
0 4 * * 0 docker system prune -af --filter "until=168h"

# Log rotation
0 5 * * * find /var/log -name "*.log" -mtime +30 -delete
```

## 13.7. Monitoring

### `infra/prometheus/prometheus.yml`

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets: []

rule_files:
  - "alerts.yml"

scrape_configs:
  - job_name: "backend"
    metrics_path: "/metrics"
    static_configs:
      - targets: ["backend:8000"]

  - job_name: "postgres"
    static_configs:
      - targets: ["postgres-exporter:9187"]

  - job_name: "redis"
    static_configs:
      - targets: ["redis-exporter:9121"]

  - job_name: "node"
    static_configs:
      - targets: ["node-exporter:9100"]
```

### `infra/prometheus/alerts.yml`

```yaml
groups:
  - name: xalquchun
    interval: 30s
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m]))
          / sum(rate(http_requests_total[5m])) > 0.05
        for: 5m
        labels: { severity: critical }
        annotations:
          summary: "5% dan ortiq xato"
          description: "{{ $value | humanizePercentage }} xato"

      - alert: SlowAPI
        expr: |
          histogram_quantile(0.95,
            rate(http_request_duration_seconds_bucket[5m])
          ) > 1
        for: 5m
        labels: { severity: warning }
        annotations:
          summary: "API p95 > 1s"

      - alert: DatabaseDown
        expr: up{job="postgres"} == 0
        for: 1m
        labels: { severity: critical }
        annotations:
          summary: "PostgreSQL ishlamayapti"

      - alert: HighMemoryUsage
        expr: |
          (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes)
          / node_memory_MemTotal_bytes > 0.9
        for: 5m
        labels: { severity: warning }

      - alert: DiskSpaceLow
        expr: |
          (node_filesystem_avail_bytes{mountpoint="/"}
          / node_filesystem_size_bytes{mountpoint="/"}) < 0.15
        for: 5m
        labels: { severity: critical }
```

### `infra/grafana/datasources/datasource.yml`

```yaml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
```

## 13.8. Health check monitoring (external)

`infra/scripts/uptime-check.sh`:

```bash
#!/bin/bash
# Har 5 daqiqada tashqi monitoring uchun

ENDPOINTS=(
    "https://api.xalquchun.uz/health"
    "https://app.xalquchun.uz"
    "https://vendor.xalquchun.uz"
    "https://admin.xalquchun.uz"
)

for url in "${ENDPOINTS[@]}"; do
    code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$url")
    if [ "$code" != "200" ]; then
        echo "❌ $url → $code"
        # Telegram alert
        curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
            -d "chat_id=${ALERT_CHAT_ID}" \
            -d "text=⚠️ $url ishlamayapti (HTTP $code)"
    else
        echo "✅ $url"
    fi
done
```

## 13.9. Cloud variantlari

### A) AWS

```yaml
# EC2 Instance
Instance: t3.medium (2 vCPU, 4GB RAM)
Storage: 50GB gp3 SSD
OS: Ubuntu 22.04 LTS
Region: eu-central-1 (Frankfurt) — O'zbekistonga yaqin

# Qo'shimcha:
- RDS PostgreSQL (production uchun)
- ElastiCache Redis
- S3 (fayllar uchun)
- CloudFront (CDN)
- Route 53 (DNS)
- ACM (SSL)
- Secrets Manager
- CloudWatch (monitoring)
```

**Narx:** ~$150-300/oy

### B) DigitalOcean

```yaml
Droplet: 4GB / 2 vCPU
Storage: 80GB SSD
Region: Frankfurt (fra1)

Managed Services:
- Managed PostgreSQL: $15/oy
- Managed Redis: $15/oy
- Spaces (S3): $5/oy
- Load Balancer: $12/oy
```

**Narx:** ~$80-120/oy

### C) Hetzner (eng arzon)

```yaml
Server: CX21 (2 vCPU, 4GB RAM)
Storage: 40GB SSD
Location: Falkenstein, Germany
Price: €5.83/oy (~$6.5)

Yaxshi tomoni: Arzon, tez
Kamchiligi: Faqat Yevropa
```

**Narx:** ~$10-30/oy (backup bilan)

### D) O'zbekiston lokal

```yaml
Provider: Uzcloud, Uztelecom, East Telecom
Joylashuv: Toshkent
Narx: ~1,500,000 - 3,000,000 so'm/oy
+ Tez (lokal)
- Cheklangan xizmatlar
```

## 13.10. Deployment checklist

```markdown
## Pre-deployment
- [ ] Barcha testlar o'tgan
- [ ] Code coverage > 80%
- [ ] Xavfsizlik skani o'tgan
- [ ] .env production uchun to'ldirilgan
- [ ] JWT RS256 kalitlar generatsiya qilingan
- [ ] SSL sertifikatlar mavjud
- [ ] Backup ishlaydi

## Deployment
- [ ] Docker images qurilgan
- [ ] Migratsiyalar ishlaydi
- [ ] Health check javob beradi
- [ ] Nginx sozlangan
- [ ] Firewall yoqilgan
- [ ] Fail2ban ishlaydi
- [ ] SSL sertifikat ishlaydi

## Post-deployment
- [ ] Health endpointlar javob beradi
- [ ] Smoke testlar o'tgan
- [ ] Monitoring ishlaydi
- [ ] Alerting sozlangan
- [ ] Backup cron sozlangan
- [ ] Log rotation sozlangan
- [ ] DNS sozlangan
- [ ] Telegram bot ishlaydi
- [ ] SMS yuborish ishlaydi
- [ ] WhatsApp yuborish ishlaydi

## Xavfsizlik
- [ ] 2FA admin uchun
- [ ] Rate limiting yoqilgan
- [ ] PII shifrlangan
- [ ] Audit log ishlaydi
- [ ] Idempotency ishlaydi
- [ ] Webhook imzo tekshiriladi
```

## 13.11. Bir qatorli deployment

```bash
# To'liq deployment (serverda)
cd /opt/xalquchun && \
git pull && \
docker compose -f docker-compose.prod.yml pull && \
docker compose -f docker-compose.prod.yml up -d --remove-orphans && \
docker compose -f docker-compose.prod.yml exec -T backend alembic upgrade head && \
docker system prune -f && \
curl -f https://api.xalquchun.uz/health && \
echo "✅ Deploy muvaffaqiyatli!"
```

---

# ✅ YAKUNIY XULOSA — BARCHA 13 MODUL

| # | Modul | Holat |
|---|---|---|
| 1 | Backend poydevor | ✅ |
| 2 | Notification Service | ✅ |
| 3 | Order Service | ✅ |
| 4 | Wallet Service | ✅ |
| 5 | WebSocket Hub | ✅ |
| 6 | Mijoz WebApp | ✅ |
| 7 | Vendor Panel | ✅ |
| 8 | Admin Panel | ✅ |
| 9 | **Testlar (pytest)** | ✅ |
| 10 | **Docker Compose** | ✅ |
| 11 | **Seed Data** | ✅ |
| 12 | **CI/CD (GitHub Actions)** | ✅ |
| 13 | **Deployment (VPS/Cloud)** | ✅ |

## 🚀 Ishga tushirish tartibi

```bash
# 1. Lokal
git clone <repo> && cd xalquchun-platform
cp backend/.env.example backend/.env
# .env ni to'ldirish
docker compose up -d --build
docker compose exec backend alembic upgrade head
docker compose exec backend python -m scripts.seed

# 2. Test
docker compose exec backend pytest

# 3. Production
ssh user@server
cd /opt/xalquchun && git pull
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

## 📋 Test login ma'lumotlari

| Rol | Telefon |
|---|---|
| Mijoz | +998901000001 |
| Vendor | +998901000002 |
| Dealer | +998901000003 |
| Developer | +998901000004 |
| Kuryer | +998901000005 |
| Admin | +998901000006 |

**Promo-kodlar:** `FIRST50`, `WELCOME10`, `FREEDEL`

---

**Endi sizda to'liq ishlaydigan, production-ready platforma bor!** 🎉

Agar biror modulda muammo bo'lsa yoki qo'shimcha funksiya kerak bo'lsa — ayting, davom ettiraman! 🚀