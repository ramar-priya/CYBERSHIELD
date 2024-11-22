from flask import Flask, render_template, request, send_file, redirect, url_for
import os
import subprocess
from fpdf import FPDF
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import requests
import socket
import dns.resolver
import dns.reversename

app = Flask(__name__)

class WebCrawler:
    def __init__(self):
        self.visited_urls = set()
        self.max_depth = 3

    def crawl(self, url, depth=0):
        if depth >= self.max_depth or url in self.visited_urls:
            return []
        self.visited_urls.add(url)
        found_urls = [url]  

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')

            for link in links:
                next_url = link.get('href')
                next_url = urljoin(url, next_url)

                if self.is_same_domain(url, next_url) and next_url not in self.visited_urls:
                    found_urls.extend(self.crawl(next_url, depth + 1))

        except Exception as e:
            print(f"Error crawling {url}: {e}")
        return found_urls

    def is_same_domain(self, base_url, target_url):
        base_domain = urlparse(base_url).netloc
        target_domain = urlparse(target_url).netloc
        return base_domain == target_domain


# Home route
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/passwordchecker')
def passwordchecker():
    return render_template('password_checker.html')

@app.route('/passwordgenerator')
def passwordgenerator():
    return render_template('password_generator.html')

@app.route('/encoding')
def encoding():
    return render_template('text_translation.html')

# Nmap page route
@app.route('/nmap')
def nmap_page():
    return render_template('nmap_index.html')

@app.route('/steg')
def steg():
    return render_template('steg.html')

@app.route('/hashing')
def hashing():
    return render_template('hashing.html')

# Nmap scanning route
@app.route('/scan', methods=['POST'])
def scan():
    target = request.form.get('target')
    if not target:
        return render_template('nmap_index.html', scan_output="Invalid target provided.")

    # Run Nmap command
    try:
        result = subprocess.check_output(["nmap", "-sV", target], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        result = f"Error running Nmap: {e.output}"

    # Save the result for PDF generation
    with open("scan_result.txt", "w") as f:
        f.write(result)

    return render_template('nmap_index.html', scan_output=result)

# Download PDF route
@app.route('/download')
def download_pdf():
    # Convert text result to PDF
    if not os.path.exists("scan_result.txt"):
        return redirect(url_for('nmap_page'))

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    with open("scan_result.txt", "r") as f:
        for line in f:
            pdf.cell(200, 10, txt=line, ln=True)

    pdf_output = "scan_result.pdf"
    pdf.output(pdf_output)

    return send_file(pdf_output, as_attachment=True)

# Web Crawler route
@app.route('/crawler', methods=['GET', 'POST'])
def crawler():
    if request.method == 'POST':
        url = request.form.get('url')
        crawler = WebCrawler()

        urls = crawler.crawl(url)

        return render_template('results.html', urls=urls[:10])

    return render_template('crawler.html')

def domain_to_ip(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except socket.gaierror:
        return "Invalid domain or unable to resolve."

# Function for Reverse DNS Lookup (PTR Record)
def ip_to_domain(ip):
    try:
        reverse_ip = dns.reversename.from_address(ip)
        domain = dns.resolver.resolve(reverse_ip, "PTR")
        return domain[0].to_text()
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
        return "No PTR record found."

# Function to fetch MX Records
def get_mx_records(domain):
    try:
        result = dns.resolver.resolve(domain, 'MX')
        return [str(rdata.exchange) for rdata in result]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return ["No MX records found."]

# Function to fetch NS Records
def get_ns_records(domain):
    try:
        result = dns.resolver.resolve(domain, 'NS')
        return [str(rdata.target) for rdata in result]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return ["No NS records found."]

# Function to fetch TXT Records
def get_txt_records(domain):
    try:
        result = dns.resolver.resolve(domain, 'TXT')
        return [rdata.to_text() for rdata in result]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return ["No TXT records found."]

@app.route("/dnslookup", methods=["GET", "POST"])
def nslookup_tool():
    results = None

    if request.method == "POST":
        user_input = request.form.get("query")

        # Check for empty input
        if not user_input or user_input.strip() == "":
            return render_template("index.html", results={"error": "Please provide a valid input."})

        results = {}

        try:
            # If input is an IP, perform reverse lookup
            socket.inet_aton(user_input)
            results["type"] = "IP Address"
            results["reverse_domain"] = ip_to_domain(user_input)
        except socket.error:
            # Else, assume it's a domain
            results["type"] = "Domain"
            results["ip"] = domain_to_ip(user_input)
            results["mx"] = get_mx_records(user_input)
            results["ns"] = get_ns_records(user_input)
            results["txt"] = get_txt_records(user_input)

    return render_template("dnslookup.html", results=results)

def caesar_cipher(text, shift, decrypt=False):
    if decrypt:
        shift = -shift
    result = ""
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - start + shift) % 26 + start)
        else:
            result += char
    return result

def atbash_cipher(text):
    result = ""
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            result += chr(start + 25 - (ord(char) - start))
        else:
            result += char
    return result

def substitution_cipher(text, key, decrypt=False):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = key.upper()
    if decrypt:
        mapping = {key[i]: alphabet[i] for i in range(26)}
    else:
        mapping = {alphabet[i]: key[i] for i in range(26)}
    result = ""
    for char in text.upper():
        result += mapping.get(char, char)
    return result

def reverse_cipher(text):
    return text[::-1]

def vigenere_cipher(text, key, decrypt=False):
    key = key.upper()
    result = ""
    key_index = 0
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            shift = ord(key[key_index]) - ord('A')
            shift = -shift if decrypt else shift
            result += chr((ord(char) - start + shift) % 26 + start)
            key_index = (key_index + 1) % len(key)
        else:
            result += char
    return result

@app.route('/encryption')
def enc():
    return render_template('encryption.html')


@app.route('/encrypt', methods=['POST'])
def encrypt():
    text = request.form.get('text')
    cipher_type = request.form.get('cipher')
    shift = int(request.form.get('shift', 0))
    key = request.form.get('key', '')

    if cipher_type == "Caesar":
        result = caesar_cipher(text, shift)
    elif cipher_type == "Atbash":
        result = atbash_cipher(text)
    elif cipher_type == "Substitution":
        result = substitution_cipher(text, key)
    elif cipher_type == "Reverse":
        result = reverse_cipher(text)
    elif cipher_type == "Vigenere":
        result = vigenere_cipher(text, key)
    else:
        result = "Invalid cipher selected."

    return render_template('encryption.html', result=result, text=text)

if __name__ == "__main__":
    app.run(debug=True)
