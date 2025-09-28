import express from "express";
import fetch from "node-fetch";

const app = express();
app.use(express.json());

const seenLinks = new Set();
const BOT_TOKEN = process.env.8466271055:AAFJHcvJ3WR2oAI7g1Xky2760qLgM68WXMM;
const TELEGRAM_API = `https://api.telegram.org/bot${BOT_TOKEN}`;

async function sendMessage(chatId, text) {
  await fetch(`${TELEGRAM_API}/sendMessage`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ chat_id: chatId, text }),
  });
}

app.post("/api/webhook", async (req, res) => {
  const message = req.body.message;
  if (!message) return res.send("ok");

  const chatId = message.chat.id;
  const text = message.text || "";

  const urls = text.match(/https?:\/\/\S+/g) || [];
  for (let url of urls) {
    if (seenLinks.has(url)) {
      await sendMessage(chatId, `重复粉 ❌❌\n${url}`);
    } else {
      seenLinks.add(url);
      await sendMessage(chatId, `正常粉 ✅✅\n${url}`);
    }
  }

  res.send("ok");
});

export default app;
