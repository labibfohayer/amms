# AMMS (Al Modina Madrasah Management System) - ডেপ্লয়মেন্ট গাইড

এই গাইডটিতে AMMS প্রজেক্টকে প্রোডাকশনে (Render এবং Vercel) ডেপ্লয় করার সম্পূর্ণ ধাপসমূহ বর্ণনা করা হলো।

## ১. GitHub রিপোজিটরি তৈরি (GitHub Repository)
১. [GitHub](https://github.com/)-এ লগইন করুন এবং একটি নতুন Repository তৈরি করুন।
২. আপনার প্রজেক্ট ফোল্ডারে টার্মিনাল ওপেন করুন (যেখানে `.gitignore` ফাইলটি আছে):
```bash
git init
git add .
git commit -m "Initial commit for production"
git branch -M main
git remote add origin https://github.com/your-username/your-repo-name.git
git push -u origin main
```

## ২. রেন্ডার (Render) এ ব্যাকএন্ড ডেপ্লয়মেন্ট
১. [Render](https://render.com/)-এ লগইন করুন এবং Dashboard থেকে **New > PostgreSQL** এ ক্লিক করুন। ডাটাবেসের একটি নাম দিন এবং Create করুন।
২. ডাটাবেস তৈরি হয়ে গেলে এর **Internal Database URL** কপি করে রাখুন।
৩. আবার **New > Web Service** এ ক্লিক করুন এবং আপনার GitHub রিপোজিটরিটি কানেক্ট করুন।
৪. Web Service এর সেটিংস নিচের মত দিন:
   - **Name**: amms-backend (বা আপনার পছন্দমত)
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn config.wsgi:application`
৫. **Environment Variables** এ গিয়ে নিচের ভ্যালুগুলো দিন:
   - `ENVIRONMENT` = `production`
   - `SECRET_KEY` = (যে কোনো একটি সিক্রেট কি বা দীর্ঘ টেক্সট)
   - `DATABASE_URL` = (আগে কপি করা Internal Database URL)
   - `WHATSAPP_SERVICE_URL` = (এটি আপাতত খালি রাখুন বা যদি পাবলিক আইপি থাকে তবে সেটি দিন)
   - `WHATSAPP_NUMBER` = (আপনার হোয়াটসঅ্যাপ নাম্বার)
৬. Deploy এ ক্লিক করুন। কিছুক্ষণ পর ব্যাকএন্ড লাইভ হয়ে যাবে।

## ৩. ভার্সেল (Vercel) এ ফ্রন্টএন্ড ডেপ্লয়মেন্ট
১. [Vercel](https://vercel.com/)-এ লগইন করুন এবং **Add New > Project** এ ক্লিক করে আপনার GitHub রিপোজিটরিটি ইমপোর্ট করুন।
২. Framework Preset হিসেবে **Next.js** নির্বাচন করুন।
৩. **Root Directory** হিসেবে `frontend` ফোল্ডারটি সিলেক্ট করুন।
৪. **Environment Variables** অংশে নিচের ভ্যালুটি দিন:
   - `NEXT_PUBLIC_API_URL` = `https://আপনার-render-backend-url.onrender.com` (আপনার Render ব্যাকএন্ডের আসল URL দিন)
৫. Deploy এ ক্লিক করুন।

## ৪. লোকালি হোয়াটসঅ্যাপ সার্ভিস (WhatsApp Service) রান করা
১. আপনার পিসিতে `whatsapp-service` ফোল্ডারে যান।
২. ডিপেন্ডেন্সি ইন্সটল করুন: `npm install`
৩. সার্ভিসটি রান করুন: `npm start`
৪. টার্মিনালে একটি QR কোড আসবে, সেটি হোয়াটসঅ্যাপ অ্যাপ দিয়ে স্ক্যান করুন।

## ৫. অ্যান্ড্রয়েড ফোনে PWA (Progressive Web App) ইন্সটল করা
১. অ্যান্ড্রয়েড ফোনের Chrome ব্রাউজারে আপনার Vercel ফ্রন্টএন্ড লিংকে যান।
২. মেনু (৩ ডট) থেকে **"Add to Home Screen"** বা **"Install App"** অপশনে ক্লিক করুন।
৩. অ্যাপটি আপনার ফোনের হোম স্ক্রিনে একটি সাধারণ অ্যাপের মতই দেখা যাবে এবং ব্যবহার করা যাবে।
