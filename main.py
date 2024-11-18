from flask import Flask, request, jsonify, send_from_directory
import re
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Serve the ai-plugin.json file
@app.route("/ai-plugin.json")
def serve_manifest():
    return send_from_directory(os.getcwd(), "ai-plugin.json")

# Serve the openapi.yaml file
@app.route("/openapi.yaml")
def serve_openapi():
    return send_from_directory(os.getcwd(), "openapi.yaml")

# Serve the logo image (photo.png)
@app.route("/photo.png")
def serve_logo():
    return send_from_directory(os.getcwd(), "photo.png")

# Function to rewrite messages based on the selected accent
def rewrite_message(message, style):
    # Normalize the input by replacing spaces with underscores
    style = style.replace(" ", "_").lower()

    accents = {
        "yard_talk": f"Wah gwan, mi say: {message}",
        "tdot_slang": f"Yo fam, what you sayin’? {message}",
        "east_end_banter": f"Alright, mate? {message}, innit?",
        "aussie_chatter": f"G’day, mate! {message}, no worries!",
        "nyc_hustle": f"Yo, whatchu talkin’ ‘bout? {message}, kid!",
        "dublin_craic": f"Ah sure, it’s grand! {message}, let’s grab a pint!",
        "highland_hype": f"Aye, laddie, {message}, ye ken?",
        "parisian_twist": f"Allo, mon ami! {message}, oui?",
        "bollywood_buzz": f"Arrey yaar, {message}, haan?",
        "yall_drawl": f"Well, bless your heart! {message}, y’all.",
        "mzansi_mix": f"Eish, my bru, {message}, neh?",
        "rasta_vibes": f"Bless up, I-man say: {message}, seen?",
        "moscow_street_talk": f"Da, my friend, {message}, yes?",
        "tex_mex_twang": f"Hola, amigo! {message}, por favor!",
        "cajun_speak": f"Laissez les bons temps rouler! {message}, cher.",
        "norwegian_nordic": f"Hei, venn! {message}, ikke sant?",
        "berlin_beat": f"Hallo, mein Freund! {message}, ja?",
        "tokyo_talk": f"Konnichiwa! {message}, ne?",
        "mumbai_street_style": f"Aree baap re! {message}, kya bolta hai?",
        "italian_flair": f"Ciao, bella! {message}, capisce?",
        "brazilian_beat": f"Opa! {message}, tudo bem?",
        "new_zealand_zing": f"Cheers, mate! {message}, sweet as!",
        "caribbean_creole": f"Mwen di sa: {message}, wi?",
        "arabian_accent": f"As-salamu alaykum! {message}, insha’Allah.",
        "chinese_mandarin_influence": f"Nǐ hǎo! {message}, duì ma?",
        "korean_pop_vibe": f"Annyeong! {message}, jinjja?",
        "spanish_lilt": f"¡Hola! {message}, ¿verdad?",
        "swahili_swag": f"Jambo! {message}, sawa?",
        "canadian_francophone": f"Salut, mon ami! {message}, eh?"
    }
    return accents.get(
        style, f"Style not recognized. Here’s your message: {message}"
    )

@app.route("/", methods=["GET"])
def home():
    guide = {
        "message": "Welcome to the Accent Switch API. Use the available routes to interact with the plugin.",
        "instructions": "Enter your prompt in the format: '<your message> in <style>'.",
        "example_request": "I am heading to the store in tdot_slang",
    }
    return jsonify(guide), 200

@app.route("/rewrite", methods=["POST"])
def rewrite():
    try:
        data = request.json
        prompt = data.get("prompt", "")
        match = re.match(r'^(.*)\s+in\s+(\w+)$', prompt.strip(), re.IGNORECASE)
        if not match:
            return jsonify({
                "error": "Invalid format. Please use: '<your message> in <style>'"
            }), 400

        message = match.group(1).strip()
        style = match.group(2).strip().lower()

        if not message:
            return jsonify({"error": "Message cannot be empty."}), 400

        rewritten_message = rewrite_message(message, style)
        return jsonify({"rewritten_message": rewritten_message}), 200

    except Exception as e:
        return jsonify({
            "rewritten_message": f"Error occurred. Here’s your message: {prompt}"
        }), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)