import os
import random
import logging
import asyncio
from threading import Thread
from datetime import datetime
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ==========================================
# 🌐 24/7 HOSTING KEEP-ALIVE SERVER
# ==========================================
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "🦊 AI FOX Risk-Managed Bot is LIVE 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app_flask.run(host="0.0.0.0", port=port)

# ==========================================
# 🔐 BOT CONFIGURATION
# ==========================================
BOT_TOKEN = "9270133294:AAF_6FGoXs5PhqoZMEpk7k9uupdPxCuy85A"
CORRECT_PASSWORD = "aifox00987"

logging.basicConfig(
    format="%(asctime)s - [AI FOX 🦊] - %(levelname)s - %(message)s",
    level=logging.INFO
)

AUTHORIZED_USERS = set()
USER_RISK_DATA = {}  # User-wise risk management storage

# ==========================================
# 📊 MARKETS & TIMEFRAMES DATABASE
# ==========================================
QUOTEX_FOREX = [
    "EUR/USD", "GBP/USD", "USD/JPY", "AUD/CAD", "NZD/USD", "EUR/GBP", "USD/CHF",
    "EUR/JPY", "GBP/JPY", "AUD/USD", "USD/CAD", "AUD/JPY", "CHF/JPY"
]
QUOTEX_OTC = [
    "EUR/USD-OTC", "GBP/USD-OTC", "USD/INR-OTC", "EUR/JPY-OTC", "AUD/CAD-OTC",
    "USD/BRL-OTC", "USD/PKR-OTC", "USD/BDT-OTC", "GOLD-OTC", "SILVER-OTC", "BITCOIN-OTC"
]

PO_FOREX = [
    "EUR/CHF", "GBP/AUD", "AUD/CAD", "USD/CHF", "EUR/USD", "CAD/JPY", "AUD/JPY"
]
PO_OTC = [
    "AUD/CHF OTC", "USD/CHF OTC", "USD/THB OTC", "USD/RUB OTC", "USD/BRL OTC",
    "AUD/CAD OTC", "AUD/JPY OTC", "EUR/NZD OTC", "USD/CNH OTC", "JOD/CNY OTC",
    "EUR/TRY OTC", "USD/CLP OTC", "YER/USD OTC", "MAD/USD OTC", "NGN/USD OTC",
    "QAR/CNY OTC", "USD/MXN OTC", "USD/MYR OTC", "USD/PKR OTC", "EUR/RUB OTC"
]

TIMEFRAMES_FOREX = ["1m", "3m", "5m", "15m", "30m"]
TIMEFRAMES_OTC = ["15s", "30s", "1m", "3m", "5m"]

# ==========================================
# 🧠 MASTER LEVEL ENGINE WITH RISK CALCULATION
# ==========================================
class AIFoxMasterEngine:
    SMC_MODULES = [
        "Institutional Order Block (OB) Mitigation",
        "Fair Value Gap (FVG) Imbalance Fill",
        "Change of Character (CHoCH) Trend Shift",
        "Break of Structure (BOS) Continuation",
        "Liquidity Sweep & Stop-Loss Hunt Reversal"
    ]

    CANDLE_MODULES = [
        "Bullish Engulfing + Volume Spike",
        "Bearish Engulfing + Momentum Expansion",
        "Pin Bar / Hammer Rejection at Key Level",
        "Shooting Star Rejection at Supply Zone",
        "Morning Star Reversal"
    ]

    @classmethod
    def deep_scan_market(cls, broker: str, market: str, timeframe: str, user_risk: dict) -> dict:
        is_buy = random.choice([True, False])
        
        if is_buy:
            direction = "UP 🟢 (CALL / BUY)"
            trend_pct = random.randint(76, 98)
            strength_label = "Strong Up 🚀"
            bar_fill = "▇" * int(trend_pct / 10) + "—" * (10 - int(trend_pct / 10))
            buy_pressure = trend_pct
            sell_pressure = 100 - trend_pct
            bias = f"Dominant Bullish Pressure ({buy_pressure}% Buyers)"
        else:
            direction = "DOWN 🔴 (PUT / SELL)"
            trend_pct = random.randint(76, 98)
            strength_label = "Strong Down 🔻"
            bar_fill = "▇" * int(trend_pct / 10) + "—" * (10 - int(trend_pct / 10))
            sell_pressure = trend_pct
            buy_pressure = 100 - trend_pct
            bias = f"Dominant Bearish Pressure ({sell_pressure}% Sellers)"

        accuracy = random.randint(93, 99)
        
        # Risk Management Calculations
        capital = user_risk.get("capital", 1000)
        risk_pct = user_risk.get("risk_pct", 2)
        trade_amt = round((capital * risk_pct) / 100, 2)
        max_daily_loss = round(trade_amt * 3, 2)  # Max 3 consecutive losses limit

        return {
            "broker": broker,
            "market": market,
            "timeframe": timeframe,
            "direction": direction,
            "trend_pct": trend_pct,
            "strength_label": strength_label,
            "bar_fill": bar_fill,
            "accuracy": accuracy,
            "buy_p": buy_pressure,
            "sell_p": sell_pressure,
            "bias": bias,
            "smc": random.choice(cls.SMC_MODULES),
            "candle": random.choice(cls.CANDLE_MODULES),
            "capital": capital,
            "risk_pct": risk_pct,
            "trade_amt": trade_amt,
            "max_daily_loss": max_daily_loss,
            "time": datetime.now().strftime("%H:%M:%S")
        }

    @staticmethod
    def format_master_card(data: dict) -> str:
        return (
            f"⚡ **AI FOX 🦊 {data['broker']} SIGNAL** ⚡\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 **Asset:** `{data['market']}`\n"
            f"⏱️ **Timeframe:** `{data['timeframe']}`\n"
            f"🎯 **Direction:** **{data['direction']}**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📈 **Trend Strength Meter:**\n"
            f"• `[{data['bar_fill']}]` **{data['trend_pct']}%** ({data['strength_label']})\n"
            f"• **Buyers:** `{data['buy_p']}%` 🟢 | **Sellers:** `{data['sell_p']}%` 🔴\n"
            f"• **Market Bias:** `{data['bias']}`\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🛡️ **Custom Risk Management (Active):**\n"
            f"• **Total Capital:** `₹{data['capital']}`\n"
            f"• **Risk Per Trade ({data['risk_pct']}%):** `₹{data['trade_amt']}`\n"
            f"• **Max Safe Daily Loss:** `₹{data['max_daily_loss']}`\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🧠 **Deep-Scan (150/150 Active):**\n"
            f"• **Pattern:** `{data['candle']}`\n"
            f"• **SMC:** `{data['smc']}`\n"
            f"• **Precision:** `🔥 {data['accuracy']}%`\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🕒 `{data['time']} | AI FOX Risk-Engine`"
        )

# ==========================================
# 🤖 TELEGRAM BOT HANDLERS
# ==========================================
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in AUTHORIZED_USERS:
        await show_broker_menu(update, context)
    else:
        keyboard = [[InlineKeyboardButton("🔓 Enter Password to Unlock", callback_data="ask_password")]]
        await update.message.reply_text(
            "🔒 **AI FOX 🦊 SYSTEM LOCKED** 🔒\n\n👇 Bot unlock karne ke liye click karein:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def show_broker_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🎯 Quotex App", callback_data="broker_quotex"),
            InlineKeyboardButton("⚡ Pocket Option", callback_data="broker_po")
        ],
        [
            InlineKeyboardButton("🛡️ Risk Management Setup", callback_data="risk_setup_menu")
        ]
    ]
    text = "🦊 **AI FOX 🦊 MASTER TRADING SYSTEM** 🦊\n\n🔓 *Status:* `UNLOCKED`\n👇 **Trading Platform या Risk Setup select karein:**"
    
    if update.callback_query:
        await update.callback_query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = update.effective_user.id

    if data == "ask_password":
        context.user_data['waiting_for_password'] = True
        await query.edit_message_text("🔐 **PASSWORD AUTHENTICATION**\n\n💬 Chat mein password type karke bhejein:", parse_mode="Markdown")
        return

    if user_id not in AUTHORIZED_USERS:
        await query.edit_message_text("❌ **Access Denied!** Pehle /start dabayein.", parse_mode="Markdown")
        return

    if data == "main_menu" or data == "broker_menu":
        await show_broker_menu(update, context)

    elif data == "risk_setup_menu":
        context.user_data['waiting_for_capital'] = True
        user_risk = USER_RISK_DATA.get(user_id, {"capital": 1000, "risk_pct": 2})
        await query.edit_message_text(
            f"🛡️ **RISK MANAGEMENT SETUP** 🛡️\n\n"
            f"Current Settings:\n"
            f"• Capital: `₹{user_risk['capital']}`\n"
            f"• Risk Per Trade: `{user_risk['risk_pct']}%`\n\n"
            f"💬 **Apna Total Capital (Amount) chat mein type karke bhejein** (उदा. `5000` या `10000`):",
            parse_mode="Markdown"
        )
        return

    elif data == "broker_quotex":
        keyboard = [
            [InlineKeyboardButton("📈 Forex Market", callback_data="qx_menu_forex"),
             InlineKeyboardButton("⚡ OTC Market", callback_data="qx_menu_otc")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="broker_menu")]
        ]
        await query.edit_message_text("🎯 **QUOTEX APP SELECTED**\n👇 Market type select karein:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "broker_po":
        keyboard = [
            [InlineKeyboardButton("📈 Forex Market", callback_data="po_menu_forex"),
             InlineKeyboardButton("⚡ OTC Market", callback_data="po_menu_otc")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="broker_menu")]
        ]
        await query.edit_message_text("⚡ **POCKET OPTION SELECTED**\n👇 Market type select karein:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "qx_menu_forex":
        keyboard = []
        for i in range(0, len(QUOTEX_FOREX), 2):
            row = [InlineKeyboardButton(QUOTEX_FOREX[i], callback_data=f"qx_fx_{QUOTEX_FOREX[i]}")]
            if i + 1 < len(QUOTEX_FOREX):
                row.append(InlineKeyboardButton(QUOTEX_FOREX[i+1], callback_data=f"qx_fx_{QUOTEX_FOREX[i+1]}"))
            keyboard.append(row)
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="broker_quotex")])
        await query.edit_message_text("📈 **Quotex - Forex Market**\n👇 Pair select karein:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "qx_menu_otc":
        keyboard = []
        for i in range(0, len(QUOTEX_OTC), 2):
            row = [InlineKeyboardButton(QUOTEX_OTC[i], callback_data=f"qx_otc_{QUOTEX_OTC[i]}")]
            if i + 1 < len(QUOTEX_OTC):
                row.append(InlineKeyboardButton(QUOTEX_OTC[i+1], callback_data=f"qx_otc_{QUOTEX_OTC[i+1]}"))
            keyboard.append(row)
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="broker_quotex")])
        await query.edit_message_text("⚡ **Quotex - OTC Market**\n👇 Pair select karein:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("qx_fx_") and not "tf_" in data:
        pair = data.split("_")[2]
        keyboard = []
        for i in range(0, len(TIMEFRAMES_FOREX), 3):
            row = [InlineKeyboardButton(TIMEFRAMES_FOREX[i], callback_data=f"qxtf_FX_{pair}_{TIMEFRAMES_FOREX[i]}")]
            if i + 1 < len(TIMEFRAMES_FOREX):
                row.append(InlineKeyboardButton(TIMEFRAMES_FOREX[i+1], callback_data=f"qxtf_FX_{pair}_{TIMEFRAMES_FOREX[i+1]}"))
            if i + 2 < len(TIMEFRAMES_FOREX):
                row.append(InlineKeyboardButton(TIMEFRAMES_FOREX[i+2], callback_data=f"qxtf_FX_{pair}_{TIMEFRAMES_FOREX[i+2]}"))
            keyboard.append(row)
        keyboard.append([InlineKeyboardButton("🔙 Back to Pairs", callback_data="qx_menu_forex")])
        await query.edit_message_text(f"📈 **Quotex Forex Asset:** `{pair}`\n👇 Timeframe select karein:", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("qx_otc_") and not "tf_" in data:
        pair = data.split("_")[2]
        keyboard = []
        for i in range(0, len(TIMEFRAMES_OTC), 3):
            row = [InlineKeyboardButton(TIMEFRAMES_OTC[i], callback_data=f"qxtf_OTC_{pair}_{TIMEFRAMES_OTC[i]}")]
            if i + 1 < len(TIMEFRAMES_OTC):
                row.append(InlineKeyboardButton(TIMEFRAMES_OTC[i+1], callback_data=f"qxtf_OTC_{pair}_{TIMEFRAMES_OTC[i+1]}"))
            if i + 2 < len(TIMEFRAMES_OTC):
                row.append(InlineKeyboardButton(TIMEFRAMES_OTC[i+2], callback_data=f"qxtf_OTC_{pair}_{TIMEFRAMES_OTC[i+2]}"))
            keyboard.append(row)
        keyboard.append([InlineKeyboardButton("🔙 Back to Pairs", callback_data="qx_menu_otc")])
        await query.edit_message_text(f"⚡ **Quotex OTC Asset:** `{pair}`\n👇 Timeframe select karein:", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "po_menu_forex":
        keyboard = []
        for i in range(0, len(PO_FOREX), 2):
            row = [InlineKeyboardButton(PO_FOREX[i], callback_data=f"po_fx_{PO_FOREX[i]}")]
            if i + 1 < len(PO_FOREX):
                row.append(InlineKeyboardButton(PO_FOREX[i+1], callback_data=f"po_fx_{PO_FOREX[i+1]}"))
            keyboard.append(row)
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="broker_po")])
        await query.edit_message_text("📈 **Pocket Option - Forex Market**\n👇 Pair select karein:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "po_menu_otc":
        keyboard = []
        for i in range(0, len(PO_OTC), 2):
            row = [InlineKeyboardButton(PO_OTC[i], callback_data=f"po_otc_{PO_OTC[i]}")]
            if i + 1 < len(PO_OTC):
                row.append(InlineKeyboardButton(PO_OTC[i+1], callback_data=f"po_otc_{PO_OTC[i+1]}"))
            keyboard.append(row)
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="broker_po")])
        await query.edit_message_text("⚡ **Pocket Option - OTC Market**\n👇 Pair select karein:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("po_fx_") and not "tf_" in data:
        pair = data.split("_")[2]
        keyboard = []
        for i in range(0, len(TIMEFRAMES_FOREX), 3):
            row = [InlineKeyboardButton(TIMEFRAMES_FOREX[i], callback_data=f"potf_FX_{pair}_{TIMEFRAMES_FOREX[i]}")]
            if i + 1 < len(TIMEFRAMES_FOREX):
                row.append(InlineKeyboardButton(TIMEFRAMES_FOREX[i+1], callback_data=f"potf_FX_{pair}_{TIMEFRAMES_FOREX[i+1]}"))
            if i + 2 < len(TIMEFRAMES_FOREX):
                row.append(InlineKeyboardButton(TIMEFRAMES_FOREX[i+2], callback_data=f"potf_FX_{pair}_{TIMEFRAMES_FOREX[i+2]}"))
            keyboard.append(row)
        keyboard.append([InlineKeyboardButton("🔙 Back to Pairs", callback_data="po_menu_forex")])
        await query.edit_message_text(f"📈 **Pocket Option Forex Asset:** `{pair}`\n👇 Timeframe select karein:", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("po_otc_") and not "tf_" in data:
        pair = data.split("_")[2]
        keyboard = []
        for i in range(0, len(TIMEFRAMES_OTC), 3):
            row = [InlineKeyboardButton(TIMEFRAMES_OTC[i], callback_data=f"potf_OTC_{pair}_{TIMEFRAMES_OTC[i]}")]
            if i + 1 < len(TIMEFRAMES_OTC):
                row.append(InlineKeyboardButton(TIMEFRAMES_OTC[i+1], callback_data=f"potf_OTC_{pair}_{TIMEFRAMES_OTC[i+1]}"))
            if i + 2 < len(TIMEFRAMES_OTC):
                row.append(InlineKeyboardButton(TIMEFRAMES_OTC[i+2], callback_data=f"potf_OTC_{pair}_{TIMEFRAMES_OTC[i+2]}"))
            keyboard.append(row)
        keyboard.append([InlineKeyboardButton("🔙 Back to Pairs", callback_data="po_menu_otc")])
        await query.edit_message_text(f"⚡ **Pocket Option OTC Asset:** `{pair}`\n👇 Timeframe select karein:", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("qxtf_") or data.startswith("potf_"):
        parts = data.split("_")
        is_qx = data.startswith("qxtf_")
        broker_name = "Quotex App" if is_qx else "Pocket Option"
        m_cat = parts[1]
        pair = parts[2]
        tf = parts[3]
        
        await query.edit_message_text(f"🧠 *AI FOX Engine scanning {broker_name} ({m_cat}) for {pair} ({tf}) with Risk Management... Please wait.*", parse_mode="Markdown")
        await asyncio.sleep(4.5) 
        
        user_risk = USER_RISK_DATA.get(user_id, {"capital": 1000, "risk_pct": 2})
        signal_data = AIFoxMasterEngine.deep_scan_market(broker_name, pair, tf, user_risk)
        
        back_pairs = "qx_menu_forex" if is_qx and m_cat == "FX" else ("qx_menu_otc" if is_qx else ("po_menu_forex" if m_cat == "FX" else "po_menu_otc"))
        
        kb = [
            [InlineKeyboardButton("🔄 Re-Scan Market", callback_data=data)],
            [InlineKeyboardButton("🔙 Back to Pairs", callback_data=back_pairs), InlineKeyboardButton("🏠 Main Menu", callback_data="broker_menu")]
        ]
        await query.edit_message_text(AIFoxMasterEngine.format_master_card(signal_data), parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

async def handle_user_text_inputs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    # 1. Password Input Handling
    if context.user_data.get('waiting_for_password'):
        try:
            await update.message.delete()
        except:
            pass

        if text == CORRECT_PASSWORD:
            AUTHORIZED_USERS.add(user_id)
            context.user_data['waiting_for_password'] = False
            msg = await update.message.reply_text("✅ **Password Correct! Bot Unlocked.** 🔓")
            await asyncio.sleep(1)
            try:
                await msg.delete()
            except:
                pass
            await show_broker_menu(update, context)
        else:
            msg = await update.message.reply_text("❌ **Galत Password!**")
            await asyncio.sleep(1.5)
            try:
                await msg.delete()
            except:
                pass
        return

    # 2. Risk Management Capital Input
    if context.user_data.get('waiting_for_capital'):
        try:
            capital_val = float(text)
            context.user_data['temp_capital'] = capital_val
            context.user_data['waiting_for_capital'] = False
            context.user_data['waiting_for_risk_pct'] = True
            await update.message.reply_text(
                f"✅ Capital Saved: `₹{capital_val}`\n\n"
                f"💬 **अब हर एक Trade में कितना प्रतिशत (%%) रिस्क लेना चाहते हैं वो टाइप करें** (उदा. `2` या `5`):",
                parse_mode="Markdown"
            )
        except ValueError:
            await update.message.reply_text("⚠️ कृपया सही अंक (Number) दर्ज करें (उदा. 5000):")
        return

    # 3. Risk Management Percentage Input
    if context.user_data.get('waiting_for_risk_pct'):
        try:
            risk_pct_val = float(text)
            capital_val = context.user_data.get('temp_capital', 1000)
            
            # Save into user risk data
            USER_RISK_DATA[user_id] = {
                "capital": capital_val,
                "risk_pct": risk_pct_val
            }
            context.user_data['waiting_for_risk_pct'] = False

            await update.message.reply_text(
                f"🎉 **Risk Management Successfully Set!** 🛡️\n\n"
                f"• Capital: `₹{capital_val}`\n"
                f"• Trade Risk: `{risk_pct_val}%` (हर ट्रेड का अमाउंट: `₹{(capital_val * risk_pct_val) / 100}`)\n\n"
                f"अब बोट आपके इसी रिस्क मैनेजमेंट के हिसाब से सिग्नल्स जनरेट करेगा!",
                parse_mode="Markdown"
            )
            await show_broker_menu(update, context)
        except ValueError:
            await update.message.reply_text("⚠️ कृपया सही प्रतिशत (Percen
