import express from "express";
import session from "express-session";
import { OpenAI } from "openai";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();

app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "../views"));
app.use(express.urlencoded({ extended: true }));

app.use(
  session({
    secret: process.env.SESSION_SECRET || "your-secret-key",
    resave: false,
    saveUninitialized: true,
  })
);

function getClient(req) {
  const apiKey = req.session.OPENAI_API_KEY;
  if (!apiKey) return null;
  return new OpenAI({ apiKey });
}

async function translate(req, text, target_lang = "en", src_lang = "ko") {
  if (!text.trim()) return "";
  const client = getClient(req);
  if (!client) return "API 키가 필요합니다.";
  const prompt = `다음 문장을 ${src_lang}에서 ${target_lang}로 번역해 주세요. 번역결과만 출력해.\n문장: ${text}, 번역결과: `;
  const response = await client.chat.completions.create({
    model: "gpt-4o",
    messages: [{ role: "user", content: prompt }],
    max_tokens: 1000,
  });
  return response.choices[0].message.content.trim();
}

app.get("/set_api_key", (req, res) => {
  res.render("set_api_key");
});

app.post("/set_api_key", (req, res) => {
  req.session.OPENAI_API_KEY = req.body.api_key;
  res.redirect("/");
});

app.get("/", (req, res) => {
  if (!req.session.OPENAI_API_KEY) return res.redirect("/set_api_key");
  res.render("index", { translated: "", text: "", src_lang: "ko", lang: "en" });
});

app.post("/", async (req, res) => {
  if (!req.session.OPENAI_API_KEY) return res.redirect("/set_api_key");
  const { text, src_lang, lang } = req.body;
  const translated = await translate(req, text, lang, src_lang);
  res.render("index", { translated, text, src_lang, lang });
});

export default app; 