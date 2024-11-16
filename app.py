from flask import Flask, render_template, request, send_file, redirect, url_for
import os
import subprocess
from fpdf import FPDF
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import requests

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

if __name__ == "__main__":
    app.run(debug=True)
