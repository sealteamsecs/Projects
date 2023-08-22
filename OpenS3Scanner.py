import requests
import urllib3
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

# Suppress TLS/SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



def generate_s3_bucket_urls(sld):
    """
    Generate a list of potential S3 bucket URLs using common keywords and the SLD.
    """
    aws_regions = [
        "us-east-2","us-east-1","us-west-1","us-west-2","af-south-1",
        "ap-east-1","ap-south-2","ap-southeast-3","ap-southeast-4",
        "ap-south-1","ap-northeast-3","ap-northeast-2","ap-southeast-1",
        "ap-southeast-2","ap-northeast-1", "ca-central-1", "eu-central-1",
        "eu-west-1","eu-west-2","eu-south-1","eu-west-3","eu-south-2",
        "eu-north-1","eu-central-2","il-central-1", "me-south-1",
        "me-central-1","sa-east-1","us-gov-east-1","us-gov-west-1"
    ]

    # Common keywords to test in the URL
    common_keywords = [
        "alpha", "api", "app", "assets", "backup", "beta", 
        "blog", "bucket", "cdn", "client", "cloud", "config", "content", 
        "dashboard", "data", "demo", "dev", "development", "docs", "documents", "exports", "files",
        "forum", "ftp", "help", "imports", "labs", "login", "mail", 
        "media", "mobile", "news", "orders", "partner", "portal", "private", "prod", 
        "production", "public", "raw", "records", "releases", "reports", "s3", "sandbox", "sdk", 
        "secure", "shop", "smtp", "software", "stage", "staging", "static", 
        "store", "support", "temp", "test", "testing", "tools", 
        "uploads", "vendor", "web", "wiki", "www"
    ]

    # Define URL patterns using placeholders for the sld, keyword, and region.
    # This will allow easy addition of new patterns in the future.
    url_patterns = [
        "https://{sld}.s3.{region}.amazonaws.com",
        "https://{keyword}-{sld}.s3.{region}.amazonaws.com",
        "https://{sld}-{keyword}.s3.{region}.amazonaws.com",
        "https://{keyword}{sld}.s3.{region}.amazonaws.com",
        "https://{sld}{keyword}.s3.{region}.amazonaws.com",
        "https://{keyword}.{sld}.s3.{region}.amazonaws.com"
    ]

    s3_bucket_urls = set()
    for region in aws_regions:
        for keyword in common_keywords:
            # Avoid generating a URL with the same keyword and sld
            if keyword == sld:
                continue
            for pattern in url_patterns:
                url = pattern.format(sld=sld, keyword=keyword, region=region)
                s3_bucket_urls.add(url)  # Add to set; duplicates are ignored

    return list(s3_bucket_urls)  # Convert set back to list for compatibility


def is_bucket_open(url):
    #print(url)
    try:
        response = requests.get(url, verify=False, timeout=5)
        if response.status_code == 200:
            print(url)
            return True
        return False
    except requests.RequestException:
        return False

def check_s3_buckets(urls):
    open_buckets = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        future_to_url = {executor.submit(is_bucket_open, url): url for url in urls}
        for future in as_completed(future_to_url):  # Changed from concurrent.futures.as_completed
            url = future_to_url[future]
            if future.result():
                open_buckets.append(url)
    return open_buckets



if __name__ == "__main__":
    # Get's user input - requires just the second level domain
    domain = input("Enter an SLD (e.g., example.com without .com): ").strip()
    s3_bucket_urls = generate_s3_bucket_urls(domain)

    # Check which buckets are open
    open_buckets = check_s3_buckets(s3_bucket_urls)

    # Print the open buckets
    for bucket in open_buckets:
        print(f"Open bucket: {bucket}")  
