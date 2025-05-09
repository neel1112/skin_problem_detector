from flask import Flask, request, Response
from flask.templating import render_template
from flask import request
from werkzeug.utils import secure_filename
from app import app
import torch
from PIL import Image
import torchvision.transforms as T
import os
import json




def predict(model, img, tr, classes):
    img_tensor = tr(img)
    out = model(img_tensor.unsqueeze(0))
    pred, idx = torch.max(out, 1)
    return classes[idx]

def get_transforms():
    transform = []
    transform.append(T.Resize((512, 512)))
    transform.append(T.ToTensor())
    return T.Compose(transform)


@app.route('/', methods=['GET'])
def np_page():
    # Render the k.html file
    return render_template('start.html')



@app.route('/hello', methods=['GET'])
def hello_page():
    # Render the k.html file
    return render_template('hello.html')


    
@app.route('/npbhai', methods=['GET'])
def npbhai():
    latest_message = ''
    try:
        with open('latest_message.txt', 'r', encoding='utf-8') as f:
            latest_message = f.read().strip()
    except FileNotFoundError:
        pass
    # Render the k.html file
    return render_template('home1.html', latest_message=latest_message)


    
@app.route('/about', methods=['GET'])
def about():
    # Render the k.html file
    return render_template('about.html')
        
@app.route('/skin', methods=['GET'])
def skin():
    # Render the k.html file
    return render_template('skin .html')
        
@app.route('/team', methods=['GET'])
def team():
    # Render the k.html file
    return render_template('team.html')
        
@app.route('/contect', methods=['GET'])
def contect():
    # Render the k.html file
    return render_template('contect.html')



    




@app.route('/np', methods=['GET', 'POST'])
def home_page():
    res = None
    from flask import jsonify
    if request.method == 'POST':
        classes = ['acanthosis-nigricans',
                'acne',
                'acne-scars',
                'alopecia-areata',
                'dry',
                'melasma',
                'oily',
                'vitiligo',
                'warts']
        f = request.files['file']
        filename = secure_filename(f.filename)
        path = os.path.join(app.config['UPLOAD_PATH'], filename)
        f.save(path)
       
        model = torch.load('./skin-model-pokemon.pt', map_location=torch.device('cpu'), weights_only=False)
        device = torch.device('cpu')
        model.to(device)
        img = Image.open(path).convert("RGB")
        tr = get_transforms()
        res = predict(model, img, tr, classes)
        # If AJAX, return JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'res': res})
        else:
            # If not AJAX, render the template with result
            return render_template("index.html", res=res)
    # Fallback to normal render (GET)
    return render_template("index.html", res=res)

@app.route('/k', methods=['GET'])
def k_page():
    # Render the k.html file
    return render_template('k.html')

@app.route('/hair', methods=['GET'])
def hairpage():
  
    return render_template('hair.html')

# Newsletter subscription route
@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    if email:
        with open('subscribers.txt', 'a') as f:
            f.write(email + '\n')
    latest_message = ''
    try:
        with open('latest_message.txt', 'r', encoding='utf-8') as f:
            latest_message = f.read().strip()
    except FileNotFoundError:
        pass
    return render_template('home1.html', message='Thank you for subscribing!', latest_message=latest_message)

# Data page to show subscribers and contact us submissions
@app.route('/data', methods=['GET'])
def data_page():
    subscribers = []
    contact_submissions = []
    try:
        with open('subscribers.txt', 'r') as f:
            subscribers = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        pass
    try:
        import json
        with open('contact_submissions.json', 'r', encoding='utf-8') as f:
            contact_submissions = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        contact_submissions = []
    return render_template('data.html', subscribers=subscribers, contact_submissions=contact_submissions)

# Route to send a message to subscribers (admin action)
@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form.get('message')
    if message:
        with open('latest_message.txt', 'w', encoding='utf-8') as f:
            f.write(message)
    subscribers = []
    try:
        with open('subscribers.txt', 'r') as f:
            subscribers = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        pass
    return render_template('data.html', subscribers=subscribers, msg_sent=True)

# Route to send an individual message to a subscriber
@app.route('/send_message_individual', methods=['POST'])
def send_message_individual():
    email = request.form.get('email')
    message = request.form.get('message')
    if email and message:
        # Load or create the messages file
        messages = {}
        try:
            with open('individual_messages.json', 'r', encoding='utf-8') as f:
                messages = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            messages = {}
        messages[email] = message
        with open('individual_messages.json', 'w', encoding='utf-8') as f:
            json.dump(messages, f)
    subscribers = []
    try:
        with open('subscribers.txt', 'r') as f:
            subscribers = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        pass
    return render_template('data.html', subscribers=subscribers, msg_sent=True)

# Endpoint to get an individual message for a given email (AJAX)
@app.route('/get_individual_message')
def get_individual_message():
    from flask import jsonify
    email = request.args.get('email')
    message = ''
    if email:
        try:
            with open('individual_messages.json', 'r', encoding='utf-8') as f:
                messages = json.load(f)
                message = messages.get(email, '')
        except (FileNotFoundError, json.JSONDecodeError):
            message = ''
    return jsonify({'message': message})

# Add a route to handle contact us form submissions and store them
@app.route('/contact_submit', methods=['POST'])
def contact_submit():
    # Get all form fields
    name = request.form.get('name')
    email = request.form.get('email')
    location = request.form.get('location')
    number = request.form.get('number')
    reason = request.form.get('reason')
    message = request.form.get('message')
    subscribe = request.form.get('subscribe')
    callback = request.form.get('callback')
    # Prepare the submission dict
    submission = {
        'name': name,
        'email': email,
        'location': location,
        'number': number,
        'reason': reason,
        'message': message,
        'subscribe': bool(subscribe),
        'callback': bool(callback)
    }
    # Save to JSON file (append mode)
    import json
    try:
        with open('contact_submissions.json', 'r', encoding='utf-8') as f:
            submissions = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        submissions = []
    submissions.append(submission)
    with open('contact_submissions.json', 'w', encoding='utf-8') as f:
        json.dump(submissions, f, indent=2)
    # Optionally, handle newsletter subscription
    if subscribe:
        try:
            with open('subscribers.txt', 'a') as f:
                f.write(email + '\n')
        except Exception:
            pass
    return render_template('contect.html', success=True)
