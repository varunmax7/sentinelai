# 🌐 MaxAlert AI - Public Access via Ngrok

## Your Public URL
**https://adele-unfocused-scientistically.ngrok-free.dev**

This URL is now live and accessible from any device worldwide!

## 📱 Access Instructions

### From Any Device:
1. Open your browser (Chrome, Safari, Firefox, etc.)
2. Navigate to: **https://adele-unfocused-scientistically.ngrok-free.dev**
3. You may see an ngrok warning page - click "Visit Site" to continue
4. You'll see the MaxAlert AI login page

### Test Accounts:
Use these accounts to test the application:

**Coordinator/Official Account:**
- Username: `maxx` or `demo` or `varunmax7`
- Password: (your password)

**Volunteer Account:**
- Username: `varunmax7` or `demo` or `maxx`
- Password: (your password)

## 🧪 Testing the Volunteer Assignment Feature

### Step 1: Login as Coordinator
1. Go to: https://adele-unfocused-scientistically.ngrok-free.dev/login
2. Login with coordinator account
3. Navigate to: Volunteer Management

### Step 2: Assign a Volunteer
1. Click "Assign to Hazard" tab
2. Select a hazard from dropdown
3. Click "Assign Volunteer" button
4. You should see success modal

### Step 3: Check Notification (on different device)
1. On another device (phone/tablet), open the same URL
2. Login as the volunteer you just assigned
3. Go to Notifications
4. You should see the assignment notification
5. Click Accept or Decline

## 📊 Features to Test

### ✅ Volunteer Management
- Register as volunteer
- View all volunteers
- Assign volunteers to hazards
- Track volunteer status

### ✅ Notifications
- Receive assignment notifications
- Accept/Decline assignments
- View notification history

### ✅ Hazard Reporting
- Submit hazard reports
- View hazard feed
- Comment on reports
- Like/View reports

### ✅ Emergency Management
- Create emergency events
- Manage resources
- Coordinate responses

## 🔧 Technical Details

### Ngrok Configuration
- **Local Port:** 5001
- **Public URL:** https://adele-unfocused-scientistically.ngrok-free.dev
- **Protocol:** HTTPS (secure)
- **Status:** Running

### Ngrok Web Interface
You can monitor ngrok traffic at:
- **http://localhost:4040**

This shows:
- All HTTP requests
- Response times
- Request/Response details
- Traffic statistics

## 🚨 Important Notes

### 1. Ngrok Free Tier Limitations
- ⚠️ URL changes when ngrok restarts
- ⚠️ Session expires after 2 hours (free tier)
- ⚠️ Limited to 40 connections/minute
- ⚠️ Warning page before accessing site

### 2. Security Considerations
- ✅ HTTPS encryption enabled
- ⚠️ Don't share sensitive data on free tier
- ⚠️ URL is publicly accessible
- ✅ Flask session security still applies

### 3. Performance
- Response time may be slower than localhost
- Depends on your internet connection
- Ngrok adds ~50-200ms latency

## 🔄 Restarting Ngrok

If ngrok stops or you need to restart:

```bash
/Users/ramavathvarun/Desktop/AlertAI/ngrok http 5001
```

The URL will change, so you'll need to share the new URL.

## 📱 QR Code Access

You can create a QR code for easy mobile access:
1. Go to: https://www.qr-code-generator.com/
2. Enter: https://adele-unfocused-scientistically.ngrok-free.dev
3. Generate and scan with your phone

## 🐛 Troubleshooting

### Issue: "Site can't be reached"
**Solution:**
1. Check if Flask app is running: `ps aux | grep "python app.py"`
2. Check if ngrok is running: `ps aux | grep ngrok`
3. Restart ngrok if needed

### Issue: "Tunnel not found"
**Solution:**
1. Ngrok session expired (2 hour limit on free tier)
2. Restart ngrok: `/Users/ramavathvarun/Desktop/AlertAI/ngrok http 5001`
3. Share new URL

### Issue: Slow response times
**Solution:**
1. This is normal with ngrok free tier
2. Upgrade to paid plan for better performance
3. Or use for testing only

### Issue: "ERR_NGROK_802"
**Solution:**
1. Check ngrok authentication: `ngrok config check`
2. Re-authenticate if needed: `ngrok config add-authtoken YOUR_TOKEN`
3. Get token from: https://dashboard.ngrok.com/get-started/your-authtoken

## 📞 Share with Team

Send this message to your team:

```
🌐 MaxAlert AI is now live!

Access the app from any device:
https://adele-unfocused-scientistically.ngrok-free.dev

Test the new volunteer assignment feature:
1. Login as coordinator
2. Go to Volunteer Management → Assign to Hazard
3. Assign a volunteer
4. Login as volunteer on another device
5. Check notifications and accept/decline

Note: You may see an ngrok warning - just click "Visit Site"
```

## 🎯 Next Steps

1. **Test on mobile devices**
   - Test volunteer assignment flow
   - Check notifications on mobile
   - Verify responsive design

2. **Share with stakeholders**
   - Send the URL to team members
   - Gather feedback
   - Test with real users

3. **Monitor usage**
   - Check ngrok dashboard: http://localhost:4040
   - Monitor Flask logs in terminal
   - Track any errors

## 📈 Upgrade Options

For production use, consider:
- **Ngrok Paid Plan:** Custom domain, no session limits
- **Cloud Hosting:** AWS, Google Cloud, Heroku
- **VPS:** DigitalOcean, Linode
- **Cloudflare Tunnel:** Free alternative to ngrok

## ⚡ Quick Commands

**Start ngrok:**
```bash
/Users/ramavathvarun/Desktop/AlertAI/ngrok http 5001
```

**Check ngrok status:**
```bash
ps aux | grep ngrok
```

**Stop ngrok:**
```bash
pkill ngrok
```

**View ngrok dashboard:**
```bash
open http://localhost:4040
```

---

**Status:** ✅ LIVE
**URL:** https://adele-unfocused-scientistically.ngrok-free.dev
**Started:** 2026-01-25 20:26:17 IST
